import datetime as dt
import unittest
from engine.solar_intervals import solar_interval_evidence,PROFILE

class SolarIntervalTests(unittest.TestCase):
    def test_day_night_intervals_and_thirds(self):
        utc=dt.timezone.utc
        day=solar_interval_evidence(dt.datetime(2000,1,1,9,tzinfo=utc),13.0827,80.2707,solar_event_profile=PROFILE)
        self.assertEqual(day['period'],'day')
        self.assertEqual(day['status'],'explicit_model_interval')
        start=dt.datetime.fromisoformat(day['interval_start_utc']);end=dt.datetime.fromisoformat(day['interval_end_utc'])
        self.assertLess(start,dt.datetime(2000,1,1,9,tzinfo=utc));self.assertGreater(end,dt.datetime(2000,1,1,9,tzinfo=utc))
        for fraction,lord in ((.1,'Mercury'),(.5,'Sun'),(.9,'Saturn')):
            x=solar_interval_evidence(start+(end-start)*fraction,13.0827,80.2707,solar_event_profile=PROFILE)
            self.assertEqual(x['tribhaga_evidence']['active_lord'],lord)
            self.assertEqual(x['tribhaga_evidence']['rupa_by_planet']['Jupiter'],1)
        night=solar_interval_evidence(dt.datetime(2000,1,1,18,tzinfo=utc),13.0827,80.2707,solar_event_profile=PROFILE)
        self.assertEqual(night['period'],'night')
        self.assertIsNone(night['total_strength'])

    def test_boundary_and_polar_abstain(self):
        utc=dt.timezone.utc
        d=solar_interval_evidence(dt.datetime(2000,1,1,9,tzinfo=utc),13.0827,80.2707,solar_event_profile=PROFILE)
        start=dt.datetime.fromisoformat(d['interval_start_utc']);end=dt.datetime.fromisoformat(d['interval_end_utc'])
        for t in (start,start+(end-start)/3,start+(end-start)*2/3,end):
            x=solar_interval_evidence(t,13.0827,80.2707,solar_event_profile=PROFILE)
            self.assertEqual(x['status'],'boundary_unresolved')
            self.assertIsNone(x['tribhaga_evidence'])
        x=solar_interval_evidence(dt.datetime(2000,6,21,12,tzinfo=utc),80,0,solar_event_profile=PROFILE)
        self.assertEqual(x['status'],'unavailable')
        self.assertIsNone(x['tribhaga_evidence'])

    def test_invalid_profile_clock_or_coords(self):
        t=dt.datetime(2000,1,1,tzinfo=dt.timezone.utc)
        for args in ((t,90,0,PROFILE),(t,float('nan'),0,PROFILE),(t,10,0,'guessed'),(t.replace(tzinfo=None),10,0,PROFILE)):
            with self.assertRaises(ValueError):solar_interval_evidence(args[0],args[1],args[2],solar_event_profile=args[3])
