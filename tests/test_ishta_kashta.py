import math
import unittest
from engine.ishta_kashta import ishta_kashta

class IshtaTests(unittest.TestCase):
    def test_original_sun_example_and_distinct_alternative(self):
        x=ishta_kashta(.957,.810,component_profile='printed Sripati Sun fixture')
        self.assertEqual(round(x['sripati_root_profile']['historical_ishta'],3),.880)
        self.assertEqual(round(x['sripati_root_profile']['historical_kashta'],3),.090)
        self.assertAlmostEqual(x['quoted_parashara_average_profile']['historical_ishta'],.8835)
        self.assertIsNone(x['selected_profile'])
        self.assertIsNone(x['total_strength'])

    def test_ranges_noncomplement_and_extremes(self):
        for a in (0,.2,.5,1):
            for b in (0,.1,.8,1):
                x=ishta_kashta(a,b,component_profile='test')
                s=x['sripati_root_profile'];p=x['quoted_parashara_average_profile']
                self.assertTrue(0<=s['historical_ishta']<=1)
                self.assertTrue(0<=s['historical_kashta']<=1)
                self.assertAlmostEqual(p['historical_ishta']+p['historical_kashta'],1)
        x=ishta_kashta(1,0,component_profile='test')['sripati_root_profile']
        self.assertEqual(x['historical_ishta'],0)
        self.assertEqual(x['historical_kashta'],0)

    def test_bad_or_undocumented_inputs(self):
        for bad in (-.01,1.01,float('inf'),float('nan')):
            with self.assertRaises(ValueError):ishta_kashta(bad,.5,component_profile='test')
        with self.assertRaises(ValueError):ishta_kashta(.5,.5,component_profile='')
