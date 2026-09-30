import unittest
from engine.pathak_angular_strength_audit import pathak_angular_strength_audit


class PathakAngularStrengthTests(unittest.TestCase):
    def test_existing_fractions_cross_checked(self):
        x = pathak_angular_strength_audit()
        self.assertTrue(x['existing_kendra_refinement_corroborated'])
        self.assertEqual([r['printed_fraction_rupa'] for r in x['rows']], [.25, .5, .75, 1.0])
        self.assertEqual(x['phaladeepika_increasing_order'], [4, 10, 7, 1])
        self.assertEqual(x['source']['pdf_pages'], [68])
        from engine.strength_components import components
        for house, sign in ((1, 'Aries'), (4, 'Cancer'), (7, 'Libra'), (10, 'Capricorn')):
            cs = components('Aries', {'Mars': {'sign': sign}})['planets']['Mars']['house_strength_candidates']
            expected = next(r['printed_fraction_rupa'] for r in x['rows'] if r['house'] == house)
            self.assertEqual(next(c['rupa'] for c in cs if c['rule'] == 'kendra_refinement'), expected)

    def test_attributed_lord_scope_not_occupant_formula(self):
        x = pathak_angular_strength_audit()
        self.assertEqual(x['commentary_attributed_laghu_parashari_increasing_order'], [1, 4, 7, 10])
        self.assertTrue(x['quoted_alternate_verse_mentions_kendra_lords'])
        self.assertFalse(x['attributed_order_independently_verified_against_laghu_parashari'])
        self.assertFalse(x['alternate_order_numeric_fractions_explicit'])
        self.assertFalse(x['alternate_order_applied_to_occupants'])
        for key in ('selected_school', 'selected_house_component', 'total_strength', 'global_precedence'):
            self.assertIsNone(x[key])
