import unittest
from engine.full_strength_table_audit import audit_printed_full_strength_table

class FullTableAuditTests(unittest.TestCase):
 def test_verified_mars_reading_closes_without_fit(self):
  x=audit_printed_full_strength_table()
  self.assertEqual(x['subtotal_matches'],7)
  self.assertEqual(x['aspect_equations_match'],7)
  self.assertIsNone(x['computed_natal_total'])
  self.assertIsNone(x['selected_profile'])
  mars=next(r for r in x['rows'] if r['planet']=='Mars')
  self.assertEqual(mars['sum_of_printed_components'],'7.370')
  self.assertEqual(mars['printed_subtotal'],'7.370')
  self.assertEqual(mars['subtotal_delta'],'0.000')
  self.assertEqual(mars['component_sum_adjusted'],'7.731')
  self.assertEqual(mars['printed_final'],'7.731')
  self.assertEqual({r['planet'] for r in x['rows'] if r['cross_table_positional_delta']!='0.000'},{'Venus','Saturn'})
