import unittest
from engine.historical_day_count import historical_day_count as h

class HistoricalDayTests(unittest.TestCase):
 def test_printed_recipe_from_inputs_to_lords(self):
  x=h(1955884954,0,21,epoch_profile='Sripati printed creation-year fixture')
  self.assertEqual(x['additive_months_floor'],721384701)
  self.assertEqual(x['lunar_days'],725760124491)
  self.assertEqual(x['subtractive_days_floor'],11356018356)
  self.assertEqual(x['terrestrial_days'],714404106135)
  self.assertEqual(x['lord_evidence']['lords'],{'year':'Jupiter','month':'Venus','weekday':'Venus'})
  self.assertIsNone(x['modern_date_conversion']);self.assertIsNone(x['total_temporal_strength'])
 def test_no_invented_epoch_and_integer_residual_bounds(self):
  for y,m,d in [(True,0,0),(1,12,0),(1,0,30),(-1,0,0),(1,1.5,0)]:
   with self.assertRaises(ValueError):h(y,m,d,epoch_profile='fixture')
  with self.assertRaises(ValueError):h(1,0,0,epoch_profile='')
