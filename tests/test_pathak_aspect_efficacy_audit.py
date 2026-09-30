import unittest
from engine.pathak_aspect_efficacy_audit import pathak_aspect_efficacy_audit


class PathakAspectEfficacyTests(unittest.TestCase):
    def test_separate_primary_and_attributed_readings(self):
        x = pathak_aspect_efficacy_audit()
        self.assertTrue(x['primary_reading']['seventh_aspect_most_effective'])
        self.assertFalse(x['primary_reading']['other_aspects_equal_efficacy_asserted'])
        a = x['attributed_other_teachers_reading']
        self.assertTrue(a['special_aspects_equally_important_in_yogas'])
        self.assertEqual(a['named_special_aspects'], {'Jupiter': [5, 9], 'Mars': [4, 8], 'Saturn': [3, 10]})
        self.assertTrue(x['english_1937_other_teachers_not_less_efficacious_reading_corroborated'])
        self.assertEqual(x['hindi_source']['pdf_pages'], [68])
        self.assertEqual(x['english_source']['pdf_pages'], [74])

    def test_no_numeric_or_global_selection(self):
        x = pathak_aspect_efficacy_audit()
        for k in ('selected_reading', 'numeric_efficacy_weights',
                  'universal_qualifying_aspect_definition', 'global_outcome_precedence'):
            self.assertIsNone(x[k])
