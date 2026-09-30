"""JhaSudha special-planet formulas with unresolved boundary jumps retained."""
from fractions import Fraction as F
from .bphs_jha_general_aspect import bphs_jha_general_aspect,SOURCE_URL

CLASSICAL=('Sun','Moon','Mars','Mercury','Jupiter','Venus','Saturn')


def interval_value(planet,signs,u):
 if planet=='Saturn':
  if signs==1:return 2*u,'Saturn one-sign twice traversed degrees'
  if signs==2:return 60-u/2,'Saturn two-sign60 minus half traversed degrees'
  if signs==8:return 30+u,'Saturn eight-sign30 plus traversed degrees'
  if signs==9:return 30-u,'Saturn nine-sign remaining degrees'
 if planet=='Mars':
  if signs==2:return 15+F(3,2)*u,'Mars two-sign15 plus1.5 traversed degrees'
  if signs in (3,7):return 60-u,'Mars three/seven-sign60 minus traversed degrees'
  if signs==6:return F(60),'Mars six-sign full60'
 if planet=='Jupiter':
  if signs in (3,7):return 45+u/2,'Jupiter three/seven-sign45 plus half traversed degrees'
  if signs in (4,8):return 60-2*u,'Jupiter four/eight-sign60 minus twice traversed degrees'
 # Extend each general piece only to its adjacent endpoints.
 if signs in (0,10,11):return F(0),'general zero interval'
 if signs==1:return u/2,'general one-sign half traversed degrees'
 if signs==2:return 15+u,'general two-sign15 plus traversed degrees'
 if signs==3:return 45-u/2,'general three-sign45 minus half traversed degrees'
 if signs==4:return 30-u,'general four-sign remaining degrees'
 if signs==5:return 2*u,'general five-sign twice traversed degrees'
 return (300-(signs*30+u))/2,'general beyond six-sign half remaining to300'


def bphs_jha_aspect_candidates(planet,aspector_longitude,aspected_longitude,*,coordinate_profile):
 if planet not in CLASSICAL:raise ValueError('Classical aspecting planet required')
 general=bphs_jha_general_aspect(aspector_longitude,aspected_longitude,coordinate_profile=coordinate_profile)
 delta=F(general['directed_difference_degrees_rational']);k=int(delta//30);u=delta-k*30
 boundary=delta>0 and u==0
 intervals=[(k,u,'right_interval')]
 if boundary:intervals.insert(0,(k-1,F(30),'left_interval'))
 rows=[]
 for signs,arc,side in intervals:
  value,label=interval_value(planet,signs,arc)
  rows.append({'interval_side':side,'completed_signs':signs,'traversed_degrees_rational':str(arc),
   'rule':label,'unsigned_aspect_virupa_rational':str(value)})
 values=sorted(set(F(r['unsigned_aspect_virupa_rational']) for r in rows))
 return {'profile':'bphs_jha_sudha27_special_directed_candidates','aspecting_planet':planet,
  'coordinate_profile':coordinate_profile,'directed_difference_degrees_rational':str(delta),
  'formula_candidates':rows,'distinct_unsigned_virupa_rational':[str(v) for v in values],
  'determinate_unsigned_virupa_rational':str(values[0]) if len(values)==1 else None,
  'exact_sign_boundary':boundary,'boundary_convention_selected':None,
  'source':{'url':SOURCE_URL,'pdf_page':185,'printed_page':153,'chapter':27,'slokas':'8-12',
   'verified_against_page_image':True},'selected_geometry_profile':None,'whole_strength':None,
  'notice':'Special interior formulas remain distinct from general interpolation and Santhanam simplified additions. At exact sign boundaries both adjacent formula endpoints are shown; differing values stay unknown. Saturn and Jupiter have unequal endpoints at270degrees in this printed reading. No smoothing, editorial repair, chart provenance certification, benefic classification or Drigbala total is inferred.'}
