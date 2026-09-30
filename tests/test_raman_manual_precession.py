import unittest
from fractions import Fraction as F
from engine.raman_manual_precession import raman_manual_year_precession as calc,raman_manual_precession_audit as audit

class ManualPrecessionTests(unittest.TestCase):
 def test_printed_years_and_rate(self):
  self.assertEqual(F(calc(1912)['precession_arcseconds_rational']),76255)
  self.assertEqual(F(calc(1918)['precession_arcseconds_rational']),76557)
  self.assertEqual(F(calc(1932)['precession_arcseconds_rational']),F(231785,3))
  self.assertEqual(F(calc(1933)['precession_arcseconds_rational'])-F(calc(1932)['precession_arcseconds_rational']),F(151,3))
 def test_year_only_no_identity_or_moon_fit(self):
  a=audit();self.assertEqual(a['rows'][2]['exact_minus_printed_arcseconds_rational'],'2/3')
  self.assertFalse(a['illustrated_1932_moon_aya_comparison']['printed_moon_output_explained'])
  self.assertIsNone(calc(1932)['selected_modern_ayanamsa']);self.assertIsNone(calc(1932)['odd_day_correction'])
  self.assertIsNone(a['selected_chart_frame'])
 def test_invalid_years(self):
  for year in [True,1932.5,'1932',396]:
   with self.assertRaises(ValueError):calc(year)
