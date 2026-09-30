import unittest
from engine.continuous_strength import uchchabala,digbala,continuous_components,NEECHA,WEAKEST_BHAVA

class ContinuousTests(unittest.TestCase):
    def test_source_example(self):
        sun=17+43/60+30/3600
        self.assertAlmostEqual(uchchabala('Sun',sun)['rupa'],10336.5/10800)
        self.assertEqual(round(uchchabala('Sun',sun)['rupa'],3),0.957)
        fourth=90+7+42/60+11/3600
        self.assertAlmostEqual(digbala('Sun',sun,{4:fourth})['rupa'],(2*30+19+58/60+41/3600)/180)
        self.assertEqual(round(digbala('Sun',sun,{4:fourth})['rupa'],3),0.444)

    def test_extremes_and_units(self):
        for p,low in NEECHA.items():
            self.assertEqual(uchchabala(p,low)['rupa'],0)
            self.assertEqual(uchchabala(p,(low+180)%360)['rupa'],1)
            self.assertEqual(uchchabala(p,(low+90)%360)['virupa'],30)
            self.assertEqual(digbala(p,0,{WEAKEST_BHAVA[p]:0})['rupa'],0)
            self.assertEqual(digbala(p,180,{WEAKEST_BHAVA[p]:0})['rupa'],1)
        self.assertAlmostEqual(uchchabala('Sun',0)['rupa'],170/180)
        self.assertAlmostEqual(uchchabala('Sun',359)['rupa'],169/180)

    def test_no_fake_centres_or_total(self):
        p={'Sun':{'longitude':10},'Rahu':{'longitude':12}}
        x=continuous_components(p)
        self.assertIsNone(x['total_strength']);self.assertIsNone(x['planets']['Sun']['digbala'])
        self.assertNotIn('Rahu',x['planets'])
        with self.assertRaises(ValueError):digbala('Sun',10,{1:10})
        for lon in (-1,360,float('nan'),float('inf')):
            with self.assertRaises(ValueError):uchchabala('Sun',lon)
