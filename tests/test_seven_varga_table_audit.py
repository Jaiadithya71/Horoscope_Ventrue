import unittest
from engine.seven_varga_table_audit import audit_printed_seven_varga_table

class VargaTableAuditTests(unittest.TestCase):
 def test_decimal_and_fraction_profiles_separate(self):
  x=audit_printed_seven_varga_table()
  self.assertEqual(x['decimal_sums_matching'],6)
  self.assertIsNone(x['selected_natal_component'])
  rs={r['planet']:r for r in x['rows']}
  self.assertEqual(rs['Venus']['printed_decimal_sum'],'0.905')
  self.assertEqual(rs['Venus']['exact_fraction_sum_if_fractional_relation_values_used'],'29/32')
  self.assertEqual(rs['Saturn']['printed_decimal_sum'],'0.686')
  self.assertEqual(rs['Saturn']['printed_total'],'.689')
  self.assertEqual(rs['Saturn']['exact_fraction_sum_if_fractional_relation_values_used'],'11/16')
  self.assertEqual(rs['Mercury']['exact_fraction_sum_if_fractional_relation_values_used'],'27/16')
