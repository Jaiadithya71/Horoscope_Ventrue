import unittest
from engine.historical_declination import historical_declination,historical_ayana_from_longitude

class HistoricalDeclinationTests(unittest.TestCase):
    def test_table_knots_and_four_quadrants(self):
        cumulative=(0,362,703,1002,1238,1388,1440)
        for i,minutes in enumerate(cumulative):
            a=i*15
            self.assertAlmostEqual(historical_declination(a)['declination_degrees'],minutes/60)
            self.assertAlmostEqual(historical_declination(180-a)['declination_degrees'],minutes/60)
            self.assertAlmostEqual(historical_declination(180+a if a else 180)['declination_degrees'],-minutes/60)
            if a:self.assertAlmostEqual(historical_declination(360-a)['declination_degrees'],-minutes/60)

    def test_original_sun_worked_arithmetic(self):
        # PDF67 Sun0-17-43-30 + ayanamsa0-21-47-38 =39-31-08.
        t=17+43/60+30/3600 +21+47/60+38/3600
        x=historical_ayana_from_longitude('Sun',t,longitude_profile='PDF67 input')
        d=x['historical_declination']['declination_degrees']
        self.assertAlmostEqual(d*60,703+(9+31/60+8/3600)/15*299)
        # Printed892.737 differs by.006185 arcminutes, not exact arithmetic.
        self.assertAlmostEqual(d*60,892.737,delta=.007)
        rows=x['ayana_candidates']['candidates']
        self.assertAlmostEqual(rows[0]['rupa'],.8099,delta=.0001)
        self.assertAlmostEqual(rows[1]['rupa'],rows[0]['rupa']*2)
        self.assertIsNone(x['total_strength'])

    def test_bad_and_unprofiled(self):
        for bad in (-1,360,float('inf'),float('nan')):
            with self.assertRaises(ValueError):historical_declination(bad)
        with self.assertRaises(ValueError):historical_ayana_from_longitude('Sun',20,longitude_profile='')
