import unittest
from engine.bhava_geometry import bhava_geometry,house_membership
from engine.continuous_strength import digbala

class BhavaTests(unittest.TestCase):
    def test_page_example_centres_and_sandhi(self):
        asc=14+31/60+46/3600
        fourth=97+42/60+11/3600
        x=bhava_geometry(asc,(fourth+180)%360)
        # Printed example rounds intermediate thirds to seconds; check within1s.
        self.assertAlmostEqual(x['centres'][2],42+15/60+14/3600,delta=1/3600)
        self.assertAlmostEqual(x['centres'][3],69+58/60+43/3600,delta=1/3600)
        # The page's worked paragraph has 2-9-53-43; table has2-9-58-43.
        # Exact trisection is2-9-58-42.6667, matching table, not paragraph typo.
        self.assertAlmostEqual(x['boundary_after_house'][1],28+23/60+30/3600,delta=1/3600)
        self.assertEqual(house_membership(asc,x)['house'],1)
        self.assertTrue(house_membership(x['boundary_after_house'][1],x)['at_sandhi'])
        self.assertEqual(house_membership(x['boundary_after_house'][1]+.001,x)['house'],2)
        self.assertEqual(round(digbala('Sun',17+43/60+30/3600,x['centres'])['rupa'],3),.444)

    def test_wrap_and_invalid_anchors(self):
        x=bhava_geometry(350,260)
        self.assertEqual(x['centres'][2],20)
        self.assertEqual(x['boundary_after_house'][1],5)
        self.assertEqual(house_membership(0,x)['house'],1)
        self.assertEqual(house_membership(6,x)['house'],2)
        self.assertEqual(len(x['centres']),12)
        for a,m in ((0,0),(0,180),(-1,270),(float('nan'),270)):
            with self.assertRaises(ValueError):bhava_geometry(a,m)

class NatalGeometryIntegrationTests(unittest.TestCase):
    def test_degree_direction_integrated_without_changing_whole_sign(self):
        from engine.natal import natal_chart
        from engine.continuous_strength import digbala
        x=natal_chart('2000-01-01','14:30','Asia/Kolkata',13.0827,80.2707,'Chennai, India')
        g=x['sripati_degree_geometry']
        self.assertEqual(len(g['centres']),12)
        self.assertAlmostEqual(g['centres'][1],x['ascendant']['longitude'],delta=.00001)
        self.assertAlmostEqual(g['centres'][10],x['midheaven']['longitude'],delta=.00001)
        sun=x['placements']['Sun']
        d=x['natal_factors']['continuous_strength_components']['planets']['Sun']['digbala']
        self.assertEqual(d['rupa'],digbala('Sun',sun['longitude'],g['centres'])['rupa'])
        self.assertIn('whole_sign_house_from_ascendant',sun)
        self.assertIn('sripati_degree_house',sun)
        self.assertIsNone(x['natal_factors']['continuous_strength_components']['total_strength'])

    def test_geometry_does_not_change_with_house_label(self):
        # Asymmetrical quadrants are distinct from30-degree whole-sign boxes.
        x=bhava_geometry(28.58,289.28)
        self.assertNotEqual(x['centres'][2]-x['centres'][1],30)
        self.assertNotEqual(x['centres'][2],30)

class NatalPrecisionIntegrationTests(unittest.TestCase):
    def test_all_returned_angles_keep_geometry_precision(self):
        from engine.natal import natal_chart
        from engine.bhava_effectiveness import bhava_effectiveness
        x=natal_chart('2000-01-01','14:30','Asia/Kolkata',13.0827,80.2707,'Chennai, India')
        g=x['sripati_degree_geometry']
        self.assertEqual(g['centres'][1],x['ascendant']['longitude'])
        self.assertEqual(g['centres'][10],x['midheaven']['longitude'])
        for p in x['placements'].values():
            self.assertEqual(p['bhava_effectiveness_evidence'],bhava_effectiveness(p['longitude'],g))
        for name in ('ascendant','midheaven'):
            self.assertEqual(x[name]['longitude_display_5dp'],round(x[name]['longitude'],5))
