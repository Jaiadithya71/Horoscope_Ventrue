import unittest
from engine.sripati_edition_strength_audit import edition_strength_audit

class EditionAuditTests(unittest.TestCase):
 def test_distinct_edition_rows_not_automatic_correction(self):
  x=edition_strength_audit();self.assertEqual(x['earlier_subtotals_match'],7)
  self.assertTrue(all(r['1919_aspect_equation_matches'] for r in x['rows']))
  changes={r['planet']:r['changed_component_rows'] for r in x['rows'] if r['changed_component_rows']}
  self.assertEqual(set(changes),{'Jupiter','Saturn'})
  self.assertEqual(changes['Saturn'][0]['1919'],'.026')
  self.assertFalse(x['sun_doubling_allocation_resolved']);self.assertIsNone(x['selected_natal_total'])

 def test_upstream_trace_arithmetic_not_input_validation(self):
  x=edition_strength_audit()['upstream_component_trace']
  self.assertEqual(x['jupiter']['seven_varga_delta'],x['jupiter']['positional_delta'])
  self.assertEqual(x['jupiter']['seven_varga_delta'],'0.125')
  self.assertEqual(x['saturn']['1919_local_motion_table_rupa'],'.062')
  self.assertNotEqual(x['saturn']['1919_local_motion_table_rupa'],x['saturn']['1919_aggregate_motion_rupa'])
