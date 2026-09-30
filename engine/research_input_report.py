"""One explicit birth-input entry point, with source lanes and missing gates kept separate."""
import argparse,json,sys,math
import datetime as dt
from .natal import natal_chart,PERIODS,birth_utc
from .convention_condition_report import convention_condition_report
from .period_condition_report import period_condition_report
from .raman_strength_composition import raman_supplied_composition
from .strength_layout import supplied_layout_audit
from .strength_profile_inventory import strength_profile_inventory
from .precedence_inventory import precedence_inventory

BIRTH_KEYS={'date','time','timezone','latitude','longitude','place'}
CLASSICAL={'Sun','Moon','Mars','Mercury','Jupiter','Venus','Saturn'}


def research_input_report(birth,*,period_pair=None,supplied_strength=None,query_instant=None):
 if not isinstance(birth,dict) or set(birth)!=BIRTH_KEYS:raise ValueError('Birth requires exactly date,time,timezone,latitude,longitude,place')
 for key in ('date','time','timezone','place'):
  if not isinstance(birth[key],str) or not birth[key].strip():raise ValueError('Nonempty birth text fields required')
 for key in ('latitude','longitude'):
  if type(birth[key]) not in (int,float) or not math.isfinite(birth[key]):raise ValueError('Finite numeric birth coordinates required')
 query=None
 if query_instant is not None:
  if not isinstance(query_instant,str):raise ValueError('Query instant must be an aware ISO timestamp string')
  query=dt.datetime.fromisoformat(query_instant)
  if query.tzinfo is None or query.utcoffset() is None:raise ValueError('Query instant must include explicit timezone offset')
 if period_pair is not None:
  if not isinstance(period_pair,dict) or set(period_pair)!={'main_lord','sub_lord'}:raise ValueError('Period pair requires exactly main_lord and sub_lord')
  if any(p not in dict(PERIODS) for p in period_pair.values()):raise ValueError('Known period lords required')
 strength=[]
 if supplied_strength is not None:
  if not isinstance(supplied_strength,dict) or set(supplied_strength)-CLASSICAL:raise ValueError('Supplied strength must map classical planets to explicit declarations')
  for planet,entry in supplied_strength.items():
   if not isinstance(entry,dict):raise ValueError('Strength declaration must be object')
   profile=entry.get('source_layout')
   if profile=='raman_art121_ayana_in_kala':
    required={'source_layout','components','declared_complete','component_profile','war_treatment'}
    if set(entry)!=required:raise ValueError('Exact Raman declaration fields required')
    evidence=raman_supplied_composition(**{k:v for k,v in entry.items() if k!='source_layout'})
   elif profile=='sripati_iii20_supplied_base':
    required={'source_layout','components','layout','complete','component_profile'}
    if set(entry)!=required:raise ValueError('Exact Sripati base declaration fields required')
    evidence=supplied_layout_audit(**{k:v for k,v in entry.items() if k!='source_layout'})
   else:raise ValueError('Known explicit source layout required; no inferred layout')
   strength.append({'planet':planet,'source_layout':profile,'evidence':evidence,
    'chart_identity_match_verified':False,'converted_to_condition_strength_flag':False})
 chart=natal_chart(**birth)
 period=None if period_pair is None else period_condition_report(chart['ascendant']['sign'],chart['placements'],**period_pair)
 conventions=None if query is None else convention_condition_report(birth_utc(birth['date'],birth['time'],birth['timezone']),query,chart['ascendant']['sign'],chart['placements'])
 return {'status':'explicit_birth_research_evidence_not_personal_forecast','natal_chart':chart,
  'query_convention_condition_evidence':conventions,
  'explicit_period_pair_evidence':period,'active_period_inferred':False,
  'supplied_strength_evidence':strength,'strength_evidence_origin':'Caller declarations, not reconstructed or certified from this chart',
  'strength_requirements':strength_profile_inventory(),'precedence_requirements':precedence_inventory(),
  'selected_complete_strength':None,'selected_calendar_profile':None,'global_outcome':None,'empirical_accuracy':None,
  'notice':'Existing modern Moshier/Lahiri chart model is labeled, not a selected historical frame. Birth, source arithmetic and explicit period-pair evidence are separate lanes. Caller-supplied strengths do not create strong/weak flags, change chart coordinates or select an active calendar. Sripati base excludes signed-aspect assembly; Raman layout already includes signedDrik and Ayana withinKala. No cross-source sum, rank or personal forecast. Research licensing and source-rights gates still apply.'}


def main():
 a=argparse.ArgumentParser(description=__doc__);a.add_argument('--input-json',required=True,help='Exact research input JSON file, or - for stdin')
 args=a.parse_args()
 try:
  if args.input_json=='-':payload=json.load(sys.stdin)
  else:
   with open(args.input_json) as f:payload=json.load(f)
  if not isinstance(payload,dict) or set(payload)-{'birth','period_pair','supplied_strength','query_instant'} or 'birth' not in payload:raise ValueError('Input requires birth; only period_pair, supplied_strength and query_instant are optional')
  print(json.dumps(research_input_report(**payload),indent=2))
 except (ValueError,TypeError,OSError) as exc:a.error(str(exc))


if __name__=='__main__':main()
