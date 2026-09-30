import unittest
from engine.luminary_cheshta_rays import luminary_cheshta_rays as calc

class LuminaryRaysTests(unittest.TestCase):
    def test_original_sun_moon_not_a_strength_winner(self):
        sun=17+43/60+30/3600
        moon=270+14+29/60+39/3600
        ayana=21+47/60+38/3600
        x=calc(sun,moon,ayana,coordinate_profile='original IV sexagesimal example')
        self.assertAlmostEqual(x['luminaries']['Sun']['cheshtakendra_degrees'],120+9+31/60+8/3600)
        for p,printed in (('Sun',5.317),('Moon',4.107)):
            self.assertLess(abs(x['luminaries'][p]['cheshta_rays']-printed),.001)
            self.assertEqual(x['luminaries'][p]['source']['chapter'],'IV')
        self.assertIsNone(x['selected_shadbala_motion_component'])
        self.assertIsNone(x['total_strength'])

    def test_fold_extrema_and_missing_profile(self):
        for moon,rays in ((0,1),(180,7),(270,4)):
            self.assertEqual(calc(0,moon,0,coordinate_profile='synthetic')['luminaries']['Moon']['cheshta_rays'],rays)
        for sun,moon,ayana,profile in ((360,0,0,'x'),(0,-1,0,'x'),(0,0,float('nan'),'x'),(0,0,0,'')):
            with self.assertRaises(ValueError):calc(sun,moon,ayana,coordinate_profile=profile)
