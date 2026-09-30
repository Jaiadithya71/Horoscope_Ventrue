"""BPHS27.19 supplied aspect-amount arithmetic, not a geometry/profile winner."""
from decimal import Decimal as D,InvalidOperation

CLASSICAL=('Sun','Moon','Mars','Mercury','Jupiter','Venus','Saturn')
SOURCE_URL='https://ia903205.us.archive.org/30/items/brihatparasarahorashastrabyr.santhanam/Brihat%20Par%C4%81%C5%9Bara%20Hor%C4%81%20%C5%9Ah%C4%81stra%20By%20R.%20Santhanam.pdf'


def bphs_supplied_drigbala(target,aspect_amounts_virupa,classifications,*,aspect_profile,classification_profile):
 if target not in CLASSICAL:raise ValueError('Classical target required')
 if not all(isinstance(p,str) and p.strip() for p in (aspect_profile,classification_profile)):raise ValueError('Named aspect and classification provenance required')
 others=set(CLASSICAL)-{target}
 if not isinstance(aspect_amounts_virupa,dict) or set(aspect_amounts_virupa)-others:raise ValueError('Only six other classical aspect amounts permitted')
 if not isinstance(classifications,dict) or set(classifications)-others:raise ValueError('Only six other classical classifications permitted')
 rows=[];missing=[]
 for p in CLASSICAL:
  if p==target:continue
  x=aspect_amounts_virupa.get(p);kind=classifications.get(p)
  if kind is not None and kind not in ('benefic','malefic'):raise ValueError('Explicit benefic/malefic class or unknown required')
  amount=None
  if x is not None:
   if isinstance(x,bool):raise ValueError('Finite aspect magnitude0..60virupa required')
   try:amount=D(str(x))
   except InvalidOperation as exc:raise ValueError('Numeric aspect magnitude required') from exc
   if not amount.is_finite() or not 0<=amount<=60:raise ValueError('Finite aspect magnitude0..60virupa required')
  if amount is None or kind is None:missing.append(p)
  quarter=None if amount is None or kind is None else amount/4*(1 if kind=='benefic' else -1)
  extra=None if amount is None else amount if p in ('Mercury','Jupiter') else D(0)
  net=None if quarter is None or extra is None else quarter+extra
  rows.append({'aspecting_planet':p,'supplied_unsigned_virupa':str(amount) if amount is not None else None,
   'supplied_classification':kind,'signed_quarter_virupa':str(quarter) if quarter is not None else None,
   'full_mercury_jupiter_extra_virupa':str(extra) if extra is not None else None,
   'candidate_net_virupa':str(net) if net is not None else None})
 total=None if missing else sum(D(r['candidate_net_virupa']) for r in rows)
 return {'target':target,'profile':'bphs27_19_signed_quarter_plus_full_mercury_jupiter',
  'aspect_profile':aspect_profile,'classification_profile':classification_profile,'rows':rows,
  'missing_planets_or_classifications':missing,'candidate_drigbala_virupa':str(total) if total is not None else None,
  'candidate_drigbala_rupa':str(total/60) if total is not None else None,
  'source':{'url':SOURCE_URL,'pdf_page':235,'printed_page':225,'chapter':27,'sloka':19,'verified_against_page_image':True},
  'unsigned_geometry_source_gates':{
   'source_url':SOURCE_URL,'pdf_pages':[209,210,211],'printed_pages':[199,200,201],
   'verified_against_page_image':True,
   'conflicts':['General English subtraction direction differs from Mars/Jupiter direction',
    'Rule6 above160 overlaps150to180 branch',
    'Mars simplified range210to249 differs from main7sign interval',
    'Simplified constant additions do not generally match special-planet main formulas'],
   'sripati_geometry_imported':False,'unique_bphs_geometry_verified':False},
  'selected_geometry_profile':None,'selected_strength_profile':None,'complete_total_strength':None,
  'notice':'Santhanam reproduction27.19 additive reading on explicitly supplied unsigned aspect magnitudes/classifications. No Sripati geometry imported as BPHS, self-aspect, hidden classification, strength-total assembly or profile winner. Quarter sign and fullMercury/Jupiter extra are shown separately, including a supplied maleficMercury case. Missing class even at zero aspect remains unknown. Use only once within a caller-validated source-consistent composition; not an additional adjustment to a Drik-inclusive total.'}
