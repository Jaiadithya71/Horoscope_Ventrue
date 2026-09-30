import unittest
from decimal import Decimal
from engine.planetary_war import supplied_war_adjustment

class AdjustmentTests(unittest.TestCase):
 def call(self,**kw):
  opts=dict(winner='Mars',war_condition_confirmed=True,complete_prewar_totals=True,
   adjustment_profile='sripati_absolute_difference_per_supplied_latitude_unit_candidate',
   latitude_a=1,latitude_b=0,latitude_unit='degrees')
  opts.update(kw)
  return supplied_war_adjustment('Mars','Venus',6,4,**opts)
 def test_transfer_and_conservation(self):
  r=self.call();self.assertEqual(r['transfer_amount'],'2')
  self.assertEqual(sum(Decimal(x) for x in r['candidate_adjusted_totals'].values()),10)
  self.assertIsNone(r['engine_certified_total'])
 def test_units_exposed(self):
  a=self.call();b=self.call(latitude_a=60,latitude_unit='arcminutes')
  self.assertAlmostEqual(float(a['transfer_amount'])/float(b['transfer_amount']),60)
 def test_no_clipping(self):
  r=self.call(latitude_a=.1)
  self.assertEqual(r['negative_candidate_totals'],['Venus'])
 def test_gates(self):
  for opts in ({'winner':'Venus'},{'complete_prewar_totals':False},{'latitude_unit':None},{'latitude_a':0}):
   with self.assertRaises(ValueError):self.call(**opts)
 def test_quoted_profile(self):
  r=self.call(adjustment_profile='quoted_parashara_absolute_difference_candidate')
  self.assertEqual(r['transfer_amount'],'2')
