import unittest
from engine.research_input_report import period_input_coverage,research_input_report
from test_research_input_report import BIRTH

class PeriodCoverageTests(unittest.TestCase):
 def test_missing_node_is_unknown_not_absent_rule(self):
  x=period_input_coverage({'Rahu':{'sign':'Aries','longitude':1}},'Ketu','Rahu')
  ketu,rahu=x['rows'];self.assertFalse(ketu['placement_present'])
  self.assertIn('longitude',ketu['missing_placement_fields'])
  self.assertFalse(rahu['node_ownership_dignity_strength_applicability_verified'])
  self.assertFalse(x['complete_period_evidence'])
 def test_integrated_node_pair_missingness_visible(self):
  x=research_input_report(BIRTH,period_pair={'main_lord':'Ketu','sub_lord':'Rahu'})
  c=x['explicit_pair_input_coverage']['rows'];self.assertEqual(c[0]['lord'],'Ketu')
  self.assertFalse(c[0]['placement_present']);self.assertTrue(c[1]['placement_present'])
  self.assertIsNone(x['global_outcome'])
 def test_classical_coverage_does_not_certify_full_conditions(self):
  x=research_input_report(BIRTH,period_pair={'main_lord':'Sun','sub_lord':'Moon'})
  for row in x['explicit_pair_input_coverage']['rows']:
   self.assertTrue(row['placement_present']);self.assertFalse(row['all_period_conditions_evaluable'])
  self.assertEqual(x['query_pair_input_coverage'],[])
