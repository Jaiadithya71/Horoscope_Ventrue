"""XV.1 translation discrepancy and XV.5 scoped recovery, not outcomes."""
from .debilitation_cancellation_candidates import _and,_or


def _validate(*values):
 if any(x is not None and type(x) is not bool for x in values):
  raise ValueError('Grounded bool or None required')


def _not(value):return None if value is None else not value


def xv1_dignity_qualification(depressed=None,eclipsed=None,inimical_sign=None):
 """Other XV.1 conditions are outside this isolated final qualification."""
 _validate(depressed,eclipsed,inimical_sign)
 safe=_and(_and(_not(depressed),_not(eclipsed)),_not(inimical_sign))
 literal=_and(_and(depressed,eclipsed),inimical_sign)
 return {'qualification_candidates':[
  {'source':'original1937 PDF189 printed152 XV.1','reading':'not depressed, not eclipsed, not inimical','condition':safe},
  {'source':'Kapoor PDF145 XV.1','reading':'literal reproduction omits negation: depressed, combust and inimical','condition':literal}],
  'source_negation_discrepancy':True,'selected_profile':None,'personal_outcome':None,
  'notice':'Final dignity clause only. Literal later reproduction is retained as an error/discrepancy candidate, not a verified alternative classical school or global adverse-dignity override. Other ownership/occupation/aspect and malefic-free requirements are not certified.'}


def xv5_recovery_condition(lord_in_dusthana=None,occupied_by_dusthana_lord=None,
                          benefic_aspect=None):
 _validate(lord_in_dusthana,occupied_by_dusthana_lord,benefic_aspect)
 adverse=_or(lord_in_dusthana,occupied_by_dusthana_lord)
 recovery=_and(adverse,benefic_aspect)
 adverse_without_recovery=_and(adverse,_not(benefic_aspect))
 return {'adverse_base_condition':adverse,'benefic_aspect_exception':recovery,
  'adverse_condition_without_checked_exception':adverse_without_recovery,
  'selected_personal_effect':None,'global_precedence':None,
  'source':{'slug':'phaladeepika-1937','chapter':'XV','sloka':5,'pdf_page':191,
     'printed_page':154,'verified_against_page_image':True},
  'comparison_source':{'title':'Kapoor Phaladeepika','pdf_page':147,'verified_against_page_image':True},
  'notice':'Scoped XV.5 exception only. No universal recovery over XV.3/6 or other rules, no strength or timing decision. Lord/dusthana frame and aspect convention must be grounded externally. Missing aspect is unknown, not no recovery; no adverse base does not itself imply favorable result.'}


def chart_xv5_candidates(house,ascendant_sign,placements,classifications,*,classification_profile):
 """Target-house/lord geometry hypotheses and explicitly supplied classes."""
 from .forecast import sign_index
 from .synthesis import LORDS,LORD_SOURCE,ASPECT_SOURCE
 from .friendship import CLASSICAL
 if type(house) is not int or not 1<=house<=12:raise ValueError('House1..12 required')
 if not classification_profile:raise ValueError('Named supplied classification profile required')
 if any(p not in CLASSICAL or k not in ('benefic','malefic') for p,k in classifications.items()):
  raise ValueError('Supplied classical benefic/malefic classes required')
 asc=sign_index(ascendant_sign);target=(asc+house-1)%12
 lord=LORDS[target]
 def OR(values):
  r=False
  for value in values:r=_or(r,value)
  return r
 def occupied(p,profile):
  pos=placements.get(p,{})
  if profile=='whole_sign':
   return None if pos.get('sign') is None else (sign_index(pos['sign'])-asc)%12+1
  value=pos.get('sripati_degree_house')
  h=value.get('house') if isinstance(value,dict) else value
  if h is not None and (type(h) is not int or not 1<=h<=12):raise ValueError('Degree house1..12 or unknown required')
  return h
 rows=[]
 for house_profile in ('whole_sign','sripati_degree_bhava'):
  lord_house=occupied(lord,house_profile)
  for frame in ('ascendant_dusthanas','target_house_dusthanas'):
   bad={6,8,12} if frame=='ascendant_dusthanas' else {(house+h-2)%12+1 for h in (6,8,12)}
   bad_lords=sorted({LORDS[(asc+h-1)%12] for h in bad})
   lord_bad=None if lord_house is None else lord_house in bad
   bad_occupant=OR([None if occupied(p,house_profile) is None else occupied(p,house_profile)==house for p in bad_lords])
   for aspect_profile in ('whole_sign_full','whole_sign_seventh_only'):
    pairs=[]
    for planet in CLASSICAL:
     pos=placements.get(planet,{});sign=pos.get('sign');kind=classifications.get(planet)
     relative=None if sign is None else (target-sign_index(sign))%12+1
     full={7}|({'Mars':{4,8},'Jupiter':{5,9},'Saturn':{3,10}}.get(planet,set()) if aspect_profile=='whole_sign_full' else set())
     aspect=None if relative is None else relative in full
     benefic=None if kind is None else kind=='benefic'
     pairs.append({'planet':planet,'supplied_class':kind,'relative_sign_house':relative,
        'aspect_condition':aspect,'benefic_aspect_condition':_and(benefic,aspect)})
    flags=OR([p['benefic_aspect_condition'] for p in pairs])
    rows.append({'occupation_profile':house_profile,'dusthana_reference':frame,
      'dusthana_houses_from_ascendant':sorted(bad),'dusthana_lords':bad_lords,
      'house_lord':lord,'lord_house_from_ascendant':lord_house,
      'aspect_profile':aspect_profile,'aspect_target':'target_Rasi_not_degree_Bhava_centre',
      'supplied_aspect_class_evidence':pairs,
      'condition_evidence':xv5_recovery_condition(lord_bad,bad_occupant,flags)})
 return {'house':house,'reference_sign':ascendant_sign,'classification_profile':classification_profile,
  'candidates':rows,'geometry_sources':[LORD_SOURCE,ASPECT_SOURCE],
  'selected_profile':None,'personal_outcome':None,
  'notice':'KapoorXV.5 specifies Lagna placement, original translation leaves dusthana frame less explicit. Both reference frames remain hypotheses. Degree-Bhava occupation does not change sign ownership or make sign aspects centre-target degree aspects. Partial positions/classes can prove a supplied qualifying aspect, but cannot prove its absence. No selected benefic class, strength, global recovery or personal effect.'}
