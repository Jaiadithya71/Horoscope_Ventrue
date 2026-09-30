"""Directional occupied-sign owner evidence, not selected XX.14 condition flags."""
from .friendship import CLASSICAL,natural_relation,compound_relation,NATURAL_SOURCE,PREFERENCE_SOURCE
from .synthesis import LORDS
from .forecast import sign_index
from .chart_evidence_inputs import validate_sign_longitude


def period_relation_context(placements,main_lord,sub_lord):
 validate_sign_longitude(placements);rows=[]
 for lord in dict.fromkeys((main_lord,sub_lord)):
  p=placements.get(lord,{})
  sign=p.get('sign');owner=None if sign is None else LORDS[sign_index(sign)]
  natural=None;candidate=None;missing=[]
  if sign is None:missing.append('lord_sign')
  if owner is not None and placements.get(owner,{}).get('sign') is None:missing.append('occupied_sign_owner_placement')
  if lord not in CLASSICAL:status='node_relationship_applicability_unknown'
  elif owner is None:status='unresolved_sign'
  elif owner==lord:status='own_sign_not_two_planet_relationship'
  else:
   status='directional_source_candidates_only';natural=natural_relation(lord,owner)
   owner_sign=placements.get(owner,{}).get('sign')
   if owner_sign is not None:
    house=(sign_index(owner_sign)-sign_index(sign))%12+1
    candidate=compound_relation(natural,house)
  rows.append({'lord':lord,'occupied_sign':sign,'occupied_sign_owner':owner,'status':status,
   'natural_relation_lord_to_owner':natural,'rasi_relative_compound_candidate':candidate,
   'missing_inputs':missing,'selected_friendly_sign':None,'selected_inimical_sign':None,
   'sources':[NATURAL_SOURCE,PREFERENCE_SOURCE],
   'notice':'Natural relation points from period lord to sign owner, not reverse. Rasi-relative compound profile is commentary evidence only. Own sign needs no self-friendship. Node relationship applicability unverified; missing owner placement does not mean temporal enemy. No mapping to XX.14 friendly/inimical flags selected.'})
 return {'rows':rows,'selected_relation_profile':None,'selected_period_conditions':None,
  'notice':'Context beside disposition evidence only. IV.10 natural preference does not settle XX.14 sign classification, compound house convention, solar rays, strength or outcomes.'}
