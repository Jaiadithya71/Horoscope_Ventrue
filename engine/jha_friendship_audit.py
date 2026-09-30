"""Independent Jha3 direct Rasi friendship worked audit, not varga arbitration."""
from .bphs_jha_general_aspect import SOURCE_URL
from .friendship import natural_relation,compound_relation


def jha_friendship_audit():
 signs={'Sun':6,'Moon':12,'Mars':6,'Mercury':6,'Jupiter':4,'Venus':5,'Saturn':1}
 expected={'Moon':'neutral','Mars':'neutral','Mercury':'enemy','Jupiter':'very_friend','Venus':'neutral','Saturn':'very_enemy'}
 rows=[]
 for p,printed in expected.items():
  house=(signs[p]-signs['Sun'])%12+1;natural=natural_relation('Sun',p)
  # Existing numerical mapping is independently checked, not relabeled as Jha implementation.
  result=compound_relation(natural,house)['compound_relation']
  rows.append({'planet':'Sun','other':p,'other_rasi_from_sun':house,'natural_relation':natural,
   'temporary_relation':'friend' if house in (2,3,4,10,11,12) else 'enemy',
   'existing_mapping_result':result,'printed_jha_worked_relation':printed,'matches':result==printed})
 return {'profile':'jha_sudha3_direct_rasi_friendship_worked_audit','printed_rasi_indices_1_based':signs,
  'sun_directed_rows':rows,'worked_matches':sum(r['matches'] for r in rows),
  'source':{'url':SOURCE_URL,'pdf_pages':[49,50,51],'printed_pages':[17,18,19],
   'chapter':3,'slokas':'56-62','verified_against_page_image':True},
  'numeric_varga_weights_comparison':{'jha28_3_virupa':{'moolatrikona':45,'own':30,'very_friend':20,'friend':15,'neutral':10,'enemy':4,'very_enemy':2},
   'sripati_direct_owner_virupa':{'moolatrikona':45,'own':30,'very_friend':22.5,'friend':15,'neutral':7.5,'enemy':3.75,'very_enemy':1.875},
   'jha_source_pdf_page':186,'jha_source_printed_page':154,'weights_interchangeable':False},
  'sripati_owner_placement_arbitration_resolved':False,'selected_varga_profile':None,'full_strength':None,
  'notice':'Jha chapter3 independently corroborates the directed Rasi compound mapping with six Sun examples. This does not select Sripati Rasi versus recast Bhava, directowner versus ownerplacement scoring, or common numericweights. Existing helper provenance stays its own; no Jha natal vargasum or stronger/weaker flag is enabled.'}
