import unittest
from decimal import Decimal as D
from engine.raman_daily_interpolation import raman_daily_interpolation as interp

class DailyInterpolationTests(unittest.TestCase):
 def call(self,*a,**kw):return interp(*a,ephemeris_profile='supplied fixture',clock_profile='previous Greenwich noon',frame_profile='explicit supplied precession',**kw)
 def test_printed_sun_interpolation_without_second_rounding_fit(self):
  x=self.call(D(41)+D(51)/60+D(32)/3600,(D(58)*60+11)/3600,'12.75',D(21)+D(27)/60+D(41)/3600,motion_direction='direct')
  self.assertEqual(D(x['signed_traversal_degrees']),D(3491)/3600*D('12.75')/24)
  self.assertIsNone(x['selected_historical_true_longitude'])
 def test_zero_crossing_signed_branch_and_retrograde(self):
  x=self.call(359,4,12,21,motion_direction='direct');self.assertEqual(D(x['interpolated_tropical_unwrapped_degrees']),D(361))
  y=self.call(1,4,12,21,motion_direction='retrograde');self.assertEqual(D(y['interpolated_tropical_unwrapped_degrees']),D(-1));self.assertEqual(D(y['interpolated_nirayana_normalized_degrees']),D(338))
 def test_invalid_direction_day_and_bool(self):
  for args,direction in [((0,1,25,21),'direct'),((True,1,12,21),'direct'),((0,1,12,21),'stationary')]:
   with self.assertRaises(ValueError):self.call(*args,motion_direction=direction)
