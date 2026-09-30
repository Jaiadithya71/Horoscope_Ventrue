import json,unittest
from engine.research_input_report import research_input_report as report

BIRTH={'date':'2000-01-01','time':'14:30','timezone':'Asia/Kolkata','latitude':13.0,'longitude':80.0,'place':'synthetic test coordinates'}

class ResearchInputTests(unittest.TestCase):
 def test_birth_only_and_explicit_pair_no_active_selection(self):
  x=report(BIRTH);json.dumps(x);self.assertIsNone(x['explicit_period_pair_evidence'])
  y=report(BIRTH,period_pair={'main_lord':'Jupiter','sub_lord':'Mercury'})
  self.assertEqual(y['explicit_period_pair_evidence']['main_lord'],'Jupiter');self.assertFalse(y['active_period_inferred'])
  self.assertIsNone(y['global_outcome']);self.assertIsNone(y['selected_calendar_profile'])
 def test_source_arithmetic_does_not_certify_chart_or_flags(self):
  entry={'source_layout':'raman_art121_ayana_in_kala','components':{'sthana':100,'dig':20,'kala_including_ayana':30,'chesta_excluding_ayana':10,'natural':5,'signed_drik':-5},'declared_complete':True,'component_profile':'synthetic test declaration','war_treatment':'confirmed_no_war'}
  x=report(BIRTH,supplied_strength={'Sun':entry});e=x['supplied_strength_evidence'][0]
  self.assertEqual(e['evidence']['candidate_sum_virupa'],'160')
  self.assertFalse(e['chart_identity_match_verified']);self.assertFalse(e['converted_to_condition_strength_flag'])
  self.assertIsNone(x['selected_complete_strength'])
 def test_unknown_layout_unsupported_and_extra_input_rejected(self):
  for strength in [{'Sun':{'source_layout':'default'}},{'Rahu':{}}]:
   with self.assertRaises(ValueError):report(BIRTH,supplied_strength=strength)
  with self.assertRaises(ValueError):report({**BIRTH,'guess_time':True})
