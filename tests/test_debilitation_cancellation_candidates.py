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

 def test_other_recipes_independent(self):
  from engine.debilitation_cancellation_candidates import other_cancellation_recipes
  r=other_cancellation_recipes(True,True,False,None,False,False,True)
  self.assertEqual([x['condition'] for x in r['recipe_conditions']],[True,False,False,True])
  self.assertFalse(r['recipe_conditions'][1]['auspicious_house_qualification'])
  self.assertIsNone(r['personal_outcome'])
 def test_aspect_unknown_and_qualification(self):
  from engine.debilitation_cancellation_candidates import other_cancellation_recipes
  r=other_cancellation_recipes(True,aspected_by_depression_lord=True)
  self.assertTrue(r['recipe_conditions'][1]['condition'])
  self.assertIsNone(r['recipe_conditions'][1]['auspicious_house_qualification'])
 def test_printed_illustration_is_not_arbitration(self):
  from engine.debilitation_cancellation_candidates import printed_cancellation_illustration_audit
  r=printed_cancellation_illustration_audit()
  self.assertEqual(r['whole_sign_houses']['Mars'],7)
  self.assertEqual(r['whole_sign_houses']['Sun'],5)
  self.assertTrue(r['mars_kendra_claim_matches']);self.assertFalse(r['sun_kendra_claim_matches'])
  self.assertIsNone(r['cancellation_condition_used_to_arbitrate_schools'])

 def test_special_aspect_recipe_candidates_not_selected(self):
  from engine.debilitation_cancellation_candidates import chart_cancellation_candidates
  r=chart_cancellation_candidates('Leo',{'Saturn':{'sign':'Aries','longitude':10},'Mars':{'sign':'Capricorn','longitude':280},'Venus':{'sign':'Capricorn','longitude':282},'Moon':{'sign':'Leo','longitude':130}})
  row=next(x for x in r['planet_evidence'] if x['planet']=='Saturn')['condition_evidence']
  self.assertEqual(row['aspect_evidence']['relative_whole_sign_house'],4)
  self.assertIsNone(row['aspect_evidence']['degree_amount_to_VII28_condition'])
  self.assertGreater(row['aspect_evidence']['degree_aspect_amount']['rupa'],0)
  recipes=row['other_recipe_candidates']
  self.assertTrue(recipes[0]['condition_evidence']['recipe_conditions'][1]['condition'])
  self.assertFalse(recipes[1]['condition_evidence']['recipe_conditions'][1]['condition'])
 def test_recipe_missing_lord_aspect_stays_unknown(self):
  from engine.debilitation_cancellation_candidates import chart_cancellation_candidates
  r=chart_cancellation_candidates('Leo',{'Saturn':{'sign':'Aries'}})
  row=r['planet_evidence'][0]['condition_evidence']
  self.assertIsNone(row['other_recipe_candidates'][0]['condition_evidence']['recipe_conditions'][1]['condition'])
  self.assertIsNone(row['aspect_evidence']['degree_aspect_amount'])
