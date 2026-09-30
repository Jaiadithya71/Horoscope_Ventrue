import unittest
from fractions import Fraction as F
from engine.bphs_jha_special_aspect import bphs_jha_aspect_candidates as aspect

class JhaSpecialTests(unittest.TestCase):
 def calc(self,p,d):return aspect(p,0,d,coordinate_profile='synthetic common frame')
 def test_interior_formulas(self):
  for p,d,v in [('Saturn',86,47),('Saturn',250,40),('Saturn',280,20),('Mars',80,45),('Mars',192,60),('Mars',220,50),('Jupiter',100,50),('Jupiter',130,40),('Jupiter',220,50),('Jupiter',250,40)]:
   self.assertEqual(F(self.calc(p,d)['determinate_unsigned_virupa_rational']),v)
 def test_boundary_disagreements_are_not_fixed(self):
  for p,vs in [('Saturn',['30','60']),('Jupiter',['0','15'])]:
   x=self.calc(p,270);self.assertIsNone(x['determinate_unsigned_virupa_rational'])
   self.assertEqual(x['distinct_unsigned_virupa_rational'],vs);self.assertIsNone(x['boundary_convention_selected'])
  for d in (30,60,90,120,150,180,210,240,270,300,330):
   self.assertIsNotNone(self.calc('Mars',d)['determinate_unsigned_virupa_rational'])
 def test_general_planets_and_directed_wrap(self):
  for p in ('Sun','Moon','Mercury','Venus'):
   self.assertEqual(self.calc(p,255)['determinate_unsigned_virupa_rational'],'45/2')
  x=aspect('Saturn',350,76,coordinate_profile='synthetic');self.assertEqual(x['determinate_unsigned_virupa_rational'],'47')
 def test_range_provenance_and_invalid(self):
  for p in ('Saturn','Mars','Jupiter'):
   for d in range(360):
    for v in self.calc(p,d)['distinct_unsigned_virupa_rational']:self.assertTrue(0<=F(v)<=60)
  x=self.calc('Saturn',86);self.assertEqual(x['source']['slokas'],'8-12')
  self.assertIsNone(x['selected_geometry_profile']);self.assertIsNone(x['whole_strength'])
  with self.assertRaises(ValueError):self.calc('Rahu',86)
