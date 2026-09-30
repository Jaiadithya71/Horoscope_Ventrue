import datetime as dt
import unittest
from engine.calendar_comparison import compare_conventions,CALENDARS,BALANCES

class ComparisonTests(unittest.TestCase):
    def test_nine_named_choices_and_disagreement(self):
        birth=dt.datetime(2000,1,1,9,tzinfo=dt.timezone.utc)
        x=compare_conventions(birth,dt.datetime(2026,1,1,tzinfo=dt.timezone.utc))
        self.assertEqual(len(x['comparison_rows']),9)
        self.assertEqual({(r['calendar_profile'],r['balance_method']) for r in x['comparison_rows']},
                         {(c,b) for c in CALENDARS for b in BALANCES})
        self.assertEqual(x['invalid_combinations'],0)
        self.assertIsNone(x['selected_profile'])
        self.assertTrue(x['distinct_computed_lord_paths'])
        self.assertNotIn('outcome',x)
        for r in x['comparison_rows']:
            self.assertEqual(len(r['hierarchy']),3)
            self.assertTrue(r['calendar_source'])

    def test_before_birth_stays_invalid_not_fallback(self):
        birth=dt.datetime(2000,1,1,9,tzinfo=dt.timezone.utc)
        x=compare_conventions(birth,birth-dt.timedelta(days=1))
        self.assertEqual(x['invalid_combinations'],9)
        self.assertIsNone(x['lord_path_agreement'])
        self.assertEqual(x['distinct_computed_lord_paths'],[])
        self.assertTrue(all(r['hierarchy'] is None for r in x['comparison_rows']))
