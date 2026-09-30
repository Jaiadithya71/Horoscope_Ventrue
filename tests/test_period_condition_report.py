import unittest
from engine.period_condition_report import period_condition_report
from engine.natal import natal_chart

class PeriodReportTests(unittest.TestCase):
 def test_integrated_scopes_do_not_vote_or_pick_calendar(self):
  n=natal_chart('2000-01-01','14:30','Asia/Kolkata',13.08,80.27,'synthetic fixture')
  x=period_condition_report(n['ascendant']['sign'],n['placements'],'Jupiter','Mercury')
  self.assertTrue(x['period_school_conflict']['unresolved_school_conflict'])
  for k in ('personal_outcome','global_precedence','selected_strength_total','selected_calendar'):self.assertIsNone(x[k])
  self.assertEqual(len(x['unfavorable_house_candidates']['candidates']),2)
  self.assertEqual(len(x['vargottama_qualification_candidates']),2)
  for r in x['vargottama_qualification_candidates']:self.assertIsNone(r['selected_result'])
  for r in n['placements'].values():self.assertNotIn('overpowered_sun_rays',r)
 def test_missing_nodes_and_no_conditionless_conclusion(self):
  x=period_condition_report('Aries',{},'Rahu','Ketu')
  self.assertFalse(x['period_school_conflict']['scope_match'])
  self.assertEqual(x['lordship_emphasis']['dual_owner_evidence'],[])
  for r in x['vargottama_qualification_candidates']:
   self.assertIsNone(r['base_qualification']);self.assertEqual(r['commentary_conditioned_candidates'],[])
  self.assertIsNone(x['personal_outcome'])

class PeriodCliGeometryTests(unittest.TestCase):
 def run_cli(self,*extra):
  import sys,subprocess,json
  p=subprocess.run([sys.executable,'-m','engine.period_condition_report','--birth-date','2000-01-01','--birth-time','14:30','--birth-tz','Asia/Kolkata','--birth-place','synthetic fixture','--birth-lat','13.08','--birth-lon','80.27','--main-lord','Jupiter','--sub-lord','Mercury',*extra],capture_output=True,text=True)
  self.assertEqual(p.returncode,0,p.stderr)
  return json.loads(p.stdout)
 def test_default_does_not_select_geometry(self):
  x=self.run_cli();self.assertFalse(x['degree_geometry_input_context']['requested'])
  self.assertIsNone(x['exact_sandhi_period_gate']['geometry_profile'])
  self.assertTrue(all('degree_bhava_geometry' in r['missing_inputs'] for r in x['exact_sandhi_period_gate']['rows']))
 def test_explicit_modern_geometry_executes_with_provenance(self):
  x=self.run_cli('--include-modern-degree-geometry')
  self.assertTrue(x['degree_geometry_input_context']['available'])
  self.assertIn('Swiss',x['exact_sandhi_period_gate']['geometry_profile'])
  self.assertTrue(all(not r['missing_inputs'] for r in x['exact_sandhi_period_gate']['rows']))
  for r in x['exact_sandhi_period_gate']['rows']:self.assertIsNone(r['selected_period_outcome'])
  self.assertTrue(x['period_school_conflict']['unresolved_school_conflict'])
  self.assertIsNone(x['global_precedence'])
