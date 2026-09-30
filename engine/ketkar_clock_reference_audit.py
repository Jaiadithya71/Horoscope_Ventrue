"""Separate historical mean clock from site-specific visible sunrise."""
from .ketkar_dated_day_audit import dated_day_audit


def clock_reference_audit():
 return {'source':{'url':dated_day_audit()['source']['url'],
  'pdf_pages':[96,97,143,168,179],'printed_pages':[29,30,76,101,112],
  'verified_against_page_image':True,'rules':'I29-33; III4 commentary; Nyasa3 row18'},
  'avanta_clock':'Ujjain mean time; other local mean clocks use rekhantara',
  'ahargana_reference':'elapsed days relative to supplied annual Aries ingress reference',
  'printed_pratah_step':'subtract fractional weekday from tithi-end elapsed days',
  'mean_time_and_sunrise_distinguished':True,
  'site_sunrise_requires':['site meridian difference','latitude/day-half correction',
    'equation-of-time correction','five pala sunrise correction specified by source'],
  'arbitrary_instant_addition':'Nyasa3 row18: mean elapsed ghati divided by60; example20ghati15pala becomes.3375days',
  'utc_dawn_timestamp':None,'actual_visible_sunrise_timestamp':None,
  'modern_timezone_selected':None,
  'notice':'III day arithmetic uses a mean-clock reference; I29-33 separately converts mean time to sunrise-relative and local mean clocks. The word dawn alone is not permission to use a modern sunrise calculator. Exact Gregorian clock origin/UTC alignment for this dated fixture still unverified. Do not silently identify mean reference with visible sunrise or modern IST.'}
