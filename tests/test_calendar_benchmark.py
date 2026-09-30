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
