import unittest
from engine.ketkar_solar_example_reconstruction import reconstruct_solar_example

class SolarReconstructionTests(unittest.TestCase):
 def test_composed_fixture_and_caveats(self):
  r=reconstruct_solar_example()
  self.assertTrue(r['apsis_arithmetic_matches'])
  self.assertTrue(r['longitude_matches_at_printed_precision'])
  self.assertEqual(r['candidate_manda_radius'],'1000.7')
  self.assertFalse(r['table_inputs_reconstructed_from_year_alone'])
  self.assertIsNone(r['utc_dawn_timestamp']);self.assertIsNone(r['outcome_accuracy'])
