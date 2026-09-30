import unittest
from engine.bhava_geometry import bhava_geometry
from engine.period_sandhi_gate import period_sandhi_gate

class SandhiPeriodTests(unittest.TestCase):
    def test_exact_wrap_boundary_has_local_override(self):
        g=bhava_geometry(350,260);b=g['boundary_after_house'][12]
        r=period_sandhi_gate({'Jupiter':{'longitude':b}},'Jupiter','Jupiter',geometry=g,geometry_profile='supplied Sripati anchors')['rows'][0]
        self.assertTrue(r['scoped_sandhi_override_active'])
        self.assertEqual(r['geometry_evidence']['historical_effect_fraction'],0)
        self.assertIsNone(r['geometry_evidence']['membership']['house'])
        self.assertFalse(r['favorable_dignity_or_strength_can_remove_sandhi_clause'])
        self.assertIsNone(r['selected_period_outcome'])

    def test_near_is_not_exact_and_centre_is_full(self):
        g=bhava_geometry(10,300);b=g['boundary_after_house'][1]
        x=period_sandhi_gate({'Mars':{'longitude':b-1e-8},'Venus':{'longitude':10}},'Mars','Venus',geometry=g,geometry_profile='supplied')
        self.assertFalse(x['rows'][0]['scoped_sandhi_override_active'])
        self.assertGreater(x['rows'][0]['geometry_evidence']['historical_effect_fraction'],0)
        self.assertEqual(x['rows'][1]['geometry_evidence']['historical_effect_fraction'],1)

    def test_missing_geometry_and_position_are_not_clear(self):
        x=period_sandhi_gate({'Moon':{'longitude':20}},'Moon','Sun')
        self.assertTrue(all(r['at_exact_sandhi'] is None for r in x['rows']))
        self.assertEqual(x['rows'][1]['missing_inputs'],['longitude','degree_bhava_geometry'])
        self.assertIsNone(x['global_precedence'])

    def test_geometry_requires_profile(self):
        with self.assertRaises(ValueError):period_sandhi_gate({},'Sun','Moon',geometry=bhava_geometry(10,300))
