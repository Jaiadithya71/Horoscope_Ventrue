import unittest
from engine.raman_motion_source_audit import raman_motion_source_audit

class RamanMotionAuditTests(unittest.TestCase):
 def test_arithmetic_errors_not_repaired(self):
  x=raman_motion_source_audit();v=x['venus_example48']
  self.assertEqual(v['exact_sum_printed_terms'],'875.15');self.assertFalse(v['sum_matches_printed_total'])
  self.assertEqual(v['sum_mod360'],'155.15');self.assertEqual(v['printed_final'],'158.35')
  self.assertFalse(x['mercury']['fractional_row_matches'])
  self.assertFalse(x['saturn']['summary_matches_rule_at_two_places'])
 def test_worked_values_and_assignments_retained_not_selected(self):
  x=raman_motion_source_audit();s=next(r for r in x['worked_kendra_rows'] if r['planet']=='Saturn')
  self.assertEqual(s['exact_kendra_from_printed_inputs'],'63.42')
  self.assertFalse(x['named_raman_assignments']['ketkar_equivalence_verified'])
  self.assertIsNone(x['selected_motion_profile']);self.assertFalse(x['arbitrary_date_ephemeris_complete'])
