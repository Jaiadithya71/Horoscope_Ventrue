import unittest
from engine.period_context_requirements import period_context_requirements
from engine.period_condition_report import period_condition_report

class PeriodContextTests(unittest.TestCase):
 def test_references_not_global_composition_rule(self):
  x=period_context_requirements()
  self.assertEqual(len(x['referenced_contexts']),6)
  self.assertFalse(x['all_referenced_rules_implemented'])
  self.assertIsNone(x['global_composition_order']);self.assertIsNone(x['personal_outcome'])
 def test_runnable_report_does_not_claim_all_context(self):
  x=period_condition_report('Aries',{},'Sun','Moon')
  self.assertFalse(x['xx21_context_requirements']['all_referenced_rules_implemented'])
  self.assertIsNone(x['global_precedence'])
