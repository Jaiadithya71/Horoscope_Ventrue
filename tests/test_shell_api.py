import json,unittest
from api.calculate import response_body
BIRTH=dict(date='2000-01-01',time='14:30',timezone='Asia/Kolkata',latitude=13.,longitude=80.,place='Synthetic example')
class ShellAdapterTests(unittest.TestCase):
 def call(self,birth):
  status,raw=response_body(json.dumps({'birth':birth}).encode());return status,json.loads(raw)
 def test_engine_unknowns_preserved(self):
  status,r=self.call(BIRTH);self.assertEqual(status,200)
  for key in ('global_outcome','selected_complete_strength','selected_calendar_profile','empirical_accuracy'):self.assertIsNone(r[key])
  self.assertFalse(r['active_period_inferred'])
 def test_rejects_bad_timezone(self):
  self.assertEqual(self.call({**BIRTH,'timezone':'not-a-zone'})[0],400)
 def test_rejects_bounds(self):
  self.assertEqual(self.call({**BIRTH,'latitude':90})[0],400)
 def test_dst_gap_and_fold_rejected(self):
  for date,time in [('2024-03-10','02:30'),('2024-11-03','01:30')]:
   self.assertEqual(self.call({**BIRTH,'date':date,'time':time,'timezone':'America/New_York'})[0],400)
 def test_no_arbitrary_report_options(self):
  self.assertEqual(response_body(json.dumps({'birth':BIRTH,'query_instant':'2026-01-01'}).encode())[0],400)
 def test_invalid_json(self):self.assertEqual(response_body(b'bad')[0],400)
 def test_oversize(self):self.assertEqual(response_body(b' '*8193)[0],400)
