import unittest
from engine.pathak_strength_threshold_audit import pathak_strength_threshold_audit


class PathakThresholdTests(unittest.TestCase):
    def test_all_thresholds_and_completeness_gate(self):
        x = pathak_strength_threshold_audit()
        self.assertTrue(x['all_existing_thresholds_corroborated'])
        self.assertEqual([r['printed_required_total_rupa'] for r in x['rows']], [6.5, 6, 5, 7, 6.5, 5.5, 5])
        for row in x['rows']:
            self.assertTrue(row['synthetic_exact_threshold_accepted'])
            self.assertIsNone(row['incomplete_threshold_classification'])
        self.assertEqual(x['source']['pdf_pages'], [72, 73])

    def test_emphasis_not_numeric_total(self):
        x = pathak_strength_threshold_audit()
        self.assertEqual(x['component_emphasis'], {'Moon': 'paksha', 'other_planets': 'positional'})
        for key in ('selected_natal_total', 'selected_composition', 'global_precedence', 'personal_outcome'):
            self.assertIsNone(x[key])
