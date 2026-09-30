import unittest
from decimal import Decimal as D
from engine.bphs_supplied_drigbala import bphs_supplied_drigbala as drig,CLASSICAL

class BphsDrigTests(unittest.TestCase):
 def call(self,target='Sun',amounts=None,classes=None):
  others=[p for p in CLASSICAL if p!=target]
  return drig(target,amounts if amounts is not None else dict.fromkeys(others,60),classes if classes is not None else dict.fromkeys(others,'benefic'),aspect_profile='supplied degree amount fixture',classification_profile='supplied fixture')
 def test_full_extra_distinct_from_quarter_only(self):
  x=self.call();self.assertEqual(D(x['candidate_drigbala_virupa']),210)
  self.assertEqual(D(x['candidate_drigbala_rupa']),D('3.5'))
  self.assertIsNone(x['selected_geometry_profile']);self.assertIsNone(x['complete_total_strength'])
 def test_malefic_mercury_and_no_self_extra(self):
  kinds=dict.fromkeys(set(CLASSICAL)-{'Sun'},'malefic');x=self.call(classes=kinds)
  self.assertEqual(D(x['candidate_drigbala_virupa']),30)
  mercury=next(r for r in x['rows'] if r['aspecting_planet']=='Mercury')
  self.assertEqual(D(mercury['signed_quarter_virupa']),-15);self.assertEqual(D(mercury['full_mercury_jupiter_extra_virupa']),60)
  x=self.call('Mercury');self.assertEqual(D(x['candidate_drigbala_virupa']),150)
 def test_unknown_and_invalid_inputs(self):
  amounts=dict.fromkeys(set(CLASSICAL)-{'Sun'},0);classes=dict.fromkeys(amounts,'benefic');del classes['Moon']
  self.assertIsNone(self.call(amounts=amounts,classes=classes)['candidate_drigbala_virupa'])
  for v in (True,-1,61,'NaN'):
   amounts['Moon']=v
   with self.assertRaises(ValueError):self.call(amounts=amounts)
