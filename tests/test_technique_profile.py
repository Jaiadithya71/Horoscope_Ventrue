import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PROFILE=ROOT/'profiles/balaji_public_technique.json'

class ProfileTests(unittest.TestCase):
    def test_evidence_and_calibration_contract(self):
        p=json.loads(PROFILE.read_text())
        self.assertEqual(len(p['sample']),7)
        ids={v['video_id'] for v in p['sample']}
        for row in p['method']:
            self.assertIn(row['status'],('observed','mentioned-not-derived'))
            self.assertTrue(row['evidence'])
            for e in row['evidence']:
                self.assertIn(e['video_id'],ids)
                self.assertGreaterEqual(e['seconds'],0)
            self.assertTrue(row['engine'])
            self.assertTrue(row['book_alignment'])
        d=next(r for r in p['method'] if r['id']=='dasha-bhukti-antara')
        self.assertEqual(d['status'],'mentioned-not-derived')
        self.assertIn('not proven',d['book_alignment'])
        self.assertIn('not a private-consultation reconstruction',p['scope'])

if __name__=='__main__':unittest.main()
