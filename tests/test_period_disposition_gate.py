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
