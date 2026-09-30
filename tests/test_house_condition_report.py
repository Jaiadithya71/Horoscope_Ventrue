import unittest
from engine.house_condition_report import house_condition_report

class HouseReportTests(unittest.TestCase):
 def test_scoped_conditions_not_global_winner(self):
  r=house_condition_report(7,'Aries',{'Venus':{'sign':'Virgo'},'Jupiter':{'sign':'Aries'}},{'Jupiter':'benefic'},classification_profile='supplied',strength_profile='externally verified fixture',bhava_strong=True,lord_strong=True,karaka_strong=True)
  self.assertTrue(r['xv5_scoped_recovery']['candidates'][0]['condition_evidence']['benefic_aspect_exception'])
  self.assertTrue(r['xv25_26_supplied_strength_conditions'][0]['condition_evidence']['all_three_strength_condition'])
  self.assertEqual(r['house_lord_debilitation_candidates']['planet'],'Venus')
  self.assertIsNone(r['global_precedence']);self.assertIsNone(r['personal_outcome'])
 def test_missing_degree_stays_unchecked(self):
  r=house_condition_report(7,'Aries',{'Venus':{'sign':'Libra'}},{},classification_profile='partial')
  self.assertEqual(r['xv25_26_supplied_strength_conditions'][1]['condition_evidence']['unchecked_alternative_planets'],['Venus'])
