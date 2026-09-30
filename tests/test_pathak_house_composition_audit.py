import unittest
from engine.pathak_house_composition_audit import pathak_house_composition_audit


class PathakHouseCompositionTests(unittest.TestCase):
    def test_term_list_and_commentator_referral(self):
        x = pathak_house_composition_audit()
        self.assertEqual(x['named_additive_terms'], ['house_lord_strength', 'one_rupa', 'house_directional_strength', 'house_aspect_strength'])
        self.assertEqual(x['fixed_addition_rupa'], 1)
        self.assertTrue(x['independent_hindi_and_english_term_list_matches'])
        self.assertTrue(x['english_commentator_refers_to_sripati_chapters_2_and_3'])
        self.assertFalse(x['referral_is_blanket_compatibility_proof'])
        self.assertEqual(x['hindi_source']['pdf_pages'], [73])

    def test_missing_inputs_not_assembled(self):
        x = pathak_house_composition_audit()
        self.assertEqual(len(x['unresolved_assembly_inputs']), 4)
        for key in ('selected_house_total', 'selected_component_profile', 'global_precedence', 'personal_outcome'):
            self.assertIsNone(x[key])
