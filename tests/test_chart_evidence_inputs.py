import unittest
from engine.chart_evidence_inputs import validate_sign_longitude
from engine.house_growth_scope import chart_house_growth_candidates
from engine.dual_owner_occupation_exception import dual_owner_occupation_exception
from engine.lagna_house_strength_connective import chart_lagna_strength_candidates
from engine.period_condition_report import period_condition_report

class ChartInputTests(unittest.TestCase):
 def test_coherent_labels_and_missing_not_filled(self):
  p={'Mars':{'longitude':30},'Venus':{'sign':'Taurus','longitude':30}}
  validate_sign_longitude(p);self.assertNotIn('sign',p['Mars'])
 def test_nonfinite_and_bool_longitude_rejected(self):
  for lon in (True,float('nan'),float('inf'),360,-1):
   with self.assertRaises(ValueError):validate_sign_longitude({'Mars':{'longitude':lon}})
 def test_new_bridges_reject_label_disagreement(self):
  p={'Mars':{'sign':'Aries','longitude':31}}
  for call in (lambda:dual_owner_occupation_exception('Aries',p),lambda:chart_lagna_strength_candidates(7,'Aries',p),lambda:chart_house_growth_candidates(7,'Aries',p,{},classification_profile='supplied')):
   with self.assertRaises(ValueError):call()
 def test_standalone_class_map_not_silently_ignored(self):
  for c in ({'Jupitr':'benefic'},{'Jupiter':'unknown'},[]):
   with self.assertRaises(ValueError):chart_house_growth_candidates(7,'Aries',{},c,classification_profile='supplied')
 def test_period_dual_ownership_scoped_to_actual_pair(self):
  x=period_condition_report('Aries',{},'Jupiter','Mercury')
  self.assertEqual({r['planet'] for r in x['xv29_own_other_house_exception']['rows']},{'Jupiter','Mercury'})
  self.assertEqual(period_condition_report('Aries',{},'Sun','Rahu')['xv29_own_other_house_exception']['rows'],[])
