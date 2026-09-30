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

class LuminaryMultiplierChainTests(unittest.TestCase):
 def test_one_upstream_double_no_second_identity_double(self):
  from engine.luminary_motion_identity import supplied_bphs_doubled_component_chain
  for p,v,w in [('Sun',.810,1.620),('Moon',.518,1.036)]:
   x=supplied_bphs_doubled_component_chain(p,v,base_component_profile='explicit supplied base hypothesis')
   self.assertAlmostEqual(x['doubled_upstream_component_rupa'],w)
   self.assertEqual(x['motion_identity']['motion_rupa'],x['doubled_upstream_component_rupa'])
   self.assertIsNone(x['engine_computed_base_component']);self.assertIsNone(x['total_strength'])
 def test_doubled_component_cannot_reenter_as_base(self):
  from engine.luminary_motion_identity import supplied_bphs_doubled_component_chain
  with self.assertRaises(ValueError):supplied_bphs_doubled_component_chain('Sun',1.62,base_component_profile='not undoubled')
