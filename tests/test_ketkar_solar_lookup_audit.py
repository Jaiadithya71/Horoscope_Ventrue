import unittest
from engine.ketkar_solar_lookup_audit import solar_lookup_audit

class SolarLookupTests(unittest.TestCase):
 def test_actual_adjacent_rows_reproduce_example(self):
  r=solar_lookup_audit()
  self.assertEqual(r['computed_true_centre_degrees'],'93.1724480')
  self.assertEqual(r['computed_radius_residual'],'0.67910')
  self.assertTrue(r['true_centre_matches_at_printed_precision'])
  self.assertTrue(r['radius_matches_at_printed_precision'])
  self.assertFalse(r['source_selects_unique_interpolation_and_rounding'])
  self.assertIsNone(r['selected_solar_longitude'])
