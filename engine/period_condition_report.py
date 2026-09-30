"""Run checked scoped period conditions on an explicit lord pair, no prediction."""
from .period_school_conflict import period_school_conflict
from .period_dusthana_condition import chart_period_dusthana_candidates
from .vargottama_period_qualification import chart_vargottama_period_qualifications,vargottama_period_qualification
from .combustion_candidates import chart_combustion_candidates
from .lordship_precedence import lordship_precedence
from .period_sandhi_gate import period_sandhi_gate
from .dual_owner_occupation_exception import dual_owner_occupation_exception
from .period_disposition_gate import chart_period_disposition_candidates
from .period_context_requirements import period_context_requirements
from .natal_factors import dignity
from .vargas import six_vargas


def period_condition_report(reference_sign,placements,main_lord,sub_lord,*,geometry=None,geometry_profile=None):
 school=period_school_conflict(main_lord,sub_lord)
 houses=chart_period_dusthana_candidates(reference_sign,placements,main_lord,sub_lord)
 rays=chart_combustion_candidates(placements)
 base=chart_vargottama_period_qualifications(placements)
 qualified=[]
 for lord in dict.fromkeys((main_lord,sub_lord)):
  p=placements.get(lord,{})
  candidates=[]
  if p.get('longitude') is not None and lord in base['planets']:
   d=dignity(lord,p['sign'],p['longitude']);v=six_vargas(p['longitude'])['vargottama']
   for c in rays['planets'][lord].get('candidates',[]):
    candidates.append({'sun_ray_candidate':c,'vargottama_qualification':vargottama_period_qualification(v,d['flags']['fall_sign'],c['candidate_overpowered_sun_rays']),
      'selection_status':'Commentary threshold hypothesis only, not source-selected Sun-ray flag'})
  qualified.append({'lord':lord,'base_qualification':base['planets'].get(lord),
                    'commentary_conditioned_candidates':candidates,'selected_result':None})
 owners=lordship_precedence(reference_sign)
 owners['dual_owner_evidence']=[r for r in owners['dual_owner_evidence'] if r['planet'] in (main_lord,sub_lord)]
 other=dual_owner_occupation_exception(reference_sign,{p:v for p,v in placements.items() if p in (main_lord,sub_lord)})
 other['rows']=[r for r in other['rows'] if r['planet'] in (main_lord,sub_lord)]
 other['lord_pair_scope']={'main_lord':main_lord,'sub_lord':sub_lord,'single_owner_or_node_lords_have_no_dual_owner_row':True}
 return {'main_lord':main_lord,'sub_lord':sub_lord,
    'lord_pair_origin':'Explicit caller input, not inferred active date or selected dasha/calendar convention',
    'xx21_context_requirements':period_context_requirements(),
    'period_school_conflict':school,'unfavorable_house_candidates':houses,
    'xx14_lord_disposition_candidates':chart_period_disposition_candidates(reference_sign,placements,main_lord,sub_lord),
    'exact_sandhi_period_gate':period_sandhi_gate(placements,main_lord,sub_lord,geometry=geometry,geometry_profile=geometry_profile),
    'vargottama_qualification_candidates':qualified,'lordship_emphasis':owners,
    'xv29_own_other_house_exception':other,
    'selected_strength_total':None,'selected_calendar':None,'personal_outcome':None,
    'global_precedence':None,'status':'scoped_condition_evidence_only',
    'notice':'No vote, numerical weights or global winner between these different scopes. A specific exception within one verse cannot override another verse or unchosen school. Absence of a checked conflict is not correctness or a forecast. Birth/motion/geometry uncertainty and missing source selection remain.'}


def main():
 import argparse,json
 from .natal import natal_chart,PERIODS
 a=argparse.ArgumentParser(description=__doc__)
 a.add_argument('--birth-date',required=True);a.add_argument('--birth-time',required=True)
 a.add_argument('--birth-tz',required=True);a.add_argument('--birth-place',required=True)
 a.add_argument('--birth-lat',required=True,type=float);a.add_argument('--birth-lon',required=True,type=float)
 a.add_argument('--include-modern-degree-geometry',action='store_true',
   help='Explicitly evaluate the Sripati degree-geometry candidate from this chart modern Swiss Lahiri ascendant/MC; not historical profile selection')
 a.add_argument('--main-lord',required=True,choices=list(dict(PERIODS)))
 a.add_argument('--sub-lord',required=True,choices=list(dict(PERIODS)))
 args=a.parse_args()
 try:
  n=natal_chart(args.birth_date,args.birth_time,args.birth_tz,args.birth_lat,args.birth_lon,args.birth_place)
  g=n['sripati_degree_geometry'] if args.include_modern_degree_geometry else None
  usable=g is not None and g.get('status')!='unavailable'
  x=period_condition_report(n['ascendant']['sign'],n['placements'],args.main_lord,args.sub_lord,
    geometry=g if usable else None,geometry_profile='Sripati quadrant trisection of modern Swiss Moshier Lahiri ascendant/MC candidate' if usable else None)
  x['degree_geometry_input_context']={'requested':args.include_modern_degree_geometry,
    'available':usable if args.include_modern_degree_geometry else None,
    'geometry':g,'midheaven':n['midheaven'] if args.include_modern_degree_geometry else None,
    'notice':'Explicit optional modern-anchor candidate, not source-selected historical ephemeris. Unavailable geometry is not replaced by whole-sign houses.'}
  x['chart_input_context']={k:n[k] for k in ('birth_utc','birth_place','latitude','longitude','ascendant','model')}
  print(json.dumps(x,indent=2))
 except ValueError as exc:a.error(str(exc))


if __name__=='__main__':main()
