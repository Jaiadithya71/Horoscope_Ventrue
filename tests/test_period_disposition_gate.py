import unittest
from engine.period_disposition_gate import period_disposition_gate as gate

class PeriodDispositionTests(unittest.TestCase):
 def test_retrograde_in_dusthana_not_silent_winner(self):
  x=gate(retrograde=True,good_house=False,input_profile='supplied')
  self.assertTrue(x['1937_favorable_disjunction'])
  self.assertTrue(x['shared_adverse_disjunction'])
  self.assertTrue(x['opposed_conditions_active'])
  self.assertIsNone(x['selected_polarity']);self.assertIsNone(x['personal_outcome'])
 def test_unknowns_not_absence(self):
  x=gate(input_profile='supplied')
  self.assertIsNone(x['1937_favorable_disjunction']);self.assertIsNone(x['shared_adverse_disjunction'])
  self.assertIsNone(x['opposed_conditions_active'])
 def test_friendly_scope_omission_not_school_selection(self):
  x=gate(friendly_sign=True,input_profile='supplied')
  self.assertTrue(x['1937_favorable_disjunction']);self.assertTrue(x['later_friendly_sign_omission'])
  self.assertIsNone(x['later_favorable_connective_selected'])
 def test_false_truthy_flag_rejected(self):
  with self.assertRaises(ValueError):gate(own_sign=1,input_profile='supplied')
  with self.assertRaises(ValueError):gate(input_profile=True)

class ChartPeriodDispositionTests(unittest.TestCase):
 def test_retrograde_dusthana_and_missing_degree(self):
  from engine.period_disposition_gate import chart_period_disposition_candidates as chart
  x=chart('Aries',{'Jupiter':{'sign':'Virgo','retrograde':True}},'Jupiter','Mercury')
  a,b=x['rows'][:2]
  self.assertTrue(a['condition_evidence']['opposed_conditions_active'])
  self.assertIsNone(b['supplied_house'])
  self.assertIsNone(b['condition_evidence']['shared_adverse_disjunction'])
  self.assertIsNone(a['condition_evidence']['supplied_flags']['overpowered_rays'])
 def test_node_not_given_lord_chapter_polarity(self):
  from engine.period_disposition_gate import chart_period_disposition_candidates as chart
  x=chart('Aries',{'Rahu':{'sign':'Virgo','retrograde':True}},'Rahu','Rahu')
  self.assertEqual(len(x['rows']),2)
  self.assertTrue(all(not r['classical_scope_applicability'] for r in x['rows']))
  self.assertTrue(all(r['condition_evidence']['1937_favorable_disjunction'] is None for r in x['rows']))
