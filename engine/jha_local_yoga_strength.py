"""Jha28.37-38 scoped supplied-strength comparison, not global outcome rank."""
from fractions import Fraction as F
from .bphs_jha_special_aspect import CLASSICAL
from .bphs_jha_general_aspect import SOURCE_URL


def local_yoga_strength_candidate(house,contributors,*,scope_profile,strength_profile):
 if type(house) is not int or not 1<=house<=12:raise ValueError('Explicit common house1..12 required')
 for p in (scope_profile,strength_profile):
  if not isinstance(p,str) or not p.strip():raise ValueError('Named scope and common strength provenance required')
 if not isinstance(contributors,list) or len(contributors)<2:raise ValueError('At least two explicit yoga contributors required')
 keys={'planet','house','yoga_reference','role','total_virupa','declared_complete','source_strength_profile'}
 seen=set();rows=[];blocks=[]
 for row in contributors:
  if not isinstance(row,dict) or set(row)!=keys:raise ValueError('Exact contributor fields required')
  p=row['planet']
  if p not in CLASSICAL or p in seen:raise ValueError('Distinct classical contributor planets required')
  seen.add(p)
  if type(row['house']) is not int or not 1<=row['house']<=12:raise ValueError('Contributor house1..12 required')
  if row['role'] not in ('fortune_increasing','fortune_decreasing','other','unknown'):raise ValueError('Explicit supplied role required')
  for k in ('yoga_reference','source_strength_profile'):
   if not isinstance(row[k],str) or not row[k].strip():raise ValueError('Named contributor reference/profile required')
  if type(row['declared_complete']) is not bool:raise ValueError('Explicit complete boolean required')
  value=row['total_virupa'];amount=None
  if value is not None:
   if isinstance(value,bool):raise ValueError('Finite nonnegative strengthvirupa required')
   try:amount=F(str(value))
   except (ValueError,ZeroDivisionError) as exc:raise ValueError('Finite nonnegative strengthvirupa required') from exc
   if amount<0:raise ValueError('Nonnegative total strength required')
  reasons=[]
  if row['house']!=house:reasons.append('different_house_scope')
  if not row['declared_complete']:reasons.append('partial_strength')
  if amount is None:reasons.append('missing_total')
  if row['source_strength_profile']!=strength_profile:reasons.append('different_strength_profile')
  if reasons:blocks.append(p)
  rows.append({**row,'total_virupa_rational':str(amount) if amount is not None else None,'blockers':reasons})
 maxvalue=None if blocks else max(F(r['total_virupa_rational']) for r in rows)
 leaders=[] if maxvalue is None else [r['planet'] for r in rows if F(r['total_virupa_rational'])==maxvalue]
 return {'profile':'jha_sudha28_37_38_same_house_supplied_contributor_comparison',
  'house':house,'scope_profile':scope_profile,'strength_profile':strength_profile,'contributors':rows,
  'blocked_contributors':blocks,'arithmetic_maximum_virupa_rational':str(maxvalue) if maxvalue is not None else None,
  'arithmetic_maximum_contributors':leaders,'unique_arithmetic_leader':leaders[0] if len(leaders)==1 else None,
  'tie_rule_verified':False,'group_strength_pooling_rule_verified':False,
  'source':{'url':SOURCE_URL,'pdf_pages':[192,193],'printed_pages':[160,161],'chapter':28,'slokas':'37-38',
   'verified_against_page_image':True},'supplied_yoga_roles_independently_verified':False,
  'supplied_totals_independently_verified':False,'global_rank':None,'selected_effect':None,'personal_outcome':None,
  'notice':'Scoped arithmetic leader of caller-declared complete common-profile same-house yoga contributors only. This does not classify yoga roles, certify source-consistent natal totals, pool favorable/adverse groups, break ties or override other house/period/transit rules. A partial score is never promoted to complete strength. Unknown role remains unknown and no outcome is generated.'}
