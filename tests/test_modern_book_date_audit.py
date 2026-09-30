import unittest
from engine.modern_book_date_audit import audit_example50

class ModernBookAuditTests(unittest.TestCase):
    def test_exact_balance_but_printed_endpoint_disagrees(self):
        x=audit_example50()
        self.assertEqual(x['balance_fraction'],'257/800')
        self.assertEqual(x['remaining_years'],'1799/800')
        self.assertEqual(x['computed_360_day_endpoint'],'2002-07-16T19:02:00-04:00')
        self.assertAlmostEqual(x['computed_minus_published_approx_hours'],24+2/60)
        self.assertIsNone(x['selected_calendar'])
        self.assertEqual(x['source_pdf_pages'],[24,222,223,224])
        self.assertIn('explicitly overrides',x['stated_nakshatra_example_year_profile'])
