import unittest
from engine.calendar_benchmark import run_benchmark

class CalendarBenchmarkTests(unittest.TestCase):
    def test_seven_published_complete_boundaries(self):
        result=run_benchmark()
        self.assertEqual(result['fixed_profile_date_matches'],7)
        self.assertEqual(result['return_profile_date_matches'],3)
        self.assertEqual(len(result['rows']),7)
        self.assertEqual(result['rows'][3]['published_local_end_date'],'2032-04-01')
        self.assertEqual(result['rows'][3]['solar_return_local_end_date'],'2032-04-02')
        self.assertEqual(result['source_pdf_pages'],[3,4,5])
        self.assertIn('Not an exact-time reference',result['notice'])
        self.assertNotIn('prediction_accuracy',result)

    def test_estimate_spread_not_exact_reference(self):
        import datetime as dt
        result=run_benchmark()
        self.assertFalse(result['exact_reference_times_available'])
        self.assertTrue(result['calendar_profiles_are_not_interchangeable'])
        for r in result['rows']:
            seconds=(dt.datetime.fromisoformat(r['solar_return_utc_estimate'])-dt.datetime.fromisoformat(r['fixed_365_25_utc_estimate'])).total_seconds()
            self.assertAlmostEqual(r['return_minus_fixed_hours'],seconds/3600)
        self.assertGreater(result['rows'][-1]['return_minus_fixed_hours'],10)

class AngularBenchmarkTests(unittest.TestCase):
    def test_explicit_angular_profile_exposes_not_fits_spread(self):
        import datetime as dt
        x=run_benchmark()
        self.assertEqual(x['angular_profile_date_matches'],sum(r['angular_profile_match'] for r in x['rows']))
        self.assertFalse(x['exact_reference_times_available'])
        for r in x['rows']:
            seconds=(dt.datetime.fromisoformat(r['angular_solar_utc_estimate'])-dt.datetime.fromisoformat(r['solar_return_utc_estimate'])).total_seconds()
            self.assertAlmostEqual(seconds/3600,r['angular_minus_elapsed_return_hours'])
        self.assertGreater(max(abs(r['angular_minus_elapsed_return_hours']) for r in x['rows']),24)
