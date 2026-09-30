import unittest
import datetime as dt
from engine.convention_condition_report import convention_condition_report
from engine.natal import birth_utc,natal_chart

class ConventionConditionReportTests(unittest.TestCase):
 def test_nine_profiles_route_without_false_prediction(self):
  n=natal_chart('2000-01-01','14:30','Asia/Kolkata',13.08,80.27,'synthetic fixture')
  b=birth_utc('2000-01-01','14:30','Asia/Kolkata')
  x=convention_condition_report(b,dt.datetime(2026,1,1,tzinfo=dt.timezone.utc),n['ascendant']['sign'],n['placements'])
  self.assertEqual(len(x['profile_condition_routes']),9)
  keys={r['key']:r['evidence'] for r in x['distinct_pair_conditions']}
  for r in x['profile_condition_routes']:
   if r['lord_path'] is not None:
    self.assertEqual(r['condition_lord_pair'],r['lord_path'][:2])
    e=keys[r['condition_evidence_key']]
    self.assertEqual([e['main_lord'],e['sub_lord']],r['condition_lord_pair'])
    self.assertIsNone(e['personal_outcome'])
   else:self.assertIsNone(r['condition_evidence_key'])
  self.assertIsNone(x['personal_outcome']);self.assertIsNone(x['selected_profile'])
  self.assertIsNone(x['global_precedence'])
 def test_query_before_birth_does_not_route_invalid_profiles(self):
  b=birth_utc('2000-01-01','14:30','Asia/Kolkata')
  x=convention_condition_report(b,b-dt.timedelta(days=1),'Aries',{})
  self.assertEqual(x['distinct_pair_conditions'],[])
  self.assertTrue(all(r['condition_evidence_key'] is None for r in x['profile_condition_routes']))
