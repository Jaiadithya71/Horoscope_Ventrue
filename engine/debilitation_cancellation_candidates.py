"""VII.26 scoped conditional candidates, not strength or outcome arbitration."""


def _or(a,b):
 return True if a is True or b is True else False if a is False and b is False else None


def _and(a,b):
 return False if a is False or b is False else True if a is True and b is True else None


def cancellation_candidates(debilitated=None,depression_lord_kendra=None,
                            exaltation_sign_lord_kendra=None,
                            planet_exalted_in_depression_sign_kendra=None):
 """Inputs must be explicitly source-grounded; unknown is never false.

 Each Kendra flag means from either Lagna or Moon. Sign mapping, aspects,
 alternative VII.27-30 recipes, complete strength and outcome remain outside
 this isolated VII.26 helper. No candidate is selected.
 """
 flags=(debilitated,depression_lord_kendra,exaltation_sign_lord_kendra,
        planet_exalted_in_depression_sign_kendra)
 if any(x is not None and not isinstance(x,bool) for x in flags):
  raise ValueError('Grounded bool or None required')
 candidates=[]
 for meaning,value in [('own_exaltation_sign_lord',exaltation_sign_lord_kendra),
                       ('planet_exalted_in_occupied_depression_sign',planet_exalted_in_depression_sign_kendra)]:
  for connective,op in [('either',_or),('both',_and)]:
   candidates.append({'uchchanatha_reading':meaning,'connective_reading':connective,
     'qualifying_condition':_and(debilitated,op(depression_lord_kendra,value)),
     'scope':'VII.26 condition only; not complete cancellation assessment',
     'source_references':['phaladeepika-1937 PDF117 printed80 VII.26 and note',
                          'phaladeepika-kapoor PDF89 VII.26 commentary']})
 return {'candidates':candidates,'selected_profile':None,'total_strength':None,
   'personal_outcome':None,'global_precedence':None,
   'notice':'Kapoor explicitly reports either-versus-both and alternate Uchchanatha readings. This helper preserves the axes, not an assertion that every school uses all four combinations. A false VII.26 condition does not deny VII.27-30. A true flag does not undo all adverse factors or assert status, wealth or an event.'}


def chart_cancellation_candidates(ascendant_sign,placements):
 """Whole-sign VII.26 geometry only; no Rasi/Bhava equivalence asserted."""
 from .forecast import sign_index,SIGNS
 from .synthesis import LORDS,LORD_SOURCE
 from .natal_factors import EXALTATION,SOURCE_DIGNITY,dignity
 asc=sign_index(ascendant_sign)
 moon=placements.get('Moon',{}).get('sign')
 moon_i=sign_index(moon) if moon is not None else None
 def kendra(planet):
  sign=placements.get(planet,{}).get('sign')
  if sign is None:return None
  i=sign_index(sign)
  return _or((i-asc)%12 in (0,3,6,9),
             (i-moon_i)%12 in (0,3,6,9) if moon_i is not None else None)
 rows=[]
 for planet,exalted_sign in EXALTATION.items():
  p=placements.get(planet)
  if p is None:continue
  sign=p['sign'];d=dignity(planet,sign,p.get('longitude'))
  fall=SIGNS[(sign_index(exalted_sign)+6)%12]
  depression_lord=LORDS[sign_index(fall)]
  exaltation_lord=LORDS[sign_index(exalted_sign)]
  other=next((x for x,s in EXALTATION.items() if s==fall),None)
  row=cancellation_candidates(d['flags']['fall_sign'],kendra(depression_lord),
                             kendra(exaltation_lord),kendra(other) if other else None)
  rows.append({'planet':planet,'occupied_sign':sign,'depression_sign':fall,
    'depression_lord':depression_lord,'own_exaltation_sign_lord':exaltation_lord,
    'planet_exalted_in_depression_sign':other,'condition_evidence':row})
 return {'house_profile':'whole_sign_from_ascendant_or_moon',
  'reference_sign':ascendant_sign,'moon_sign':moon,'planet_evidence':rows,
  'geometry_sources':[LORD_SOURCE,SOURCE_DIGNITY],
  'selected_profile':None,'personal_outcome':None,
  'notice':'If no classical planet is exalted in the depression sign (e.g. Moon/Scorpio), the alternative condition is unresolved, not false. This bridge uses sign Kendra geometry only; no degree-Bhava substitution, global cancellation, complete strength or outcome inferred.'}
