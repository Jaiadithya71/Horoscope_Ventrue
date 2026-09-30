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
