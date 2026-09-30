"""Supplied complete lord totals under explicit cross-sign weighting hypotheses."""
import math
from fractions import Fraction
from .continuous_strength import source


def bhava_lord_candidates(coverage,totals,*,total_profile,complete):
 if not total_profile:raise ValueError('Named total profile required')
 if type(complete) is not bool:raise ValueError('Explicit completeness bool required')
 for planet,total in totals.items():
  if type(total) not in (int,float) or not math.isfinite(total) or total<0:raise ValueError('Finite nonnegative supplied total required')
 rows=[]
 for house in coverage['houses']:
  parts=house['sign_segments'];missing=sorted({p['lord'] for p in parts if p['lord'] not in totals})
  candidates=[]
  for profile,denom in [('fixed_30_degree_example_extension',30),('normalized_actual_house_arc',house['house_arc_degrees'])]:
   terms=[{'sign':p['sign'],'lord':p['lord'],'arc_degrees':p['arc_degrees'],
     'supplied_total_rupa':totals.get(p['lord']),'weight':p['arc_degrees']/denom,
     'contribution_rupa':None if not complete or p['lord'] not in totals else p['arc_degrees']/denom*totals[p['lord']]} for p in parts]
   candidates.append({'profile':profile,'denominator_degrees':denom,'terms':terms,
      'weighted_lord_total_rupa':None if not complete or missing else sum(t['contribution_rupa'] for t in terms),
      'scope':'Explicit hypothesis extension of30degree worked example, not a selected unequal-house mandate'})
  rows.append({'house':house['house'],'missing_lords':missing,'candidates':candidates,
     'selected_weighted_lord_total':None,'total_bhava_strength':None})
 return {'houses':rows,'supplied_total_profile':total_profile,'supplied_totals_declared_complete':complete,
   'source':source('23 cross-sign commentary example',78,64),'selected_profile':None,
   'notice':'Caller completeness is a declared input, not verified engine Shadbala. Incomplete totals produce no products. Fixed30degree versus normalized actual house arc remain hypotheses; neither printed erroneous example nor centre sign chooses a winner. Aspect/direction/occupant terms and personal outcomes absent.'}


def audit_printed_cross_sign_example():
 j=Fraction(1)+Fraction(36,60)+Fraction(30,3600)
 m=Fraction(28)+Fraction(23,60)+Fraction(30,3600)
 a=j/30*Fraction('8.613');b=m/30*Fraction('7.731')
 return {'source':source('23 cross-sign commentary example',78,64),
    'supplied_arcs_degrees':[str(j),str(m)],'supplied_lord_totals':['8.613','7.731'],
    'exact_contributions_rupa':[float(a),float(b)],'exact_sum_rupa':float(a+b),
    'printed_contributions_rupa':['.465','7.316'],'printed_sum_rupa':'7.781',
    'printed_contribution_sum_matches':Fraction('.465')+Fraction('7.316')==Fraction('7.781'),
    'jupiter_exact_minus_printed_rupa':float(a-Fraction('.465')),
    'exact_sum_minus_printed_rupa':float(a+b-Fraction('7.781')),
    'selected_weighting_profile':None,
    'notice':'Printed final sum adds printed terms correctly but Jupiter term disagrees with its displayed arc/total. Rounded supplied lord totals already have other source inconsistencies. No correction, print fit, reconstructed geometry or unequal-house denominator selected.'}
