import unittest
from decimal import Decimal as D
from engine.raman_worked_motion_audit import raman_worked_motion_audit as audit

class WorkedMotionAuditTests(unittest.TestCase):
 def test_source_true_coordinates_are_independent(self):
  x=audit();self.assertEqual(len(x['rows']),5)
  self.assertEqual(x['rows'][0]['opening_true_dms'],[229,30,34])
  self.assertTrue(all(r['arithmetic_candidates'][0]['true_degrees']!=r['arithmetic_candidates'][1]['true_degrees'] for r in x['rows']))
  self.assertEqual(x['coordinate_frame_evidence']['opening_true_label'],'Nirayana/ex-precession')
 def test_exact_decimal_arithmetic_is_not_rounded_fit(self):
  x=audit();mars=x['rows'][0]['arithmetic_candidates'][0];mercury=x['rows'][1]['arithmetic_candidates'][0]
  self.assertEqual(D(mars['cheshtakendra_degrees']),D('293.31'))
  self.assertEqual(D(mercury['cheshtakendra_degrees']),D('353.115'))
  self.assertEqual(D(mercury['difference_from_printed_kendra_degrees']),D('.005'))
  self.assertIsNone(x['selected_motion_input']);self.assertFalse(x['universal_wrap_rule_verified'])
