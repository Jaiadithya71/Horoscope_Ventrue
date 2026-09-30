import unittest
from engine.lagna_house_strength_connective import lagna_house_strength_connective as gate

class LagnaStrengthConnectiveTests(unittest.TestCase):
 def test_mixed_true_link_has_disagreement_not_adverse(self):
  x=gate(True,bhava_status='strong',lord_status='weak',strength_profile='supplied')
  self.assertEqual([r['condition'] for r in x['favorable_condition_candidates']],[True,False])
  self.assertTrue(x['favorable_connective_disagreement'])
  self.assertIsNone(x['adverse_condition']);self.assertIsNone(x['personal_outcome'])
 def test_three_valued_link_and_strength(self):
  x=gate(True,bhava_status='strong',strength_profile='supplied')
  self.assertEqual([r['condition'] for r in x['favorable_condition_candidates']],[True,None])
  self.assertIsNone(x['favorable_connective_disagreement'])
  self.assertEqual([r['condition'] for r in gate(False)['favorable_condition_candidates']],[False,False])
  self.assertEqual([r['condition'] for r in gate()['favorable_condition_candidates']],[None,None])
 def test_false_flag_not_weak_status(self):
  with self.assertRaises(ValueError):gate(True,bhava_status=False,strength_profile='supplied')
  with self.assertRaises(ValueError):gate(True,bhava_status='strong')
  with self.assertRaises(ValueError):gate(1)
