import unittest
from engine.dated_example_audit import secondary_example_audit

class DatedExampleAuditTests(unittest.TestCase):
    def test_source_arithmetic_does_not_authenticate_dates(self):
        x=secondary_example_audit();time,longitude=x['rows']
        self.assertAlmostEqual(time['elapsed_fraction'],.5463158976466961)
        self.assertEqual(longitude['elapsed_fraction'],.54625)
        self.assertLess(time['remaining_years'],longitude['remaining_years'])
        self.assertTrue(x['same_monotone_calendar_order_conflict'])
        self.assertNotAlmostEqual(time['implied_fixed_days_per_year'],longitude['implied_fixed_days_per_year'],places=2)
        self.assertLess(longitude['published_minus_computed_hours'],-16)
        self.assertIsNone(x['adopted_calendar_profile'])
