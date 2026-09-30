import unittest
from engine.degree_aspects import degree_aspect,degree_aspect_evidence,BASE_QUARTERS

class DegreeAspectTests(unittest.TestCase):
    def test_base_knots_and_midpoints(self):
        for k in range(12):
            self.assertEqual(degree_aspect('Sun',0,30*k)['rupa'],BASE_QUARTERS[k]/4)
            self.assertEqual(degree_aspect('Sun',0,30*k+15)['rupa'],(BASE_QUARTERS[k]+BASE_QUARTERS[k+1])/8)

    def test_special_knots_and_taper(self):
        for p,knots in (('Jupiter',(120,240)),('Saturn',(60,270)),('Mars',(90,210))):
            for x in knots:
                self.assertEqual(degree_aspect(p,0,x)['rupa'],1)
                self.assertAlmostEqual(degree_aspect(p,0,x+1e-6)['rupa'],1,places=6)
                self.assertAlmostEqual(degree_aspect(p,0,x-1e-6)['rupa'],1,places=6)
        self.assertIsNotNone(degree_aspect('Jupiter',0,120)['translation_conflict_notice'])

    def test_original_worked_examples(self):
        sun=17+43/60+30/3600
        moon=270+14+29/60+39/3600
        jupiter=240+1+25/60+1/3600
        self.assertEqual(round(degree_aspect('Sun',sun,moon)['rupa'],3),.277)
        x=degree_aspect('Jupiter',jupiter,sun)
        self.assertEqual(round(x['base_rupa'],3),.228)
        self.assertEqual(round(x['special_addition_rupa'],3),.228)
        self.assertEqual(round(x['rupa'],3),.456)

    def test_rotation_direction_limits(self):
        self.assertEqual(degree_aspect('Sun',350,170)['rupa'],1)
        self.assertNotEqual(degree_aspect('Sun',0,90)['rupa'],degree_aspect('Sun',90,0)['rupa'])
        for p in ('Sun','Moon','Mars','Mercury','Jupiter','Venus','Saturn'):
            for degree in range(360):
                x=degree_aspect(p,0,degree)
                self.assertTrue(0<=x['rupa']<=1)
                self.assertTrue(x['special_addition_rupa']>=0)
        for bad in (-1,360,float('nan')):
            with self.assertRaises(ValueError):degree_aspect('Sun',bad,0)
        with self.assertRaises(ValueError):degree_aspect('Rahu',0,0)

    def test_no_net_or_node_inference(self):
        x=degree_aspect_evidence({'Sun':{'longitude':0},'Moon':{'longitude':90},'Rahu':{'longitude':120}})
        self.assertEqual(len(x['directed_pairs']),2)
        self.assertIsNone(x['signed_total'])
