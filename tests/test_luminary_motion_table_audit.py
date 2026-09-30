import unittest
from engine.luminary_motion_table_audit import luminary_motion_table_audit

class LuminaryTableTests(unittest.TestCase):
 def test_table_identity_not_universal_rule(self):
  r=luminary_motion_table_audit()
  self.assertTrue(all(x['exact_printed_equality'] for x in r['rows']))
  self.assertEqual([x['doubled_comparison_not_substituted'] for x in r['rows']],['1.620','1.036'])
  self.assertFalse(r['universal_luminary_motion_rule_verified'])
  self.assertFalse(r['IV_ray_components_substituted']);self.assertIsNone(r['total_strength'])
