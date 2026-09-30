import unittest,json,subprocess,sys
from engine.validation_report import validation_report

class JhaReportTests(unittest.TestCase):
 def run_cli(self,*args):return subprocess.run([sys.executable,'-m','engine.bphs_jha_aspect_report',*args],capture_output=True,text=True)
 def test_integrated_source_diagnostics(self):
  x=validation_report()['bphs_jha_aspect_source_validation']
  self.assertFalse(x['unique_bphs_geometry_verified']);self.assertEqual(len(x['boundary_diagnostics']),2)
  for row in x['boundary_diagnostics']:self.assertIsNone(row['determinate_unsigned_virupa_rational'])
 def test_cli_coordinate_case(self):
  r=self.run_cli('--aspecting-planet','Saturn','--aspector-longitude','200','--aspected-longitude','286','--coordinate-profile','synthetic test')
  self.assertEqual(r.returncode,0,r.stderr)
  x=json.loads(r.stdout);self.assertEqual(x['supplied_coordinate_candidates']['determinate_unsigned_virupa_rational'],'47');self.assertIsNone(x['total_strength'])
 def test_cli_source_only_and_rejects_partial_or_invalid(self):
  r=self.run_cli();self.assertEqual(r.returncode,0,r.stderr);self.assertIsNone(json.loads(r.stdout)['supplied_coordinate_candidates'])
  for args in [('--aspecting-planet','Saturn'),('--aspecting-planet','Saturn','--aspector-longitude','NaN','--aspected-longitude','286','--coordinate-profile','synthetic')]:
   r=self.run_cli(*args);self.assertNotEqual(r.returncode,0);self.assertEqual(r.stdout,'')

class JhaJsonReportTests(unittest.TestCase):
 def payload(self):
  from engine.bphs_jha_special_aspect import CLASSICAL
  return {'target':'Sun','longitudes':{p:100 if p=='Sun' else 0 for p in CLASSICAL},
   'classifications':dict.fromkeys(set(CLASSICAL)-{'Sun'},'benefic'),
   'coordinate_profile':'synthetic common degree frame','classification_profile':'supplied synthetic classes'}
 def run_input(self,payload,*args):return subprocess.run([sys.executable,'-m','engine.bphs_jha_aspect_report','--input-json','-',*args],input=json.dumps(payload),capture_output=True,text=True)
 def test_cli_json_and_integrated_bridge(self):
  r=self.run_input(self.payload());self.assertEqual(r.returncode,0,r.stderr);x=json.loads(r.stdout)
  self.assertEqual(x['supplied_drigbala_evidence']['candidate_drigbala_virupa_rational'],'155')
  self.assertFalse(x['chart_identity_match_verified']);self.assertIsNone(x['total_strength']);self.assertIsNone(x['personal_forecast'])
  self.assertEqual(validation_report()['bphs_jha_aspect_source_validation']['synthetic_drigbala_bridge_check']['candidate_drigbala_virupa_rational'],'155')
 def test_cli_boundary_and_missing_inputs_preserved(self):
  p=self.payload();p['longitudes']['Sun']=270;r=self.run_input(p);self.assertEqual(r.returncode,0,r.stderr)
  x=json.loads(r.stdout)['supplied_drigbala_evidence'];self.assertIsNone(x['candidate_drigbala_virupa_rational']);self.assertEqual(x['blocked_planets'],['Jupiter','Saturn'])
  del p['longitudes']['Moon'];r=self.run_input(p);self.assertEqual(r.returncode,0,r.stderr);self.assertIn('Moon',json.loads(r.stdout)['supplied_drigbala_evidence']['blocked_planets'])
 def test_cli_exact_schema_and_mixed_modes_rejected(self):
  p=self.payload()
  for bad in ([],{},dict(p,unit='automatic'),dict(p,coordinate_profile=''),dict(p,longitudes={'Sun':True})):
   r=self.run_input(bad);self.assertNotEqual(r.returncode,0);self.assertEqual(r.stdout,'')
  r=self.run_input(p,'--aspecting-planet','Saturn');self.assertNotEqual(r.returncode,0);self.assertEqual(r.stdout,'')
