"""Coherent labeled five-piece hypotheses, not selected positional strength."""
from .continuous_strength import continuous_components,source
from .seven_varga_strength import chart_direct_owner_candidates

PAIRS=(('rasi_relative','rasi_house'),('lagna_bhava_relative','sripati_degree_bhava'))


def positional_candidates(placements):
 continuous=continuous_components(placements)['planets']
 varga=chart_direct_owner_candidates(placements)
 out=[]
 for row in varga['planets']:
  planet=row['planet'];c=continuous[planet];candidates=[]
  for relation,house in PAIRS:
   v=next(x['component'] for x in row['candidates'] if x['house_profile']==relation)
   k=next((x for x in c['kendradibala_candidates']['candidates'] if x['profile']==house),None)
   pieces={'uchcha':c['uchchabala']['rupa'],'seven_varga_direct_owner':v['rupa'],
           'rasi_navamsa_parity':c['yugmayugmabala']['rupa'],'house_category':None if k is None else k['rupa'],
           'base_decan':c['drekkanabala']['rupa']}
   missing=[name for name,value in pieces.items() if value is None]
   candidates.append({'relation_profile':relation,'house_category_profile':house,
     'decan_profile':'base_quarter_rupa_not_own_shadvarga_refinement',
     'profile_pairing_status':'Explicit modeling hypothesis, not a source mandate equating relationship and Kendra house conventions',
     'pieces_rupa':pieces,'base_five_piece_sum_rupa':None if missing else sum(pieces.values()),
     'unresolved_pieces':missing,'seven_varga_evidence':v,
     'continuous_piece_evidence':{name:c[name] for name in ('uchchabala','yugmayugmabala','kendradibala_candidates','drekkanabala')},
     'not_included':['owner-own-placement/recast relationship alternative','quoted own-Shadvarga decan refinement'],
     'source':source('2-5 positional five-piece table',53,39)})
  vals=[x['base_five_piece_sum_rupa'] for x in candidates]
  out.append({'planet':planet,'candidates':candidates,'candidate_difference_present':len(set(vals))>1,
              'selected_positional_total':None,'full_strength_total':None})
 return {'planets':out,'selected_profile':None,'selected_positional_total':None,'full_strength_total':None,
    'notice':'Five-piece sums are explicit coherent base-model hypotheses only. No mixed Rasi/Bhava fallback, selected full positional total, planet rank, Bhava lord strength, rectification, outcome probability or prediction is enabled.'}
