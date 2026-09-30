import unittest
from engine.angular_trinal_period_readings import angular_trinal_period_readings
from engine.period_manifestation_gate import period_manifestation_gate

class PathakPairCorroborationTests(unittest.TestCase):
    def test_unrelated_no_harm_not_positive_override(self):
        x=angular_trinal_period_readings('Aries','Sun','Saturn',related=False,evidence_profile='supplied relation')
        p=x['independent_hindi_commentary']
        self.assertTrue(p['unrelated_no_harm_clause_corroborated'])
        self.assertFalse(p['unrelated_positive_good_extension_selected'])
        self.assertEqual(p['nearby_xx46_explicit_trikona_houses'],[5,9])
        self.assertFalse(p['nearby_enumeration_transferred_to_xx49'])
        self.assertIsNone(x['selected_translation'])
        self.assertIsNone(x['selected_trikona_scope'])
        self.assertIsNone(x['personal_outcome'])

    def test_manifestation_crossreference_not_new_algorithm(self):
        x=period_manifestation_gate('Sun','Moon')
        p=x['independent_hindi_commentary']
        self.assertEqual(p['relation_cross_reference'],'XV.30')
        self.assertTrue(p['own_subperiod_owned_house_effect_nonautomatic_corroborated'])
        self.assertIsNone(p['similar_circumstances_algorithm_selected'])
        self.assertIsNone(x['xx44_supplied_activation_condition'])
