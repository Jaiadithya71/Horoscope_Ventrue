import unittest
from engine.sripati_worked_temporal_audit import worked_temporal_audit

class WorkedTemporalTests(unittest.TestCase):
    def test_explicit_clock_phase_and_third(self):
        x=worked_temporal_audit()
        self.assertEqual(x['clock_inputs']['elapsed_from_midnight_ghatika'],'337/24')
        self.assertEqual(x['natonnata_nearest_diagnostic_matches'],7)
        self.assertTrue(all(r['natonnata_pipeline_agrees'] for r in x['rows']))
        self.assertEqual(x['tribhaga_matches'],7)
        self.assertEqual(x['phase'],'dark_half')
        self.assertEqual(x['paksha_nearest_diagnostic_matches'],4)
        self.assertEqual([r['planet'] for r in x['rows'] if not r['paksha_matches_nearest_three_diagnostic']],['Sun','Mars','Saturn'])
        self.assertTrue(all(r['paksha_pipeline_candidates']['candidate_conflict'] for r in x['rows']))
        self.assertIsNone(x['selected_temporal_values'])
        self.assertIsNone(x['selected_natal_total'])
