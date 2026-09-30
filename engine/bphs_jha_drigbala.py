"""JhaSudha28.19 coordinate-to-aspect arithmetic, never a whole natal strength."""
from fractions import Fraction as F
from .bphs_jha_special_aspect import bphs_jha_aspect_candidates,CLASSICAL
from .bphs_jha_general_aspect import SOURCE_URL


def bphs_jha_drigbala(target,longitudes,classifications,*,coordinate_profile,classification_profile):
 if target not in CLASSICAL:raise ValueError('Classical target required')
 if not isinstance(longitudes,dict) or set(longitudes)-set(CLASSICAL):raise ValueError('Classical longitude mapping required')
 others=set(CLASSICAL)-{target}
 if not isinstance(classifications,dict) or set(classifications)-others:raise ValueError('Only other classical classifications required')
 for p in (coordinate_profile,classification_profile):
  if not isinstance(p,str) or not p.strip():raise ValueError('Named coordinate and classification provenance required')
 # Validate every supplied coordinate even when target is absent.
 from .bphs_jha_general_aspect import number
 for v in longitudes.values():
  if v is not None:number(v)
 rows=[];blocked=[]
 for planet in CLASSICAL:
  if planet==target:continue
  kind=classifications.get(planet)
  if kind is not None and kind not in ('benefic','malefic'):raise ValueError('Explicit benefic/malefic or unknown required')
  geometry=None;reasons=[]
  if longitudes.get(target) is None or longitudes.get(planet) is None:reasons.append('missing_longitude')
  else:geometry=bphs_jha_aspect_candidates(planet,longitudes[planet],longitudes[target],coordinate_profile=coordinate_profile)
  amount=None if geometry is None else geometry['determinate_unsigned_virupa_rational']
  if geometry and amount is None:reasons.append('unresolved_geometry_boundary')
  if kind is None:reasons.append('missing_classification')
  a=None if amount is None else F(amount)
  quarter=None if a is None or kind is None else a/4*(1 if kind=='benefic' else -1)
  extra=None if a is None else a if planet in ('Mercury','Jupiter') else F(0)
  net=None if quarter is None or extra is None else quarter+extra
  if reasons:blocked.append(planet)
  rows.append({'aspecting_planet':planet,'geometry':geometry,'supplied_classification':kind,
   'signed_quarter_virupa_rational':str(quarter) if quarter is not None else None,
   'full_mercury_jupiter_extra_virupa_rational':str(extra) if extra is not None else None,
   'candidate_net_virupa_rational':str(net) if net is not None else None,'blockers':reasons})
 total=None if blocked else sum(F(r['candidate_net_virupa_rational']) for r in rows)
 return {'profile':'bphs_jha_sudha28_19_directed_signedquarter_plus_full_mercury_jupiter',
  'target':target,'coordinate_profile':coordinate_profile,'classification_profile':classification_profile,
  'rows':rows,'blocked_planets':blocked,'candidate_drigbala_virupa_rational':str(total) if total is not None else None,
  'candidate_drigbala_rupa_rational':str(total/60) if total is not None else None,
  'source':{'url':SOURCE_URL,'pdf_pages':[189,190],'printed_pages':[157,158],'chapter':28,'sloka':19,
   'verified_against_page_image':True},'selected_strength_profile':None,'complete_total_strength':None,
  'notice':'Exact source-specific aspect adjustment only, self excluded. Missing target/aspector positions, explicit classes or unresolved special boundary blocks total. Mercury full extra remains separate even under suppliedmalefic classification. This reuses Jha geometry, not Santhanam commentary or Sripati; caller coordinates/classes are not book-certified. Never add to a Drik-inclusive suppliedtotal.'}
