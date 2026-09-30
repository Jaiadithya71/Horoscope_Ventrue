"""Jha chapter4 supplied time-fraction Moon, not modern true ephemeris."""
from fractions import Fraction as F
from .bphs_jha_general_aspect import SOURCE_URL


def jha_traversal_moon(elapsed_stars,elapsed_pal,total_pal,*,traversal_profile):
 if type(elapsed_stars) is not int or not 0<=elapsed_stars<27:raise ValueError('Elapsed complete stars0..26 required')
 if not isinstance(traversal_profile,str) or not traversal_profile.strip():raise ValueError('Named supplied traversal provenance required')
 if isinstance(elapsed_pal,bool) or isinstance(total_pal,bool):raise ValueError('Finite traversal amounts required')
 try:elapsed=F(str(elapsed_pal));total=F(str(total_pal))
 except (ValueError,ZeroDivisionError) as exc:raise ValueError('Finite traversal amounts required') from exc
 if total<=0 or not 0<=elapsed<total:raise ValueError('Positive total and0<=elapsed<total required')
 fraction=elapsed/total;longitude=(elapsed_stars+fraction)*F(40,3)
 return {'profile':'jha_sudha4_supplied_timefraction_moon','traversal_profile':traversal_profile,
  'elapsed_stars':elapsed_stars,'elapsed_fraction_rational':str(fraction),
  'moon_longitude_degrees_rational':str(longitude),
  'longitude_sector_fraction_rational':str(longitude/F(40,3)-elapsed_stars),
  'source':{'url':SOURCE_URL,'pdf_page':53,'printed_page':21,'chapter':4,
   'section':'Moon interpolation commentary formula1','verified_against_page_image':True},
  'modern_true_moon_identity_verified':False,'selected_ephemeris_profile':None,
  'notice':'Linear timefraction-to-longitude construction on supplied star traversal. Timefraction and longitudefraction agree by construction here, not for arbitrary true ephemeris. No sector entry/exit, calendar instant, modern ayanamsa or historical panchanga is generated.'}


def jha_traversal_moon_audit():
 x=jha_traversal_moon(16,2755,3434,traversal_profile='printed Anuradha45;55/57;14 supplied fixture')
 exact=F(x['moon_longitude_degrees_rational']);printed=F(224)+F(1,60)+F(49,3600)
 return {'worked_candidate':x,'printed_moon_degrees_rational':str(printed),
  'exact_minus_printed_arcseconds_rational':str((exact-printed)*3600),
  'printed_input_elapsed_pal':2755,'printed_input_total_pal':3434,
  'selected_rounding_policy':None,'exact_civil_endpoint':None,
  'notice':'Printed integer-second Moon is independently audited, not an exact astronomical oracle. The source itself warns direct daily true-speed interpolation is coarse forMoon; its timefraction construction is a distinct input profile.'}
