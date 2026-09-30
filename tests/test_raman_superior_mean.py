import unittest
from decimal import Decimal as D
from engine.raman_superior_mean import raman_superior_mean as lookup,raman_superior_example_audit as audit

class SuperiorMeanTests(unittest.TestCase):
 def test_raw_table_errors_retained(self):
  x=lookup('Jupiter',600,12,epoch_clock_profile='fixture')
  self.assertEqual(x['printed_pieces'][0]['printed_entry'],'42.86')
  self.assertEqual(lookup('Mars',8000,12,epoch_clock_profile='fixture')['printed_pieces'][0]['printed_entry'],'232.55')
  self.assertEqual(lookup('Saturn',0,12,epoch_clock_profile='fixture')['epoch_constant'],'236.74')
 def test_worked_comparison_does_not_fit(self):
  x=audit();self.assertEqual([r['exact_raw_lookup_matches'] for r in x['rows']],[True,False,False])
  self.assertEqual(D(x['rows'][1]['lookup']['raw_mean_degrees']),D('232.0896'))
  self.assertEqual(D(x['rows'][2]['lookup']['raw_mean_degrees']),D('35.657'))
 def test_tens_and_negative_days(self):
  x=lookup('Mars',60,0,epoch_clock_profile='fixture');self.assertEqual(D(x['printed_pieces'][0]['motion_degrees']),D('31.44'))
  y=lookup('Mars',-60,0,epoch_clock_profile='fixture');self.assertEqual(D(y['raw_mean_degrees']),D('238.78'))
  self.assertIsNone(y['selected_unwrapped_mean'])
 def test_invalid_input(self):
  for v in (True,'NaN',100000):
   with self.assertRaises(ValueError):lookup('Mars',v,12,epoch_clock_profile='fixture')
