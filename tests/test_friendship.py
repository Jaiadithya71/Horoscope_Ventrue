import unittest
from engine.friendship import natural_relation, relationship_evidence, CLASSICAL
from engine.precedence import reconcile_claims

class FriendshipTests(unittest.TestCase):
    def test_directed_natural_relations(self):
        self.assertEqual(natural_relation('Moon','Mercury'),'friend')
        self.assertEqual(natural_relation('Mercury','Moon'),'enemy')
        self.assertEqual(natural_relation('Sun','Mercury'),'neutral')
        self.assertEqual(natural_relation('Saturn','Mars'),'enemy')
        for p in CLASSICAL:
            for q in CLASSICAL:
                if p!=q:self.assertIn(natural_relation(p,q),('friend','neutral','enemy'))
        with self.assertRaises(ValueError):natural_relation('Rahu','Sun')
        with self.assertRaises(ValueError):natural_relation('Sun','Sun')

    def test_preference_is_scoped_and_retains_both_facts(self):
        result=relationship_evidence({'Sun':{'sign':'Aries'},'Saturn':{'sign':'Cancer'}})
        pair=result['directed_pairs'][0]
        self.assertEqual(pair['natural_relation'],'enemy')
        self.assertTrue(pair['temporal_friend_condition'])
        self.assertEqual(pair['preferred_relation_evidence']['relation'],'enemy')
        self.assertEqual(pair['preferred_relation_evidence']['source']['sloka'],'10')
        self.assertIsNone(result['outcome_precedence'])
        self.assertEqual(relationship_evidence({'Rahu':{'sign':'Aries'}})['directed_pairs'],[])

    def test_scoped_preference_cannot_unlock_outcomes(self):
        claim={'topic':'work','interval':'2026','polarity':'positive','citation':'IV.10',
               'strength_verified':True,'timing_verified':True}
        self.assertEqual(reconcile_claims([claim])[0]['status'],'abstain')
