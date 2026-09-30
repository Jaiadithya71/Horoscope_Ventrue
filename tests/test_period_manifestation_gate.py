import unittest
from engine.period_manifestation_gate import period_manifestation_gate as gate
from engine.period_condition_report import period_condition_report

class ManifestationGateTests(unittest.TestCase):
 def test_own_subperiod_not_auto_house_effect_or_no_effect(self):
  x=gate('Jupiter','Jupiter')
  self.assertTrue(x['same_lord_pair'])
  self.assertFalse(x['automatic_owned_house_effect_from_same_lord_pair'])
  self.assertIsNone(x['xx44_supplied_activation_condition'])
  self.assertIsNone(x['selected_personal_effect'])
 def test_distinct_supplied_evidence_unknowns(self):
  self.assertIsNone(gate('Jupiter','Mercury')['xx44_supplied_activation_condition'])
  self.assertTrue(gate('Jupiter','Mercury',related=True,evidence_profile='supplied')['xx44_supplied_activation_condition'])
  self.assertFalse(gate('Jupiter','Mercury',related=False,similarly_circumstanced=False,evidence_profile='supplied')['xx44_supplied_activation_condition'])
 def test_truthy_rejected_and_report_retains_scope(self):
  with self.assertRaises(ValueError):gate('Sun','Moon',related=1,evidence_profile='supplied')
  x=period_condition_report('Aries',{},'Sun','Sun')
  self.assertIsNone(x['xx43_44_manifestation_conditions']['selected_personal_effect'])
  self.assertIsNone(x['global_precedence'])
