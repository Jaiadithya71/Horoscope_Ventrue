import unittest
from engine.ketkar_dated_day_audit import dated_day_audit

class DatedDayTests(unittest.TestCase):
 def test_corrected_example_and_negative_day_chain(self):
  r=dated_day_audit()
  self.assertEqual(r['printed_example']['saka_year'],1850)
  self.assertEqual(r['calculated_gregorian_weekday'],'Thursday')
  self.assertTrue(r['tithi_end_arithmetic_matches']);self.assertTrue(r['ujjain_arithmetic_matches']);self.assertTrue(r['kashi_arithmetic_matches'])
  self.assertEqual(r['computed_ujjain_dawn_days'],'-7.977')
  self.assertIsNone(r['utc_dawn_timestamp']);self.assertIsNone(r['mean_planet_longitudes'])

class SolarCentreTests(unittest.TestCase):
 def test_printed_bridge_not_a_selected_profile(self):
  from engine.ketkar_dated_day_audit import solar_centre_day_audit
  r=solar_centre_day_audit()
  self.assertTrue(r['centre_day_chain_matches'])
  self.assertEqual(r['computed_solar_longitude_degrees'],'352.167')
  self.assertIsNone(r['selected_solar_longitude'])
  self.assertFalse(r['table11_true_centre_lookup_reconstructed'])
