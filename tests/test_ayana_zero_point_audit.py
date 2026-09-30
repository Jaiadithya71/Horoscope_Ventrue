import unittest
from engine.historical_declination import ayana_zero_point_consistency_audit

class AyanaZeroPointTests(unittest.TestCase):
 def test_equator_sentence_does_not_license_global_double(self):
  r=ayana_zero_point_consistency_audit()
  self.assertEqual(len(r['rows']),7)
  for row in r['rows']:
   self.assertEqual(row['base_zero_point_rupa'],'0.5')
   self.assertFalse(row['base_matches_equator_sentence'])
   self.assertIsNone(row['selected_ayana_rupa'])
   if row['planet']=='Sun':self.assertEqual(row['explicit_multiplier_rupa'],'1.0')
   else:self.assertIsNone(row['explicit_multiplier_rupa'])
  self.assertIsNone(r['source_selected_profile']);self.assertIsNone(r['total_strength'])
