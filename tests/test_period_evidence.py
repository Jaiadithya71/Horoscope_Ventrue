import datetime as dt
import unittest
from fractions import Fraction
from engine.period_evidence import period_units, lunar_traversal_evidence
from engine.forecast import swe, FLAGS, julian_day
from engine.natal import STAR_ARC

class PeriodEvidenceTests(unittest.TestCase):
    def test_exact_book_units(self):
        sun=period_units(['Sun','Sun'])
        self.assertEqual((sun['years'],sun['months'],sun['days']),(0,3,18))
        saturn=period_units(['Saturn','Mercury'])
        self.assertEqual((saturn['years'],saturn['months'],saturn['days']),(2,8,9))
        self.assertEqual(saturn['source']['pdf_page'],258)
        child=period_units(['Saturn','Mercury','Venus'])
        frac=child['exact_year_fraction']
        self.assertEqual(Fraction(frac['numerator'],frac['denominator']),Fraction(19*17*20,120*120))
        for path in ([],['Unknown'],['Sun']*4):
            with self.assertRaises(ValueError):period_units(path)

    def test_traversal_roots_and_separate_methods(self):
        birth=dt.datetime(2000,1,1,9,tzinfo=dt.timezone.utc)
        result=lunar_traversal_evidence(birth)
        entry=dt.datetime.fromisoformat(result['sector_entry_utc'])
        exit=dt.datetime.fromisoformat(result['sector_exit_utc'])
        self.assertLess(entry,birth)
        self.assertGreater(exit,birth)
        for instant,target in ((entry,(result['star_index_1_based']-1)*STAR_ARC),(exit,result['star_index_1_based']*STAR_ARC%360)):
            actual=swe.calc_ut(julian_day(instant),swe.MOON,FLAGS)[0][0]
            self.assertLess(abs((actual-target+180)%360-180),0.00003)
        self.assertNotAlmostEqual(result['total_traversal_ghatikas'],60,places=2)
        candidates=result['balance_candidates']
        self.assertNotAlmostEqual(candidates[0]['remaining_years'],candidates[1]['remaining_years'],places=3)
        self.assertNotAlmostEqual(candidates[1]['remaining_years'],candidates[2]['remaining_years'],places=5)
        self.assertEqual(result['status'],'unresolved_source_convention')
        self.assertEqual(candidates[1]['source']['pdf_page'],18)
        self.assertEqual(candidates[1]['source']['sloka'],16)
        self.assertNotIn('selected_method',result)
        self.assertNotIn('outcome',result)

    def test_wraparound_and_naive_rejection(self):
        # Find a Revati birth near a wraparound: deterministic search fixture.
        instant=dt.datetime(2000,1,1,tzinfo=dt.timezone.utc)
        for _ in range(80):
            lon=swe.calc_ut(julian_day(instant),swe.MOON,FLAGS)[0][0]%360
            if lon>=26*STAR_ARC:break
            instant+=dt.timedelta(hours=12)
        self.assertGreaterEqual(lon,26*STAR_ARC)
        result=lunar_traversal_evidence(instant)
        self.assertEqual(result['star_index_1_based'],27)
        self.assertLess(dt.datetime.fromisoformat(result['sector_entry_utc']),instant)
        self.assertGreater(dt.datetime.fromisoformat(result['sector_exit_utc']),instant)
        with self.assertRaises(ValueError):lunar_traversal_evidence(dt.datetime(2000,1,1))

class CommentaryCrossChecks(unittest.TestCase):
    def test_kapoor_worked_balance_units(self):
        # p.175 fixed-divisor example: 20 ghatikas * 16 years /60.
        self.assertEqual(Fraction(20*16,60),Fraction(16,3))
        # p.176 longitude example: Cancer 13d12m, elapsed Pushya 9d52m.
        expired=Fraction(9*60+52,13*60+20)*19
        remain=19-expired
        self.assertEqual(expired,Fraction(703,50))
        self.assertEqual(remain,Fraction(247,50))
        # Exact units: 14y 0m 21.6d expired, 4y 11m 8.4d remaining.
        self.assertEqual((expired-14)*360,Fraction(108,5))
        self.assertEqual((remain-4)*12-11,Fraction(7,25))

    def test_bphs_worked_traversal_and_printed_typo(self):
        # BPHS vol.II p.508: 58gh15pal =3495, but page prints3415.
        # Printed product24435 disagrees with both printed3415*7 and corrected3495*7.
        expired_palas=58*60+15
        total_palas=59*60+31
        self.assertEqual(expired_palas,3495)
        self.assertEqual(expired_palas*7,24465)
        self.assertNotEqual(expired_palas,3415)
        self.assertNotEqual(expired_palas*7,24435)
        remain=7-Fraction(expired_palas*7,total_palas)
        self.assertGreater(remain,0)
        self.assertLess(remain,1)

    def test_explicit_dated_methods_preserve_default_and_disagreement(self):
        from engine.solar_dates import dated_hierarchy
        birth=dt.datetime(2000,1,1,9,tzinfo=dt.timezone.utc)
        lon=swe.calc_ut(julian_day(birth),swe.MOON,FLAGS)[0][0]%360
        normal=dated_hierarchy(birth,lon,birth)
        measured=dated_hierarchy(birth,lon,birth,balance_method='normalized_actual_traversal_fraction')
        literal=dated_hierarchy(birth,lon,birth,balance_method='printed_XIX_3_fixed_60_divisor')
        self.assertEqual(normal['birth_balance_method'],'equal_sector_longitude_fraction')
        self.assertNotEqual(normal['hierarchy'][0]['end_utc_estimate'],measured['hierarchy'][0]['end_utc_estimate'])
        self.assertNotEqual(measured['hierarchy'][0]['end_utc_estimate'],literal['hierarchy'][0]['end_utc_estimate'])
        self.assertIn('birth_balance_evidence',measured)
        with self.assertRaises(ValueError):dated_hierarchy(birth,lon+1,birth,balance_method='normalized_actual_traversal_fraction')
        with self.assertRaises(ValueError):dated_hierarchy(birth,lon,birth,balance_method='unknown')
        from engine.natal import dasha_at_solar_offset
        with self.assertRaises(ValueError):dasha_at_solar_offset(0,0,initial_remaining_years=8)
