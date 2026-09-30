"""Sripati III.14 supplied historical epoch-count arithmetic, no date inference."""
from .continuous_strength import source
from .temporal_lords import historical_lords


def historical_day_count(elapsed_creation_solar_years,elapsed_solar_months,elapsed_lunar_days,*,epoch_profile):
 if not epoch_profile:raise ValueError('Named externally grounded epoch profile required')
 for v in (elapsed_creation_solar_years,elapsed_solar_months,elapsed_lunar_days):
  if type(v) is not int or v<0:raise ValueError('Nonnegative completed historical counts required')
 if not 0<=elapsed_solar_months<12 or not 0<=elapsed_lunar_days<30:
  raise ValueError('Residual solar months0..11 and lunar days0..29 required')
 # Source example derives both additive months and subtractive days from
 # completed creation years. Do not silently recast as exact lunar-day ratio.
 years=elapsed_creation_solar_years
 additive=years*1593336//4320000
 solar_months=years*12+elapsed_solar_months
 lunar_months=solar_months+additive
 lunar_days=lunar_months*30+elapsed_lunar_days
 subtractive=years*25082252//4320000
 terrestrial=lunar_days-subtractive
 if terrestrial<0:raise ValueError('Supplied epoch counts give negative terrestrial day count')
 return {'epoch_profile':epoch_profile,'supplied_completed_creation_solar_years':years,
    'supplied_residual_solar_months':elapsed_solar_months,'supplied_residual_lunar_days':elapsed_lunar_days,
    'additive_months_floor':additive,'lunar_months':lunar_months,'lunar_days':lunar_days,
    'subtractive_days_floor':subtractive,'terrestrial_days':terrestrial,
    'lord_evidence':historical_lords(terrestrial),'source':source('14 commentary epoch example',62,48),
    'continued_source':source('14 commentary epoch example',63,49),
    'modern_date_conversion':None,'total_temporal_strength':None,
    'notice':'Exact supplied-count reproduction of this commentary recipe only. Residual month/tithi inputs and creation/Kali epoch are not inferred from modern Gregorian dates. Floor omissions follow printed example, not a general independent panchanga accuracy claim. No civil year/month shortcut or automatic weekday convention.'}
