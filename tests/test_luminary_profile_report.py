import unittest
from engine.luminary_profile_report import luminary_profile_report as report

class LuminaryProfileReportTests(unittest.TestCase):
 def test_missing_declination_and_unknown_association_not_filled(self):
  x=report(0,240)
  self.assertTrue(all(r['sripati_ayana_candidates'] is None and r['bphs_ayana_component'] is None for r in x['rows']))
  self.assertIsNone(x['rows'][2]['bphs_paksha_candidates']['selected_paksha_rupa'])
  self.assertIsNone(x['total_strength'])
 def test_out_of_domain_not_clipped_or_replaced(self):
  x=report(0,240,declinations={'Sun':23.6,'Moon':25},declination_profile='supplied comparison fixture')
  self.assertIsNotNone(x['rows'][0]['sripati_ayana_candidates']);self.assertIsNone(x['rows'][0]['bphs_ayana_component'])
  self.assertEqual(x['rows'][0]['bphs_declination_domain_status'],'outside_named_formula_domain')
  self.assertIsNone(x['rows'][1]['sripati_ayana_candidates'])
 def test_cli_executes_separate_profiles(self):
  import subprocess,sys,json
  r=subprocess.run([sys.executable,'-m','engine.luminary_profile_report','--sun-longitude','0','--moon-longitude','240','--sun-declination','10','--declination-profile','supplied fixture'],capture_output=True,text=True)
  self.assertEqual(r.returncode,0,r.stderr)
  x=json.loads(r.stdout);self.assertEqual(len(x['rows']),3);self.assertIsNone(x['selected_strength_profile'])
  s=x['rows'][0]['bphs_ayana_component'];self.assertEqual(s['sun_motion_identity']['motion_rupa'],s['ayana_rupa'])
