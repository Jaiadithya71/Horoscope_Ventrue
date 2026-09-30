import unittest
from engine.strength_layout import supplied_layout_audit
from engine.full_strength_table_audit import audit_printed_full_strength_table

class StrengthLayoutTests(unittest.TestCase):
 def test_all_printed_rows_equivalent_when_motion_merged(self):
  for r in audit_printed_full_strength_table()['rows']:
   a=supplied_layout_audit(r['printed_components'],layout='expanded_printed_rows',complete=True,component_profile='printed example')
   b=supplied_layout_audit(r['five_class_layout'],layout='five_classes_inclusive_motion',complete=True,component_profile='same printed example merged')
   self.assertEqual(a['supplied_base_sum_rupa'],b['supplied_base_sum_rupa'])
   self.assertIsNone(a['engine_computed_full_strength'])
 def test_double_counting_keys_rejected(self):
  with self.assertRaises(ValueError):supplied_layout_audit({'cheshta_including_ayana':1,'ayana':1},layout='five_classes_inclusive_motion',complete=True,component_profile='bad')
 def test_missing_not_zero_complete_not_certification(self):
  r=supplied_layout_audit({'sthana':1},layout='expanded_printed_rows',complete=True,component_profile='partial')
  self.assertIsNone(r['supplied_base_sum_rupa'])
  self.assertIn('ayana',r['missing_base_components'])
