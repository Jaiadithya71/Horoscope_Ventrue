import unittest
from engine.friendship import compound_relation,compound_relationship_candidates
from engine.seven_varga_strength import direct_owner_seven_varga

class CompoundTests(unittest.TestCase):
    def test_six_cases(self):
        expected={'friend':('very_friend','neutral'),'neutral':('friend','enemy'),'enemy':('neutral','very_enemy')}
        for n,(f,e) in expected.items():
            for house in range(1,13):
                self.assertEqual(compound_relation(n,house)['compound_relation'],f if house in (2,3,4,10,11,12) else e)
        for bad in (0,13,True):
            with self.assertRaises(ValueError):compound_relation('friend',bad)

    def test_profiles_disagree_and_no_selected(self):
        x=compound_relationship_candidates({'Sun':{'sign':'Aries','sripati_degree_house':{'house':1}},'Moon':{'sign':'Taurus','sripati_degree_house':{'house':1}}})
        self.assertTrue(x['directed_pairs'][0]['candidate_conflict'])
        self.assertIsNone(x['selected_profile'])

    def test_source_sun_direct_example(self):
        x=direct_owner_seven_varga('Sun',17+43/60+30/3600,{'Mars':'very_friend','Moon':'very_friend','Mercury':'friend','Jupiter':'neutral'},relation_profile='sripati_printed_worked_relations',rasi_moolatrikona=False)
        self.assertEqual([r['rupa'] for r in x['vargas']],[.375,.375,.5,.5,.25,.375,.125])
        self.assertEqual(x['rupa'],2.5)

    def test_missing_abstention_and_own_varga_not_moola(self):
        x=direct_owner_seven_varga('Sun',17.725,{},relation_profile='unresolved')
        self.assertIsNone(x['rupa'])
        self.assertEqual(x['vargas'][2]['rupa'],.5)
        x=direct_owner_seven_varga('Sun',120,{},relation_profile='test',rasi_moolatrikona=True)
        self.assertEqual(x['vargas'][0]['rupa'],.75)
        self.assertEqual(x['vargas'][2]['rupa'],.5)
        with self.assertRaises(ValueError):direct_owner_seven_varga('Sun',17.725,{},relation_profile='test',rasi_moolatrikona=True)
        with self.assertRaises(ValueError):direct_owner_seven_varga('Sun',17.725,{'Mars':'self'},relation_profile='test')

class ChartSevenVargaCandidatesTests(unittest.TestCase):
    def test_candidate_bridge_preserves_missing_bhava_and_no_winner(self):
        from engine.seven_varga_strength import chart_direct_owner_candidates
        # All owners exist, but no degree-Bhava assignment is supplied.
        p={a:{'sign':s,'longitude':l} for a,s,l in [('Sun','Aries',17.725),('Moon','Capricorn',284),
              ('Mars','Pisces',351),('Mercury','Aries',10),('Jupiter','Sagittarius',245),
              ('Venus','Taurus',42),('Saturn','Cancer',100)]}
        x=chart_direct_owner_candidates(p)
        self.assertEqual(len(x['planets']),7)
        for row in x['planets']:
            self.assertIsNotNone(row['candidates'][0]['component']['rupa'])
            # Sun/Moon owners may cover some pieces, but no missing relation is filled.
            self.assertIsNone(row['candidates'][1]['component']['rupa'])
            self.assertIsNone(row['selected_component'])
        self.assertIsNone(x['total_strength'])
        self.assertIsNone(x['positional_total'])

    def test_complete_geometry_keeps_both_profiles_and_sources(self):
        from engine.natal import natal_chart
        from engine.seven_varga_strength import chart_direct_owner_candidates
        n=natal_chart('2000-01-01','14:30','Asia/Kolkata',13.0827,80.2707,'Chennai, India')
        x=chart_direct_owner_candidates(n['placements'])
        for r in x['planets']:
            for c in r['candidates']:
                self.assertEqual(c['component']['score_status'],'explicit_input_component')
                self.assertTrue(c['component']['strength_sources'])
                self.assertIn('Phaladeepika1937',c['component']['relation_profile'])
        self.assertIsNone(x['selected_profile'])
