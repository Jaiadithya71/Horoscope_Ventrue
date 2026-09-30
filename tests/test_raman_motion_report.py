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
 def test_optional_table_candidates_preserve_supplied_path(self):
  d=self.inputs();original=report(**d)
  d['inferior_table_requests']={'Mercury':dict(elapsed_days='6862.578',birth_year_offset=18,epoch_clock_profile='independently supplied inferior clock')}
  x=report(**d)
  self.assertEqual(x['candidates'],original['candidates']);self.assertEqual(len(x['inferior_table_motion_candidates']),4)
  self.assertEqual(x['inferior_table_evidence']['Mercury']['supplied_elapsed_days'],'6862.578')
  self.assertTrue(all(r['motion_input_evidence']['motion_evidence'] is not None for r in x['inferior_table_motion_candidates']))
 def test_table_missing_clock_no_fallback_and_unknown_cell(self):
  d=self.inputs();d['inferior_table_requests']={'Mercury':dict(elapsed_days=10000,birth_year_offset=18)}
  with self.assertRaises(TypeError):report(**d)
  d['inferior_table_requests']['Mercury']['epoch_clock_profile']='supplied unknown-cell fixture'
  x=report(**d)
  self.assertEqual(len(x['inferior_table_motion_candidates']),4)
  self.assertTrue(all(r['motion_input_evidence']['missing_inputs']==['sighrochcha'] for r in x['inferior_table_motion_candidates']))
 def test_no_optional_table_request_changes_existing_default(self):
  x=report(**self.inputs());self.assertEqual(x['inferior_table_evidence'],{});self.assertEqual(x['inferior_table_motion_candidates'],[])
