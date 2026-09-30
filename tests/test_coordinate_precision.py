import datetime as dt
import unittest
from unittest.mock import patch
from engine.forecast import position,forecast
from engine.transit_phase import transit_phase
from engine.vargas import six_vargas

class CoordinatePrecisionTests(unittest.TestCase):
    def test_display_rounding_never_changes_decision_input(self):
        instant=dt.datetime(2000,1,1,tzinfo=dt.timezone.utc)
        for lon in (9.999999,19.999999,29.999999,359.999999):
            with patch('engine.forecast.swe.calc_ut',return_value=((lon,0,1,1,0,0),0)):
                p=position(instant,'Sun')
            self.assertEqual(p['longitude'],lon)
            self.assertNotEqual(p['longitude_display_5dp'],lon)
            self.assertEqual(p['sign'],('Pisces' if lon>330 else 'Aries'))
            self.assertFalse(transit_phase('Sun',p['longitude'])['boundary_unresolved'])
            self.assertEqual(six_vargas(p['longitude'])['vargas'][0]['sign'],p['sign'])

    def test_forecast_uses_unrounded_value(self):
        with patch('engine.forecast.swe.calc_ut',return_value=((9.999999,0,1,1,0,0),0)):
            p=forecast('2000-01-01','Aries',('Sun',))['placements']['Sun']
        self.assertTrue(p['transit_phase_evidence']['active_condition'])
        self.assertEqual(p['longitude_display_5dp'],10)
