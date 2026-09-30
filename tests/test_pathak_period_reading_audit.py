import unittest
from engine.pathak_period_reading_audit import pathak_period_reading_audit


class PathakReadingTests(unittest.TestCase):
    def test_term_and_local_qualification_corroboration(self):
        x = pathak_period_reading_audit()
        self.assertTrue(x['disposition']['friendly_sign_term_retained'])
        self.assertIsNone(x['disposition']['favorable_connective_selected'])
        self.assertTrue(x['vargottama']['fall_or_solar_obscuration_mixed_qualification_corroborated'])
        self.assertEqual(x['vargottama']['source']['pdf_pages'], [239])

    def test_other_house_scope_remains_unresolved(self):
        x = pathak_period_reading_audit()
        p = x['main_sub_pair']
        self.assertEqual(p['main_dusthana_set_explicit'], [6, 8, 12])
        self.assertFalse(p['subperiod_other_house_restricted_to_dusthana_explicit'])
        self.assertIsNone(p['subperiod_scope_selected'])
        self.assertIsNone(p['existing_sastri_or_kapoor_boolean_selected'])
        self.assertIsNone(x['global_precedence'])
        self.assertIsNone(x['personal_outcome'])
