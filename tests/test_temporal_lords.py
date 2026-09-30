import unittest
from engine.temporal_lords import *

class TemporalLordTests(unittest.TestCase):
    def test_all_thirds_and_jupiter(self):
        for period,lords in THIRDS.items():
            for i,p in enumerate(lords):
                x=tribhaga(period,(i+.5)/3)
                self.assertEqual(x['active_lord'],p)
                self.assertEqual(sum(x['rupa_by_planet'].values()),2)
                self.assertEqual(x['rupa_by_planet']['Jupiter'],1)
        x=tribhaga('day',1/3)
        self.assertTrue(x['boundary_unresolved'])
        self.assertIsNone(x['active_lord'])
        self.assertIsNone(x['rupa_by_planet']['Sun'])
        self.assertEqual(x['rupa_by_planet']['Jupiter'],1)
        self.assertEqual(tribhaga('night',0)['active_lord'],'Moon')

    def test_original_historical_example(self):
        x=historical_lords(714404106135)
        self.assertEqual(x['elapsed_360_day_years'],1984455850)
        self.assertEqual(x['elapsed_30_day_months'],23813470204)
        self.assertEqual(x['remainders'],{'year':5,'month':6,'weekday':6})
        self.assertEqual(x['lords'],{'year':'Jupiter','month':'Venus','weekday':'Venus'})
        self.assertEqual(historical_lords(7)['lords']['weekday'],'Saturn')
        self.assertEqual(historical_lords(1)['lords']['weekday'],'Sun')

    def test_hour_cycle_printed_sequence(self):
        for i,p in enumerate(('Sun','Venus','Mercury','Moon','Saturn','Jupiter','Mars')):
            self.assertEqual(kala_hora('Sun',(i+.5)/24)['lord'],p)
        self.assertEqual(kala_hora('Sun',23.5/24)['lord'],'Mercury')
        self.assertEqual(kala_hora('Moon',0)['lord'],'Moon')
        self.assertIsNone(kala_hora('Sun',1/24)['lord'])

    def test_positional_disagreement_not_selected(self):
        x=positional_hora_candidates('Venus',14+31/60+46/3600,17+43/60+30/3600)
        self.assertAlmostEqual(x['doubled_arc_degrees'],23*30+23+36/60+32/3600)
        self.assertEqual(x['remainder'],2)
        self.assertEqual(x['candidates'],{'completed_signs_zero_based':'Moon','remainder_one_based':'Mercury'})
        self.assertIsNone(x['selected_lord'])

    def test_lord_fractions_missing(self):
        x=lord_components(year='Jupiter',month='Venus',weekday='Venus',hora='Moon')
        r=x['rupa_components_by_planet']
        self.assertEqual(r['Jupiter']['year'],.25)
        self.assertEqual(r['Venus']['month'],.5)
        self.assertEqual(r['Venus']['weekday'],.75)
        self.assertEqual(r['Moon']['hora'],1)
        self.assertIsNone(lord_components()['rupa_components_by_planet']['Sun']['year'])
        self.assertIsNone(x['total_strength'])

    def test_invalid_inputs(self):
        for bad in (-1,1,float('nan'),float('inf')):
            with self.assertRaises(ValueError):tribhaga('day',bad)
            with self.assertRaises(ValueError):kala_hora('Sun',bad)
        for bad in (-1,1.5,True,None):
            with self.assertRaises(ValueError):historical_lords(bad)
        with self.assertRaises(ValueError):tribhaga('civil',0)
        with self.assertRaises(ValueError):lord_components(year='Rahu')
        with self.assertRaises(ValueError):positional_hora_candidates('Sun',360,0)
