import unittest
from engine.sripati_worked_strength_candidate import worked_direct_owner_candidates

class WorkedStrengthTests(unittest.TestCase):
    def test_exact_components_not_print_fit(self):
        x=worked_direct_owner_candidates()
        totals={r['planet']:r['candidates'][0]['exact_total_rupa'] for r in x['rows']}
        self.assertEqual(totals,{'Sun':'5/2','Moon':'17/8','Mars':'11/4','Mercury':'27/16','Jupiter':'25/8','Venus':'29/32','Saturn':'11/16'})
        for row in x['rows']:
            self.assertEqual(row['candidates'][0]['exact_total_rupa'],row['candidates'][1]['exact_total_rupa'])
            self.assertTrue(all(c['float_component_equals_exact'] for c in row['candidates']))
            self.assertIsNone(row['selected_component'])
        jupiter=next(r for r in x['rows'] if r['planet']=='Jupiter')['candidates'][0]
        self.assertEqual(jupiter['difference_from_1919_printed_total'],'-1/8')
        self.assertEqual(jupiter['difference_from_later_printed_total'],'0')
        self.assertIsNone(x['selected_natal_total'])
        self.assertIsNone(x['selected_profile'])
