import unittest
from fractions import Fraction as F
from engine.bphs_jha_general_aspect import bphs_jha_general_aspect as aspect,jha_printed_aspect_audit

class JhaAspectTests(unittest.TestCase):
 def calc(self,a,b):return aspect(a,b,coordinate_profile='synthetic common degree frame')
 def test_directed_and_cross_zero(self):
  self.assertEqual(F(self.calc(10,265)['unsigned_aspect_virupa_rational']),F('22.5'))
  self.assertEqual(F(self.calc(265,10)['unsigned_aspect_virupa_rational']),F('37.5'))
  self.assertEqual(self.calc(350,75)['directed_difference_degrees_rational'],'85')
 def test_general_knots_and_range(self):
  for d,v in [(0,0),(30,0),(60,15),(90,45),(120,30),(150,0),(180,60),(300,0),(359,0)]:
   self.assertEqual(F(self.calc(0,d)['unsigned_aspect_virupa_rational']),v)
  for d in range(360):self.assertTrue(0<=F(self.calc(0,d)['unsigned_aspect_virupa_rational'])<=60)
 def test_independent_worked_arithmetic(self):
  x=jha_printed_aspect_audit();rows=x['general_worked_rows']
  self.assertEqual(F(rows[0]['exact_minus_printed_rational']),0)
  self.assertEqual(F(rows[1]['exact_minus_printed_virupa_seconds_rational']),F('0.5'))
  self.assertEqual(F(x['saturn_printed_multiplication_check']['exact_minus_printed_rational']),20)
  self.assertFalse(x['special_geometry_enabled'])
 def test_provenance_and_invalid(self):
  x=self.calc(0,86);self.assertEqual(x['source']['chapter'],27)
  self.assertFalse(x['special_planet_rules_applied']);self.assertIsNone(x['selected_geometry_profile'])
  for bad in (True,-1,360,'NaN','Infinity'):
   with self.assertRaises(ValueError):self.calc(bad,0)
  with self.assertRaises(ValueError):aspect(0,86,coordinate_profile='')
