import unittest
from engine.sripati_worked_positional_candidate import worked_positional_candidates

class WorkedPositionalTests(unittest.TestCase):
    def test_matrix_agreement_not_profile_selection(self):
        x=worked_positional_candidates()
        self.assertEqual(x['candidate_count'],28)
        self.assertFalse(x['fixture_distinguishes_axes'])
        for row in x['rows']:
            self.assertTrue(all(c['float_pipeline_agrees_with_exact'] for c in row['candidates']))
            self.assertEqual(len({c['exact_total_rupa'] for c in row['candidates']}),1)
            self.assertIsNone(row['selected_positional_total'])
        jupiter=next(r for r in x['rows'] if r['planet']=='Jupiter')['candidates'][0]
        self.assertAlmostEqual(jupiter['exact_total_decimal'],4.311572530864197)
        self.assertLess(float(__import__('fractions').Fraction(jupiter['difference_from_1919_printed_total'])),-.12)
        self.assertIsNone(x['selected_natal_total'])
