import unittest
from engine.ketkar_auxiliary_audit import auxiliary_audit,combine_auxiliaries

class AuxiliaryTests(unittest.TestCase):
 def test_printed_vectors(self):
  r=auxiliary_audit()
  self.assertTrue(r['start_matches']);self.assertTrue(r['end_matches'])
  self.assertEqual(r['computed_1851_auxiliaries'][0],59)
  self.assertIsNone(r['attraction_days']);self.assertIsNone(r['mean_planet_longitudes'])
 def test_no_carry_between_columns(self):
  self.assertEqual(combine_auxiliaries([999,0,0,0,0,0],[1,0,0,0,0,0]),[0]*6)
 def test_invalid_inputs(self):
  for a,b in [([0]*5,[0]*6),([True]*6,[0]*6),([1000]*6,[0]*6),([0]*6,[-1]*6),('bad',[0]*6)]:
   with self.assertRaises(ValueError):combine_auxiliaries(a,b)
