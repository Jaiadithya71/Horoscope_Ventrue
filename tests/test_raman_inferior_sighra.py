import unittest
from engine.raman_inferior_sighra import raman_inferior_sighra as lookup

class InferiorSighraTests(unittest.TestCase):
 def test_unreadable_cell_and_raw_nonuniform_rows(self):
  x=lookup('Mercury',10000,18,epoch_clock_profile='supplied')
  self.assertTrue(x['unreadable_cells']);self.assertTrue(all(r['sighrochcha_degrees'] is None for r in x['candidates']))
  self.assertEqual(lookup('Mercury',70,18,epoch_clock_profile='supplied')['printed_pieces'][0]['printed_entry'],'266.46')
  self.assertEqual(lookup('Venus',70,18,epoch_clock_profile='supplied')['printed_pieces'][0]['printed_entry'],'116.15')
 def test_coefficients_not_selected_or_fitted(self):
  x=lookup('Mercury','6862.578',18,epoch_clock_profile='supplied')
  self.assertEqual(x['fractional_motion_degrees'],'2.36402')
  self.assertNotEqual(x['candidates'][0]['sighrochcha_degrees'],x['candidates'][1]['sighrochcha_degrees'])
  self.assertIsNone(x['selected_sighrochcha']);self.assertFalse(x['historical_ephemeris_verified'])
 def test_invalid_inputs(self):
  for v in (True,'NaN',100000):
   with self.assertRaises(ValueError):lookup('Mercury',v,18,epoch_clock_profile='supplied')
  with self.assertRaises(ValueError):lookup('Venus',2,18.5,epoch_clock_profile='supplied')
