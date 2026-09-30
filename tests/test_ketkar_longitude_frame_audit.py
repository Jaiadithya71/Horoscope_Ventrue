import unittest
from engine.ketkar_longitude_frame_audit import longitude_frame_audit

class FrameTests(unittest.TestCase):
 def test_offset_and_wrap(self):
  r=longitude_frame_audit()
  self.assertEqual(r['computed_ayanamsa_degrees'],'22.840')
  self.assertTrue(r['mars_frame_bridge_matches'])
  self.assertEqual(r['source_sayana_solar_candidate_degrees'],'15.007')
  self.assertIsNone(r['utc_dawn_timestamp']);self.assertIsNone(r['independent_ephemeris_agreement'])
