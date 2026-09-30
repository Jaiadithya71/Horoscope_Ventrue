import unittest
import datetime as dt
from engine.natal import dasha_at_solar_offset
from engine.solar_dates import dated_hierarchy,Fixed36525Calendar

class PeriodPrecisionTests(unittest.TestCase):
 def test_rounding_display_cannot_feed_calendar_mapping(self):
  birth=dt.datetime(2000,1,1,tzinfo=dt.timezone.utc)
  moon=1.23456789
  x=dasha_at_solar_offset(moon,0)
  e=x['hierarchy'][0]['end_solar_years_after_birth']
  self.assertNotEqual(e,x['hierarchy'][0]['offset_display_9dp']['end'])
  c=Fixed36525Calendar(birth)
  y=dated_hierarchy(birth,moon,birth,calendar_profile='fixed_365_25_day_software_comparison')
  self.assertEqual(y['hierarchy'][0]['end_utc_estimate'],c.at_offset(e).isoformat())
  self.assertNotEqual(y['hierarchy'][0]['end_utc_estimate'],c.at_offset(round(e,9)).isoformat())
 def test_full_precision_nested_boundary_enters_next_child(self):
  x=dasha_at_solar_offset(1.23456789,0)
  e=x['hierarchy'][2]['end_solar_years_after_birth']
  before=dasha_at_solar_offset(1.23456789,e-1e-11)
  after=dasha_at_solar_offset(1.23456789,e)
  self.assertEqual(before['hierarchy'][2]['lord'],x['hierarchy'][2]['lord'])
  self.assertNotEqual(after['hierarchy'][2]['lord'],x['hierarchy'][2]['lord'])
