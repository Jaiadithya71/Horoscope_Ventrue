import unittest
from engine.combustion_candidates import combustion_candidates as c,chart_combustion_candidates

class CombustionCandidateTests(unittest.TestCase):
 def test_explicit_motion_and_wrap(self):
  x=c('Mercury',1,348,None)
  self.assertEqual(x['separation_in_ecliptic_longitude_degrees'],13)
  self.assertEqual([r['candidate_overpowered_sun_rays'] for r in x['candidates']],[True,False])
  self.assertTrue(x['candidate_conflict']);self.assertIsNone(x['selected_overpowered_sun_rays'])
  self.assertTrue(c('Venus',9,0,False)['candidates'][0]['candidate_overpowered_sun_rays'])
  self.assertFalse(c('Venus',9,0,True)['candidates'][0]['candidate_overpowered_sun_rays'])
 def test_boundaries_and_noncopied_nodes(self):
  for p,orb in [('Moon',12),('Mars',17),('Jupiter',11),('Saturn',15)]:
   self.assertIsNone(c(p,orb,0)['candidates'][0]['candidate_overpowered_sun_rays'])
   self.assertFalse(c(p,orb+0.00001,0)['candidates'][0]['candidate_overpowered_sun_rays'])
   self.assertTrue(c(p,orb-0.00001,0)['candidates'][0]['candidate_overpowered_sun_rays'])
  for p in ('Sun','Rahu','Ketu'):self.assertEqual(c(p,1,0)['status'],'not_covered')
 def test_missing_is_not_false_and_no_mutation(self):
  placements={'Mercury':{'longitude':13,'retrograde':False},'Sun':{'longitude':0}}
  x=chart_combustion_candidates(placements)
  self.assertNotIn('overpowered_sun_rays',placements['Mercury'])
  self.assertIsNone(x['selected_profile'])
  self.assertEqual(chart_combustion_candidates({'Mars':{'longitude':1}})['planets']['Mars']['status'],'unresolved_coordinates')
  with self.assertRaises(ValueError):c('Mercury',1,0,0)
