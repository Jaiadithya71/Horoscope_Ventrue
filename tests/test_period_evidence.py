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
        self.assertIsNone(candidates[1]['source'])
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
