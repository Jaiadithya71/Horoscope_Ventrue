import unittest
from engine.bhava_geometry import bhava_geometry
from engine.bhava_effectiveness import bhava_effectiveness

class BhavaEffectTests(unittest.TestCase):
    def test_centre_boundaries_and_halves(self):
        g=bhava_geometry(350,260)
        for h in range(1,13):
            c=g['centres'][h];b=g['boundary_after_house'][h]
            self.assertEqual(bhava_effectiveness(c,g)['historical_effect_fraction'],1)
            edge=bhava_effectiveness(b,g)
            self.assertEqual(edge['historical_effect_fraction'],0)
            self.assertIsNone(edge['membership']['house'])
            midpoint=(c+(b-c)%360/2)%360
            self.assertAlmostEqual(bhava_effectiveness(midpoint,g)['historical_effect_fraction'],.5)

    def test_asymmetric_quadrants_and_near_boundary(self):
        g=bhava_geometry(10,300)
        c=g['centres'][1];before=g['boundary_after_house'][12];after=g['boundary_after_house'][1]
        for edge in (before,after):
            delta=(edge-c+180)%360-180
            x=(c+delta/2)%360
            self.assertAlmostEqual(bhava_effectiveness(x,g)['historical_effect_fraction'],.5)
        near=(after-1e-8)%360
        self.assertGreater(bhava_effectiveness(near,g)['historical_effect_fraction'],0)
        self.assertFalse(bhava_effectiveness(near,g)['qualifies_despite_strength'])
