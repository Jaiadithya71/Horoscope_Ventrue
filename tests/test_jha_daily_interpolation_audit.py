import unittest
from fractions import Fraction as F
from engine.jha_daily_interpolation_audit import jha_daily_interpolation_audit as audit

class JhaDailyTests(unittest.TestCase):
 def test_exact_printed_operand_arithmetic(self):
  x=audit();self.assertEqual(F(x['elapsed_hours_rational']),F('36.82'))
  self.assertEqual(F(x['exact_minus_printed_traversal_arcseconds_rational']),F('-0.05'))
  self.assertEqual(F(x['exact_minus_printed_final_arcseconds_rational']),F('0.05'))
  self.assertTrue(x['printed_arc_subtraction_matches_printed_final'])
 def test_no_clock_speed_or_helper_repair(self):
  x=audit();self.assertIsNone(x['printed_clock_label_conflict']['selected_clock_labels'])
  self.assertIsNone(x['mean_true_speed_boundary']['selected_physical_speed_profile'])
  self.assertFalse(x['raman_helper_reused']);self.assertFalse(x['arbitrary_date_ephemeris_verified'])
