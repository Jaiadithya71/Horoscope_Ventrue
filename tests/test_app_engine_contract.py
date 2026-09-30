"""Tonight's display paths and unknown semantics, not astronomical truth fixtures."""
import json,subprocess,sys,unittest
from engine.research_input_report import research_input_report

BIRTH={'date':'2000-01-01','time':'14:30','timezone':'Asia/Kolkata','latitude':13.0,'longitude':80.0,'place':'synthetic contract fixture'}
REPORT_TYPES={'status':str,'natal_chart':dict,'query_pair_input_coverage':list,'active_period_inferred':bool,
 'supplied_strength_evidence':list,'strength_evidence_origin':str,'strength_requirements':dict,
 'precedence_requirements':dict,'notice':str}
NULL_GATES=('selected_complete_strength','selected_calendar_profile','global_outcome','empirical_accuracy')

class AppContractTests(unittest.TestCase):
 def test_minimal_report_display_paths_and_unknowns(self):
  x=research_input_report(BIRTH)
  for key,kind in REPORT_TYPES.items():self.assertIsInstance(x[key],kind,key)
  for key in NULL_GATES:self.assertIsNone(x[key],key)
  for key in ('query_convention_condition_evidence','explicit_pair_input_coverage','explicit_period_pair_evidence'):self.assertIsNone(x[key],key)
  self.assertFalse(x['active_period_inferred']);self.assertEqual(x['query_pair_input_coverage'],[])
  n=x['natal_chart']
  for key in ('birth_utc','birth_place','model','notice'):self.assertIsInstance(n[key],str)
  for key in ('latitude','longitude'):self.assertIsInstance(n[key],float)
  self.assertIsInstance(n['ascendant']['sign'],str);self.assertIsInstance(n['ascendant']['longitude_display_5dp'],float)
  self.assertEqual(set(n['placements']),{'Sun','Moon','Mercury','Venus','Mars','Jupiter','Saturn','Rahu'})
  for p in n['placements'].values():
   self.assertIsInstance(p['sign'],str);self.assertIsInstance(p['longitude_display_5dp'],float)
   self.assertIsInstance(p['retrograde'],bool);self.assertIsInstance(p['whole_sign_house_from_ascendant'],int)
   self.assertIn('at_sandhi',p['sripati_degree_house']);self.assertIn('source',p['sripati_degree_house'])
  star=n['moon_nakshatra']
  for key in ('name','sign','convention'):self.assertIsInstance(star[key],str)
  for key in ('index_1_based','pada'):self.assertIsInstance(star[key],int)
  self.assertIsInstance(star['source'],dict)
  periods=n['moon_periods']
  self.assertIsInstance(periods['initial_lord'],str);self.assertIsInstance(periods['initial_remaining_solar_years'],float)
  for key in ('date_limit','method_note'):self.assertIsInstance(periods[key],str)
  for row in periods['periods']:
   self.assertIsInstance(row['lord'],str)
   for key in ('start_solar_years_after_birth','end_solar_years_after_birth'):self.assertIsInstance(row[key],(int,float))
 def test_cli_file_snapshot_paths_stay_compatible(self):
  r=subprocess.run([sys.executable,'-m','engine.research_input_report','--input-json','profiles/research/synthetic-birth-input.json'],capture_output=True,text=True,timeout=30)
  self.assertEqual(r.returncode,0,r.stderr);x=json.loads(r.stdout)
  for key in REPORT_TYPES:self.assertIn(key,x)
  self.assertEqual(x['explicit_period_pair_evidence']['main_lord'],'Jupiter')
  for key in NULL_GATES:self.assertIsNone(x[key])
  self.assertFalse(x['active_period_inferred'])
 def test_query_paths_are_named_candidates_not_selected_dates(self):
  x=research_input_report(BIRTH,query_instant='2026-01-01T00:00:00+00:00')
  routes=x['query_convention_condition_evidence'];self.assertEqual(len(routes['profile_condition_routes']),9)
  self.assertIsNone(routes['selected_profile']);self.assertIsNone(x['selected_calendar_profile'])
  for row in routes['profile_condition_routes']:
   self.assertIsInstance(row['calendar_profile'],str);self.assertIsInstance(row['birth_balance_profile'],str)
   self.assertIn('calendar_status',row);self.assertIn('lord_path',row)
  self.assertFalse(x['active_period_inferred'])
