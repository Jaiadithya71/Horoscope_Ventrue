import unittest
from engine.ketkar_mercury_upstream import mercury_upstream_candidate

class MercuryUpstreamTests(unittest.TestCase):
 def test_two_matches_one_disagreement(self):
  r=mercury_upstream_candidate()
  self.assertEqual(r['printed_mercury_centre_days'],'54.086')
  self.assertEqual(r['rounded_candidate_centre_degrees'],'208.292')
  self.assertEqual(r['rounded_candidate_samanantara'],'-0.29')
  self.assertEqual(r['rounded_candidate_residual'],'63.0')
  self.assertFalse(r['linear_candidate_reproduces_printed_residual'])
  self.assertIsNone(r['residual_selected_for_true_chain'])
