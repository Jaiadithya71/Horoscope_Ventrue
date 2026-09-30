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
