import unittest
from engine.period_dusthana_condition import period_dusthana_condition as c,chart_period_dusthana_candidates

class DusthanaPeriodTests(unittest.TestCase):
 def flags(self,x):return [r['condition_present'] for r in x['candidates']]
 def test_mixed_owner_occupant_interpretations_stay_distinct(self):
  self.assertEqual(self.flags(c([6],1,[2],8)),[True,False])
  self.assertEqual(self.flags(c([6],1,[8],2)),[True,True])
  self.assertEqual(self.flags(c([2],6,[3],12)),[True,True])
  self.assertEqual(self.flags(c([2],1,[3],4)),[False,False])
  self.assertIsNone(c([6],1,[2],8)['personal_outcome'])
 def test_partial_three_valued_evidence(self):
  self.assertEqual(self.flags(c(None,None,[6],None)),[None,None])
  self.assertEqual(self.flags(c([],1,None,None)),[False,False])
  self.assertEqual(self.flags(c([6],None,[8],None)),[True,True])
  with self.assertRaises(ValueError):c([0],1,[2],3)
 def test_node_unknown_and_no_bhava_fallback(self):
  x=chart_period_dusthana_candidates('Aries',{'Mercury':{'whole_sign_house_from_ascendant':1},'Venus':{'whole_sign_house_from_ascendant':8}},'Mercury','Venus')
  self.assertEqual(self.flags(x['candidates'][0]['condition_evidence']),[True,False])
  self.assertEqual(self.flags(x['candidates'][1]['condition_evidence']),[None,None])
  n=chart_period_dusthana_candidates('Aries',{'Rahu':{'whole_sign_house_from_ascendant':6}},'Rahu','Mercury')
  self.assertIsNone(n['candidates'][0]['condition_evidence']['inputs']['main_owns'])
