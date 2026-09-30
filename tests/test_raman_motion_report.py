import unittest
from engine.raman_motion_report import raman_motion_report as report

class RamanReportTests(unittest.TestCase):
 def inputs(self):return dict(local_mean_timestamp='1912-08-08T13:00:00',longitude=91,clock_kind='local_mean_solar_time',clock_profile='supplied fixture',sun_revolution_branch=0,superior_means={'Mars':200},true_longitudes={'Mars':220,'Mercury':110},inferior_sighra={'Mercury':130},input_profile='supplied other motion inputs',coordinate_branch='explicit same revolution fixture')
 def test_two_raw_constants_propagate_to_motion(self):
  x=report(**self.inputs());self.assertEqual(len(x['candidates']),2)
  for p in ('Mars','Mercury'):
   rows=[next(r for r in c['motion_input_evidence']['rows'] if r['planet']==p) for c in x['candidates']]
   self.assertNotEqual(rows[0]['motion_evidence']['cheshtakendra_degrees'],rows[1]['motion_evidence']['cheshtakendra_degrees'])
  self.assertIsNone(x['selected_motion_profile']);self.assertIsNone(x['total_strength'])
 def test_branch_and_missing_inputs_remain_explicit(self):
  d=self.inputs();d['sun_revolution_branch']=1
  x=report(**d);self.assertAlmostEqual(x['candidates'][0]['assigned_sun_unwrapped'],473.693)
  self.assertIsNone(next(r for r in x['candidates'][0]['motion_input_evidence']['rows'] if r['planet']=='Venus')['motion_evidence'])
  d['sun_revolution_branch']=True
  with self.assertRaises(ValueError):report(**d)
 def test_cli_runs_json_input(self):
  import subprocess,json,sys
  r=subprocess.run([sys.executable,'-m','engine.raman_motion_report','--input-json','-'],input=json.dumps(self.inputs()),capture_output=True,text=True)
  self.assertEqual(r.returncode,0,r.stderr);self.assertEqual(len(json.loads(r.stdout)['candidates']),2)
