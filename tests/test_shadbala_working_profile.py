import unittest
from engine.forecast import swe, julian_day
import datetime as dt
from engine import shadbala_working_profile as w
from engine.natal import natal_chart
from engine.solar_meridian_clock import PROFILE as M
from engine.solar_intervals import PROFILE as S

# Sripati III p55 printed worked table: (declination degrees, rupa)
PRINTED_AYANA = {'Sun': (14.877, .810), 'Moon': (-18.984, .895), 'Mars': (7.806, .662),
                 'Mercury': (6.420, .633), 'Jupiter': (-23.607, .008), 'Venus': (13.657, .784),
                 'Saturn': (17.938, .126)}


class ShadbalaWorkingProfileTests(unittest.TestCase):
    def test_minima_match_sripati_p66(self):
        self.assertEqual(w.MINIMUM_VIRUPA, {'Sun': 390, 'Moon': 360, 'Mars': 300, 'Mercury': 420,
                                            'Jupiter': 390, 'Venus': 330, 'Saturn': 300})

    def test_ayana_rule_recomputes_printed_table(self):
        for planet, (dec, printed) in PRINTED_AYANA.items():
            self.assertAlmostEqual(w._ayana_rupa(planet, dec), printed, delta=.0015, msg=planet)

    def test_cheshta_opposition_is_full_and_conjunction_is_empty(self):
        # outer planet: true longitude opposite the mean Sun -> kendra 180 -> 1 Rupa
        r = w.cheshtabala_modern_mean('Mars', 100.0, 280.0 + 0.0, {'Mars': 100.0}, 0.0)
        self.assertAlmostEqual(r['rupa'], 1.0, places=6)
        r = w.cheshtabala_modern_mean('Mars', 100.0, 100.0, {'Mars': 100.0}, 0.0)
        self.assertAlmostEqual(r['rupa'], 0.0, places=6)

    def test_mean_helio_stand_in_stays_within_equation_of_centre(self):
        bound = {'Mercury': 24, 'Venus': 2, 'Mars': 12, 'Jupiter': 6, 'Saturn': 8}
        for year in (1950, 1975, 1990, 2010, 2024):
            jd = julian_day(dt.datetime(year, 3, 1, tzinfo=dt.timezone.utc))
            t = (jd - 2451545.0) / 36525
            for p, (a, b) in w.MEAN_HELIO.items():
                true = swe.calc_ut(jd, w.SWE[p], swe.FLG_MOSEPH | swe.FLG_HELCTR)[0][0]
                diff = abs(w._wrap180(true - (a + b * t)))
                self.assertLess(diff, bound[p] + 1, (year, p, diff))

    def test_chart_profile_is_interval_valued_and_never_one_number(self):
        c = natal_chart('1990-05-15', '10:30:00', 'Asia/Calcutta', 13.08, 80.27, 'Chennai',
                        solar_event_profile=S, meridian_profile=M)
        r = w.shadbala_working_profile(c, timezone='Asia/Calcutta')
        self.assertEqual(r['weekday_lord'], 'Mars')  # Tuesday 15 May 1990
        ok = {'meets_sripati_minimum_in_all_variants', 'below_sripati_minimum_in_all_variants',
              'unresolved_across_variants', 'unresolved_planetary_war'}
        for p, row in r['planets'].items():
            lo, hi = row['total_rupa_interval']
            self.assertLessEqual(lo, hi)
            self.assertIn(row['verdict'], ok)
            self.assertNotIn('total_rupa', row)
            if row['verdict'] == 'meets_sripati_minimum_in_all_variants':
                self.assertGreaterEqual(lo, row['minimum_rupa'])
        self.assertEqual(len(r['planets']), 7)


if __name__ == '__main__':
    unittest.main()
