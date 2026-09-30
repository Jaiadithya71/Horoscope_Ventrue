import json,os,subprocess,sys,unittest
from engine.research_input_report import research_input_report
from test_research_input_report import BIRTH

class ResearchInputCliTests(unittest.TestCase):
 def runcli(self,payload):
  return subprocess.run([sys.executable,'-m','engine.research_input_report','--input-json','-'],input=json.dumps(payload),text=True,capture_output=True,env=os.environ.copy(),timeout=30)
 def test_stdin_success(self):
  r=self.runcli({'birth':BIRTH});self.assertEqual(r.returncode,0,r.stderr)
  x=json.loads(r.stdout);self.assertIsNone(x['query_convention_condition_evidence'])
  self.assertFalse(x['active_period_inferred'])
 def test_errors_have_no_report_or_traceback(self):
  for payload in [{},{'birth':BIRTH,'guess':True},{'birth':{**BIRTH,'time':'not-a-time'}},
   {'birth':{**BIRTH,'place':12}},{'birth':{**BIRTH,'latitude':True}},
   {'birth':BIRTH,'query_instant':'2026-01-01T00:00:00'},
   {'birth':BIRTH,'supplied_strength':{'Sun':{'source_layout':'default'}}}]:
   r=self.runcli(payload);self.assertEqual(r.returncode,2,r.stderr)
   self.assertEqual(r.stdout,'');self.assertNotIn('Traceback',r.stderr)
 def test_optional_query_routes_nine_profiles_without_overwriting_explicit_pair(self):
  x=research_input_report(BIRTH,query_instant='2026-01-01T00:00:00+00:00',period_pair={'main_lord':'Jupiter','sub_lord':'Mercury'})
  c=x['query_convention_condition_evidence'];self.assertEqual(len(c['profile_condition_routes']),9)
  self.assertIsNone(c['selected_profile']);self.assertIsNone(x['selected_calendar_profile'])
  self.assertEqual(x['explicit_period_pair_evidence']['sub_lord'],'Mercury')
  self.assertFalse(x['active_period_inferred'])
