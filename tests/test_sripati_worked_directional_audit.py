import unittest
from engine.sripati_worked_directional_audit import worked_directional_audit

class WorkedDigbalaTests(unittest.TestCase):
    def test_cross_table_and_formula_conflicts(self):
        x=worked_directional_audit()
        self.assertEqual(x['local_rows_equal_observed_floor'],5)
        failures=[r['planet'] for r in x['rows'] if not r['local_equals_observed_floor']]
        self.assertEqual(failures,['Mercury','Jupiter'])
        mars=next(r for r in x['rows'] if r['planet']=='Mars')
        self.assertEqual(mars['later_local_printed'],'.554')
        self.assertEqual(mars['later_aggregate_printed'],'.534')
        self.assertAlmostEqual(mars['calculated_rupa'],.55454012345679)
        self.assertTrue(all(r['float_pipeline_agrees_with_exact'] for r in x['rows']))
        self.assertFalse(x['mercury_jupiter_exchange_hypothesis']['intent_verified'])
        self.assertIsNone(x['selected_natal_total'])
