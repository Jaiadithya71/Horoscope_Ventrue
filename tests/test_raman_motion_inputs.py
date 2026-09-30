import unittest
from engine.raman_motion_inputs import raman_motion_inputs as report

class RamanInputsTests(unittest.TestCase):
 def test_explicit_assignments_not_heliocentric_fill(self):
  x=report(181.23,{'Mars':266.34},{'Mars':229.50,'Mercury':181.52},{'Mercury':174.49},input_profile='supplied Raman fixture',coordinate_branch='same printed revolution')
  m=next(r for r in x['rows'] if r['planet']=='Mercury');a=x['rows'][0]
  self.assertEqual(m['assigned_mean_unwrapped'],181.23);self.assertEqual(a['assigned_sighrochcha_normalized'],181.23)
  self.assertAlmostEqual(m['motion_evidence']['cheshtakendra_degrees'],353.115)
  self.assertFalse(x['ephemeris_inputs_computed']);self.assertFalse(x['ketkar_equivalence_verified'])
 def test_missing_inputs_and_branch_not_defaulted(self):
  x=report(None,{}, {},{},input_profile='supplied incomplete',coordinate_branch='declared')
  self.assertTrue(all(r['motion_evidence'] is None for r in x['rows']))
  with self.assertRaises(ValueError):report(0,{}, {},{},input_profile='supplied',coordinate_branch='')
 def test_bad_angles_names_rejected(self):
  for v in (True,float('nan')):
   with self.assertRaises(ValueError):report(v,{}, {},{},input_profile='supplied',coordinate_branch='declared')
  with self.assertRaises(ValueError):report(0,{'Mercury':200},{},{},input_profile='supplied',coordinate_branch='declared')
