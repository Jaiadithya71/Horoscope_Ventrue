import unittest
from engine.sripati_edition_strength_audit import edition_strength_audit

class EditionAuditTests(unittest.TestCase):
 def test_distinct_edition_rows_not_automatic_correction(self):
  x=edition_strength_audit();self.assertEqual(x['earlier_subtotals_match'],7)
  self.assertTrue(all(r['1919_aspect_equation_matches'] for r in x['rows']))
  changes={r['planet']:r['changed_component_rows'] for r in x['rows'] if r['changed_component_rows']}
  self.assertEqual(set(changes),{'Mars','Jupiter','Saturn'})
  self.assertEqual(changes['Mars'][0]['1919'],'.554')
  self.assertEqual(changes['Saturn'][0]['1919'],'.026')
  self.assertFalse(x['sun_doubling_allocation_resolved']);self.assertIsNone(x['selected_natal_total'])
