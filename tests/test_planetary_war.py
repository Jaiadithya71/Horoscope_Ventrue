import unittest
from engine.planetary_war import planetary_war_evidence

class WarTests(unittest.TestCase):
    def test_wrapped_separation_boundary_and_north_evidence(self):
        x=planetary_war_evidence('Mars','Venus',359.8,.2,latitude_a=.1,latitude_b=.2,coordinate_profile='fixture')
        self.assertAlmostEqual(x['longitude_separation_degrees'],.4)
        self.assertTrue(x['commentary_less_than_one_degree_condition'])
        self.assertEqual(x['north_planet'],'Venus')
        self.assertIsNone(x['selected_winner'])
        self.assertIsNone(x['adjusted_total_strength'])
        self.assertFalse(planetary_war_evidence('Mars','Venus',0,1,coordinate_profile='fixture')['commentary_less_than_one_degree_condition'])

    def test_exact_and_minute_conditions_not_merged(self):
        x=planetary_war_evidence('Mars','Venus',20,20,latitude_a=0,latitude_b=0,coordinate_profile='fixture')
        self.assertTrue(x['main_verse_exact_longitude_agreement'])
        self.assertIsNone(x['north_planet'])
        x=planetary_war_evidence('Mars','Venus',20,20.01,coordinate_profile='fixture')
        self.assertTrue(x['within_one_arcminute'])
        self.assertFalse(x['main_verse_exact_longitude_agreement'])
        self.assertIsNone(x['north_planet'])

    def test_invalid(self):
        for a,b in [('Sun','Venus'),('Mars','Mars'),('Rahu','Venus')]:
            with self.assertRaises(ValueError):planetary_war_evidence(a,b,20,20,coordinate_profile='fixture')
        with self.assertRaises(ValueError):planetary_war_evidence('Mars','Venus',20,20,coordinate_profile='')
        with self.assertRaises(ValueError):planetary_war_evidence('Mars','Venus',20,20,latitude_a=float('nan'),coordinate_profile='fixture')

class WarIntegrationTests(unittest.TestCase):
    def test_natal_keeps_all_ten_pairs_and_no_winner(self):
        from engine.natal import natal_chart
        x=natal_chart('2000-01-01','14:30','Asia/Kolkata',13.0827,80.2707,'Chennai, India')
        w=x['natal_factors']['planetary_war_coordinate_evidence']
        self.assertEqual(len(w['pairs']),10)
        self.assertEqual(w['missing_coordinate_pairs'],[])
        self.assertIsNone(w['selected_winners'])
        for pair in w['pairs']:
            for p in pair['planets']:
                self.assertEqual(pair['supplied_latitudes'][p],x['placements'][p]['ecliptic_latitude_degrees'])
        self.assertIsNone(w['adjusted_total_strength'])

    def test_missing_chart_does_not_become_no_war(self):
        from engine.planetary_war import chart_war_evidence
        x=chart_war_evidence({'Mars':{'longitude':20}},coordinate_profile='fixture')
        self.assertEqual(x['pairs'],[])
        self.assertEqual(len(x['missing_coordinate_pairs']),10)
