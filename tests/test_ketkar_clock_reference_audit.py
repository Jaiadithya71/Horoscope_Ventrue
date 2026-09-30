import unittest
from engine.ketkar_clock_reference_audit import clock_reference_audit

class ClockTests(unittest.TestCase):
 def test_no_timestamp_guessed(self):
  r=clock_reference_audit()
  self.assertTrue(r['mean_time_and_sunrise_distinguished'])
  self.assertIsNone(r['utc_dawn_timestamp'])
  self.assertIsNone(r['actual_visible_sunrise_timestamp'])
  self.assertIsNone(r['modern_timezone_selected'])
