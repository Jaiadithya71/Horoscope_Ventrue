import unittest
from fractions import Fraction as F
from engine.jha_luminary_component_audit import jha_luminary_component_audit as audit

class JhaLuminaryAuditTests(unittest.TestCase):
 def test_phase_exact_printed_worked_reading(self):
  p=audit()['paksha_worked'];self.assertEqual(F(p['exact_benefic_virupa_rational']),F(15575,360))
  self.assertEqual(F(p['exact_minus_printed_benefic_seconds_rational']),0)
  self.assertEqual(F(p['exact_minus_printed_malefic_seconds_rational']),0)
  self.assertEqual(p['worked_moon_multiplier'],1);self.assertFalse(p['universal_moon_multiplier_verified'])
 def test_ayana_operand_and_intermediate_errors_retained(self):
  a=audit()['ayana_worked'];self.assertEqual(a['printed_residual_change_arcseconds'],-1200)
  self.assertNotEqual(F(a['next_operand_times12_minus_printed_product_arcseconds_rational']),0)
  self.assertEqual(F(a['printed_product_div30_minus_printed_quotient_arcseconds_rational']),612)
  self.assertEqual(F(a['printed_quotient_plus78_minus_printed_accumulation_arcseconds_rational']),0)
  self.assertEqual(F(a['printed_accumulation_plus90_div3_minus_printed_ayana_arcseconds_rational']),F(1801,3))
 def test_no_multiplier_or_strength_winner(self):
  x=audit();self.assertIsNone(x['selected_multiplier_policy']);self.assertIsNone(x['full_strength'])
