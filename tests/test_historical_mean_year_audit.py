import unittest
from fractions import Fraction
from engine.historical_mean_year_audit import historical_mean_year_audit

class HistoricalMeanYearTests(unittest.TestCase):
 def test_different_source_constants_not_silent_return_truth(self):
  x=historical_mean_year_audit()
  self.assertEqual(x['solar_year_yuga_ratio'],str(Fraction(1577917828,4320000)))
  self.assertTrue(x['rule_says_mean_sun']);self.assertFalse(x['exact_endpoint_verified'])
  self.assertIsNone(x['selected_calendar'])
  self.assertAlmostEqual(x['summary_reported_day_addition_minus_printed_seconds'],27.84,places=2)
  rows={r['profile']:r for r in x['calendar_comparisons']}
  self.assertEqual(rows['VII20_yuga_ratio_mean_year']['local_clock_endpoint'],'1903-01-07T00:06:18.176632')
  self.assertGreater(rows['VII20_yuga_ratio_mean_year']['computed_minus_printed_seconds'],10000)
  self.assertLess(abs(rows['summary_approximate_mean_year']['computed_minus_printed_seconds']),60)
