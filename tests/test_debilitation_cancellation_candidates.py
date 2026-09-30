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

 def test_saturn_aries_distinguishes_venus_and_sun(self):
  from engine.debilitation_cancellation_candidates import chart_cancellation_candidates
  r=chart_cancellation_candidates('Aries',{'Saturn':{'sign':'Aries'},'Mars':{'sign':'Taurus'},'Venus':{'sign':'Cancer'},'Sun':{'sign':'Gemini'},'Moon':{'sign':'Aries'}})
  s=next(x for x in r['planet_evidence'] if x['planet']=='Saturn')
  self.assertEqual(s['own_exaltation_sign_lord'],'Venus')
  self.assertEqual(s['planet_exalted_in_depression_sign'],'Sun')
  self.assertEqual([x['qualifying_condition'] for x in s['condition_evidence']['candidates']],[True,False,False,False])
 def test_missing_moon_not_false_for_non_kendra_from_ascendant(self):
  from engine.debilitation_cancellation_candidates import chart_cancellation_candidates
  r=chart_cancellation_candidates('Aries',{'Saturn':{'sign':'Aries'},'Mars':{'sign':'Taurus'}})
  self.assertEqual([x['qualifying_condition'] for x in next(x for x in r['planet_evidence'] if x['planet']=='Saturn')['condition_evidence']['candidates']],[None]*4)
 def test_absent_exalted_classical_is_unknown(self):
  from engine.debilitation_cancellation_candidates import chart_cancellation_candidates
  r=chart_cancellation_candidates('Aries',{'Moon':{'sign':'Scorpio'},'Mars':{'sign':'Taurus'}})
  self.assertIsNone(next(x for x in r['planet_evidence'] if x['planet']=='Moon')['planet_exalted_in_depression_sign'])
