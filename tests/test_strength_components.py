import unittest
from engine.strength_components import components
from engine.natal_factors import natal_factors

class StrengthComponentTests(unittest.TestCase):
    def test_house_candidates_preserve_verse_difference(self):
        result=components('Aries',{'Venus':{'sign':'Cancer','retrograde':False},'Mars':{'sign':'Capricorn','retrograde':True},'Sun':{'sign':'Taurus'},'Moon':{'sign':'Gemini'}})
        v=result['planets']['Venus']
        self.assertEqual([x['rupa'] for x in v['house_strength_candidates']],[1,0.25])
        self.assertTrue(v['house_candidate_conflict'])
        self.assertTrue(v['directional_house_condition']['matched'])
        self.assertEqual(result['planets']['Sun']['house_strength_candidates'][0]['rupa'],0.5)
        self.assertEqual(result['planets']['Moon']['house_strength_candidates'][0]['rupa'],0.25)
        self.assertTrue(result['planets']['Mars']['retrograde_motional_condition']['matched'])
        self.assertIsNone(result['total_strength'])

    def test_ordinal_not_total_and_unknown_motion(self):
        result=components('Aries',{'Mercury':{'sign':'Aries'},'Saturn':{'sign':'Libra'},'Rahu':{'sign':'Leo'}})['planets']
        self.assertEqual(result['Mercury']['natural_strength_order']['ordinal'],3)
        self.assertFalse(result['Mercury']['house_candidate_conflict'])
        self.assertIsNone(result['Mercury']['retrograde_motional_condition']['matched'])
        self.assertEqual(result['Rahu']['status'],'not_scored')
        self.assertTrue(result['Saturn']['directional_house_condition']['matched'])
        self.assertEqual(result['Saturn']['house_strength_candidates'][1]['source']['pdf_page'],74)
        with self.assertRaises(ValueError):components('Aries',{'Mars':{'sign':'Cancer','retrograde':'yes'}})

    def test_integrated_partial_only(self):
        result=natal_factors('Aries',{'Sun':{'sign':'Aries','longitude':10}})
        self.assertEqual(result['strength_components']['status'],'partial_evidence_only')
        self.assertNotIn('outcome',result)
