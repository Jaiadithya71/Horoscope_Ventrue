import unittest
from fractions import Fraction as F
from engine.three_segment_ayana import three_segment_ayana_candidates as calc,worked_three_segment_ayana_audit

class ThreeSegmentAyanaTests(unittest.TestCase):
    def test_residual_endpoints_and_external_worked_examples(self):
        for deg,expected in [(0,0),(20,30),(30,45),(40,56),(60,78),(75,84),(90,90)]:
            x=calc('Mars',F(deg))['candidates'][0]
            self.assertEqual(x['khanda_accumulated_value'],expected)
            self.assertTrue(x['base_within_zero_one'])
        self.assertEqual(calc('Mars',F(90))['candidates'][0]['base_rupa'],1)
        self.assertEqual(calc('Mars',F(270))['candidates'][0]['base_rupa'],0)
        self.assertEqual(calc('Moon',F(270))['candidates'][0]['base_rupa'],1)
        self.assertEqual(calc('Mercury',F(270))['candidates'][0]['base_rupa'],1)
    def test_literal_overflow_and_models_never_selected(self):
        x=calc('Mars',F(59))
        self.assertGreater(x['candidates'][1]['base_rupa'],1)
        self.assertFalse(x['candidates'][1]['base_within_zero_one'])
        self.assertIsNone(x['selected_profile'])
        audit=worked_three_segment_ayana_audit()
        self.assertEqual(len(audit['rows']),7)
        self.assertTrue(all(abs(r['residual_minus_six_increment_base'])>1e-8 for r in audit['rows']))
        self.assertIsNone(audit['selected_natal_total'])
        with self.assertRaises(ValueError):calc('Rahu',20)
