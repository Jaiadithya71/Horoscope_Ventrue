import unittest
from engine.angular_trinal_pair_conditions import angular_trinal_pair_conditions as gate

class AngularTrinalTests(unittest.TestCase):
 def test_aries_saturn_jupiter_roles_and_unknown_strength(self):
  x=gate('Aries','Saturn','Jupiter',related=True,evidence_profile='supplied')
  r=x['candidates'][0]
  self.assertTrue(r['xx45_related_pair_condition'])
  self.assertIsNone(r['xx46_related_strong_kendra_condition'])
  self.assertEqual(r['extra_dusthana_ownership'],[12])
  self.assertIsNone(x['personal_outcome'])
 def test_relation_false_not_unknown_strength_override(self):
  x=gate('Aries','Saturn','Jupiter',related=False,evidence_profile='supplied')
  self.assertFalse(x['candidates'][0]['xx46_related_strong_kendra_condition'])
 def test_self_and_nodes_not_auto_relation(self):
  self.assertTrue(all(r['xx45_related_pair_condition'] is None for r in gate('Taurus','Saturn','Saturn')['candidates']))
  self.assertTrue(all(r['ownership_pair_condition'] is None for r in gate('Aries','Rahu','Ketu')['candidates']))
