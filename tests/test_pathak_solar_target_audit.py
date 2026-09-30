import unittest
from fractions import Fraction as F
from engine.pathak_solar_target_audit import pathak_solar_target_audit


class PathakTargetAuditTests(unittest.TestCase):
    def test_balance_and_target_errors_preserved(self):
        x = pathak_solar_target_audit()
        self.assertEqual(F(x['exact_normalized_remaining_years_rational']), F(950, 167))
        self.assertEqual(F(x['printed_minus_exact_balance_palas_rational']), F(-15, 167))
        self.assertEqual(F(x['computed_minus_printed_target_arcseconds_rational']), -270 * 3600)
        self.assertFalse(x['worked_endpoint_arithmetic_matches'])

    def test_commentary_interpretation_not_universal_selection(self):
        x = pathak_solar_target_audit()
        self.assertEqual(x['supported_named_calendar_interpretation'], 'solar_angular_target')
        self.assertFalse(x['elapsed_utc_interpolation_explicitly_supported'])
        self.assertIsNone(x['selected_calendar_profile'])
        self.assertIsNone(x['exact_civil_endpoint'])
        self.assertFalse(x['app_contract_changed'])
        self.assertEqual(x['source']['pdf_pages'], [222, 223])

    def test_edition_and_sign_context_retained(self):
        x = pathak_solar_target_audit()
        self.assertEqual(x['edition']['reprint_year'], 2007)
        self.assertTrue(x['edition']['publisher_all_rights_reserved'])
        self.assertFalse(x['public_release_rights_cleared'])
        self.assertIn('Aquarius', x['source_sign_numbering'])
        self.assertFalse(x['input_sign_explanation_found_in_worked_passage'])
