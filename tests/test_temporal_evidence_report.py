import unittest
import datetime as dt
from engine.temporal_evidence_report import temporal_evidence_report as t
from engine.solar_meridian_clock import PROFILE as MERIDIAN
from engine.solar_intervals import PROFILE as SOLAR

class TemporalReportTests(unittest.TestCase):
 def test_missing_epoch_not_gregorian_default(self):
  x=t(dt.datetime(2000,1,1,9,tzinfo=dt.timezone.utc),13.08,80.27,{'Sun':{'longitude':256}},10,
      solar_event_profile=SOLAR,meridian_profile=MERIDIAN)
  self.assertIsNone(x['supplied_historical_day_evidence']);self.assertIsNone(x['positional_hora_candidates'])
  self.assertIsNone(x['total_temporal_strength']);self.assertIsNone(x['selected_temporal_profile'])
  self.assertIsNone(x['temporal_lord_component_candidates'][0]['components']['supplied_lords']['year'])
 def test_supplied_epoch_keeps_hora_candidates_and_no_summing(self):
  counts={'elapsed_creation_solar_years':1955884954,'elapsed_solar_months':0,'elapsed_lunar_days':21,'epoch_profile':'printed fixture not modern birth match'}
  x=t(dt.datetime(2000,1,1,9,tzinfo=dt.timezone.utc),13.08,80.27,{'Sun':{'longitude':17+43/60+30/3600}},14+31/60+46/3600,
      solar_event_profile=SOLAR,meridian_profile=MERIDIAN,historical_inputs=counts)
  self.assertEqual(x['supplied_historical_day_evidence']['lord_evidence']['lords']['year'],'Jupiter')
  self.assertEqual(len(x['temporal_lord_component_candidates']),2)
  self.assertEqual({v['components']['supplied_lords']['hora'] for v in x['temporal_lord_component_candidates']},{'Moon','Mercury'})
  self.assertIsNone(x['total_strength']);self.assertIsNone(x['total_temporal_strength'])
  with self.assertRaises(ValueError):t(dt.datetime(2000,1,1,9,tzinfo=dt.timezone.utc),13.08,80.27,{},None,
      solar_event_profile=SOLAR,meridian_profile=MERIDIAN,historical_inputs={})
