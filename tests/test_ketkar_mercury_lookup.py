import unittest
from engine.ketkar_mercury_lookup import mercury_lookup_candidate

class MercuryLookupTests(unittest.TestCase):
    def test_five_actual_row_inputs(self):
        r=mercury_lookup_candidate()
        self.assertTrue(r['matches_narrative_at_candidate_precision'])
        self.assertEqual(r['computed']['inantara'],'-21.207184')
        self.assertEqual(r['computed']['radius'],'1069.882')
        self.assertFalse(r['source_selects_unique_rounding'])
    def test_limits_and_endpoints(self):
        self.assertEqual(mercury_lookup_candidate(270)['computed']['inantara'],'-21.162')
        self.assertEqual(mercury_lookup_candidate(269)['computed']['inantara'],'-21.290')
        with self.assertRaises(ValueError):mercury_lookup_candidate(268)
