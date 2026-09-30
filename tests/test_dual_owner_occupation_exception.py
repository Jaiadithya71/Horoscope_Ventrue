import unittest
from engine.dual_owner_occupation_exception import dual_owner_occupation_exception

class DualOwnerExceptionTests(unittest.TestCase):
 def row(self,ref,p,s):
  x=dual_owner_occupation_exception(ref,{} if s is None else {p:{'sign':s}})
  return next(r for r in x['rows'] if r['planet']==p)
 def test_printed_virgo_saturn_example(self):
  r=self.row('Virgo','Saturn','Capricorn')
  self.assertTrue(r['scoped_exception_active'])
  self.assertEqual(r['occupied_own_house_emphasized'],5)
  self.assertEqual(r['dusthana_ownership_effect_excluded_in_this_clause'],6)
  self.assertIsNone(r['selected_personal_effect'])
 def test_dusthana_moola_not_overriding_exception(self):
  r=self.row('Scorpio','Mars','Scorpio')
  self.assertTrue(r['scoped_exception_active'])
  self.assertEqual(r['dusthana_ownership_effect_excluded_in_this_clause'],6)
 def test_own_dusthana_and_other_sign_not_exception(self):
  self.assertFalse(self.row('Virgo','Saturn','Aquarius')['scoped_exception_active'])
  self.assertFalse(self.row('Virgo','Saturn','Pisces')['scoped_exception_active'])
  self.assertFalse(self.row('Taurus','Saturn','Capricorn')['dual_ownership_condition'])
 def test_eligible_missing_stays_unknown_ineligible_false(self):
  self.assertIsNone(self.row('Virgo','Saturn',None)['scoped_exception_active'])
  self.assertFalse(self.row('Taurus','Saturn',None)['scoped_exception_active'])
