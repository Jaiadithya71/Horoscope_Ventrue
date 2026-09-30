"""Scoped source evidence for one caller-selected house, not a reading."""
from .bhava_recovery_conditions import chart_xv5_candidates
from .debilitation_cancellation_candidates import chart_cancellation_candidates
from .bhava_condition_gate import audit_bhava_conditions
from .synthesis import LORDS
from .forecast import sign_index


def house_condition_report(house,reference_sign,placements,classifications,*,
  classification_profile,strength_profile=None,bhava_strong=None,lord_strong=None,karaka_strong=None):
 recovery=chart_xv5_candidates(house,reference_sign,placements,classifications,
                              classification_profile=classification_profile)
 cancels=chart_cancellation_candidates(reference_sign,placements)
 lord=LORDS[(sign_index(reference_sign)+house-1)%12]
 lord_cancel=next((x for x in cancels['planet_evidence'] if x['planet']==lord),None)
 checks=[]
 for profile,field in [('whole_sign','whole_sign_house_from_ascendant'),('sripati_degree_bhava','sripati_degree_house')]:
  houses={}
  for p,v in placements.items():
   if profile=='whole_sign':h=(sign_index(v['sign'])-sign_index(reference_sign))%12+1
   else:
    h=v.get(field);h=h.get('house') if isinstance(h,dict) else h
   houses[p]=h
  checks.append({'occupation_profile':profile,'condition_evidence':audit_bhava_conditions(house,
   bhava_strong=bhava_strong,lord_strong=lord_strong,karaka_strong=karaka_strong,
   strength_profile=strength_profile,planet_houses=houses)})
 return {'house':house,'reference_sign':reference_sign,'house_lord':lord,
   'xv5_scoped_recovery':recovery,'house_lord_debilitation_candidates':lord_cancel,
   'xv25_26_supplied_strength_conditions':checks,'global_precedence':None,'personal_outcome':None,
   'selected_strength_total':None,'timing':None,
   'notice':'Input flags/classes are caller supplied, not certified complete strength. VII cancellation does not substitute for XV strength or overrule XV26. XV5 recovery does not resolve unrelated competing conditions. No vote, combined polarity, probability or personal event. No active period/calendar inferred.'}
