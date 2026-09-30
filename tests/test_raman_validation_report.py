import json
import unittest
from engine.raman_validation_report import raman_validation_report
from engine.validation_report import validation_report

class RamanReportTests(unittest.TestCase):
 def test_all_checks_serializable_and_gates_hold(self):
  x=raman_validation_report();json.dumps(x)
  self.assertEqual(len(x['checks']),10)
  self.assertFalse(x['coherent_full_chart_benchmark'])
  self.assertFalse(x['balaji_personal_consultation_replication_verified'])
  for key in ('selected_natal_total','selected_chart_frame','selected_war_winner','empirical_outcome_accuracy'):self.assertIsNone(x[key])
  self.assertNotIn('accuracy_percentage',x)
  for issue in x['critical_source_disagreements']:self.assertIn(issue['check'],x['checks'])
 def test_main_report_contains_same_independent_checks(self):
  self.assertEqual(validation_report()['raman_source_validation'],raman_validation_report())
 def test_critical_unknowns_do_not_disappear(self):
  x=raman_validation_report()['checks']
  self.assertIsNone(x['manual_1932_interpolation_and_frames']['selected_ayanamsa'])
  self.assertIsNone(x['printed_full_component_arithmetic']['selected_printed_correction'])
  self.assertIsNone(x['temporal_clock_phase_and_row_sums']['selected_rounding_policy'])
