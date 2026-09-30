import unittest
from engine.raman_manual_geometry_audit import raman_manual_geometry_audit as audit

class ManualGeometryTests(unittest.TestCase):
 def test_six_printed_boundaries_reproduce_by_existing_geometry(self):
  x=audit()
  self.assertTrue(all(abs(r['signed_degree_difference'])<1e-10 for r in x['manual_printed_beginning_comparisons']))
 def test_seventh_typo_and_changed_anchors_not_merged(self):
  x=audit();r=x['seventh_centre_audit']
  self.assertAlmostEqual(r['computed_from_opposite_ascendant'],r['rule_example_degrees'])
  self.assertAlmostEqual(r['printed_table_degrees']-r['rule_example_degrees'],30)
  self.assertNotEqual(x['manual_1935_geometry']['anchor_inputs'],x['later_graha_balas_opening_geometry']['anchor_inputs'])
  self.assertIsNone(x['selected_anchor_set']);self.assertFalse(x['residential_disagreement_resolved'])
