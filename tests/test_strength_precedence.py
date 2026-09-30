import unittest
from engine.strength_precedence import condition_precedence,check_supplied_total,THRESHOLDS

class PrecedenceTests(unittest.TestCase):
    def test_scope_not_global_priority(self):
        x=condition_precedence('Mars','Cancer',95,True,False)
        self.assertEqual(x['condition_evidence'][0]['source']['sloka'],'4')
        self.assertIsNone(x['total_strength'])
        self.assertIsNone(x['global_outcome_precedence'])
        self.assertFalse(x['unresolved_conflict'])
        x=condition_precedence('Mercury','Virgo',167,True,True)
        self.assertTrue(x['unresolved_conflict'])
        self.assertEqual(x['condition_evidence'][-1]['positional_rupa_candidate'],0)
        self.assertEqual(condition_precedence('Moon','Cancer',95)['component_emphasis']['kind'],'paksha')
        self.assertEqual(condition_precedence('Rahu','Aries')['status'],'not_scored')
        with self.assertRaises(ValueError):condition_precedence('Mars','Aries',retrograde='yes')

    def test_totals_must_be_explicitly_complete(self):
        for planet,threshold in THRESHOLDS.items():
            self.assertIsNone(check_supplied_total(planet,threshold)['meets_book_threshold'])
            self.assertTrue(check_supplied_total(planet,threshold,True)['meets_book_threshold'])
            self.assertFalse(check_supplied_total(planet,threshold-0.01,True)['meets_book_threshold'])
        for total in (-1,float('nan'),float('inf')):
            with self.assertRaises(ValueError):check_supplied_total('Sun',total,True)
