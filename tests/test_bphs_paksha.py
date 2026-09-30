import unittest
from engine.bphs_paksha import bphs_paksha_candidates as gate
from engine.continuous_strength import pakshabala_candidates

class BphsPakshaTests(unittest.TestCase):
 def test_dark_moon_complement_then_double_not_redouble(self):
  x=gate('Moon',0,240);r=x['candidates'][0]
  self.assertFalse(r['benefic_classification_candidate'])
  self.assertAlmostEqual(r['paksha_rupa'],2/3)
  self.assertEqual(r['moon_motion_identity']['motion_rupa'],r['paksha_rupa'])
  self.assertNotEqual(r['undoubled_paksha_rupa'],pakshabala_candidates('Moon',0,240)['candidates'][0]['rupa'])
 def test_mercury_unknown_association_not_fixed_benefic(self):
  x=gate('Mercury',0,60)
  self.assertIsNone(x['selected_paksha_rupa']);self.assertEqual(len(x['candidates']),2)
  self.assertAlmostEqual(gate('Mercury',0,60,mercury_with_malefic=True,association_profile='supplied')['selected_paksha_rupa'],2/3)
 def test_exact_lunar_boundaries_unselected(self):
  for lon in (0,180):
   x=gate('Moon',0,lon);self.assertEqual(len(x['candidates']),2);self.assertIsNone(x['selected_paksha_rupa'])
 def test_invalid_flags_and_longitudes_rejected(self):
  for x in (True,360,float('nan')):
   with self.assertRaises(ValueError):gate('Moon',0,x)
  with self.assertRaises(ValueError):gate('Mercury',0,60,mercury_with_malefic=True)
  with self.assertRaises(ValueError):gate('Mercury',0,60,mercury_with_malefic=1,association_profile='supplied')
