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

class ChartLagnaStrengthTests(unittest.TestCase):
 def test_link_geometry_and_flags_separate(self):
  from engine.lagna_house_strength_connective import chart_lagna_strength_candidates as chart
  x=chart(7,'Aries',{'Mars':{'sign':'Libra'},'Venus':{'sign':'Virgo'}},bhava_strong=True,lord_strong=False,strength_profile='supplied')
  a,b=x['candidates']
  self.assertTrue(a['occupation_matches_target'])
  self.assertIsNone(b['occupation_matches_target'])
  self.assertEqual([r['condition'] for r in a['condition_evidence']['favorable_condition_candidates']],[True,None])
  self.assertIsNone(a['condition_evidence']['supplied_lord_status'])
 def test_same_lord_not_self_conjunction(self):
  from engine.lagna_house_strength_connective import chart_lagna_strength_candidates as chart
  x=chart(8,'Aries',{'Mars':{'sign':'Libra'}})
  self.assertFalse(x['candidates'][0]['same_sign_association_candidate'])
  self.assertFalse(x['candidates'][0]['condition_evidence']['supplied_lagna_link'])
 def test_contradictory_strength_is_rejected(self):
  from engine.lagna_house_strength_connective import chart_lagna_strength_candidates as chart
  with self.assertRaises(ValueError):chart(7,'Aries',{},lord_strong=True,lord_status='weak',strength_profile='supplied')

class IndependentHindiConnectiveTests(unittest.TestCase):
 def test_explicit_or_corroboration_not_winner(self):
  x=gate(True,bhava_status='strong',lord_status='weak',strength_profile='supplied')
  p=x['independent_hindi_reading']
  self.assertTrue(p['condition'])
  self.assertEqual(p['explicit_hindi_favorable_connective'],'or')
  self.assertEqual(p['source']['pdf_page'],193)
  self.assertIsNone(p['adverse_condition_selected'])
  self.assertIsNone(x['selected_profile'])
  self.assertEqual(len(x['favorable_condition_candidates']),2)
 def test_unknown_lord_not_weak_or_automatic_adverse(self):
  x=gate(True,bhava_status='strong',strength_profile='supplied')
  self.assertTrue(x['independent_hindi_reading']['condition'])
  self.assertIsNone(x['adverse_condition'])
  self.assertIsNone(gate()['independent_hindi_reading']['condition'])
