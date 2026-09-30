import unittest
from decimal import Decimal as D
from engine.raman_strength_composition import raman_supplied_composition as compose,raman_printed_composition_audit as audit

class RamanCompositionTests(unittest.TestCase):
 def call(self,parts,complete=True):return compose(parts,declared_complete=complete,component_profile='supplied Raman fixture',war_treatment='confirmed_no_war')
 def parts(self):return {'sthana':100,'dig':20,'kala_including_ayana':30,'chesta_excluding_ayana':10,'natural':5,'signed_drik':-5}
 def test_signed_source_layout_and_missing_gate(self):
  x=self.call(self.parts());self.assertEqual(D(x['candidate_sum_virupa']),160)
  self.assertIsNone(self.call(self.parts(),False)['candidate_sum_rupa'])
  parts=self.parts();parts['signed_drik']=None;self.assertIsNone(self.call(parts)['candidate_sum_virupa'])
 def test_duplicate_ayana_and_inclusive_motion_rejected(self):
  for key in ('ayana','cheshta_including_ayana'):
   parts=self.parts();parts[key]=20
   with self.assertRaises(ValueError):self.call(parts)
 def test_arithmetic_disagreements_and_unknowns_preserved(self):
  a=audit();rows={x['planet']:x for x in a['rows']}
  self.assertEqual(rows['Mercury']['sum_candidates'][0]['sum_minus_printed_total_virupa'],'0.00')
  self.assertGreater(D(rows['Mercury']['division_minus_printed_rupa']),D('.1'))
  self.assertEqual(rows['Mars']['sum_candidates'][0]['sum_minus_printed_total_virupa'],'3.00')
  self.assertEqual(len(rows['Saturn']['sum_candidates']),2)
  self.assertIsNone(rows['Sun']['printed_components_virupa'][3]);self.assertFalse(a['coherent_full_chart_benchmark'])
