import unittest
from engine.bphs_declination_ayana import supplied_bphs_declination_ayana as ayana
from engine.continuous_strength import ayanabala_candidates

class BphsDeclinationTests(unittest.TestCase):
 def test_equator_and_extrema(self):
  for p in ('Sun','Moon','Mercury','Mars','Jupiter','Venus','Saturn'):
   x=ayana(p,0,declination_profile='supplied fixture')
   self.assertEqual(x['ayana_rupa'],1 if p=='Sun' else .5)
   self.assertIsNone(x['total_strength'])
  self.assertEqual(ayana('Sun',23.45,declination_profile='fixture')['ayana_rupa'],2)
  self.assertEqual(ayana('Sun',-23.45,declination_profile='fixture')['ayana_rupa'],0)
  self.assertEqual(ayana('Moon',-23.45,declination_profile='fixture')['ayana_rupa'],1)
  self.assertEqual(ayana('Mercury',-23.45,declination_profile='fixture')['ayana_rupa'],1)
 def test_sripati_not_substituted_and_identity_not_redoubled(self):
  x=ayana('Sun',10,declination_profile='supplied fixture')
  self.assertNotEqual(x['ayana_rupa'],ayanabala_candidates('Sun',10)['candidates'][1]['rupa'])
  self.assertEqual(x['sun_motion_identity']['motion_rupa'],x['ayana_rupa'])
  self.assertIsNone(x['selected_sripati_ayana'])
 def test_invalid_and_out_of_range_rejected(self):
  for value in (True,float('nan'),23.451,-24):
   with self.assertRaises(ValueError):ayana('Sun',value,declination_profile='fixture')
  with self.assertRaises(ValueError):ayana('Sun',0,declination_profile='')
