import unittest
from engine.house_condition_report import house_condition_report

class HouseReportTests(unittest.TestCase):
 def test_scoped_conditions_not_global_winner(self):
  r=house_condition_report(7,'Aries',{'Venus':{'sign':'Virgo'},'Jupiter':{'sign':'Aries'}},{'Jupiter':'benefic'},classification_profile='supplied',strength_profile='externally verified fixture',bhava_strong=True,lord_strong=True,karaka_strong=True)
  self.assertTrue(r['xv5_scoped_recovery']['candidates'][0]['condition_evidence']['benefic_aspect_exception'])
  self.assertTrue(r['xv25_26_supplied_strength_conditions'][0]['condition_evidence']['all_three_strength_condition'])
  self.assertEqual(r['house_lord_debilitation_candidates']['planet'],'Venus')
  self.assertIsNone(r['global_precedence']);self.assertIsNone(r['personal_outcome'])
 def test_missing_degree_stays_unchecked(self):
  r=house_condition_report(7,'Aries',{'Venus':{'sign':'Libra'}},{},classification_profile='partial')
  self.assertEqual(r['xv25_26_supplied_strength_conditions'][1]['condition_evidence']['unchecked_alternative_planets'],['Venus'])

class HouseCliTests(unittest.TestCase):
 def run_cli(self,*extra):
  import subprocess,sys
  return subprocess.run([sys.executable,'-m','engine.house_condition_report',
   '--birth-date','2000-01-01','--birth-time','14:30','--birth-tz','Asia/Kolkata',
   '--birth-place','synthetic Chennai fixture','--birth-lat','13.08','--birth-lon','80.27',
   '--house','7','--classification-file','benchmarks/house_condition_classification_fixture.json',*extra],
   capture_output=True,text=True)
 def test_runnable_end_to_end(self):
  import json
  p=self.run_cli();self.assertEqual(p.returncode,0,p.stderr)
  x=json.loads(p.stdout)
  self.assertEqual(len(x['xv5_scoped_recovery']['candidates']),8)
  self.assertIsNone(x['personal_outcome']);self.assertIsNone(x['selected_strength_total'])
  self.assertEqual(x['xv25_26_supplied_strength_conditions'][0]['condition_evidence']['missing_strength'],['bhava','lord','karaka'])
 def test_bad_class_file_fail_closed(self):
  import tempfile,json
  with tempfile.NamedTemporaryFile(mode='w',suffix='.json') as f:
   json.dump({'profile':'bad','classes':{'Jupiter':'unknown'}},f);f.flush()
   p=self.run_cli('--classification-file',f.name)
   self.assertNotEqual(p.returncode,0);self.assertEqual(p.stdout,'')
 def test_truthy_strength_rejected(self):
  import tempfile,json
  with tempfile.NamedTemporaryFile(mode='w',suffix='.json') as f:
   json.dump({'profile':'bad','bhava':1},f);f.flush()
   p=self.run_cli('--strength-file',f.name)
   self.assertNotEqual(p.returncode,0);self.assertEqual(p.stdout,'')
 def test_missing_file_not_empty_classification(self):
  p=self.run_cli('--classification-file','/tmp/does-not-exist-house-classes.json')
  self.assertNotEqual(p.returncode,0);self.assertEqual(p.stdout,'')

 def test_condition_declarations_not_arbitration(self):
  import tempfile,json
  with tempfile.NamedTemporaryFile(mode='w',suffix='.json') as f:
   json.dump({'lord_eclipsed':False,'lord_inimical_sign':False,'xv6_clauses':{'all_three_weak':True,'afflicted_without_benefics':False,'adverse_relative_occupation':False}},f);f.flush()
   p=self.run_cli('--condition-file',f.name);self.assertEqual(p.returncode,0,p.stderr)
   r=json.loads(p.stdout)
   self.assertEqual([x['condition'] for x in r['xv6_supplied_connective_candidates']['candidates']],[False,True])
   self.assertEqual(len(r['xv3_lord_target_candidates']['candidates']),8)
   self.assertIsNone(r['personal_outcome'])
 def test_unknown_condition_key_fails(self):
  import tempfile,json
  with tempfile.NamedTemporaryFile(mode='w',suffix='.json') as f:
   json.dump({'automatic_global_winner':True},f);f.flush()
   p=self.run_cli('--condition-file',f.name)
   self.assertNotEqual(p.returncode,0);self.assertEqual(p.stdout,'')

 def test_input_schema_typos_not_ignored(self):
  import tempfile,json
  cases=[('--strength-file',{'profile':'test','bhavva':True}),
         ('--condition-file',{'xv6_clauses':[]}),
         ('--classification-file',{'profile':'test','classes':{},'selected_global_winner':True}),
         ('--classification-file',{'profile':True,'classes':{}}),
         ('--condition-file',[])]
  for flag,value in cases:
   with self.subTest(flag=flag,value=value), tempfile.NamedTemporaryFile(mode='w',suffix='.json') as f:
    json.dump(value,f);f.flush();p=self.run_cli(flag,f.name)
    self.assertNotEqual(p.returncode,0);self.assertEqual(p.stdout,'')

class HouseSeverityIntegrationTests(unittest.TestCase):
 def report(self,**kw):
  return house_condition_report(1,'Aries',{'Mars':{'sign':'Virgo'}},{},classification_profile='explicit fixture',**kw)
 def test_local_rules_remain_separate(self):
  r=self.report(strength_profile='external full profile',lord_strength_status='strong')
  rows=r['xv9_supplied_lord_severity_candidates']
  self.assertEqual(rows[0]['qualification']['scoped_textual_qualification'],'slight_injury_in_this_verse')
  self.assertEqual(rows[1]['qualification']['scoped_textual_qualification'],'unresolved_house')
  self.assertTrue(r['xv10_11_lordship_emphasis'][0]['scope_overlap'])
  self.assertIsNone(r['global_precedence']);self.assertIsNone(r['personal_outcome'])
 def test_false_not_weak(self):
  r=self.report(strength_profile='supplied condition only',lord_strong=False)
  self.assertEqual(r['xv9_supplied_lord_severity_candidates'][0]['qualification']['scoped_textual_qualification'],'unresolved_strength')
 def test_explicit_status_needs_profile(self):
  with self.assertRaises(ValueError):self.report(lord_strength_status='strong')
 def test_cli_separate_status(self):
  import tempfile,json
  with tempfile.NamedTemporaryFile(mode='w',suffix='.json') as f:
   json.dump({'profile':'external fixture','lord_status':'weak'},f);f.flush()
   p=HouseCliTests().run_cli('--strength-file',f.name)
   self.assertEqual(p.returncode,0,p.stderr)
   self.assertEqual(json.loads(p.stdout)['xv9_supplied_lord_severity_candidates'][0]['qualification']['supplied_strength_status'],'weak')
