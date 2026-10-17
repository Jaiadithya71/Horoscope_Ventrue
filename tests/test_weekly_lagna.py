"""Weekly-by-lagna report shape and honesty gates, not astronomical truth fixtures."""
import datetime as dt
import json
import unittest

from engine.forecast import SIGNS
from engine.weekly_lagna import weekly_lagna_report, week_bounds_ist, RULES


class WeekBoundsTests(unittest.TestCase):
    def test_any_day_resolves_to_its_monday_ist_week(self):
        start, end = week_bounds_ist(dt.date(2026, 10, 18))  # a Sunday
        self.assertEqual((start + dt.timedelta(hours=5, minutes=30)).strftime('%Y-%m-%d %H:%M'), '2026-10-12 00:00')
        self.assertEqual((end + dt.timedelta(hours=5, minutes=30)).strftime('%Y-%m-%d %H:%M'), '2026-10-19 00:00')
        self.assertEqual((end - start).days, 7)

    def test_monday_resolves_to_itself(self):
        start, _ = week_bounds_ist(dt.date(2026, 10, 19))
        self.assertEqual((start + dt.timedelta(hours=5, minutes=30)).date().isoformat(), '2026-10-19')


class WeeklyReportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = weekly_lagna_report(dt.date(2026, 10, 15), 'Capricorn')

    def test_report_shape(self):
        r = self.report
        self.assertEqual(r['lagna'], 'Capricorn')
        self.assertEqual(len(r['day_dates_ist']), 7)
        self.assertEqual(set(r['placements']), {'Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Rahu', 'Ketu'})
        for p, v in r['placements'].items():
            self.assertEqual(len(v['signs_by_day']), 8, p)
            self.assertEqual(len(v['houses_from_lagna_by_day']), 8, p)
            for s, h in zip(v['signs_by_day'], v['houses_from_lagna_by_day']):
                self.assertIn(s, SIGNS)
                self.assertTrue(1 <= h <= 12)
                # House 1 from lagna exactly when the planet sits in the lagna sign.
                self.assertEqual(h == 1, s == 'Capricorn')
        self.assertIsNone(r['moon_findings'])
        for key in ('model', 'notice', 'sampling'):
            self.assertIsInstance(r[key], str)

    def test_ketu_is_derived_geometry_opposite_rahu(self):
        ketu, rahu = self.report['placements']['Ketu'], self.report['placements']['Rahu']
        self.assertIn('derived', ketu)
        for ks, rs in zip(ketu['signs_by_day'], rahu['signs_by_day']):
            self.assertEqual((SIGNS.index(ks) - SIGNS.index(rs)) % 12, 6)

    def test_events_inside_week_and_sorted(self):
        r = self.report
        times = [e['at_utc'] for e in r['events']]
        self.assertEqual(times, sorted(times))
        for e in r['events']:
            self.assertIn(e['kind'], ('sign_ingress', 'station_retrograde', 'station_direct'))
            at = dt.datetime.fromisoformat(e['at_utc'])
            self.assertTrue(dt.datetime.fromisoformat(r['week_start_ist'] + 'T00:00:00+05:30') <= at.replace(tzinfo=dt.timezone.utc).astimezone(dt.timezone.utc)
                            <= dt.datetime.fromisoformat(r['week_end_ist_exclusive'] + 'T00:00:00+05:30').astimezone(dt.timezone.utc))
        ingresses = [e for e in r['events'] if e['kind'] == 'sign_ingress']
        self.assertTrue(any(e['planet'] == 'Moon' for e in ingresses))  # the Moon always changes sign in a week

    def test_ingress_signs_match_daily_samples(self):
        r = self.report
        for e in r['events']:
            if e['kind'] != 'sign_ingress':
                continue
            signs = r['placements'][e['planet']]['signs_by_day']
            self.assertIn(e['from_sign'], signs)
            self.assertIn(e['to_sign'], signs)
            self.assertNotEqual(e['from_sign'], e['to_sign'])

    def test_structural_factors_cited(self):
        s = self.report['structural_factors_from_lagna']
        self.assertEqual(s['reference_sign'], 'Capricorn')
        self.assertEqual(len(s['lordships']['houses']), 12)
        self.assertTrue(s['lordships']['source']['verified_against_page_image'])

    def test_deterministic(self):
        again = weekly_lagna_report(dt.date(2026, 10, 15), 'Capricorn')
        self.assertEqual(json.dumps(self.report, sort_keys=True), json.dumps(again, sort_keys=True))


class MoonFindingsTests(unittest.TestCase):
    def test_findings_only_with_moon_sign_and_cited(self):
        with_findings = weekly_lagna_report(dt.date(2026, 10, 15), 'Aries', 'Gemini')
        self.assertIsInstance(with_findings['moon_findings'], list)
        for f in with_findings['moon_findings']:
            self.assertTrue(f['source']['verified_against_page_image'])
            self.assertEqual(f['source']['chapter'], 'XXVI')
            self.assertTrue(1 <= len(f['active_days']) <= 7)
        rule_ids = {f['rule_id'] for f in with_findings['moon_findings']}
        self.assertTrue(rule_ids <= {r['id'] for r in RULES})

    def test_unknown_signs_rejected(self):
        with self.assertRaises(ValueError):
            weekly_lagna_report(dt.date(2026, 10, 15), 'Capricornus')
        with self.assertRaises(ValueError):
            weekly_lagna_report(dt.date(2026, 10, 15), 'Aries', 'Taurusx')


if __name__ == '__main__':
    unittest.main()
