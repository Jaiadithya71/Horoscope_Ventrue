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

class AngularCalendarTests(unittest.TestCase):
    def test_root_and_inverse_not_elapsed_fraction(self):
        from engine.solar_dates import AngularSolarCalendar
        birth=dt.datetime(2000,1,1,9,tzinfo=dt.timezone.utc)
        a=AngularSolarCalendar(birth);linear=SolarCalendar(birth)
        for offset in (-2.75,-.3,0,.2,.5,1,4.81,80.125):
            instant=a.at_offset(offset)
            self.assertAlmostEqual(a.offset_at(instant),offset,places=8)
            target=(a.target+(offset%1)*360)%360
            actual=a._sun(instant)
            self.assertLess(abs((actual-target+180)%360-180),.000002)
        self.assertGreater(abs((a.at_offset(.5)-linear.at_offset(.5)).total_seconds()),3600)
        self.assertEqual(a.annual_return(1),linear.annual_return(1))

    def test_optional_profile_does_not_change_default_or_open_forecasts(self):
        birth=dt.datetime(2000,1,1,9,tzinfo=dt.timezone.utc)
        default=dated_hierarchy(birth,360/54,birth)
        angular=dated_hierarchy(birth,360/54,birth,calendar_profile='sidereal_solar_angular_progress')
        self.assertEqual(default['calendar_profile'],'elapsed_utc_return_interpolation')
        self.assertEqual(angular['calendar_profile'],'sidereal_solar_angular_progress')
        self.assertTrue(angular['modern_angular_profile_sources'])
        self.assertEqual(default['hierarchy'][0]['lord'],angular['hierarchy'][0]['lord'])
        self.assertNotIn('outcome',angular)
        with self.assertRaises(ValueError):dated_hierarchy(birth,360/54,birth,calendar_profile='unverified')

class SeparateRootRoutineChecks(unittest.TestCase):
    def test_bisection_matches_library_crossing_without_fitting(self):
        from engine.solar_dates import AngularSolarCalendar
        birth=dt.datetime(2000,1,1,9,tzinfo=dt.timezone.utc)
        a=AngularSolarCalendar(birth)
        # Separate library solver, same astronomical model. These are synthetic
        # checks, not independent ephemeris/software or empirical truth.
        for offset in (-2.75,-.3,.2,.5,4.81,80.125):
            target=(a.target+360*(offset%1))%360
            crossing=swe.solcross_ut(target,julian_day(birth)+offset*365.25636-35,FLAGS)
            bisection=julian_day(a.at_offset(offset))
            self.assertLess(abs(crossing-bisection)*86400,.1)
