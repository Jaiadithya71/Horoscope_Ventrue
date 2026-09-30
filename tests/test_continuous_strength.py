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

class DeclinationAndClockTests(unittest.TestCase):
    def test_declination_examples_and_sun_disagreement(self):
        from engine.continuous_strength import ayanabala_candidates
        x=ayanabala_candidates('Sun',892.737/60)
        self.assertEqual(round(x['candidates'][0]['rupa'],4),0.8100)
        self.assertAlmostEqual(x['candidates'][1]['rupa'],x['candidates'][0]['rupa']*2)
        self.assertTrue(x['candidate_conflict'])
        self.assertEqual(ayanabala_candidates('Moon',-24)['candidates'][0]['rupa'],1)
        self.assertEqual(ayanabala_candidates('Saturn',24)['candidates'][0]['rupa'],0)
        self.assertEqual(ayanabala_candidates('Mercury',-12)['candidates'][0]['rupa'],.75)
        for decl in (-24.1,24.1,float('nan')):
            with self.assertRaises(ValueError):ayanabala_candidates('Sun',decl)

    def test_clock_component_no_civil_clock_assumption(self):
        from engine.continuous_strength import natonnatabala
        self.assertEqual(natonnatabala('Sun',0)['rupa'],0)
        self.assertEqual(natonnatabala('Sun',12)['rupa'],1)
        self.assertEqual(natonnatabala('Venus',18)['rupa'],.5)
        self.assertEqual(natonnatabala('Saturn',0)['rupa'],1)
        self.assertEqual(natonnatabala('Mercury',3)['rupa'],1)
        for hour in (-1,24,float('nan')):
            with self.assertRaises(ValueError):natonnatabala('Sun',hour)

    def test_later_moon_doubling_remains_separate(self):
        from engine.continuous_strength import pakshabala_candidates
        x=pakshabala_candidates('Moon',0,90)
        self.assertEqual(x['candidates'][0]['rupa'],.5)
        self.assertEqual(x['later_moon_multiplier_evidence']['doubled_candidates'][0]['rupa'],1)
        self.assertIsNone(pakshabala_candidates('Mercury',0,90)['later_moon_multiplier_evidence'])

class ParityTests(unittest.TestCase):
    def test_original_worked_positions(self):
        from engine.continuous_strength import yugmayugmabala
        # Source's Sun17d43m30s: Aries/Virgo. Moon Capricorn/Taurus.
        self.assertEqual(yugmayugmabala('Sun',17+43/60+30/3600)['rupa'],.25)
        self.assertEqual(yugmayugmabala('Moon',284)['rupa'],.5)
        self.assertEqual(yugmayugmabala('Mars',359)['rupa'],0)

    def test_half_open_sign_and_navamsa_boundaries(self):
        from engine.continuous_strength import yugmayugmabala
        self.assertEqual(yugmayugmabala('Sun',0)['rupa'],.5)
        self.assertEqual(yugmayugmabala('Moon',0)['rupa'],0)
        self.assertEqual(yugmayugmabala('Venus',45)['rupa'],.5)
        self.assertEqual(yugmayugmabala('Mercury',45)['rupa'],0)
        with self.assertRaises(ValueError):yugmayugmabala('Rahu',0)

class HouseAndDecanTests(unittest.TestCase):
    def test_house_categories_and_disagreement(self):
        from engine.continuous_strength import kendradibala_candidates
        for house in range(1,13):
            x=kendradibala_candidates(house,house)
            self.assertEqual(x['candidates'][0]['rupa'],(1,.5,.25)[(house-1)%3])
            self.assertFalse(x['candidate_conflict'])
        self.assertTrue(kendradibala_candidates(1,12)['candidate_conflict'])
        self.assertEqual(len(kendradibala_candidates(1,None)['candidates']),1)
        self.assertEqual(kendradibala_candidates()['candidates'],[])
        for bad in (0,13,1.5,True):
            with self.assertRaises(ValueError):kendradibala_candidates(bad)

    def test_decan_classes_and_boundaries(self):
        from engine.continuous_strength import drekkanabala,PLANET_DEKAN_CLASS
        for p,c in PLANET_DEKAN_CLASS.items():
            preferred={'masculine':1,'neuter':2,'feminine':3}[c]
            for k in range(3):
                self.assertEqual(drekkanabala(p,30+k*10)['rupa'],.25 if k+1==preferred else 0)
        self.assertEqual(drekkanabala('Sun',9.999999)['rupa'],.25)
        self.assertEqual(drekkanabala('Sun',10)['rupa'],0)
        self.assertEqual(drekkanabala('Venus',20)['rupa'],.25)
        with self.assertRaises(ValueError):drekkanabala('Rahu',0)

    def test_source_table_and_unapplied_refinement(self):
        from engine.continuous_strength import drekkanabala
        # PDF52 source Jupiter at beginning, Sun at17deg, Moon at14deg.
        self.assertEqual(drekkanabala('Jupiter',240+5)['rupa'],.25)
        self.assertEqual(drekkanabala('Sun',17.725)['rupa'],0)
        self.assertEqual(drekkanabala('Moon',284)['rupa'],0)
        self.assertEqual(drekkanabala('Jupiter',245)['quoted_own_shadvarga_adjustment']['status'],'not_evaluated')

    def test_components_preserve_sandhi(self):
        x=continuous_components({'Sun':{'longitude':10,'whole_sign_house_from_ascendant':1,
                                     'sripati_degree_house':{'house':None,'at_sandhi':True}}})
        self.assertEqual(len(x['planets']['Sun']['kendradibala_candidates']['candidates']),1)
        self.assertIsNone(x['total_strength'])

class NatalStatusTests(unittest.TestCase):
    def test_live_natal_partial_status_and_separate_houses(self):
        from engine.natal import natal_chart
        chart=natal_chart('2000-01-01','14:30','Asia/Kolkata',13.0827,80.2707,'Chennai, India')
        factors=chart['natal_factors']
        components=factors['continuous_strength_components']
        self.assertIsNone(components['total_strength'])
        self.assertIn('global outcome precedence',factors['unresolved_conventions'])
        self.assertNotIn('numeric directional (whole-sign condition only)',factors['missing_strength_components'])
        for p,row in components['planets'].items():
            self.assertIsNotNone(row['digbala'])
            self.assertEqual(row['kendradibala_candidates']['candidates'][0]['profile'],'rasi_house')
            self.assertEqual(row['kendradibala_candidates']['candidates'][1]['profile'],'sripati_degree_bhava')
            self.assertIn('sripati_degree_house',chart['placements'][p])
            self.assertIn('whole_sign_house_from_ascendant',chart['placements'][p])

class SeventhVargaTests(unittest.TestCase):
    def test_source_owner_sequences(self):
        from engine.vargas import saptamsa,seven_varga_owner_evidence,six_vargas
        for base,owners in ((0,('Mars','Venus','Mercury','Moon','Sun','Mercury','Venus')),
                            (30,('Mars','Jupiter','Saturn','Saturn','Jupiter','Mars','Venus'))):
            for k,owner in enumerate(owners):
                self.assertEqual(saptamsa(base+(k+.5)*30/7)['owner'],owner)
        self.assertEqual(saptamsa(17.725)['sign'],'Leo')
        self.assertEqual(saptamsa(0)['part_1_based'],1)
        self.assertEqual(saptamsa(30)['sign'],'Scorpio')
        self.assertEqual(saptamsa(359.999)['part_1_based'],7)
        self.assertEqual(len(seven_varga_owner_evidence('Sun',17.725)['vargas']),7)
        self.assertEqual(len(six_vargas(17.725)['vargas']),6)
        self.assertEqual(seven_varga_owner_evidence('Sun',17.725)['score_status'],'not_scored')
        for bad in (-1,360,float('nan')):
            with self.assertRaises(ValueError):saptamsa(bad)
