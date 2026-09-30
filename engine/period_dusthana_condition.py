"""XX.22 simultaneous main/subperiod house condition, scoped interpretations."""
BAD={6,8,12}


def period_dusthana_condition(main_owns,main_occupies,sub_owns,sub_occupies):
 for owns in (main_owns,sub_owns):
  if owns is not None and (not isinstance(owns,(list,tuple)) or any(type(h) is not int or not 1<=h<=12 for h in owns)):
   raise ValueError('Complete owned-house list or unresolved None required')
 for house in (main_occupies,sub_occupies):
  if house is not None and (type(house) is not int or not 1<=house<=12):raise ValueError('Occupied house1..12 or None required')
 def own(xs):return None if xs is None else bool(BAD.intersection(xs))
 def occ(h):return None if h is None else h in BAD
 def AND(a,b):return False if a is False or b is False else True if a is True and b is True else None
 def OR(a,b):return True if a is True or b is True else False if a is False and b is False else None
 mo,mp,so,sp=own(main_owns),occ(main_occupies),own(sub_owns),occ(sub_occupies)
 sastri=AND(OR(mo,mp),OR(so,sp))
 kapoor=OR(AND(mo,so),AND(mp,sp))
 return {'inputs':{'main_owns':main_owns,'main_occupies':main_occupies,'sub_owns':sub_owns,'sub_occupies':sub_occupies},
   'candidates':[{'profile':'sastri_both_own_or_occupy_literal','condition_present':sastri},
                 {'profile':'kapoor_separate_owner_pair_or_occupant_pair','condition_present':kapoor}],
   'interpretation_difference':sastri!=kapoor,'selected_profile':None,'personal_outcome':None,
   'source':{'slug':'phaladeepika-1937','chapter':'XX','sloka':22,'pdf_page':245,'printed_page':208,
      'url':'https://archive.org/details/in.ernet.dli.2015.92117','verified_against_page_image':True},
   'comparison_source':{'title':'Phaladeepika Kapoor reproduction','pdf_page':186,'chapter':'XX','sloka':22,
      'url':'https://jyotishvidya.com/HTMLobj-9415/Mantreswara_s__Phaladeeplka_.pdf','verified_against_page_image':True},
   'notice':'Adverse conditional evidence only. English Sastri both-own-or-occupy and Kapoor separate owner/occupant pair readings kept explicit. Missing houses are unknown, not absence. Does not select global priority over Vargottama, Lagna-owner exception or competing schools; no active date or personal conclusion inferred.'}


def chart_period_dusthana_candidates(reference_sign,placements,main_lord,sub_lord):
 from .synthesis import lordship
 from .natal import PERIODS
 if main_lord not in dict(PERIODS) or sub_lord not in dict(PERIODS):raise ValueError('Known period lords required')
 owners=lordship(reference_sign)
 # Classical ownership only. Nodes remain unknown instead of empty list.
 def owns(p):return None if p in ('Rahu','Ketu') else [r['house'] for r in owners['houses'] if r['lord']==p]
 rows=[]
 for profile,field in [('whole_sign_ascendant','whole_sign_house_from_ascendant'),('sripati_degree_bhava','sripati_degree_house')]:
  def house(p):
   value=placements.get(p,{}).get(field)
   return value.get('house') if isinstance(value,dict) else value
  x=period_dusthana_condition(owns(main_lord),house(main_lord),owns(sub_lord),house(sub_lord))
  rows.append({'house_profile':profile,'condition_evidence':x})
 return {'main_lord':main_lord,'sub_lord':sub_lord,'reference_sign':reference_sign,'candidates':rows,
         'owner_evidence':owners,'selected_profile':None,'personal_outcome':None,
         'notice':'Sign ownership kept separate from occupied-house geometry. Caller supplies lord pair; no active period/calendar selected. Node ownership unknown.'}
