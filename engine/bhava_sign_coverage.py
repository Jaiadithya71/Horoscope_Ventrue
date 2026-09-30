"""Geometric sign/lord coverage of supplied Sandhi intervals, not strength weights."""
from .continuous_strength import valid_longitude
from .forecast import SIGNS
from .synthesis import LORDS,LORD_SOURCE
from .bhava_geometry import SOURCE


def bhava_sign_coverage(geometry):
 boundaries=geometry.get('boundary_after_house',{})
 if set(boundaries)!=set(range(1,13)):raise ValueError('All12boundary longitudes required')
 for v in boundaries.values():valid_longitude(v)
 spans=[(boundaries[h]-boundaries[h-1 if h>1 else 12])%360 for h in range(1,13)]
 if any(not 0<s<180 for s in spans) or abs(sum(spans)-360)>1e-8:
  raise ValueError('Ordered nondegenerate boundary cycle required')
 rows=[]
 for h,span in enumerate(spans,1):
  start=boundaries[h-1 if h>1 else 12];end=start+span
  parts=[];left=start
  while left<end:
   idx=int(left//30);right=min(end,(idx+1)*30)
   degrees=right-left
   if degrees<=0:raise ArithmeticError('Sign interval did not advance')
   parts.append({'sign':SIGNS[idx%12],'lord':LORDS[idx%12],
      'start_longitude':left%360,'end_longitude':right%360,'arc_degrees':degrees,
      'geometric_fraction_of_house':degrees/span})
   left=right
  rows.append({'house':h,'start_sandhi_longitude':start,'end_sandhi_longitude':end%360,
    'house_arc_degrees':span,'sign_segments':parts,'multiple_signs':len(parts)>1,
    'selected_lord_strength_weighting':None,'total_bhava_strength':None})
 return {'houses':rows,'geometry_source':SOURCE,'sign_lord_source':LORD_SOURCE,
    'cross_sign_strength_example_source':{'slug':'sripatipaddhati-sastri-archive-203510','chapter':'III','sloka':'23 commentary','pdf_page':78,'printed_page':64,'url':'https://archive.org/details/dli.ernet.203510','verified_against_page_image':True},
    'notice':'Geometric fractions describe coverage only, not source-selected strength weights. Source30degree example does not by itself resolve unequal-house weighting denominator or certify rounded lord totals. Half-open geometric intervals are used for coverage; exact planet Sandhi membership stays separately unresolved. No single centre-sign lord, selected total, rank or personal effect inferred.'}
