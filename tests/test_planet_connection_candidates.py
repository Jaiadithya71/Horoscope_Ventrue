import unittest
from engine.planet_connection_candidates import planet_connection_candidates as relations

class PlanetConnectionTests(unittest.TestCase):
 def test_exchange_not_self_owned_same_sign(self):
  x=relations({'Mars':{'sign':'Libra'},'Venus':{'sign':'Aries'}},'Mars','Venus')
  self.assertTrue(all(r['condition_flags']['exchange'] for r in x['candidates']))
 def test_sign_kendra_not_exact_degree(self):
  x=relations({'Sun':{'sign':'Aries','longitude':1},'Moon':{'sign':'Cancer','longitude':95}},'Sun','Moon')
  self.assertTrue(x['candidates'][0]['condition_flags']['kendra'])
  self.assertFalse(x['candidates'][1]['condition_flags']['kendra'])
  self.assertIsNone(x['candidates'][1]['related_candidate'])
  self.assertIsNone(x['selected_related'])
 def test_literal_exact_wrap_trine(self):
  x=relations({'Mars':{'longitude':350},'Jupiter':{'longitude':110}},'Mars','Jupiter')
  self.assertTrue(x['candidates'][1]['condition_flags']['trikona'])
  self.assertIsNone(x['candidates'][0]['related_candidate'])
 def test_missing_nodes_and_self_not_clear(self):
  x=relations({'Rahu':{'sign':'Aries'},'Ketu':{'sign':'Taurus'}},'Rahu','Ketu')
  self.assertTrue(all(r['related_candidate'] is None for r in x['candidates']))
  self.assertTrue(all(r['related_candidate'] is None for r in relations({'Sun':{'sign':'Aries'}},'Sun','Sun')['candidates']))
