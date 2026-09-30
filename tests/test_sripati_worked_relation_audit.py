import unittest
from engine.sripati_worked_relation_audit import worked_relation_audit

class WorkedRelationTests(unittest.TestCase):
    def test_example_cannot_arbitrate_house_profile(self):
        x=worked_relation_audit()
        self.assertEqual(x['profile_match_counts'],{'rasi_relative':47,'lagna_bhava_relative':47})
        self.assertFalse(x['profiles_distinguished_by_example'])
        self.assertEqual(x['worked_houses'],{'Sun':1,'Moon':10,'Mars':12,'Mercury':12,'Jupiter':9,'Venus':1,'Saturn':1})
        failures=[(r['planet'],r['varga']) for r in x['rows'] if r['candidates']['rasi_relative']['matches_printed'] is False]
        self.assertEqual(failures,[('Jupiter','navamsa')])
        saturn=next(r for r in x['rows'] if r['planet']=='Saturn' and r['varga']=='dwadasamsa')
        self.assertEqual(saturn['geometry_owner'],'Jupiter')
        self.assertEqual(saturn['1919_printed_relation'],'enemy')
        self.assertIsNone(x['selected_strength_total'])
