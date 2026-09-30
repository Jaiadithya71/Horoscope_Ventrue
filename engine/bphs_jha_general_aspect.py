"""Sudha commentary general directed aspect candidate, distinct edition profile."""
from fractions import Fraction as F

SOURCE_URL='https://archive.org/download/bmmv_brihat-parashar-hora-shastra-of-parashar-muni-with-sudha-commentary-by-pt.-dev-c/Brihat%20Parashar%20Hora%20Shastra%20of%20Parashar%20Muni%20with%20Sudha%20Commentary%20by%20Pt.%20Dev%20Chandra%20Jha%20Kashi%20Sanskrit%20Series%20No.%20220%20-%20Chaukhamba.pdf'


def number(x):
 if isinstance(x,bool):raise ValueError('Finite degree longitude0<=x<360 required')
 try:q=F(str(x))
 except (ValueError,ZeroDivisionError) as exc:raise ValueError('Finite numeric longitude required') from exc
 if not 0<=q<360:raise ValueError('Longitude0<=x<360 required')
 return q


def bphs_jha_general_aspect(aspector_longitude,aspected_longitude,*,coordinate_profile):
 if not isinstance(coordinate_profile,str) or not coordinate_profile.strip():raise ValueError('Named common coordinate provenance required')
 delta=(number(aspected_longitude)-number(aspector_longitude))%360
 # Piecewise boundaries use the common adjoining value, not a guessed jump.
 if delta<=30 or delta>=300:amount=F(0)
 elif delta<=60:amount=(delta-30)/2
 elif delta<=90:amount=delta-60+15
 elif delta<=120:amount=(120-delta)/2+30
 elif delta<=150:amount=150-delta
 elif delta<=180:amount=2*(delta-150)
 else:amount=(300-delta)/2
 return {'profile':'bphs_jha_sudha27_general_directed_candidate',
  'coordinate_profile':coordinate_profile,'directed_difference_degrees_rational':str(delta),
  'unsigned_aspect_virupa_rational':str(amount),
  'source':{'url':SOURCE_URL,'pdf_pages':[183,184,185],'printed_pages':[151,152,153],
   'chapter':27,'slokas':'5-7.5','verified_against_page_image':True},
  'special_planet_rules_applied':False,'selected_geometry_profile':None,
  'notice':'General directed candidate only. Does not replace Saturn/Mars/Jupiter special rules, repair Santhanam text, certify caller coordinates or calculate Drigbala/whole strength. Adjoining general formulas agree exactly at30/60/90/120/150/180/300degrees.'}


def dms(sign,degree,minute,second):
 return F(sign*30+degree)+F(minute,60)+F(str(second))/3600


def jha_printed_aspect_audit():
 sun=dms(2,5,25,15)
 fixtures=[('Sun_to_second_house',sun,dms(7,20,30,49),F(30)+F(11,60)+F(8,3600)),
  ('Sun_to_third_house',sun,dms(8,21,32,0),F(51)+F(56,60)+F(37,3600))]
 rows=[]
 for label,a,b,printed in fixtures:
  x=bphs_jha_general_aspect(a,b,coordinate_profile='Sudha printed hypothetical sexagesimal example, not natal ephemeris')
  exact=F(x['unsigned_aspect_virupa_rational'])
  rows.append({'label':label,'aspector_longitude_degrees_rational':str(a),
   'aspected_longitude_degrees_rational':str(b),'printed_virupa_rational':str(printed),
   'exact_virupa_rational':str(exact),'exact_minus_printed_rational':str(exact-printed),
   'exact_minus_printed_virupa_seconds_rational':str((exact-printed)*3600)})
 # Printed Saturn example says multiply20;5;15 by2, then prints20;10;30.
 operand=F(20)+F(5,60)+F(15,3600);printed=F(20)+F(10,60)+F(30,3600)
 return {'general_worked_rows':rows,'saturn_printed_multiplication_check':{
  'operand_rational':str(operand),'multiplier':2,'exact_rational':str(operand*2),
  'printed_rational':str(printed),'exact_minus_printed_rational':str(operand*2-printed),
  'source_pdf_page':185,'source_printed_page':153},
  'source_url':SOURCE_URL,'verified_against_page_image':True,
  'selected_corrected_table':None,'special_geometry_enabled':False,
  'notice':'Audits page-readable operands, not their hypothetical horoscope truth. Third-house half-second difference is retained without a universal truncation policy. Saturn printed product misses20virupa; no corrected table is selected.'}
