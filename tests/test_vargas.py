import unittest
from engine.vargas import six_vargas,varga_owner_evidence

class VargaTests(unittest.TestCase):
    def test_page_checked_six_divisions(self):
        a={x['varga']:x for x in six_vargas(12)['vargas']}
        self.assertEqual(len(a),6)
        self.assertEqual(a['hora']['owner'],'Sun')
        self.assertIsNone(a['hora']['sign'])
        self.assertEqual(a['drekkana']['sign'],'Leo')
        self.assertEqual(a['navamsa']['sign'],'Cancer')
        self.assertEqual(a['dwadasamsa']['sign'],'Leo')
        self.assertEqual(a['trimsamsa']['owner'],'Jupiter')
        self.assertEqual(a['navamsa']['source']['pdf_page'],62)

    def test_even_sign_and_boundaries(self):
        a={x['varga']:x for x in six_vargas(45)['vargas']}
        self.assertEqual(a['hora']['owner'],'Sun')
        self.assertEqual(a['navamsa']['sign'],'Taurus')
        self.assertTrue(six_vargas(45)['vargottama'])
        self.assertEqual(a['trimsamsa']['owner'],'Jupiter')
        for lon,owner in ((0,'Mars'),(5,'Saturn'),(10,'Jupiter'),(18,'Mercury'),(25,'Venus'),(30,'Venus'),(35,'Mercury'),(42,'Jupiter'),(50,'Saturn'),(55,'Mars')):
            self.assertEqual(six_vargas(lon)['vargas'][-1]['owner'],owner)
        self.assertEqual(six_vargas(2.5)['vargas'][4]['part_1_based'],2)
        self.assertEqual(six_vargas(10)['vargas'][2]['part_1_based'],2)
        for i,start in enumerate((0,9,6,3)*3):
            self.assertEqual(six_vargas(i*30)['vargas'][3]['sign'],('Aries','Capricorn','Libra','Cancer')[i%4])

    def test_owners_not_numeric_strength(self):
        result=varga_owner_evidence('Mars',0)
        self.assertTrue(result['vargas'][0]['own_owner'])
        self.assertEqual(result['vargas'][0]['natural_relation_to_owner'],'self')
        self.assertEqual(result['score_status'],'not_scored')
        self.assertNotIn('total_strength',result)
        for lon in (-1,360,float('nan'),float('inf')):
            with self.assertRaises(ValueError):six_vargas(lon)
        self.assertIsNone(varga_owner_evidence('Rahu',0)['vargas'][0]['natural_relation_to_owner'])
