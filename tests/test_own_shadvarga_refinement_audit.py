import unittest
from engine.own_shadvarga_refinement_audit import own_shadvarga_refinement_audit

class OwnShadvargaAuditTests(unittest.TestCase):
 def test_all_six_definition_fails_explicit_example(self):
  x=own_shadvarga_refinement_audit();j=next(r for r in x['rows'] if r['planet']=='Jupiter')
  self.assertEqual(j['own_varga_names'],['rasi','drekkana','dwadasamsa'])
  self.assertEqual(j['base_decan_rupa'],.25);self.assertEqual(j['quoted_refinement_rupa'],.5)
  self.assertFalse(x['all_six_required_guess_fits_explicit_jupiter_example'])
  self.assertFalse(x['any_own_quantifier_verified']);self.assertIsNone(x['selected_refinement_definition'])
 def test_other_quoted_values_not_invented(self):
  x=own_shadvarga_refinement_audit()
  self.assertTrue(all(r['quoted_refinement_rupa'] is None for r in x['rows'] if r['planet']!='Jupiter'))
  self.assertTrue(all(r['selected_refined_component'] is None for r in x['rows']))
