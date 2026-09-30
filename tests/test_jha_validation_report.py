import json,subprocess,sys,unittest
from engine.jha_validation_report import jha_validation_report as report

class JhaValidationTests(unittest.TestCase):
 def test_collected_existing_checks_and_closed_gates(self):
  x=report();self.assertEqual(x['status'],'source_validation_not_forecast');self.assertEqual(len(x['checks']),6)
  self.assertEqual(len(x['local_precedence_scope']),1)
  for k in ('selected_natal_total','selected_calendar_profile','global_precedence','empirical_outcome_accuracy'):self.assertIsNone(x[k])
  self.assertFalse(x['balaji_personal_consultation_replication_verified']);self.assertFalse(x['public_release_rights_cleared'])
  self.assertNotIn('accuracy_percentage',x)
 def test_cli_executes(self):
  r=subprocess.run([sys.executable,'-m','engine.jha_validation_report'],capture_output=True,text=True)
  self.assertEqual(r.returncode,0,r.stderr);x=json.loads(r.stdout)
  self.assertEqual(x['checks']['directed_geometry_and_supplied_drigbala']['synthetic_drigbala_bridge_check']['candidate_drigbala_virupa_rational'],'155')
 def test_profile_boundaries_and_page_references(self):
  x=report();self.assertEqual(x['checks']['normalized_birth_balance_and_solar_target']['source']['pdf_page'],310)
  self.assertIsNone(x['checks']['printed_strength_thresholds_and_layout']['selected_threshold_profile'])
  self.assertTrue(x['critical_source_disagreements']);self.assertTrue(x['source_profile_boundaries'])
