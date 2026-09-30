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

class RelationManifestationBridgeTests(unittest.TestCase):
 def test_candidate_true_without_selected_manifestation(self):
  x=period_condition_report('Aries',{'Mars':{'sign':'Libra'},'Venus':{'sign':'Aries'}},'Mars','Venus')
  rows=x['xx44_relation_conditioned_candidates']
  self.assertEqual(len(rows),2)
  self.assertTrue(all(r['condition_evidence']['xx44_supplied_activation_condition'] for r in rows))
  self.assertTrue(all(r['condition_evidence']['selected_personal_effect'] is None for r in rows))
  self.assertIsNone(x['xv30_lord_connection_candidates']['selected_related'])
 def test_no_relation_does_not_clear_unknown_circumstance(self):
  x=period_condition_report('Aries',{'Sun':{'sign':'Aries'},'Moon':{'sign':'Taurus'}},'Sun','Moon')
  self.assertTrue(all(r['condition_evidence']['xx44_supplied_activation_condition'] is None for r in x['xx44_relation_conditioned_candidates']))
 def test_self_does_not_activate(self):
  x=period_condition_report('Aries',{'Mars':{'sign':'Aries'}},'Mars','Mars')
  self.assertTrue(all(r['condition_evidence']['xx44_supplied_activation_condition'] is None for r in x['xx44_relation_conditioned_candidates']))
