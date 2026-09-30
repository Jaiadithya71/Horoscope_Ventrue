import unittest
from engine.pathak_protective_potency_audit import pathak_protective_potency_audit


class PathakProtectivePotencyTests(unittest.TestCase):
    def test_relative_scope_and_independent_sources(self):
        x = pathak_protective_potency_audit()
        self.assertEqual(x['relative_potency_to_jupiter'], {'Jupiter': '1', 'Mercury': '1/4', 'Venus': '1/2'})
        self.assertTrue(x['same_relative_potency_and_moon_basis_corroborated'])
        self.assertTrue(x['moon_strength_described_as_basis_of_planet_strength'])
        self.assertEqual(x['hindi_source']['pdf_pages'], [68, 69])
        self.assertEqual(x['english_source']['pdf_pages'], [74, 75])

    def test_no_strength_scaling_or_automatic_cancellation(self):
        x = pathak_protective_potency_audit()
        self.assertFalse(x['moon_dependency_formula_explicit'])
        for key in ('selected_natal_applicability', 'selected_strength_multiplier',
                    'selected_adverse_cancellation', 'global_outcome_precedence'):
            self.assertIsNone(x[key])
