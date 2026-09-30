import unittest
from engine.raman_mean_clock import raman_local_mean_clock as clock

class RamanClockTests(unittest.TestCase):
 def call(self,t,lon):return clock(t,lon,clock_kind='local_mean_solar_time',clock_profile='explicit supplied fixture')
 def test_independent1912_chain(self):
  x=self.call('1912-08-08T13:00:00',91)
  self.assertEqual(x['reference_mean_timestamp'],'1912-08-08T12:00:00')
  self.assertEqual(x['elapsed_reference_days'],'4602.5')
  from decimal import Decimal
  self.assertEqual(Decimal(x['mean_sun_table_candidates']['candidates'][0]['mean_sun_degrees']),Decimal('113.6930'))
 def test_full_longitude_correction_not_rounded_six_minutes(self):
  x=self.call('1918-10-16T14:06:16',77+35/60)
  self.assertEqual(x['reference_mean_timestamp'],'1918-10-16T13:59:56')
  self.assertIsNone(x['utc_timestamp']);self.assertIsNone(x['selected_mean_sun'])
 def test_rollover_pre_epoch_and_civil_rejection(self):
  self.assertEqual(self.call('1900-01-01T00:30:00',91)['reference_mean_timestamp'],'1899-12-31T23:30:00')
  self.assertEqual(self.call('1895-04-02T00:00:00',76)['elapsed_reference_days'],'-1735')
  with self.assertRaises(ValueError):clock('1912-08-08T13:00:00',91,clock_kind='civil_time',clock_profile='fixture')
  with self.assertRaises(ValueError):self.call('1912-08-08T13:00:00+05:30',91)
