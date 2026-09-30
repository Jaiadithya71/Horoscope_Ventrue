"""Coherent labeled five-piece hypotheses, not selected positional strength."""
from .continuous_strength import continuous_components,source
from .seven_varga_strength import chart_direct_owner_candidates

PAIRS=(('rasi_relative','rasi_house'),('lagna_bhava_relative','sripati_degree_bhava'))
INDEPENDENT_PAIRS=PAIRS+(('rasi_relative','sripati_degree_bhava'),('lagna_bhava_relative','rasi_house'))


def positional_candidates(placements):
 continuous=continuous_components(placements)['planets']
 varga=chart_direct_owner_candidates(placements)
 out=[]
 for row in varga['planets']:
  planet=row['planet'];c=continuous[planet];candidates=[]
  for relation,house in INDEPENDENT_PAIRS:
   v=next(x['component'] for x in row['candidates'] if x['house_profile']==relation)
   k=next((x for x in c['kendradibala_candidates']['candidates'] if x['profile']==house),None)
   pieces={'uchcha':c['uchchabala']['rupa'],'seven_varga_direct_owner':v['rupa'],
           'rasi_navamsa_parity':c['yugmayugmabala']['rupa'],'house_category':None if k is None else k['rupa'],
           'base_decan':c['drekkanabala']['rupa']}
   missing=[name for name,value in pieces.items() if value is None]
   candidates.append({'relation_profile':relation,'house_category_profile':house,
     'decan_profile':'base_quarter_rupa_not_own_shadvarga_refinement',
     'profile_pairing_status':'Independent relation and house-category axes; source does not mandate their coupling',
     'house_category_school':{'sripati_commentator_and_balabhadra':'sripati_degree_bhava','quoted_parashara_and_kesava':'rasi_house'},
     'house_category_school_source':source('5 commentary',52,38),
     'pieces_rupa':pieces,'base_five_piece_sum_rupa':None if missing else sum(pieces.values()),
     'unresolved_pieces':missing,'seven_varga_evidence':v,
     'continuous_piece_evidence':{name:c[name] for name in ('uchchabala','yugmayugmabala','kendradibala_candidates','drekkanabala')},
     'not_included':['owner-own-placement/recast relationship alternative','quoted own-Shadvarga decan refinement'],
     'source':source('2-5 positional five-piece table',53,39)})
  vals=[x['base_five_piece_sum_rupa'] for x in candidates]
  out.append({'planet':planet,'candidates':candidates[:2],'independent_profile_matrix':candidates,'candidate_difference_present':len(set(vals))>1,
              'selected_positional_total':None,'full_strength_total':None})
 return {'planets':out,'selected_profile':None,'selected_positional_total':None,'full_strength_total':None,
    'candidate_axes':{'relation_profile':['rasi_relative','lagna_bhava_relative'],'house_category_profile':['rasi_house','sripati_degree_bhava']},
    'notice':'Legacy paired candidates remain available, but the full four-row matrix exposes independent choices rather than assuming relation/house coupling. The Sripati commentator favors Bhava house-category while quoted Parashara/Kesava favor Rasi; this does not select a temporary-friendship convention. Five-piece sums are explicit coherent base-model hypotheses only. No mixed Rasi/Bhava fallback, selected full positional total, planet rank, Bhava lord strength, rectification, outcome probability or prediction is enabled.'}
