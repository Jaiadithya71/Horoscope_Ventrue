import unittest
from fractions import Fraction as F
from engine.jha_traversal_moon import jha_traversal_moon as moon,jha_traversal_moon_audit as audit

class JhaMoonTests(unittest.TestCase):
 def test_profile_equivalence_is_by_construction(self):
  x=moon(16,2755,3434,traversal_profile='fixture');self.assertEqual(F(x['elapsed_fraction_rational']),F(x['longitude_sector_fraction_rational']))
  self.assertFalse(x['modern_true_moon_identity_verified']);self.assertIsNone(x['selected_ephemeris_profile'])
 def test_worked_second_rounding_audit(self):
  x=audit();self.assertLess(abs(F(x['exact_minus_printed_arcseconds_rational'])),1);self.assertIsNone(x['selected_rounding_policy'])
 def test_invalid_traversal_and_boundaries(self):
  for star,a,b in [(True,0,60),(27,0,60),(0,True,60),(0,-1,60),(0,60,60),(0,0,0),(0,'NaN',60)]:
   with self.assertRaises(ValueError):moon(star,a,b,traversal_profile='fixture')
  self.assertEqual(moon(0,0,60,traversal_profile='fixture')['moon_longitude_degrees_rational'],'0')
