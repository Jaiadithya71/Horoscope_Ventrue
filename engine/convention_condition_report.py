"""Propagate unresolved calendar/balance profiles into scoped condition evidence."""
import datetime as dt
from .calendar_comparison import compare_conventions
from .period_condition_report import period_condition_report


def convention_condition_report(birth,instant,reference_sign,placements):
 matrix=compare_conventions(birth,instant)
 pairs={}
 for r in matrix['comparison_rows']:
  path=r['lord_path']
  if path is not None and len(path)>=2:
   key=tuple(path[:2])
   if key not in pairs:pairs[key]=period_condition_report(reference_sign,placements,*key)
 rows=[]
 for r in matrix['comparison_rows']:
  path=r['lord_path'];pair=path[:2] if path is not None and len(path)>=2 else None
  rows.append({'calendar_profile':r['calendar_profile'],'birth_balance_profile':r['balance_method'],
    'calendar_status':r['status'],'reason':r.get('reason'),
    'lord_path':path,'condition_lord_pair':pair,
    'condition_evidence_key':None if pair is None else '/'.join(pair)})
 return {'query_utc':matrix['query_utc'],'calendar_balance_evidence':matrix,
   'profile_condition_routes':rows,'distinct_pair_conditions':[
       {'key':'/'.join(pair),'evidence':e} for pair,e in sorted(pairs.items())],
   'selected_profile':None,'personal_outcome':None,'global_precedence':None,
   'status':'unresolved_conventions_propagated_into_scoped_conditions',
   'notice':'A profile can change the lord pair and therefore the applicable condition evidence. Identical paths/conditions do not verify a unique calendar or prediction. Invalid profiles remain invalid; no majority vote, clipping, fallback, selected school or personal result. Antara path retained for context but only checked main/subperiod rules are evaluated.'}


def main():
 import argparse,json
 from .natal import natal_chart,birth_utc
 a=argparse.ArgumentParser(description=__doc__)
 for arg in ('birth-date','birth-time','birth-tz','birth-place','at'):a.add_argument('--'+arg,required=True)
 for arg in ('birth-lat','birth-lon'):a.add_argument('--'+arg,required=True,type=float)
 args=a.parse_args()
 try:
  n=natal_chart(args.birth_date,args.birth_time,args.birth_tz,args.birth_lat,args.birth_lon,args.birth_place)
  b=birth_utc(args.birth_date,args.birth_time,args.birth_tz)
  x=convention_condition_report(b,dt.datetime.fromisoformat(args.at),n['ascendant']['sign'],n['placements'])
  x['chart_input_context']={k:n[k] for k in ('birth_utc','birth_place','latitude','longitude','ascendant','model')}
  print(json.dumps(x,indent=2))
 except ValueError as exc:a.error(str(exc))


if __name__=='__main__':main()
