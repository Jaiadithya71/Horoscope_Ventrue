import unittest
from engine.horaratna_own_varga_scope_audit import horaratna_own_varga_scope_audit


class HoraratnaOwnVargaTests(unittest.TestCase):
    def test_independent_threshold_candidate_not_any_one(self):
        r = horaratna_own_varga_scope_audit()
        rows = {p['planet']: p for p in r['worked_rows_using_existing_named_geometry']}
        self.assertEqual(rows['Jupiter']['own_varga_count'], 3)
        self.assertTrue(rows['Jupiter']['garga_minimum_three_owned_candidate'])
        self.assertTrue(rows['Sun']['any_one_owned_hypothesis'])
        self.assertFalse(rows['Sun']['garga_minimum_three_owned_candidate'])
        self.assertEqual(rows['Mars']['own_varga_count'], 2)
        self.assertFalse(rows['Mars']['garga_minimum_three_owned_candidate'])
        self.assertFalse(r['all_six_candidate_fits_explicit_jupiter_example'])

    def test_scope_and_class_order_not_merged(self):
        r = horaratna_own_varga_scope_audit()
        self.assertFalse(r['decan_class_orders_agree'])
        self.assertFalse(r['sripati_any_or_all_quantifier_settled'])
        self.assertFalse(r['horaratna_explicitly_maps_garga_threshold_to_sripati_refinement'])
        self.assertIsNone(r['selected_refinement_definition'])
        self.assertIsNone(r['selected_positional_total'])
        self.assertTrue(all(p['selected_refined_component'] is None
                            for p in r['worked_rows_using_existing_named_geometry']))
