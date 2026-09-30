import unittest
from fractions import Fraction as F
from engine.bphs_jha_drigbala import bphs_jha_drigbala as drig
from engine.bphs_jha_special_aspect import CLASSICAL

class JhaDrigTests(unittest.TestCase):
 def calc(self,target='Sun',positions=None,classes=None):
  return drig(target,dict.fromkeys(CLASSICAL,0) if positions is None else positions,
   dict.fromkeys(set(CLASSICAL)-{target},'benefic') if classes is None else classes,
   coordinate_profile='synthetic common frame',classification_profile='supplied synthetic classification')
 def test_rational_bridge_extra_and_no_self(self):
  ps=dict.fromkeys(CLASSICAL,0);ps['Sun']=100
  x=self.calc(positions=ps);self.assertEqual(F(x['candidate_drigbala_virupa_rational']),F(155))
  row=next(r for r in x['rows'] if r['aspecting_planet']=='Jupiter')
  self.assertEqual(F(row['signed_quarter_virupa_rational']),F('12.5'));self.assertEqual(F(row['full_mercury_jupiter_extra_virupa_rational']),50)
  classes=dict.fromkeys(set(CLASSICAL)-{'Sun'},'malefic');x=self.calc(positions=ps,classes=classes)
  self.assertEqual(F(x['candidate_drigbala_virupa_rational']),F(25));self.assertIsNone(x['complete_total_strength'])
 def test_boundary_and_missing_block_totals(self):
  ps=dict.fromkeys(CLASSICAL,0);ps['Sun']=270;x=self.calc(positions=ps)
  self.assertIsNone(x['candidate_drigbala_virupa_rational']);self.assertEqual(x['blocked_planets'],['Jupiter','Saturn'])
  ps.pop('Sun');x=self.calc(positions=ps);self.assertEqual(len(x['blocked_planets']),6)
 def test_missing_class_even_zero(self):
  classes=dict.fromkeys(set(CLASSICAL)-{'Sun'},'benefic');del classes['Moon']
  x=self.calc(classes=classes);self.assertIsNone(x['candidate_drigbala_virupa_rational']);self.assertEqual(x['blocked_planets'],['Moon'])
 def test_source_and_invalid(self):
  self.assertEqual(self.calc()['source']['chapter'],28)
  for ps in ({'Rahu':0},{'Sun':True},{'Sun':360}):
   with self.assertRaises(ValueError):self.calc(positions=ps)
  with self.assertRaises(ValueError):self.calc(classes={'Moon':'automatic'})
