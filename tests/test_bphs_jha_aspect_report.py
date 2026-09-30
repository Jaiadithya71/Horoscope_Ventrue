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
