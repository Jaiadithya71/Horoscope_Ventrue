import unittest
from engine.bhava_lord_candidates import bhava_lord_candidates,audit_printed_cross_sign_example
from engine.bhava_sign_coverage import bhava_sign_coverage
from engine.bhava_geometry import bhava_geometry

class BhavaLordTests(unittest.TestCase):
 def test_exact_printed_inputs_expose_bad_term(self):
  x=audit_printed_cross_sign_example()
  self.assertEqual(x['exact_contributions_rupa'],[.4617525,7.3165325])
  self.assertEqual(x['exact_sum_rupa'],7.778285)
  self.assertTrue(x['printed_contribution_sum_matches'])
  self.assertNotEqual(x['exact_sum_rupa'],float(x['printed_sum_rupa']))
 def test_unequal_arc_profiles_do_not_collapse(self):
  c=bhava_sign_coverage(bhava_geometry(14.5,290))
  totals={'Sun':8,'Moon':8,'Mars':8,'Mercury':8,'Jupiter':8,'Venus':8,'Saturn':8}
  x=bhava_lord_candidates(c,totals,total_profile='complete synthetic supplied fixture',complete=True)
  self.assertIsNone(x['selected_profile'])
  differences=0
  for h in x['houses']:
   a,b=h['candidates'];self.assertAlmostEqual(b['weighted_lord_total_rupa'],8)
   differences+=abs(a['weighted_lord_total_rupa']-b['weighted_lord_total_rupa'])>1e-8
   self.assertIsNone(h['selected_weighted_lord_total']);self.assertIsNone(h['total_bhava_strength'])
  self.assertGreater(differences,0)
 def test_incomplete_or_missing_total_does_not_emit_product(self):
  c=bhava_sign_coverage(bhava_geometry(0,270))
  for complete in (False,True):
   x=bhava_lord_candidates(c,{'Mars':7},total_profile='partial synthetic',complete=complete)
   self.assertIsNone(x['houses'][0]['candidates'][0]['weighted_lord_total_rupa'])
  with self.assertRaises(ValueError):bhava_lord_candidates(c,{},total_profile='',complete=True)
