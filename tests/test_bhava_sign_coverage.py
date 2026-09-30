import unittest
from engine.bhava_geometry import bhava_geometry
from engine.bhava_sign_coverage import bhava_sign_coverage
from engine.natal import natal_chart

class BhavaCoverageTests(unittest.TestCase):
 def test_wrap_and_exact_sign_boundaries_conserve_arc(self):
  for asc,mc in [(0,270),(10,280),(359,269),(14.5,290),(100,20)]:
   x=bhava_sign_coverage(bhava_geometry(asc,mc))
   self.assertAlmostEqual(sum(r['house_arc_degrees'] for r in x['houses']),360)
   for r in x['houses']:
    self.assertAlmostEqual(sum(s['arc_degrees'] for s in r['sign_segments']),r['house_arc_degrees'])
    self.assertAlmostEqual(sum(s['geometric_fraction_of_house'] for s in r['sign_segments']),1)
    self.assertTrue(all(0<s['arc_degrees']<=30 for s in r['sign_segments']))
    self.assertIsNone(r['selected_lord_strength_weighting']);self.assertIsNone(r['total_bhava_strength'])
  x=bhava_sign_coverage(bhava_geometry(0,270))['houses'][0]
  self.assertEqual([s['sign'] for s in x['sign_segments']],['Pisces','Aries'])
  self.assertEqual([s['lord'] for s in x['sign_segments']],['Jupiter','Mars'])
  self.assertEqual([s['arc_degrees'] for s in x['sign_segments']],[15,15])
 def test_actual_natal_evidence_not_equal_house_substitution(self):
  n=natal_chart('2000-01-01','14:30','Asia/Kolkata',13.08,80.27,'synthetic fixture')
  x=n['bhava_sign_coverage']
  self.assertEqual(len(x['houses']),12)
  self.assertTrue(any(abs(r['house_arc_degrees']-30)>1 for r in x['houses']))
 def test_malformed_cycle_rejected(self):
  with self.assertRaises(ValueError):bhava_sign_coverage({'boundary_after_house':{}})
  with self.assertRaises(ValueError):bhava_sign_coverage({'boundary_after_house':{h:0 for h in range(1,13)}})
