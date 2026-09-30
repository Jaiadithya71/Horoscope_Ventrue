import unittest
from engine.bhava_strength import bhava_digbala,WEAKEST
from engine.bhava_geometry import bhava_geometry

class BhavaStrengthTests(unittest.TestCase):
    def test_equal_geometry_original_lagna_fractions(self):
        g=bhava_geometry(0,270)['centres']
        for cat,v in (('human',1),('quadruped',.5),('watery',.5),('reptile',0)):
            self.assertEqual(bhava_digbala(1,cat,g,category_profile='supplied test category')['rupa'],v)
        for cat,weak in WEAKEST.items():
            strong=(weak+5)%12+1
            self.assertEqual(bhava_digbala(weak,cat,g,category_profile='test')['rupa'],0)
            self.assertEqual(bhava_digbala(strong,cat,g,category_profile='test')['rupa'],1)

    def test_real_geometry_not_half_by_house_count(self):
        g=bhava_geometry(10,300)['centres']
        x=bhava_digbala(1,'quadruped',g,category_profile='test')
        self.assertAlmostEqual(x['rupa'],110/180)
        self.assertNotEqual(x['rupa'],.5)
        self.assertIsNone(x['total_bhava_strength'])

    def test_validation(self):
        g=bhava_geometry(0,270)['centres']
        for h,cat,profile in ((0,'human','test'),(True,'human','test'),(1,'bird','test'),(1,'human','')):
            with self.assertRaises(ValueError):bhava_digbala(h,cat,g,category_profile=profile)
        with self.assertRaises(ValueError):bhava_digbala(1,'human',{1:0},category_profile='test')
