import unittest
from engine.debilitation_cancellation_candidates import cancellation_candidates

class CancellationTests(unittest.TestCase):
 def test_disagreement_not_erased(self):
  r=cancellation_candidates(True,False,True,False)
  self.assertEqual([x['qualifying_condition'] for x in r['candidates']],[True,False,False,False])
  self.assertIsNone(r['selected_profile']);self.assertIsNone(r['personal_outcome'])
 def test_missing_never_means_false(self):
  self.assertEqual([x['qualifying_condition'] for x in cancellation_candidates(True)['candidates']],[None]*4)
  self.assertEqual([x['qualifying_condition'] for x in cancellation_candidates(False)['candidates']],[False]*4)
 def test_no_truthy_integers(self):
  with self.assertRaises(ValueError):cancellation_candidates(1)
