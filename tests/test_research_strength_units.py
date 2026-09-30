import json,unittest
from pathlib import Path
from engine.research_input_report import research_input_report as report

class ResearchStrengthUnitTests(unittest.TestCase):
 def fixture(self):return json.loads((Path(__file__).parents[1]/'profiles/research/synthetic-strength-input.json').read_text())
 def test_layout_units_separate_and_incomplete_not_zero(self):
  x=report(**self.fixture());sun,moon=x['supplied_strength_evidence']
  self.assertEqual(sun['input_unit'],'virupa');self.assertEqual(moon['input_unit'],'rupa')
  self.assertTrue(sun['unit_explicitly_declared']);self.assertFalse(sun['unit_conversion_applied'])
  self.assertEqual(sun['evidence']['candidate_sum_virupa'],'160')
  self.assertIsNone(moon['evidence']['supplied_base_sum_rupa'])
  self.assertIn('kala',moon['evidence']['missing_base_components']);self.assertIsNone(x['selected_complete_strength'])
 def test_wrong_or_unknown_units_rejected(self):
  for unit in ('rupa','seconds',None):
   f=self.fixture();f['supplied_strength']['Sun']['unit']=unit
   with self.assertRaises(ValueError):report(**f)
 def test_legacy_units_explicitly_marked_not_converted(self):
  f=self.fixture();del f['supplied_strength']['Sun']['unit']
  x=report(**f)['supplied_strength_evidence'][0]
  self.assertFalse(x['unit_explicitly_declared']);self.assertEqual(x['unit_origin'],'legacy source-layout contract')
