import unittest
from engine.luminary_motion_identity import supplied_luminary_motion_identity as identity

class LuminaryIdentityTests(unittest.TestCase):
 def test_identity_not_an_extra_multiplier(self):
  for p,v in [('Sun',.810),('Sun',1.620),('Moon',.518),('Moon',1.036)]:
   x=identity(p,v,component_profile='explicit supplied hypothesis')
   self.assertEqual(x['motion_rupa'],v);self.assertIsNone(x['selected_sripati_motion']);self.assertIsNone(x['total_strength'])
 def test_missing_profile_and_invalid_values_rejected(self):
  for value in [True,-1,float('nan')]:
   with self.assertRaises(ValueError):identity('Sun',value,component_profile='supplied')
  with self.assertRaises(ValueError):identity('Mars',1,component_profile='supplied')
  with self.assertRaises(ValueError):identity('Sun',1,component_profile='')
