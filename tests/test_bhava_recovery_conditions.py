import unittest
from engine.bhava_recovery_conditions import xv1_dignity_qualification,xv5_recovery_condition

class RecoveryTests(unittest.TestCase):
 def test_printed_negation_disagreement(self):
  self.assertEqual([x['condition'] for x in xv1_dignity_qualification(False,False,False)['qualification_candidates']],[True,False])
  self.assertEqual([x['condition'] for x in xv1_dignity_qualification(True,True,True)['qualification_candidates']],[False,True])
 def test_missing_not_safe(self):
  self.assertEqual([x['condition'] for x in xv1_dignity_qualification()['qualification_candidates']],[None,None])
 def test_scoped_recovery(self):
  r=xv5_recovery_condition(True,False,True)
  self.assertTrue(r['benefic_aspect_exception']);self.assertFalse(r['adverse_condition_without_checked_exception'])
  self.assertIsNone(r['selected_personal_effect'])
 def test_missing_aspect_does_not_deny_recovery(self):
  r=xv5_recovery_condition(True,False)
  self.assertIsNone(r['benefic_aspect_exception']);self.assertIsNone(r['adverse_condition_without_checked_exception'])
 def test_no_base_not_favorable_and_invalid(self):
  r=xv5_recovery_condition(False,False,True)
  self.assertFalse(r['benefic_aspect_exception']);self.assertIsNone(r['selected_personal_effect'])
  with self.assertRaises(ValueError):xv5_recovery_condition(1)

 def test_house_frame_difference(self):
  from engine.bhava_recovery_conditions import chart_xv5_candidates
  r=chart_xv5_candidates(7,'Aries',{'Venus':{'sign':'Taurus'},'Mars':{'sign':'Capricorn'},'Mercury':{'sign':'Capricorn'},'Jupiter':{'sign':'Capricorn'}},{},classification_profile='caller supplied partial')
  asc=r['candidates'][0]['condition_evidence']['adverse_base_condition']
  target=r['candidates'][2]['condition_evidence']['adverse_base_condition']
  self.assertFalse(asc);self.assertTrue(target)
  self.assertFalse(r['candidates'][0]['condition_evidence']['benefic_aspect_exception'])
 def test_no_degree_fallback_and_partial_aspect(self):
  from engine.bhava_recovery_conditions import chart_xv5_candidates
  r=chart_xv5_candidates(7,'Aries',{'Venus':{'sign':'Virgo'},'Jupiter':{'sign':'Aries'}},{'Jupiter':'benefic'},classification_profile='supplied')
  self.assertTrue(r['candidates'][0]['condition_evidence']['benefic_aspect_exception'])
  self.assertIsNone(r['candidates'][4]['lord_house_from_ascendant'])
  self.assertIsNone(r['selected_profile'])
 def test_missing_classes_not_no_aspect(self):
  from engine.bhava_recovery_conditions import chart_xv5_candidates
  r=chart_xv5_candidates(7,'Aries',{'Venus':{'sign':'Virgo'}},{},classification_profile='unresolved classes')
  self.assertIsNone(r['candidates'][0]['condition_evidence']['benefic_aspect_exception'])
  with self.assertRaises(ValueError):chart_xv5_candidates(7,'Aries',{}, {'Rahu':'benefic'},classification_profile='bad')

 def test_house_aspect_does_not_protect_lord(self):
  from engine.bhava_recovery_conditions import xv3_lord_condition
  lord=xv3_lord_condition(True,False,False,False,False,False)
  house=xv5_recovery_condition(True,False,True)
  self.assertTrue(lord['adverse_lord_without_benefic_influence'])
  self.assertTrue(house['benefic_aspect_exception'])
  self.assertIsNone(lord['personal_outcome']);self.assertIsNone(house['selected_personal_effect'])
 def test_missing_lord_influence_not_absence(self):
  from engine.bhava_recovery_conditions import xv3_lord_condition
  self.assertIsNone(xv3_lord_condition(depressed=True)['adverse_lord_without_benefic_influence'])
 def test_xv6_connective_axes(self):
  from engine.bhava_recovery_conditions import xv6_connective_candidates
  self.assertEqual([r['condition'] for r in xv6_connective_candidates(True,False,False)['candidates']],[False,True])
  self.assertEqual([r['condition'] for r in xv6_connective_candidates(None,None,True)['candidates']],[True,True])
  self.assertEqual([r['condition'] for r in xv6_connective_candidates()['candidates']],[None,None])
