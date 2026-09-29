import unittest
from engine.synthesis import lordship, aspects, structural_factors

class SynthesisTests(unittest.TestCase):
    def test_aquarius_lordship_and_safety(self):
        x=lordship('Aquarius')
        assert x['houses'][1]['lord']=='Jupiter'  # second
        assert x['houses'][10]['lord']=='Jupiter' # eleventh
        self.assertEqual(x['source']['pdf_page'],40)
        self.assertNotIn('outcome',x)

    def test_leo_saturn_aspects_are_structural(self):
        x=aspects('Saturn','Pisces','Leo')
        self.assertEqual([(t['relative_house_from_planet'],t['target_house_from_reference']) for t in x['targets']],[(3,10),(7,2),(10,5)])
        self.assertEqual(x['targets'][0]['topic_label'],'work')
        self.assertEqual(x['targets'][1]['topic_label'],'wealth')
        self.assertEqual(x['source']['pdf_page'],55)
        self.assertEqual(x['targets'][0]['topic_source']['pdf_page'],196)
        self.assertNotIn('outcome',x)
        self.assertEqual(aspects('Rahu','Aquarius','Leo')['targets'],[])

    def test_no_effect_from_structure_without_rule(self):
        x=structural_factors('Leo',{'Saturn':{'sign':'Pisces'},'Moon':{'sign':'Leo'}})
        self.assertEqual(x['planet_factors'][0]['rules_owned'],[6,7])
        self.assertIn('not a forecast',x['notice'])
        self.assertFalse(any('outcome' in row for row in x['planet_factors']))

if __name__=='__main__':unittest.main()
