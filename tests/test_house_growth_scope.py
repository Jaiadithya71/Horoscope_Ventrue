import unittest
from engine.house_growth_scope import house_growth_scope,chart_house_growth_candidates

class HouseGrowthScopeTests(unittest.TestCase):
 def row(self,h,c):return house_growth_scope(h,c,classification_profile='supplied',house_profile='supplied')
 def test_dusthana_growth_not_personal_good(self):
  for h in (6,8,12):
   for c,g,e in [('benefic','decay','reduced'),('malefic','growth','intensified')]:
    x=self.row(h,c)
    self.assertEqual(x['xv18_satyacharya_house_effect'],g)
    self.assertEqual(x['xv19_dusthana_evil_effect'],e)
    self.assertTrue(x['shared_dusthana_direction_consistent'])
    self.assertIsNone(x['personal_benefit']);self.assertIsNone(x['global_precedence'])
 def test_regular_house_and_missing(self):
  self.assertEqual(self.row(5,'benefic')['xv18_satyacharya_house_effect'],'growth')
  self.assertIsNone(self.row(5,'benefic')['xv19_dusthana_evil_effect'])
  self.assertIsNone(self.row(None,'benefic')['xv18_satyacharya_house_effect'])
  self.assertIsNone(self.row(6,None)['xv19_dusthana_evil_effect'])
 def test_mixed_occupants_not_sum_and_missing_degree_not_substitute(self):
  x=chart_house_growth_candidates(6,'Aries',{'Jupiter':{'sign':'Virgo'},'Mars':{'sign':'Virgo'}},{'Jupiter':'benefic','Mars':'malefic'},classification_profile='fixture')
  self.assertEqual(len(x['candidates'][0]['occupant_evidence']),2)
  self.assertIsNone(x['candidates'][0]['combined_house_effect'])
  self.assertEqual(x['candidates'][1]['occupant_evidence'],[])
  self.assertIn('Mars',x['candidates'][1]['unchecked_occupation'])
 def test_invalid(self):
  for h,c in [(True,'benefic'),(13,'benefic'),(6,'good')]:
   with self.assertRaises(ValueError):self.row(h,c)
