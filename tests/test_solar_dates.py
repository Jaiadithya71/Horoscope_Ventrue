import datetime as dt
import unittest
from engine.solar_dates import SolarCalendar, dated_hierarchy
from engine.forecast import swe, FLAGS, julian_day

class SolarDateTests(unittest.TestCase):
    def setUp(self):
        self.birth=dt.datetime(2000,1,1,9,tzinfo=dt.timezone.utc)
        self.cal=SolarCalendar(self.birth)

    def test_positive_negative_returns_are_solar_roots(self):
        target=swe.calc_ut(julian_day(self.birth),swe.SUN,FLAGS)[0][0]
        for n in (-4,-1,1,4,25,120):
            instant=self.cal.annual_return(n)
            actual=swe.calc_ut(julian_day(instant),swe.SUN,FLAGS)[0][0]
            self.assertLess(abs((actual-target+180)%360-180),0.000002)
            self.assertLess(abs((instant-self.birth).total_seconds()/86400-n*365.25636),4)
        self.assertEqual(self.cal.annual_return(0),self.birth)

    def test_fraction_mapping_is_monotone_and_reversible(self):
        for offset in (-3.5,0,0.2,1,3.5,24.99):
            instant=self.cal.at_offset(offset)
            self.assertAlmostEqual(self.cal.offset_at(instant),offset,places=10)
        self.assertEqual(self.cal.at_offset(0.5),self.birth+(self.cal.annual_return(1)-self.birth)/2)

    def test_birth_partial_and_half_open_major_boundary(self):
        result=dated_hierarchy(self.birth,360/54,self.birth)
        self.assertEqual(result['hierarchy'][0]['lord'],'Ketu')
        self.assertEqual(result['hierarchy'][0]['visible_start_utc_estimate'],self.birth.isoformat())
        self.assertLess(dt.datetime.fromisoformat(result['hierarchy'][0]['full_start_utc_estimate']),self.birth)
        boundary=self.cal.at_offset(3.5)
        after=dated_hierarchy(self.birth,360/54,boundary)
        self.assertEqual(after['hierarchy'][0]['lord'],'Venus')
        self.assertEqual(after['calendar_source']['pdf_page'],230)
        self.assertIn('not uniquely',after['date_limit'])
        self.assertNotIn('outcome',after)

    def test_input_rejection_and_timezone_equivalence(self):
        with self.assertRaises(ValueError):SolarCalendar(dt.datetime(2000,1,1))
        for x in (float('nan'),float('inf'),151):
            with self.assertRaises(ValueError):self.cal.at_offset(x)
        for x in (True,0.5,151):
            with self.assertRaises(ValueError):self.cal.annual_return(x)
        with self.assertRaises(ValueError):self.cal.offset_at(dt.datetime(2001,1,1))
        indian=self.birth.astimezone(dt.timezone(dt.timedelta(hours=5,minutes=30)))
        self.assertEqual(SolarCalendar(indian).annual_return(1),self.cal.annual_return(1))
