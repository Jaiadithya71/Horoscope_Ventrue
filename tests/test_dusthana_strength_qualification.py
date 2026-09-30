import unittest
from engine.dusthana_strength_qualification import dusthana_strength_qualification as q,chart_dusthana_strength_qualifications as chart

class DusthanaQualifierTests(unittest.TestCase):
 def call(self,h,s):return q(h,supplied_strength_status=s,strength_profile='externally verified fixture',house_frame='supplied frame')
 def test_strong_is_not_favorable(self):
  for h in (6,8,12):
   r=self.call(h,'strong');self.assertEqual(r['scoped_textual_qualification'],'slight_injury_in_this_verse')
   self.assertIsNone(r['global_precedence']);self.assertIsNone(r['personal_outcome'])
   self.assertEqual(self.call(h,'weak')['scoped_textual_qualification'],'immensely_harmful_in_this_verse')
 def test_unknowns_and_nonmatch(self):
  self.assertEqual(self.call(6,None)['scoped_textual_qualification'],'unresolved_strength')
  self.assertEqual(self.call(None,'strong')['scoped_textual_qualification'],'unresolved_house')
  self.assertEqual(self.call(1,'weak')['scoped_textual_qualification'],'not_applicable')
 def test_invalid(self):
  for h in (True,0,13):
   with self.assertRaises(ValueError):self.call(h,'strong')
  with self.assertRaises(ValueError):self.call(6,'moderate')
 def test_chart_missing_and_shared_owner(self):
  r=chart('Aries',{'Mars':{'sign':'Virgo'}},{'Mars':'strong'},strength_profile='supplied fixture')
  rows=r['houses'];self.assertEqual(rows[0]['qualification']['lord_occupied_house'],6)
  self.assertEqual(rows[7]['qualification'],rows[0]['qualification'])
  self.assertIsNone(rows[1]['qualification']['lord_occupied_house'])
