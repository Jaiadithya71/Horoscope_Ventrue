import unittest
from engine.precedence import reconcile_claims

class PrecedenceTests(unittest.TestCase):
    def test_conflicting_rules_abstain_without_arbitrary_priority(self):
        items=[{'topic':'work','interval':'2026','polarity':'positive','citation':'book p.10',
                'strength_verified':True,'timing_verified':True},
               {'topic':'work','interval':'2026','polarity':'negative','citation':'book p.12',
                'strength_verified':True,'timing_verified':True}]
        self.assertEqual(reconcile_claims(items)[0]['status'],'abstain')
        self.assertTrue(reconcile_claims(items)[0]['conflict'])
        items[1]['polarity']='positive';items[1]['strength_verified']=False
        self.assertFalse(reconcile_claims(items)[0]['conflict'])
        self.assertEqual(reconcile_claims(items)[0]['missing_evidence'],['strength_verified'])
        self.assertEqual(reconcile_claims([]),[])

if __name__=='__main__':unittest.main()
