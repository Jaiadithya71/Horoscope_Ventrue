import unittest
from engine.historical_declination import ayana_zero_point_consistency_audit

class AyanaZeroPointTests(unittest.TestCase):
 def test_clearer_edition_resolves_fraction_not_global_double(self):
  r=ayana_zero_point_consistency_audit()
  self.assertEqual(len(r['rows']),7)
  for row in r['rows']:
   self.assertEqual(row['base_zero_point_rupa'],'0.5')
   self.assertTrue(row['base_matches_equator_sentence'])
   self.assertEqual(row['equator_sentence_rupa'],'0.5')
   self.assertIsNone(row['selected_ayana_rupa'])
   if row['planet']=='Sun':self.assertEqual(row['explicit_multiplier_rupa'],'1.0')
   else:self.assertIsNone(row['explicit_multiplier_rupa'])
  self.assertIsNone(r['source_selected_profile']);self.assertIsNone(r['total_strength'])
