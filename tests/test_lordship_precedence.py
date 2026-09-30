import unittest
from engine.lordship_precedence import lordship_precedence
from engine.forecast import SIGNS

class LordshipPrecedenceTests(unittest.TestCase):
    def test_leo_jupiter_original_example(self):
        x=lordship_precedence('Leo')
        j=next(r for r in x['dual_owner_evidence'] if r['planet']=='Jupiter')
        self.assertEqual(j['general_rule'],{'primary_house':5,'other_house_relative_effect':.5,'sloka':11})
        self.assertEqual(j['other_owned_house'],8)
        self.assertIsNone(j['lagna_dusthana_exception'])
        self.assertIsNone(x['global_outcome_precedence'])

    def test_lagna_exception_overlap_retained(self):
        for sign,planet,dust in (('Aries','Mars',8),('Scorpio','Mars',6),('Taurus','Venus',6),('Libra','Venus',8),('Aquarius','Saturn',12)):
            row=next(r for r in lordship_precedence(sign)['dual_owner_evidence'] if r['planet']==planet)
            self.assertEqual(row['lagna_dusthana_exception']['primary_house'],1)
            self.assertEqual(row['lagna_dusthana_exception']['secondary_dusthana_house'],dust)
            self.assertTrue(row['scope_overlap'])
            self.assertIsNone(row['selected_effect_weights'])
        mars=next(r for r in lordship_precedence('Scorpio')['dual_owner_evidence'] if r['planet']=='Mars')
        self.assertEqual(mars['general_rule']['primary_house'],6)
        self.assertEqual(mars['lagna_dusthana_exception']['primary_house'],1)

    def test_all_geometry_no_single_owner(self):
        for sign in SIGNS:
            x=lordship_precedence(sign)
            self.assertEqual(len(x['dual_owner_evidence']),5)
            for r in x['dual_owner_evidence']:
                self.assertNotIn(r['planet'],('Sun','Moon'))
                self.assertEqual(len(r['owned_houses']),2)
                self.assertIn(r['general_rule']['primary_house'],[h['house'] for h in r['owned_houses']])
