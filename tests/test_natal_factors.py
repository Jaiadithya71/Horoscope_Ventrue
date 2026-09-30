import unittest
from engine.natal_factors import dignity, exchanges, mahapurusha, natal_factors

class NatalFactorTests(unittest.TestCase):
    def test_partial_strength_not_full_score(self):
        self.assertEqual(dignity('Jupiter','Cancer',95)['positional_rupa_candidates'][0]['rupa'],1)
        self.assertEqual(dignity('Saturn','Capricorn',280)['positional_rupa_candidates'][0]['rupa'],0.5)
        self.assertEqual(dignity('Saturn','Aries',10)['positional_rupa_candidates'][0]['rupa'],0)
        self.assertEqual(dignity('Mars','Gemini',63)['positional_rupa_candidates'],[])
        mercury=dignity('Mercury','Virgo',167)
        self.assertEqual(len(mercury['positional_rupa_candidates']),3)
        self.assertTrue(mercury['candidate_conflict'])
        self.assertTrue(dignity('Moon','Taurus')['candidate_conflict'])
        self.assertEqual(dignity('Rahu','Aries')['status'],'not_scored')
        with self.assertRaisesRegex(ValueError,'disagrees'):
            dignity('Jupiter','Cancer',125)

    def test_exchange_and_yoga_no_outcome(self):
        p={'Mars':{'sign':'Gemini'},'Mercury':{'sign':'Aries'},'Jupiter':{'sign':'Cancer'}}
        self.assertEqual(exchanges(p)[0]['planets'],['Mars','Mercury'])
        self.assertEqual(mahapurusha('Aries',p)[0]['name'],'Hamsa') # Jupiter in fourth
        self.assertEqual(mahapurusha('Taurus',p),[])
        self.assertFalse(any('outcome' in item for item in exchanges(p)+mahapurusha('Aries',p)))
        self.assertIn('No total strength score',natal_factors('Aries',p)['notice'])

if __name__=='__main__':unittest.main()
