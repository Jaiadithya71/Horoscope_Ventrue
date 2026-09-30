import unittest
from decimal import Decimal as D
from engine.raman_war_candidate import raman_supplied_war_candidate as war

class RamanWarTests(unittest.TestCase):
 def call(self,a='Mars',b='Mercury',x=None,y=None,**kwargs):
  return war(a,b,x or {'sthana':100,'dig':20,'kala_up_to_hora':30},y or {'sthana':90,'dig':20,'kala_up_to_hora':12},winner=kwargs.get('winner',a),war_condition_confirmed=True,partial_bases_complete=True,coordinate_profile='explicit fixture winner',diameter_difference_profile='absolute_printed_arcseconds_candidate')
 def test_partial_base_exact_transfer(self):
  x=self.call();self.assertEqual(D(x['candidate_yuddhabala_virupa']),10)
  self.assertEqual(x['candidate_kala_up_to_hora_after_war_virupa'],{'Mars':'40','Mercury':'2'})
  self.assertIsNone(x['complete_kalabala']);self.assertIsNone(x['selected_winner'])
 def test_printed_large_diameters_and_negative_no_clip(self):
  x=self.call('Jupiter','Saturn');self.assertEqual(x['printed_disc_diameters_arcseconds'],{'Jupiter':'190.4','Saturn':'158.0'})
  x=self.call(y={'sthana':0,'dig':0,'kala_up_to_hora':0});self.assertIn('Mercury',x['negative_kala_candidates'])
 def test_full_total_and_missing_part_rejected(self):
  for parts in [{'total':150},{'sthana':100,'dig':20},{'sthana':True,'dig':20,'kala_up_to_hora':30}]:
   with self.assertRaises(ValueError):self.call(x=parts)
