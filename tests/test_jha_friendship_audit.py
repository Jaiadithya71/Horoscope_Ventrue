import unittest
from engine.jha_friendship_audit import jha_friendship_audit as audit

class JhaFriendAuditTests(unittest.TestCase):
 def test_independent_directed_sun_fixture(self):
  x=audit();self.assertEqual(x['worked_matches'],6)
  self.assertTrue(all(r['matches'] for r in x['sun_directed_rows']))
  self.assertEqual(next(r for r in x['sun_directed_rows'] if r['other']=='Jupiter')['other_rasi_from_sun'],11)
 def test_weights_not_mixed_or_varga_selected(self):
  x=audit();w=x['numeric_varga_weights_comparison'];self.assertEqual(w['jha28_3_virupa']['enemy'],4)
  self.assertEqual(w['jha28_3_virupa']['very_friend'],20);self.assertEqual(w['sripati_direct_owner_virupa']['very_friend'],22.5)
  self.assertFalse(w['weights_interchangeable']);self.assertFalse(x['sripati_owner_placement_arbitration_resolved'])
  self.assertIsNone(x['selected_varga_profile']);self.assertIsNone(x['full_strength'])
