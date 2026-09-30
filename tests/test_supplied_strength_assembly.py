import unittest
from engine.strength_layout import supplied_layout_with_aspects
from engine.degree_aspects import CLASSICAL

class SuppliedAssemblyTests(unittest.TestCase):
 def call(self,**kw):
  opts=dict(components=dict(sthana=1,kala=1,dig=1,natural=1,cheshta_including_ayana=2),
   layout='five_classes_inclusive_motion',complete=True,component_profile='explicit supplied fixture',
   target='Sun',target_longitude=0,aspecting_placements={p:{'longitude':180} for p in CLASSICAL if p!='Sun'},
   classifications={p:'benefic' for p in CLASSICAL if p!='Sun'},classification_profile='supplied fixture',
   war_treatment='confirmed_no_war')
  opts.update(kw);return supplied_layout_with_aspects(**opts)
 def test_assembly(self):
  r=self.call();self.assertEqual(float(r['candidate_total_rupa']),7.5)
  self.assertIsNone(r['engine_computed_full_strength'])
 def test_missing_never_zero(self):
  for opts in ({'complete':False},{'components':{'sthana':1}},{'classifications':{}},{'aspecting_placements':{}}):
   self.assertIsNone(self.call(**opts)['candidate_total_rupa'])
 def test_war_gate(self):
  with self.assertRaises(ValueError):self.call(war_treatment=None)
 def test_layouts_same(self):
  a=self.call();b=self.call(components=dict(sthana=1,kala=1,dig=1,natural=1,cheshta=1,ayana=1),layout='expanded_printed_rows')
  self.assertEqual(a['candidate_total_rupa'],b['candidate_total_rupa'])
