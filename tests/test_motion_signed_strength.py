import unittest
from engine.motional_strength import cheshtabala
from engine.signed_aspect_strength import signed_aspect_adjustment
from engine.degree_aspects import CLASSICAL

class MotionSignedTests(unittest.TestCase):
    def test_original_five_angles(self):
        for p,a,rounded in (('Mars',325.989,.189),('Mercury',217.059,.794),('Jupiter',216.760,.796),('Venus',351.085,.050),('Saturn',11.270,.063)):
            self.assertEqual(round(cheshtabala(p,a)['rupa'],3),rounded)
        # Original table appears truncated rather than rounded for three values.
        for p,a,printed in (('Jupiter',216.760,.795),('Venus',351.085,.049),('Saturn',11.270,.062)):
            self.assertLess(abs(cheshtabala(p,a)['rupa']-printed),.001)

    def test_fold_and_rejections(self):
        for a,v in ((0,0),(90,.5),(180,1),(270,.5)):
            self.assertEqual(cheshtabala('Mars',a)['rupa'],v)
        for p,a in (('Sun',90),('Moon',90),('Rahu',90),('Mars',360),('Mars',-1),('Mars',float('nan'))):
            with self.assertRaises(ValueError):cheshtabala(p,a)

    def test_signed_explicit_profile(self):
        ps={p:{'longitude':180} for p in CLASSICAL if p!='Sun'}
        cs={p:'benefic' for p in ps}
        x=signed_aspect_adjustment('Sun',0,ps,cs,classification_profile='test supplied all benefic')
        self.assertEqual(x['signed_adjustment_rupa'],1.5)
        cs['Mars']='malefic'
        self.assertEqual(signed_aspect_adjustment('Sun',0,ps,cs,classification_profile='test supplied')['signed_adjustment_rupa'],1)
        self.assertIsNone(x['total_strength'])

    def test_missing_and_bad_classes(self):
        ps={p:{'longitude':180} for p in CLASSICAL if p!='Sun'}
        cs={p:'benefic' for p in ps};del cs['Mercury']
        x=signed_aspect_adjustment('Sun',0,ps,cs,classification_profile='test supplied')
        self.assertIsNone(x['signed_adjustment_rupa'])
        self.assertIn('Mercury',x['missing_planets_or_classifications'])
        cs['Mercury']='neutral'
        with self.assertRaises(ValueError):signed_aspect_adjustment('Sun',0,ps,cs,classification_profile='test')
        with self.assertRaises(ValueError):signed_aspect_adjustment('Sun',0,ps,{},classification_profile='')

class SuppliedMeanTrueTests(unittest.TestCase):
    def test_both_commentary_branches_equal_explicit_algebra(self):
        from engine.motional_strength import cheshta_from_supplied_mean_true as calc
        for mean,true in ((80,60),(60,80),(359,361),(-1,1)):
            x=calc('Mars',mean,true,250,input_profile='synthetic supplied inputs',coordinate_branch='explicit synthetic unwrap')
            self.assertAlmostEqual(x['cheshtakendra_degrees'],(250-(mean+true)/2)%360)
            self.assertIsNone(x['total_strength'])
            self.assertEqual(x['source']['pdf_page'],71)

    def test_wrap_is_not_silently_selected(self):
        from engine.motional_strength import cheshta_from_supplied_mean_true as calc
        a=calc('Mars',359,1,250,input_profile='synthetic',coordinate_branch='literal')
        b=calc('Mars',359,361,250,input_profile='synthetic',coordinate_branch='unwrapped across zero')
        self.assertNotEqual(a['cheshtakendra_degrees'],b['cheshtakendra_degrees'])
        self.assertAlmostEqual(abs(a['cheshtakendra_degrees']-b['cheshtakendra_degrees']),180)
        for profile,branch,mean in (('', 'literal', 0),('synthetic','',0),('synthetic','literal',float('nan'))):
            with self.assertRaises(ValueError):calc('Mars',mean,1,250,input_profile=profile,coordinate_branch=branch)
