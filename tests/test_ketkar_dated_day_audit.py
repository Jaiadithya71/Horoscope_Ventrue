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
