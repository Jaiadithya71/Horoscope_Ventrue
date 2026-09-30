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
  def mutual(a,b):
   sa=placements.get(a,{}).get('sign');sb=placements.get(b,{}).get('sign')
   return None if sa is None or sb is None else (sign_index(sb)-sign_index(sa))%12 in (0,3,6,9)
  lord_sign=placements.get(depression_lord,{}).get('sign')
  relative=None if lord_sign is None else (sign_index(sign)-sign_index(lord_sign))%12+1
  special={'Mars':{4,8},'Jupiter':{5,9},'Saturn':{3,10}}.get(depression_lord,set())
  aspect_flags=[('whole_sign_full_aspects',None if relative is None else relative in {7}|special),
                ('whole_sign_seventh_only',None if relative is None else relative==7)]
  occupation=(sign_index(sign)-asc)%12+1
  recipes=[]
  for profile,aspect_flag in aspect_flags:
   recipes.append({'aspect_condition_hypothesis':profile,
    'condition_evidence':other_cancellation_recipes(d['flags']['fall_sign'],
      mutual(depression_lord,exaltation_lord),aspect_flag,occupation not in (6,8,12),
      kendra(depression_lord),kendra(exaltation_lord),kendra(planet))})
  degree=None
  a=placements.get(depression_lord,{}).get('longitude');b=p.get('longitude')
  if a is not None and b is not None:
   from .degree_aspects import degree_aspect
   degree=degree_aspect(depression_lord,a,b)
  row['other_recipe_candidates']=recipes
  row['aspect_evidence']={'aspecting_depression_lord':depression_lord,
   'target_planet':planet,'relative_whole_sign_house':relative,
   'degree_aspect_amount':degree,'degree_amount_to_VII28_condition':None,
   'notice':'Full whole-sign versus seventh-only condition hypotheses retained, not selected. A positive degree amount is not silently a qualifying VII.28 aspect; no threshold is verified.'}
  rows.append({'planet':planet,'occupied_sign':sign,'depression_sign':fall,
    'depression_lord':depression_lord,'own_exaltation_sign_lord':exaltation_lord,
    'planet_exalted_in_depression_sign':other,'condition_evidence':row})
 return {'house_profile':'whole_sign_from_ascendant_or_moon',
  'reference_sign':ascendant_sign,'moon_sign':moon,'planet_evidence':rows,
  'geometry_sources':[LORD_SOURCE,SOURCE_DIGNITY],
  'selected_profile':None,'personal_outcome':None,
  'notice':'If no classical planet is exalted in the depression sign (e.g. Moon/Scorpio), the alternative condition is unresolved, not false. This bridge uses sign Kendra geometry only; no degree-Bhava substitution, global cancellation, complete strength or outcome inferred.'}


def other_cancellation_recipes(debilitated=None,mutual_lords_kendra=None,
     aspected_by_depression_lord=None,non_dusthana_occupation=None,
     depression_lord_kendra=None,exaltation_sign_lord_kendra=None,
     debilitated_planet_kendra=None):
 """VII.27-30 supplied conditions, deliberately not royal-event statements."""
 flags=(debilitated,mutual_lords_kendra,aspected_by_depression_lord,
        non_dusthana_occupation,depression_lord_kendra,
        exaltation_sign_lord_kendra,debilitated_planet_kendra)
 if any(x is not None and not isinstance(x,bool) for x in flags):
  raise ValueError('Grounded bool or None required')
 aspect=_and(debilitated,aspected_by_depression_lord)
 rows=[{'verse':27,'condition':_and(debilitated,mutual_lords_kendra)},
       {'verse':28,'condition':aspect,
        'auspicious_house_qualification':_and(aspect,non_dusthana_occupation)},
       {'verse':29,'condition':_and(debilitated,_or(depression_lord_kendra,exaltation_sign_lord_kendra))},
       {'verse':30,'condition':_and(debilitated,debilitated_planet_kendra)}]
 for row in rows:
  row['source']={'slug':'phaladeepika-1937','pdf_page':118,'printed_page':81,
                 'chapter':'VII','sloka':row['verse'],'verified_against_page_image':True}
 return {'recipe_conditions':rows,'selected_combination':None,'personal_outcome':None,
    'notice':'Separate text conditions only, not cancellation of every adverse factor. Aspect system remains caller-grounded. OriginalVII.28 explicitly glosses auspicious as other than6/8/12. No strength threshold, global priority or personal event inferred.'}


def printed_cancellation_illustration_audit():
 """Kapoor PDF90 displayed signs versus accompanying prose; not natal truth."""
 from .forecast import sign_index
 reference='Leo'
 placements={'Saturn':'Aries','Mars':'Aquarius','Sun':'Sagittarius','Venus':'Capricorn'}
 houses={p:(sign_index(s)-sign_index(reference))%12+1 for p,s in placements.items()}
 return {'source':{'title':'Kapoor Phaladeepika','pdf_page':90,'verified_against_page_image':True},
  'reference_sign':reference,'moon_sign':reference,'displayed_placements':placements,
  'whole_sign_houses':houses,'mars_kendra_claim_matches':houses['Mars'] in (1,4,7,10),
  'sun_kendra_claim_matches':houses['Sun'] in (1,4,7,10),
  'duplicate_node_label':'Ketu appears in Aries and Scorpio',
  'cancellation_condition_used_to_arbitrate_schools':None,
  'notice':'Image/prose inconsistency exposed, not repaired. This figure cannot establish astronomical inputs, select either/both or silently move Sun to match prose.'}
