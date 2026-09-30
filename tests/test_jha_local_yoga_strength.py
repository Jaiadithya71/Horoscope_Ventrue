import unittest
from engine.jha_local_yoga_strength import local_yoga_strength_candidate as compare

class JhaLocalStrengthTests(unittest.TestCase):
 def rows(self):return [{'planet':p,'house':9,'yoga_reference':'supplied hypothetical yoga','role':r,'total_virupa':v,'declared_complete':True,'source_strength_profile':'synthetic Jha complete declaration'} for p,r,v in [('Jupiter','fortune_increasing',400),('Saturn','fortune_decreasing',410)]]
 def calc(self,rows=None):return compare(9,self.rows() if rows is None else rows,scope_profile='supplied same-house hypothesis',strength_profile='synthetic Jha complete declaration')
 def test_local_maximum_never_outcome(self):
  x=self.calc();self.assertEqual(x['unique_arithmetic_leader'],'Saturn');self.assertIsNone(x['selected_effect']);self.assertIsNone(x['global_rank'])
  self.assertFalse(x['supplied_totals_independently_verified']);self.assertFalse(x['group_strength_pooling_rule_verified'])
 def test_ties_and_partial_missing_incompatible(self):
  rows=self.rows();rows[0]['total_virupa']=410;x=self.calc(rows);self.assertEqual(x['arithmetic_maximum_contributors'],['Jupiter','Saturn']);self.assertIsNone(x['unique_arithmetic_leader'])
  for key,value in [('declared_complete',False),('total_virupa',None),('source_strength_profile','Raman different layout'),('house',10)]:
   rows=self.rows();rows[0][key]=value;x=self.calc(rows);self.assertEqual(x['blocked_contributors'],['Jupiter']);self.assertIsNone(x['arithmetic_maximum_virupa_rational'])
 def test_exact_rational_unknownrole_and_source(self):
  rows=self.rows();rows[1]['total_virupa']='800/2';rows[1]['role']='unknown';x=self.calc(rows)
  self.assertIsNone(x['unique_arithmetic_leader']);self.assertEqual(x['source']['slokas'],'37-38')
 def test_invalid_schema_units_and_boolean(self):
  for key,value in [('total_virupa',True),('total_virupa',-1),('total_virupa','NaN'),('declared_complete',1),('planet','Rahu'),('house',True),('role','automatic')]:
   rows=self.rows();rows[0][key]=value
   with self.assertRaises(ValueError):self.calc(rows)
  rows=self.rows();rows[0]['extra']=1
  with self.assertRaises(ValueError):self.calc(rows)
