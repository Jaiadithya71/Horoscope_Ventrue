import json
import unittest
from pathlib import Path
from engine.outcome_audit_gate import audit_gate

class OutcomeAuditGateTests(unittest.TestCase):
 def test_caption_discrepancy_not_a_confirmed_predictive_miss(self):
  r=json.loads((Path(__file__).parents[1]/'benchmarks'/'balaji_outcome_audit_pending.json').read_text())[0]
  x=audit_gate(r)
  self.assertEqual(x['missing_verification'],['original_audio_verified','publication_before_result_verified','candidate_identity_verified'])
  self.assertFalse(x['eligible_for_reviewed_single_case_scoring'])
  self.assertIsNone(x['scored_predictive_outcome'])
  self.assertTrue(r['caption_result_discrepancy']);self.assertIsNone(r['scored_predictive_outcome'])
