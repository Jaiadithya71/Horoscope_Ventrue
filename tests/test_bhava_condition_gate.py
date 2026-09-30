import unittest
from engine.bhava_condition_gate import audit_bhava_conditions

class BhavaGateTests(unittest.TestCase):
    def test_unknowns_do_not_become_adverse(self):
        x=audit_bhava_conditions(5)
        self.assertIsNone(x['all_three_strength_condition'])
        self.assertIsNone(x['conflict'])
        self.assertEqual(x['unchecked_alternative_planets'],['Jupiter'])
        self.assertEqual(x['status'],'abstain')
        x=audit_bhava_conditions(5,bhava_strong=False,lord_strong=True,karaka_strong=True,strength_profile='fixture')
        self.assertFalse(x['all_three_strength_condition'])
        self.assertIsNone(x['selected_polarity'])

    def test_competing_condition_cannot_be_overridden(self):
        x=audit_bhava_conditions(5,bhava_strong=True,lord_strong=True,karaka_strong=True,
                                strength_profile='explicit test',planet_houses={'Jupiter':5})
        self.assertTrue(x['conflict'])
        self.assertEqual(x['quoted_alternative_planets_matched'],['Jupiter'])
        self.assertIsNone(x['selected_polarity'])
        x=audit_bhava_conditions(5,bhava_strong=True,lord_strong=True,karaka_strong=True,
                                strength_profile='explicit test',planet_houses={'Jupiter':6})
        self.assertFalse(x['conflict'])
        self.assertEqual(x['status'],'abstain')

    def test_bad_inputs(self):
        for house in (0,13,True,1.5):
            with self.assertRaises(ValueError):audit_bhava_conditions(house)
        with self.assertRaises(ValueError):audit_bhava_conditions(5,bhava_strong=True)
        with self.assertRaises(ValueError):audit_bhava_conditions(5,bhava_strong=1,strength_profile='test')
        with self.assertRaises(ValueError):audit_bhava_conditions(5,planet_houses={'Jupiter':False})
