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
