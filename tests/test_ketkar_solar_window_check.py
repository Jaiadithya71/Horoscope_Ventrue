import unittest
from engine.ketkar_solar_window_check import solar_window_check

class SolarWindowTests(unittest.TestCase):
    def test_explicit_samples_and_frame(self):
        r=solar_window_check()
        self.assertEqual(len(r['samples']),5)
        self.assertEqual(r['source_sayana_candidate_degrees'],15.007)
        self.assertAlmostEqual(r['samples'][0]['longitude_degrees'],14.96275594,places=5)
        self.assertTrue(all(x['speed_degrees_per_day']>0 for x in r['samples']))
    def test_range_not_validation(self):
        r=solar_window_check()
        self.assertTrue(r['candidate_within_sampled_range'])
        self.assertFalse(r['independent_ephemeris_validation'])
        self.assertFalse(r['exact_historical_instant_verified'])
        self.assertIsNone(r['chosen_timestamp'])
        self.assertIsNone(r['fitted_offset'])
