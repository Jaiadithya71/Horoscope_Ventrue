import unittest
from engine.positional_table_audit import audit_printed_positional_table

class PositionalAuditTests(unittest.TestCase):
    def test_seven_printed_sums_not_natal_or_total(self):
        x=audit_printed_positional_table()
        self.assertEqual(x['internal_arithmetic_matches'],7)
        self.assertEqual(len(x['rows']),7)
        self.assertIsNone(x['full_strength'])
        self.assertIsNone(x['selected_natal_positional_total'])
        venus=next(r for r in x['rows'] if r['planet']=='Venus')
        self.assertEqual(venus['printed_components']['uchcha'],venus['printed_components']['seven_varga'])
        for r in x['rows']:
            self.assertFalse(r['computed_from_chart'])
            self.assertEqual(r['source']['pdf_page'],53)
        self.assertEqual(len(x['unresolved_alternatives']),2)
