"""Printed JhaSudha thresholds and enumeration audit, no strength flag winner."""
from .bphs_jha_general_aspect import SOURCE_URL
from .bphs_jha_special_aspect import CLASSICAL


def jha_strength_threshold_audit():
 prose=dict(zip(CLASSICAL,(390,360,300,420,390,360,300)))
 table=dict(zip(CLASSICAL,(397,360,300,430,390,330,300)))
 groups=[(['Sun','Mercury','Jupiter'],[165,35,50,112,30]),
  (['Moon','Venus'],[133,50,30,100,40]),(['Mars','Saturn'],[96,30,40,67,20])]
 rows=[]
 for planets,values in groups:
  # Verse order cheshta then samaya; Hindi sentence reverses those labels.
  sanskrit_table=dict(zip(('positional','directional','motion','temporal','ayana'),values))
  hindi=dict(zip(('positional','directional','temporal','motion','ayana'),values))
  for p in planets:
   rows.append({'planet':p,'sanskrit_order_and_printed_table_virupa':sanskrit_table.copy(),
    'hindi_prose_heading_order_virupa':hindi.copy(),
    'different_component_labels':[k for k in sanskrit_table if sanskrit_table[k]!=hindi[k]]})
 return {'total_threshold_rows':[{'planet':p,'printed_prose_virupa':prose[p],
   'printed_table_virupa':table[p],'table_minus_prose_virupa':table[p]-prose[p]} for p in CLASSICAL],
  'disagreeing_total_planets':[p for p in CLASSICAL if prose[p]!=table[p]],
  'component_threshold_rows':rows,
  'total_source':{'url':SOURCE_URL,'pdf_pages':[191,192],'printed_pages':[159,160],
   'chapter':28,'slokas':'32-36','verified_against_page_image':True},
  'sixfold_enumeration':{'source_pdf_page':190,'source_printed_page':158,'sloka':'25.5',
   'printed_classes':['positional','directional','temporal','aspect','motion','natural'],
   'ayana_containment_selected':None},
  'selected_threshold_profile':None,'selected_composition_profile':None,
  'computed_natal_strong_weak_flags':None,'full_strength_available':False,
  'notice':'Printed-source diagnostics only. Hindi component heading order differs from Sanskrit/table order; Sun/Mercury/Venus total thresholds disagree across prose/table. Ayana30 for Sun/Mercury/Jupiter is visually verified, not OCR60. Six-class enumeration does not prove which term contains Ayana. No corrected values, natal totals or strong/weak flags are selected; partial component thresholds do not certify whole strength.'}
