import unittest
from engine.pathak_dusthana_lord_period import pathak_dusthana_lord_period as gate


class PathakOwnerPeriodTests(unittest.TestCase):
    def result(self, house=6, period=None, strong=None):
        return gate(owned_house=house, main_period_is_owner=period, lord_strong=strong,
                    strength_profile='supplied complete candidate strength', ownership_profile='supplied sign ownership')

    def test_three_clauses_require_strength_and_period(self):
        for house, verse in ((6, '7'), (8, '9'), (12, '13')):
            x = self.result(house, True, True)
            self.assertTrue(x['scoped_favorable_clause_applies'])
            self.assertEqual(x['source']['slokas'], verse)
            self.assertIsNone(x['global_polarity'])
            self.assertIsNone(x['personal_outcome'])

    def test_truth_table_and_no_adverse_inversion(self):
        for period, strong, expected in ((True, None, None), (None, True, None),
                                        (None, None, None), (False, None, False),
                                        (None, False, False), (True, False, False)):
            x = self.result(period=period, strong=strong)
            self.assertIs(x['scoped_favorable_clause_applies'], expected)
            self.assertIsNone(x['global_polarity'])
        self.assertTrue(self.result()['sixth_owner_always_adverse_rejected_by_commentary'])
        self.assertFalse(self.result(8)['sixth_owner_always_adverse_rejected_by_commentary'])

    def test_invalid_inputs(self):
        for house in (True, 1, 7, None, '6'):
            with self.assertRaises(ValueError): self.result(house)
        with self.assertRaises(ValueError): self.result(period=1)
        with self.assertRaises(ValueError): self.result(strong='strong')
        with self.assertRaises(ValueError):
            gate(owned_house=6, strength_profile='', ownership_profile='supplied')
