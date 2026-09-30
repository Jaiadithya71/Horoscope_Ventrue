import unittest
from engine.sripati_worked_lord_subtotal_audit import worked_lord_subtotal_audit

class WorkedLordSubtotalTests(unittest.TestCase):
    def test_epoch_ordinal_and_scoped_matrix(self):
        x=worked_lord_subtotal_audit()
        self.assertEqual(x['supplied_epoch_reconstruction']['terrestrial_days'],714404106135)
        self.assertEqual(x['completed_sign_index'],23)
        self.assertEqual(x['worked_ordinal_1_based'],24)
        self.assertIsNone(x['positional_hora_candidates']['original_sample_disagreement'])
        self.assertEqual(x['positional_hora_candidates']['worked_sample_supported_profile'],'completed_signs_zero_based')
        self.assertEqual(x['local_subtotals_close'],7)
        self.assertEqual(x['local_vs_full_table_matches'],7)
        self.assertEqual(len(x['candidate_matrix']),8)
        self.assertTrue(all(len(r['rows'])==7 and not r['selected'] for r in x['candidate_matrix']))
        self.assertIsNone(x['selected_natal_total'])
