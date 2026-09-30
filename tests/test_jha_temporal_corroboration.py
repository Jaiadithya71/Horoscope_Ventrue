import unittest
from engine.jha_temporal_corroboration import jha_temporal_corroboration


class JhaTemporalCorroborationTests(unittest.TestCase):
    def test_all_six_interiors_and_four_weights(self):
        x = jha_temporal_corroboration()
        self.assertEqual(len(x['third_checks']), 6)
        self.assertTrue(all(r['lord_matches'] and r['jupiter_always_virupa'] == 60
                            and r['active_lord_virupa'] == 60 for r in x['third_checks']))
        self.assertEqual([r['jha_printed_virupa'] for r in x['supplied_lord_weight_checks']], [15, 30, 45, 60])
        self.assertTrue(all(r['weight_matches'] for r in x['supplied_lord_weight_checks']))

    def test_no_calendar_boundary_or_full_strength_inference(self):
        x = jha_temporal_corroboration()
        for key in ('third_boundary_rule_corroborated', 'historical_lord_algorithm_corroborated',
                    'solar_event_model_corroborated'):
            self.assertFalse(x[key])
        self.assertIsNone(x['full_strength'])
        self.assertEqual(x['source']['slokas'], '12-13')
