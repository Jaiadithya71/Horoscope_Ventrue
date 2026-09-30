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

class NaturalAndPhaseTests(unittest.TestCase):
    def test_natural_source_fractions_not_integer_quote(self):
        from engine.continuous_strength import naisargikabala
        self.assertEqual(naisargikabala('Sun')['rupa'],1)
        self.assertEqual(naisargikabala('Saturn')['rational_rupa'],'1/7')
        self.assertEqual(naisargikabala('Saturn')['quoted_comparison']['virupa'],9)
        self.assertNotEqual(naisargikabala('Saturn')['virupa'],9)

    def test_phase_profiles_and_conflict(self):
        from engine.continuous_strength import pakshabala_candidates
        for lon,val in ((0,0),(90,.5),(180,1),(270,.5),(359,1/180)):
            x=pakshabala_candidates('Moon',0,lon)
            self.assertAlmostEqual(x['candidates'][0]['rupa'],val)
        x=pakshabala_candidates('Moon',0,300)
        self.assertTrue(x['candidate_conflict'])
        self.assertAlmostEqual(x['candidates'][0]['rupa'],1/3)
        self.assertAlmostEqual(x['candidates'][1]['rupa'],2/3)
        self.assertFalse(pakshabala_candidates('Sun',0,90)['candidate_conflict'])
        self.assertEqual(pakshabala_candidates('Mercury',0,180)['candidates'][0]['rupa'],1)
        self.assertEqual(pakshabala_candidates('Sun',0,180)['candidates'][0]['rupa'],0)
