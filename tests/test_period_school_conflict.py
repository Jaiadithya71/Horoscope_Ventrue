import unittest
from engine.period_school_conflict import period_school_conflict
from engine.precedence import reconcile_claims

class PeriodSchoolTests(unittest.TestCase):
 def test_true_source_conflict_cannot_be_resolved_by_verified_flags(self):
  x=period_school_conflict('Jupiter','Mercury')
  self.assertTrue(x['scope_match']);self.assertTrue(x['unresolved_school_conflict'])
  self.assertIsNone(x['selected_school']);self.assertIsNone(x['personal_outcome'])
  claims=[{'topic':'general_period_school','interval':'same_main_sub','polarity':c['polarity'],
           'citation':x['source'],'strength_verified':True,'timing_verified':True} for c in x['competing_school_evidence']]
  y=reconcile_claims(claims)[0]
  self.assertEqual(y['status'],'abstain');self.assertTrue(y['conflict']);self.assertEqual(y['missing_evidence'],[])
 def test_narrow_scope_no_silent_reversal_or_general_claim(self):
  for a,b in [('Mercury','Jupiter'),('Jupiter','Venus'),('Saturn','Mercury')]:
   x=period_school_conflict(a,b)
   self.assertFalse(x['scope_match']);self.assertEqual(x['competing_school_evidence'],[])
   self.assertIsNone(x['personal_outcome'])
  with self.assertRaises(ValueError):period_school_conflict('unknown','Mercury')
