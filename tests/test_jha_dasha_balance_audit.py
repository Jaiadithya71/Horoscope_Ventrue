import unittest
from fractions import Fraction as F
from engine.jha_dasha_balance_audit import jha_dasha_balance_audit as audit

class JhaDashaTests(unittest.TestCase):
 def test_normalized_balance_and_printed_units(self):
  x=audit();self.assertEqual(F(x['exact_expired_years_rational']),F(767,170))
  self.assertEqual(F(x['exact_remaining_years_rational']),F(933,170))
  self.assertEqual(x['exact_expired_decomposition']['palas'],7)
  self.assertEqual(x['exact_remaining_decomposition']['palas'],52)
  self.assertEqual(F(x['printed_expired_plus_remaining_years_rational']),10)
 def test_solar_target_printed_arithmetic(self):
  x=audit()['solar_target_check'];self.assertEqual(F(x['printed_balance_target_minus_printed_arcseconds_rational']),0)
  self.assertLess(abs(F(x['exact_target_minus_printed_arcseconds_rational'])),1)
 def test_no_calendar_selection_or_app_contract_change(self):
  x=audit();self.assertIsNone(x['selected_calendar_profile']);self.assertIsNone(x['exact_civil_endpoint']);self.assertFalse(x['app_contract_changed'])
  self.assertNotEqual(F(x['remaining_fixed60_diagnostic_years_rational']),F(x['exact_remaining_years_rational']))
