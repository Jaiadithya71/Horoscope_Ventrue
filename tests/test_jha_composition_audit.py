import unittest
from fractions import Fraction as F
from engine.jha_composition_audit import jha_composition_audit


class JhaCompositionAuditTests(unittest.TestCase):
    def test_exact_natural_ratios_not_integer_substitution(self):
        x = jha_composition_audit()
        self.assertTrue(all(r['exact_ratio_matches'] for r in x['natural_rows']))
        self.assertEqual([F(r['jha_exact_virupa_rational']) for r in x['natural_rows']],
                         [F(60 * i, 7) for i in range(1, 8)])
        self.assertEqual(sum(F(r['exact_minus_quoted_integer_rational']) != 0
                             for r in x['natural_rows']), 6)

    def test_identity_is_not_composition_selection(self):
        x = jha_composition_audit()
        self.assertEqual(x['luminary_equalities'][0]['equal_components'], ['ayana', 'cheshta'])
        self.assertEqual(x['luminary_equalities'][1]['equal_components'], ['paksha', 'cheshta'])
        for key in ('general_ayana_containment_selected', 'luminary_double_counting_selected',
                    'selected_composition_profile', 'full_strength'):
            self.assertIsNone(x[key])
        self.assertEqual(x['identity_source']['pdf_pages'], [189])
