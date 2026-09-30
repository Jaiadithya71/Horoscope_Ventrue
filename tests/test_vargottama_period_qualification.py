import unittest
from engine.vargottama_period_qualification import vargottama_period_qualification as q,chart_vargottama_period_qualifications

class VargottamaQualificationTests(unittest.TestCase):
 def test_specific_exception_not_global_precedence(self):
  for fall,eclipse in [(True,None),(None,True),(True,False),(False,True)]:
   self.assertEqual(q(True,fall,eclipse)['scoped_textual_result'],'mixed_in_this_scoped_verse')
  self.assertEqual(q(True,False,False)['scoped_textual_result'],'favorable_in_this_scoped_verse')
  self.assertIsNone(q(True,False,False)['personal_outcome'])
  self.assertIsNone(q(True,False,False)['global_precedence'])
 def test_unknown_not_absent(self):
  self.assertEqual(q(True,False,None)['scoped_textual_result'],'unresolved_qualifier')
  self.assertEqual(q(True,None,False)['scoped_textual_result'],'unresolved_qualifier')
  self.assertEqual(q(None,False,False)['scoped_textual_result'],'unresolved_vargottama')
  self.assertEqual(q(False,None,None)['scoped_textual_result'],'not_applicable')
  with self.assertRaises(ValueError):q(True,False,0)
 def test_chart_geometry_does_not_invent_uneclipsed(self):
  x=chart_vargottama_period_qualifications({'Sun':{'sign':'Aries','longitude':1},
       'Mercury':{'sign':'Pisces','longitude':359},'Rahu':{'sign':'Aries','longitude':1}})
  self.assertEqual(x['planets']['Sun']['scoped_textual_result'],'unresolved_qualifier')
  self.assertEqual(x['planets']['Mercury']['scoped_textual_result'],'mixed_in_this_scoped_verse')
  self.assertNotIn('Rahu',x['planets']);self.assertIsNone(x['active_period'])
