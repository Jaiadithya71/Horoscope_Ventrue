import unittest
from engine.sripati_worked_motion_audit import worked_motion_audit

class WorkedMotionAuditTests(unittest.TestCase):
    def test_supplied_angles_not_reconstructed_inputs(self):
        x=worked_motion_audit()
        self.assertEqual(x['local_floor3_matches'],4)
        self.assertEqual(x['earlier_local_aggregate_matches'],4)
        self.assertEqual(x['later_local_aggregate_matches'],5)
        self.assertTrue(all(r['pipeline_exact_agreement'] for r in x['rows']))
        self.assertTrue(all(all(v is None for v in r['upstream_inputs'].values()) for r in x['rows']))
        self.assertTrue(all(r['independent_angle_reconstruction'] is None for r in x['rows']))
        self.assertIsNone(x['selected_natal_total'])
