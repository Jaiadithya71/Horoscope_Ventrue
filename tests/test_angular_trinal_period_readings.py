import unittest
from engine.angular_trinal_period_readings import angular_trinal_period_readings as gate

class AngularTrinalReadingTests(unittest.TestCase):
 def test_unrelated_wording_retained_without_polarity_vote(self):
  x=gate('Aries','Jupiter','Saturn',related=False,evidence_profile='supplied')
  for r in x['candidates']:
   self.assertTrue(r['unrelated_pair_condition'])
   self.assertEqual([s['clause'] for s in r['unrelated_clause_readings']],['will not cause harm','productive of good effects'])
   self.assertIsNone(r['selected_effect'])
  self.assertIsNone(x['selected_translation'])
 def test_lagna_scope_remains_distinct(self):
  x=gate('Aries','Mars','Moon',related=False,evidence_profile='supplied')
  self.assertFalse(x['candidates'][0]['distinct_pair_ownership_condition'])
  self.assertTrue(x['candidates'][1]['distinct_pair_ownership_condition'])
 def test_unknown_relation_self_nodes(self):
  self.assertIsNone(gate('Aries','Jupiter','Saturn')['candidates'][0]['unrelated_pair_condition'])
  for pair in [('Mars','Mars'),('Rahu','Ketu')]:
   self.assertTrue(all(r['distinct_pair_ownership_condition'] is None for r in gate('Aries',*pair)['candidates']))

 def test_crosscheck_is_not_translation_winner(self):
  x=gate('Aries','Jupiter','Saturn')
  self.assertTrue(x['sanskrit_crosscheck']['negative_harm_wording_corroborated'])
  self.assertFalse(x['sanskrit_crosscheck']['independent_translation_vote'])
  self.assertIsNone(x['sanskrit_crosscheck']['critical_edition_arbitration'])
  self.assertIsNone(x['selected_translation'])
