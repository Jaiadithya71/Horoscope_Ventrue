import unittest
import datetime as dt
from engine.solar_meridian_clock import solar_meridian_clock as c,PROFILE

class MeridianClockTests(unittest.TestCase):
 def test_modern_meridians_supply_distinct_clock_candidates(self):
  t=dt.datetime(2000,1,1,9,tzinfo=dt.timezone.utc)
  x=c(t,13.08,80.27,meridian_profile=PROFILE)
  self.assertEqual(x['status'],'explicit_meridian_candidates')
  self.assertEqual(len(x['candidates']),2);self.assertIsNone(x['selected_clock_profile'])
  a,b=x['candidates']
  self.assertNotEqual(a['hours_after_model_solar_midnight'],b['hours_after_model_solar_midnight'])
  for p in x['candidates']:
   self.assertEqual(p['components']['Mercury']['rupa'],1)
   self.assertAlmostEqual(p['components']['Sun']['rupa']+p['components']['Moon']['rupa'],1)
  self.assertIsNone(x['total_strength'])
  edge=dt.datetime.fromisoformat(x['interval_start_utc'])
  self.assertEqual(c(edge,13.08,80.27,meridian_profile=PROFILE)['status'],'boundary_unresolved')
 def test_no_default_or_civil_time_substitution(self):
  t=dt.datetime(2000,1,1,9,tzinfo=dt.timezone.utc)
  for profile in ('','civil_midnight'):
   with self.assertRaises(ValueError):c(t,13.08,80.27,meridian_profile=profile)
  with self.assertRaises(ValueError):c(t.replace(tzinfo=None),13.08,80.27,meridian_profile=PROFILE)
  y=c(t.astimezone(dt.timezone(dt.timedelta(hours=5,minutes=30))),13.08,80.27,meridian_profile=PROFILE)
  self.assertEqual(y['candidates'],c(t,13.08,80.27,meridian_profile=PROFILE)['candidates'])
