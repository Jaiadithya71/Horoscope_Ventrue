"""Page-checked conditional livelihood readings, never a selected life verdict.

Phaladeepika IV.23 requires full strength examination before declaring effects.
V.1 selects a strongest route, which is not supplied by coordinate geometry.
"""
import math
from .forecast import SIGNS
from .synthesis import LORDS, LORD_SOURCE
from .vargas import six_vargas

URL='https://archive.org/details/in.ernet.dli.2015.92117'

def source(sloka,pages):
 return {'slug':'phaladeepika-1937','chapter':'V','sloka':sloka,
  'pdf_pages':pages,'printed_pages':[p-37 for p in pages],
  'url':URL,'verified_against_page_image':True}

SELECTION_SOURCE=source(1,[80,81])
STRENGTH_GATE={'slug':'phaladeepika-1937','chapter':'IV','sloka':23,
 'pdf_page':79,'printed_page':42,'url':URL,'verified_against_page_image':True}
# Restricted, non-stigmatizing excerpts, not an exhaustive translation. Keep
# omitted ethical/caste/violent allegations out of personal chart prose.
OCCUPATIONS={
 'Sun':(2,[81],['fruit trees','mantra recitation','wool','medicine','metal work','service under a ruler or respected person']),
 'Moon':(3,[81],['trade in water products such as pearls and coral','agriculture','cattle farming','pilgrimage','service under a woman','clothing trade']),
 'Mars':(4,[81],['metals','battle','cooking','land','gold','weapons','adventurous work']),
 'Mercury':(5,[81,82],['poetry','scriptural study','writing and clerical work','astrology','Vedic study for others','mantra recitation','priestly work']),
 'Jupiter':(6,[82],['religious patronage','royal patronage','reciting Puranas','study of Sastras','moral and religious instruction','money lending']),
 'Venus':(7,[82],['support through a woman','livestock','dance and vocal or instrumental music','silver','scents','milk','ornaments','silk','service as a ruler\'s companion','poetry']),
 'Saturn':(8,[82,83],['roots and fruits','physical labor','work through servants','grain','carrying loads','sculpture','wood work']),
}
SUMMARY={
 'Sun':'fruit trees, wool, medicine, metals, ritual work, or service under a ruler or respected person',
 'Moon':'water-product or clothing trade, agriculture, cattle farming, pilgrimage, or service under a woman',
 'Mars':'metals, land, gold, cooking, battle, weapons, or adventurous work',
 'Mercury':'writing, poetry, clerical work, scriptural study, astrology, or priestly work',
 'Jupiter':'religious instruction, scriptural study, patronage, or money lending',
 'Venus':'music, dance, poetry, ornaments, scents, silk, dairy, livestock, or court companionship',
 'Saturn':'physical labor, carrying loads, grain, roots and fruits, sculpture, or wood work',
}

def _longitude(value):
 if type(value) not in (int,float) or not math.isfinite(value) or not 0<=value<360:
  raise ValueError('Finite numeric sidereal longitude in [0,360) required')
 return value


def life_aspect_candidates(chart):
 """Three whole-sign reference candidates; no ranking, mixing, or timing."""
 placements=chart['placements']
 lons={p:_longitude(placements[p]['longitude']) for p in LORDS}
 asc=_longitude(chart['ascendant']['longitude'])
 for p,lon in lons.items():
  if placements[p]['sign']!=SIGNS[int(lon//30)]:
   raise ValueError('Placement sign disagrees with longitude')
 if chart['ascendant']['sign']!=SIGNS[int(asc//30)]:
  raise ValueError('Ascendant sign disagrees with longitude')
 rows=[]
 for label,lon in [('Lagna',asc),('Moon',lons['Moon']),('Sun',lons['Sun'])]:
  tenth=(int(lon//30)+9)%12
  lord=LORDS[tenth]
  nav=next(v for v in six_vargas(lons[lord])['vargas'] if v['varga']=='navamsa')
  owner=nav['owner'];sloka,pages,examples=OCCUPATIONS[owner]
  rows.append({'reference':label,'reference_sign':SIGNS[int(lon//30)],
   'house_model':'whole_sign_reference_candidate_not_selected_bhava_model',
   'tenth_sign':SIGNS[tenth],'tenth_lord':lord,'tenth_lord_longitude':lons[lord],
   'navamsa_sign':nav['sign'],'navamsa_owner':owner,
   'historical_livelihood_examples':list(examples),'occupation_source':source(sloka,pages),
   'geometry_sources':[LORD_SOURCE,nav['source']],
   'conditional_reading':f'If the {label} route is the strongest, this tradition links livelihood to {SUMMARY[owner]}.',
   'reference_selected':False,'navamsa_owner_strength':None,
   'wealth_conditional_reading':'The source associates a strong Navamsa owner with easier acquisition of wealth, and a weak owner with little wealth. Its strength is not established here.',
   'wealth_source':source(9,[83]),'income_level':None,'timing':None})
 return {'status':'conditional_source_readings_not_selected_personal_forecast',
  'career':{'candidates':rows,'selected_reference':None,'selected_profession':None,
   'selection_source':SELECTION_SOURCE,
   'unresolved':['Strongest Lagna/Moon/Sun route and its comparison semantics','Complete source-compatible strength examination','Whole-sign versus degree-bhava rule application'],
   'notice':'These are alternative historical livelihood readings, not three jobs you will have. No specific modern profession or employer is inferred.'},
  'wealth':{'candidate_reference':'career.candidates[*].wealth_conditional_reading','selected_outcome':None,
   'notice':'Conditional acquisition/ease only. No income amount, financial recommendation, or foreign move is predicted.'},
  'marriage':{'status':'not_yet_source_selected','reading':None},
  'health':{'status':'no_medical_prediction','reading':None},
  'timing':{'status':'calendar_and_outcome_selection_unresolved','reading':None},
  'strength_gate_source':STRENGTH_GATE,'empirical_accuracy':None,
  'notice':'Non-stigmatizing livelihood examples are a disclosed subset of V.2-8, not a complete translation. Ethical allegations, caste labels and violent roles are not attributed to the person. Gendered historical examples are not assumptions about the person. No Balaji consultation method or predictive validity is established.'}
