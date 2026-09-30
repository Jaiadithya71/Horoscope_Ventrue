import unittest
from engine.rectified_strength import rectify_supplied_total as calc

class RectifiedStrengthTests(unittest.TestCase):
    def test_seven_original_product_pairs(self):
        # PDF87-88 values explicitly supplied, not reconstructed by engine.
        rows=(('Sun',9.015,.880,.090,7.9332,.81135),
              ('Moon',8.197,.453,.539,3.713241,4.418183),
              ('Mars',7.731,.355,.519,2.744505,4.012389),
              ('Mercury',6.209,.201,.442,1.248009,2.744378),
              ('Jupiter',8.613,.384,.408,3.307392,3.514104),
              ('Venus',7.459,.210,.300,1.56639,2.2377),
              ('Saturn',3.844,.052,.947,.199888,3.640268))
        for p,total,i,k,a,b in rows:
            x=calc(p,total,i,k,complete=True,total_profile='original supplied printed III total',factor_profile='original IV supplied factors')
            self.assertAlmostEqual(x['rectified_ishta_rupa'],a)
            self.assertAlmostEqual(x['rectified_kashta_rupa'],b)
            self.assertIsNone(x['engine_computed_full_strength'])
            self.assertIsNone(x['aspect_rectification'])

    def test_partial_refuses_and_provenance_required(self):
        kw=dict(complete=False,total_profile='partial synthetic',factor_profile='synthetic')
        x=calc('Sun',1,.5,.5,**kw)
        self.assertIsNone(x['rectified_ishta_rupa'])
        for change in ({'complete':1},{'total_profile':''},{'factor_profile':''}):
            with self.assertRaises(ValueError):calc('Sun',1,.5,.5,**(kw|change))
        for p,t,i,k in (('Rahu',1,.5,.5),('Sun',-1,.5,.5),('Sun',float('nan'),.5,.5),('Sun',1,1.1,.5)):
            with self.assertRaises(ValueError):calc(p,t,i,k,**kw)
