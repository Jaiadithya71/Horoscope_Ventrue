"""Independent exact arithmetic on Raman's temporal worked examples."""
from decimal import Decimal as D
from fractions import Fraction as F
from .raman_motion_source_audit import SOURCE_URL

PLANETS=('Sun','Moon','Mars','Mercury','Jupiter','Venus','Saturn')
# Rows: natonnata, phase, third, year, month, weekday, hora, ayana.
# None is a printed blank, never a verified absence.
ROWS={
 'Sun':['48.320','16.540',None,None,None,None,None,'38.120'],
 'Moon':['11.680','86.920',None,None,None,None,'60.000','43.440'],
 'Mars':['11.680','16.540',None,None,None,None,None,'1.840'],
 'Mercury':['60.000','16.540',None,None,'30.000','45.000',None,'41.250'],
 'Jupiter':['48.320','43.460','60.000',None,None,None,None,'59.400'],
 'Venus':['48.320','43.460',None,None,None,None,None,'23.750'],
 'Saturn':['11.680','16.540','60.000','15.000',None,None,None,'13.750']}
TOTALS=['102.980','202.040','30.060','192.790','211.180','115.530','116.970']


def raman_temporal_audit():
 rows=[]
 # Printed Example18 minute-rounded inputs, not opening exact seconds.
 folded_phase=F(130*60+23,180)
 for p,total in zip(PLANETS,TOTALS):
  v=ROWS[p];known=sum(D(x) for x in v if x is not None)
  benefic=p in ('Moon','Jupiter','Venus') # Explicit worked-table classification only.
  phase=(folded_phase if benefic else 60-folded_phase)*(2 if p=='Moon' else 1)
  nat=F(60) if p=='Mercury' else F(145,3) if p in ('Sun','Jupiter','Venus') else F(35,3)
  rows.append({'planet':p,'printed_temporal_rows_virupa':v,'printed_kala_total_virupa':total,
   'unverified_blank_row_indices':[i for i,x in enumerate(v) if x is None],
   'sum_of_numeric_rows_virupa':str(known),'numeric_sum_minus_printed_total_virupa':str(known-D(total)),
   'complete_temporal_total':None,'blank_as_zero_sum_profile':'diagnostic_only_not_selected',
   'exact_method_b_natonnata_virupa_rational':str(nat),
   'method_b_minus_final_natonnata_rational':str(nat-F(v[0])),
   'exact_worked_minute_input_phase_virupa_rational':str(phase),
   'phase_minus_final_phase_virupa_rational':str(phase-F(v[1])),
   'worked_phase_classification':'Subha' if benefic else 'Papa'})
 return {'rows':rows,'method_a_clock_candidates':{
  'printed_natha_sexagesimal_ghatika':[5,50],'printed_natha_decimal':'5.84',
  'exact_sexagesimal_night_strength_virupa_rational':str(F(5*60+50,30)),
  'printed_decimal_night_strength_virupa':'11.68',
  'printed_method_a_mars_virupa':'21.68','method_a_formula_and_method_b_mars_printed_virupa':'11.68'},
  'worked_phase_inputs':{'sun_degrees_minutes':[180,54],'moon_degrees_minutes':[311,17],
   'folded_elongation_degrees_rational':'7823/60','moon_multiplier':2,
   'notice':'Worked rounded-minute inputs and supplied explicit Papa/Subha classification, not complete natal classification or true-coordinate reconstruction.'},
  'source':{'url':SOURCE_URL,'pdf_pages':[41,42,43,44,67,68],'printed_pages':[36,37,38,39,62,63],
   'articles':[50,51,53,55,78],'verified_against_page_image':True},
  'selected_rounding_policy':None,'selected_temporal_profile':None,
  'notice':'All seven final numeric row sums match totals if blanks contribute nothing, but this diagnostic does not prove absence. Earlier/later Natonnata discrepancies and exact clock/phase arithmetic retained. Moon doubling and worked Mercury Papa are Raman-specific; not imported into Sripati. Ayana is within this Kala table. No full temporal score or coherent chart benchmark selected.'}
