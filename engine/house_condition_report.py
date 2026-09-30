"""Scoped source evidence for one caller-selected house, not a reading."""
from .bhava_recovery_conditions import chart_xv5_candidates,chart_xv3_lord_candidates,xv6_connective_candidates
from .debilitation_cancellation_candidates import chart_cancellation_candidates
from .bhava_condition_gate import audit_bhava_conditions
from .synthesis import LORDS
from .forecast import sign_index
from .dusthana_strength_qualification import dusthana_strength_qualification
from .lordship_precedence import lordship_precedence
from .house_growth_scope import chart_house_growth_candidates


def house_condition_report(house,reference_sign,placements,classifications,*,
  classification_profile,strength_profile=None,bhava_strong=None,lord_strong=None,karaka_strong=None,
  lord_eclipsed=None,lord_inimical_sign=None,xv6_clauses=None,lord_strength_status=None):
 recovery=chart_xv5_candidates(house,reference_sign,placements,classifications,
                              classification_profile=classification_profile)
 cancels=chart_cancellation_candidates(reference_sign,placements)
 lord=LORDS[(sign_index(reference_sign)+house-1)%12]
 lord_cancel=next((x for x in cancels['planet_evidence'] if x['planet']==lord),None)
 if lord_strength_status is not None and (not isinstance(strength_profile,str) or not strength_profile.strip()):
  raise ValueError("Explicit strength profile required for XV9 status")
 checks=[];severity=[]
 for profile,field in [('whole_sign','whole_sign_house_from_ascendant'),('sripati_degree_bhava','sripati_degree_house')]:
  houses={}
  for p,v in placements.items():
   if profile=='whole_sign':h=(sign_index(v['sign'])-sign_index(reference_sign))%12+1
   else:
    h=v.get(field);h=h.get('house') if isinstance(h,dict) else h
   houses[p]=h
  severity.append({'occupation_profile':profile,'qualification':dusthana_strength_qualification(
   houses.get(lord),supplied_strength_status=lord_strength_status,
   strength_profile=strength_profile or 'unresolved_supplied_strength_profile',house_frame=profile)})
  checks.append({'occupation_profile':profile,'condition_evidence':audit_bhava_conditions(house,
   bhava_strong=bhava_strong,lord_strong=lord_strong,karaka_strong=karaka_strong,
   strength_profile=strength_profile,planet_houses=houses)})
 lord_conditions=chart_xv3_lord_candidates(house,reference_sign,placements,classifications,
  classification_profile=classification_profile,eclipsed=lord_eclipsed,inimical_sign=lord_inimical_sign)
 if xv6_clauses is not None and not isinstance(xv6_clauses,dict):raise ValueError('XV.6 clause object required')
 clauses={} if xv6_clauses is None else xv6_clauses
 if set(clauses)-{'all_three_weak','afflicted_without_benefics','adverse_relative_occupation'}:
  raise ValueError('Unknown XV.6 clause key')
 return {'house':house,'reference_sign':reference_sign,'house_lord':lord,
   'xv3_lord_target_candidates':lord_conditions,
   'xv18_19_house_growth_scope':chart_house_growth_candidates(house,reference_sign,placements,classifications,classification_profile=classification_profile),
   'xv9_supplied_lord_severity_candidates':severity,
   'xv10_11_lordship_emphasis':[r for r in lordship_precedence(reference_sign)['dual_owner_evidence'] if r['planet']==lord],
   'xv6_supplied_connective_candidates':xv6_connective_candidates(**clauses),
   'xv5_scoped_recovery':recovery,'house_lord_debilitation_candidates':lord_cancel,
   'xv25_26_supplied_strength_conditions':checks,'global_precedence':None,'personal_outcome':None,
   'selected_strength_total':None,'timing':None,
   'notice':'Input flags/classes are caller supplied, not certified complete strength. VII cancellation does not substitute for XV strength or overrule XV26. XV5 recovery, XV9 severity and XV10/11 ownership emphasis retained separately. The lord bool flag is not translated into a strong/weak XV9 status; false does not prove weakness. No overlap is silently arbitrated. No vote, combined polarity, probability or personal event. No active period/calendar inferred.'}


def main():
 import argparse,json
 from .natal import natal_chart
 a=argparse.ArgumentParser(description=__doc__)
 for flag in ('birth-date','birth-time','birth-tz','birth-place'):
  a.add_argument('--'+flag,required=True)
 for flag in ('birth-lat','birth-lon'):a.add_argument('--'+flag,required=True,type=float)
 a.add_argument('--house',required=True,type=int)
 a.add_argument('--classification-file',required=True,
   help='JSON with profile and classical planet classes; these are caller supplied, not engine certified')
 a.add_argument('--condition-file',help='Optional JSON lord_eclipsed/lord_inimical_sign and independently grounded xv6 clause flags')
 a.add_argument('--strength-file',help='Optional JSON with profile, bhava/lord/karaka bool/null flags and separate lord_status strong/weak/null')
 args=a.parse_args()
 try:
  from pathlib import Path
  classes=json.loads(Path(args.classification_file).read_text())
  if not isinstance(classes,dict) or set(classes)!={'profile','classes'} or not isinstance(classes['classes'],dict):raise ValueError('Classification requires only profile and classes objects')
  strength=json.loads(Path(args.strength_file).read_text()) if args.strength_file else {}
  if not isinstance(strength,dict) or set(strength)-{'profile','bhava','lord','karaka','lord_status'}:raise ValueError('Unknown supplied strength key or invalid object')
  conditions=json.loads(Path(args.condition_file).read_text()) if args.condition_file else {}
  if not isinstance(conditions,dict):raise ValueError('Condition object required')
  if set(conditions)-{'lord_eclipsed','lord_inimical_sign','xv6_clauses'}:raise ValueError('Unknown supplied condition key')
  n=natal_chart(args.birth_date,args.birth_time,args.birth_tz,args.birth_lat,args.birth_lon,args.birth_place)
  r=house_condition_report(args.house,n['ascendant']['sign'],n['placements'],classes['classes'],
    classification_profile=classes['profile'],strength_profile=strength.get('profile'),
    bhava_strong=strength.get('bhava'),lord_strong=strength.get('lord'),karaka_strong=strength.get('karaka'),lord_eclipsed=conditions.get('lord_eclipsed'),
    lord_inimical_sign=conditions.get('lord_inimical_sign'),xv6_clauses=conditions.get('xv6_clauses'),lord_strength_status=strength.get('lord_status'))
  r['chart_input_context']={k:n[k] for k in ('birth_utc','birth_place','latitude','longitude','ascendant','model')}
  r['input_declaration_notice']='Classification/strength files are caller declarations, not engine-verified flags. No complete strength is calculated or certified.'
  print(json.dumps(r,indent=2))
 except (ValueError,KeyError,TypeError,OSError) as exc:a.error(str(exc))


if __name__=='__main__':main()
