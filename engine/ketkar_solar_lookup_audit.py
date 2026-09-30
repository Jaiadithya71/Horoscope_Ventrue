"""Explicit local table11 interpolation candidate, not a universal ephemeris."""
from decimal import Decimal, ROUND_HALF_UP
from .ketkar_dated_day_audit import dated_day_audit


def solar_lookup_audit():
 days=Decimal('92.597');fraction=(days-Decimal(92))/Decimal(2)
 centre=Decimal('92.585')+fraction*(Decimal('94.553')-Decimal('92.585'))
 radius=Decimal('.5')+fraction*(Decimal('1.1')-Decimal('.5'))
 rounded=centre.quantize(Decimal('.001'),rounding=ROUND_HALF_UP)
 radius_rounded=radius.quantize(Decimal('.1'),rounding=ROUND_HALF_UP)
 return {'source':{'url':dated_day_audit()['source']['url'],'pdf_pages':[173,201],
  'printed_pages':[106,134],'table':'11 Sun rows92 and94','verified_against_page_image':True},
  'input_centre_days':str(days),'lower_row':{'days':'92','true_centre_degrees':'92.585','radius_residual':'.5'},
  'upper_row':{'days':'94','true_centre_degrees':'94.553','radius_residual':'1.1'},
  'candidate_interpolation':'linear_between_printed_adjacent_rows',
  'fraction_between_rows':str(fraction),'computed_true_centre_degrees':str(centre),
  'rounded_true_centre_degrees':str(rounded),'printed_example_true_centre_degrees':'93.172',
  'true_centre_matches_at_printed_precision':rounded==Decimal('93.172'),
  'computed_radius_residual':str(radius),'rounded_radius_residual':str(radius_rounded),
  'printed_example_radius_residual':'.7','radius_matches_at_printed_precision':radius_rounded==Decimal('.7'),
  'rounding_candidate':'decimal_half_up; .001 degrees and .1 radius units',
  'source_selects_unique_interpolation_and_rounding':False,
  'selected_solar_longitude':None,'total_strength':None,
  'notice':'Actual two-row lookup candidate reproduces printed centre and radius at shown precision. This does not uniquely prove rounding/interpolation for the complete book tables, reconstruct apsis or validate external ephemeris. No print-fit offset applied.'}
