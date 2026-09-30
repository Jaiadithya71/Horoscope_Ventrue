"""Raman art121 declared supplied composition and independent table arithmetic."""
from decimal import Decimal as D,InvalidOperation
from .raman_motion_source_audit import SOURCE_URL

BASE={'sthana','dig','kala_including_ayana','chesta_excluding_ayana','natural'}
# Printed component rows; ellipses for Sun/Moon motion are not certified zero.
DATA=[('Sun',['198.00','48.10','102.98',None,'60.00','15.86'],'424.24','7.08'),
 ('Moon',['126.50','31.56','202.04',None,'51.43','-21.73'],'389.80','6.50'),
 ('Mars',['172.06','55.70','33.06','22.23','17.14','0.95'],'298.14','4.97'),
 ('Mercury',['279.50','21.09','192.79','2.30','25.70','15.64'],'537.02','8.85'),
 ('Jupiter',['157.58','11.50','211.18','35.26','34.28','-16.03'],'433.71','7.23'),
 ('Venus',['178.20','15.15','115.53','5.95','42.85','18.47'],'376.15','6.27'),
 ('Saturn',['177.30','58.02','116.97','21.14','8.37',None],'389.21','6.49')]


def source():
 return {'url':SOURCE_URL,'pdf_pages':[67,68,94,95],'printed_pages':[62,63,89,90],
  'articles':[78,121],'verified_against_page_image':True}


def raman_supplied_composition(components,*,declared_complete,component_profile,war_treatment):
 if type(declared_complete) is not bool:raise ValueError('Completeness must be bool')
 if not isinstance(component_profile,str) or not component_profile.strip():raise ValueError('Named source/input profile required')
 if war_treatment not in ('confirmed_no_war','included_in_supplied_kala','excluded_candidate'):raise ValueError('Explicit war treatment required')
 if not isinstance(components,dict) or set(components)-(BASE|{'signed_drik'}):raise ValueError('Only named Raman rows allowed; no separate or inclusive-motion Ayana')
 values={}
 for key,x in components.items():
  if x is None:continue
  if isinstance(x,bool):raise ValueError('Finite numeric virupa required')
  try:v=D(str(x))
  except InvalidOperation as exc:raise ValueError('Finite numeric virupa required') from exc
  if not v.is_finite() or (key!='signed_drik' and v<0):raise ValueError('Base must be nonnegative; only Drik signed')
  values[key]=v
 missing=sorted((BASE|{'signed_drik'})-set(values))
 total=sum(values.values()) if declared_complete and not missing else None
 return {'profile':'raman_art121_ayana_in_kala','component_profile':component_profile,'declared_complete':declared_complete,
  'war_treatment':war_treatment,'missing_components':missing,'candidate_sum_virupa':str(total) if total is not None else None,
  'candidate_sum_rupa':str(total/60) if total is not None else None,'negative_candidate':total<0 if total is not None else None,
  'source':source(),'engine_certified_strength':None,'selected_strength_profile':None,
  'notice':'Source-scoped arithmetic on declared supplied virupa rows only. Ayana already within Kala, not added separately or again through inclusive motion. Signed Drik retained without clipping. Missing or incomplete rows block total; blank print entries are not automatic zero. War is supplied context, not verified detection; no second transfer. No partial-to-complete certification, natal threshold/rank or predictor.'}


def raman_printed_composition_audit():
 rows=[]
 for planet,parts,total,rupa in DATA:
  hypotheses=[('all_printed_numeric',parts)]
  if planet in ('Sun','Moon'):
   replacement=list(parts);replacement[3]='0'
   hypotheses=[('printed_motion_ellipsis_as_zero_candidate',replacement)]
  if planet=='Saturn':
   hypotheses=[]
   for sign in ('','-'):
    replacement=list(parts);replacement[5]=sign+'7.21'
    hypotheses.append(('unsigned_drik_as_'+('positive' if not sign else 'negative')+'_candidate',replacement))
  candidates=[]
  for label,vals in hypotheses:
   computed=sum(D(v) for v in vals)
   candidates.append({'profile':label,'computed_virupa':str(computed),'computed_rupa':str(computed/60),
    'sum_minus_printed_total_virupa':str(computed-D(total))})
  rows.append({'planet':planet,'printed_components_virupa':parts,'printed_total_virupa':total,'printed_total_rupa':rupa,
   'printed_total_divided_by60_rupa':str(D(total)/60),
   'division_minus_printed_rupa':str(D(total)/60-D(rupa)),'sum_candidates':candidates})
 return {'rows':rows,'mars_kala_cross_table':{'earlier_pdf67_virupa':'30.060','later_pdf94_virupa':'33.06','difference_virupa':'3.000'},
  'source':source(),'selected_printed_correction':None,'coherent_full_chart_benchmark':False,
  'notice':'Printed arithmetic audit, not true-strength reconstruction. Luminary motion ellipses are explicit zero hypotheses only. Saturn unmarked Drik sign kept both ways. Mars Kala cross-table difference and Mercury rupa mismatch retained. No repair or ranked planet selected.'}
