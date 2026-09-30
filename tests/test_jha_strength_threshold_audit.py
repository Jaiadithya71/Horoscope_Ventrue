import unittest
from engine.jha_strength_threshold_audit import jha_strength_threshold_audit as audit
from engine.validation_report import validation_report

class JhaThresholdTests(unittest.TestCase):
 def test_printed_total_conflicts(self):
  x=audit();self.assertEqual(x['disagreeing_total_planets'],['Sun','Mercury','Venus'])
  self.assertEqual([r['table_minus_prose_virupa'] for r in x['total_threshold_rows']],[7,0,0,10,0,-30,0])
 def test_component_heading_conflict_and_ocr_rejection(self):
  x=audit()
  for r in x['component_threshold_rows']:self.assertEqual(set(r['different_component_labels']),{'motion','temporal'})
  sun=next(r for r in x['component_threshold_rows'] if r['planet']=='Sun')
  self.assertEqual(sun['sanskrit_order_and_printed_table_virupa']['ayana'],30)
  self.assertEqual(sun['sanskrit_order_and_printed_table_virupa']['motion'],50)
  self.assertEqual(sun['hindi_prose_heading_order_virupa']['motion'],112)
 def test_no_layout_or_strength_winner(self):
  x=audit();self.assertIsNone(x['selected_threshold_profile']);self.assertIsNone(x['computed_natal_strong_weak_flags'])
  self.assertIsNone(x['sixfold_enumeration']['ayana_containment_selected']);self.assertFalse(x['full_strength_available'])
  self.assertIn('jha_strength_threshold_source_audit',validation_report())
