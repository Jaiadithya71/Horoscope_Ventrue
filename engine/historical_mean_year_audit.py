"""Sripati mean-Sun dated example, not Vimshottari or modern return truth."""
import datetime as dt
from fractions import Fraction

SOURCE='https://archive.org/details/dli.ernet.203510'
MEAN_YEAR=Fraction(1577917828,4320000)


def historical_mean_year_audit():
 # Local clock preserved naive: book says5h20m east of Greenwich, not modern IST.
 birth=dt.datetime(1853,4,30,5,35)
 printed=dt.datetime(1903,1,6,21,15)
 offset=Fraction('49.6847')
 earlier_days=offset*MEAN_YEAR
 summary_year=Fraction('365.256374')
 approx_days=offset*summary_year
 own_summary=dt.datetime(1902,4,30,5,35)+dt.timedelta(days=float(Fraction('251.6531')))
 rows=[]
 for name,days in [('VII20_yuga_ratio_mean_year',earlier_days),
                   ('summary_approximate_mean_year',approx_days),
                   ('fixed365_25_comparison_only',offset*Fraction('365.25'))]:
  result=birth+dt.timedelta(days=float(days))
  rows.append({'profile':name,'elapsed_days_fraction':str(days),'local_clock_endpoint':result.isoformat(),
               'computed_minus_printed_seconds':(result-printed).total_seconds()})
 return {'source_url':SOURCE,'verified_against_page_images':True,
    'primary_rule_pdf_pages':[175,176,177,178],'summary_pdf_pages':[207,208],
    'chapter':'VII','sloka':'18-20 and commentary; later summary',
    'dasha_scope':'Sripati longevity/strength-derived system, not presumed Vimshottari',
    'rule_says_mean_sun':True,'solar_year_yuga_ratio':str(MEAN_YEAR),'solar_year_yuga_ratio_days':float(MEAN_YEAR),
    'summary_approximate_year_days':float(summary_year),
    'birth_local_clock':birth.isoformat(),'elapsed_mean_solar_years':str(offset),
    'printed_local_clock_endpoint':printed.isoformat(),
    'summary_reported_day_addition_endpoint':own_summary.isoformat(),
    'summary_reported_day_addition_minus_printed_seconds':(own_summary-printed).total_seconds(),
    'calendar_comparisons':rows,'local_clock_offset_notice':'PDF208 states5hours20minutes east of Greenwich; no modern timezone imposed.',
    'selected_calendar':None,'exact_endpoint_verified':False,
    'notice':'Earlier exact yuga ratio and summary approximate mean-year constants differ by about2h51m at49.6847years. Summary rounded arithmetic reproduces printed clock within a minute, not independent astronomical accuracy. Mean Sun is explicit, not modern apparent true Sun, and this other dasha system does not resolve PhaladeepikaXIX.4 or Balaji\'s calendar settings. No print-fit constant or personal forecast.'}


if __name__=='__main__':
 import json
 print(json.dumps(historical_mean_year_audit(),indent=2))
