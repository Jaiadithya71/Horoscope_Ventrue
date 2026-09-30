import unittest
from engine.sripati_worked_ayana_audit import worked_ayana_audit

class WorkedAyanaTests(unittest.TestCase):
    def test_exact_source_chain_not_print_fit(self):
        x=worked_ayana_audit()
        self.assertEqual(x['declination_floor3_matches'],6)
        self.assertEqual(x['ayana_base_floor3_matches'],6)
        self.assertTrue(all(r['pipeline_exact_agreement'] for r in x['rows']))
        sun=x['rows'][0]
        self.assertEqual(sun['printed_declination_both_editions'],'14.877')
        self.assertAlmostEqual(sun['calculated_declination_degrees'],14.879053086419754)
        self.assertAlmostEqual(sun['calculated_base_ayana_rupa'],.8099802726337448)
        self.assertEqual(len(sun['ayana_pipeline_candidates']['candidates']),2)
        self.assertIsNone(x['selected_natal_total'])
