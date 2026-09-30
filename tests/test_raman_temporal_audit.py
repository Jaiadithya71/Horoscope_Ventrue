import unittest
from fractions import Fraction as F
from decimal import Decimal as D
from engine.raman_temporal_audit import raman_temporal_audit as audit

class RamanTemporalAuditTests(unittest.TestCase):
 def test_final_numeric_rows_sum_but_blank_gate_holds(self):
  for row in audit()['rows']:
   self.assertEqual(D(row['numeric_sum_minus_printed_total_virupa']),0)
   self.assertIsNone(row['complete_temporal_total'])
   self.assertTrue(row['unverified_blank_row_indices'])
 def test_phase_classification_and_double(self):
  rows={r['planet']:r for r in audit()['rows']}
  self.assertEqual(rows['Mercury']['worked_phase_classification'],'Papa')
  self.assertEqual(F(rows['Moon']['exact_worked_minute_input_phase_virupa_rational']),2*F(rows['Jupiter']['exact_worked_minute_input_phase_virupa_rational']))
  self.assertEqual(F(rows['Mercury']['exact_worked_minute_input_phase_virupa_rational'])+F(rows['Jupiter']['exact_worked_minute_input_phase_virupa_rational']),60)
 def test_methods_not_silently_unified(self):
  a=audit();clock=a['method_a_clock_candidates']
  self.assertEqual(clock['printed_method_a_mars_virupa'],'21.68')
  self.assertEqual(F(a['rows'][2]['exact_method_b_natonnata_virupa_rational']),F(35,3))
  self.assertNotEqual(F(clock['exact_sexagesimal_night_strength_virupa_rational']),F(clock['printed_decimal_night_strength_virupa']))
  self.assertIsNone(a['selected_rounding_policy'])
