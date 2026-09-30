import unittest
from engine.raman_mean_sun import raman_mean_sun_from_elapsed_days as lookup,raman_mean_sun_example_audit

class RamanMeanSunTests(unittest.TestCase):
 def test_independent_worked_fixture_and_discrepancy(self):
  x=raman_mean_sun_example_audit();self.assertTrue(x['repeated_constant_candidate_matches_example'])
  self.assertFalse(x['1918_printed_fraction_matches_fourteen_hours'])
  self.assertEqual(x['motion_from_printed_fraction'],'0.5726336')
  self.assertIsNone(x['selected_epoch_conversion'])
 def test_raw_typo_and_constants_not_fixed(self):
  x=lookup(4,epoch_clock_profile='explicit supplied fixture')
  self.assertEqual(x['table_pieces'][0]['value_degrees'],'3.9524')
  self.assertEqual(x['four_times_one_day_diagnostic'],'3.9424')
  self.assertEqual(len(x['candidates']),2);self.assertIsNone(x['selected_mean_sun'])
 def test_negative_and_domain_limits(self):
  x=lookup(-1,epoch_clock_profile='explicit supplied fixture')
  self.assertEqual(x['candidates'][0]['mean_sun_degrees'],'256.4712')
  for v in (True,'NaN',100000):
   with self.assertRaises(ValueError):lookup(v,epoch_clock_profile='supplied')
