import unittest
from decimal import Decimal
from engine.ketkar_true_planet import (true_sighra_radius, corrected_inantara,
                                     true_geocentric_longitude,mercury_example)

class TruePlanetTests(unittest.TestCase):
    def test_radius_composition(self):
        self.assertEqual(true_sighra_radius('1069.9','22.8','.7'),Decimal('1093.4'))
    def test_ratio_and_sign(self):
        self.assertEqual(corrected_inantara('-3',100,150),Decimal('-2'))
        self.assertEqual(corrected_inantara('3',100,150),Decimal('2'))
    def test_wrap(self):
        self.assertEqual(true_geocentric_longitude('1','-3'),Decimal('358'))
        self.assertEqual(true_geocentric_longitude('359','3'),Decimal('2'))
    def test_invalid_radii(self):
        with self.assertRaises(ValueError):corrected_inantara(1,0,1)
        with self.assertRaises(ValueError):true_sighra_radius(1,-2,0)
    def test_disagreement_retained(self):
        r=mercury_example()
        self.assertTrue(r['narrative_final_matches'])
        self.assertFalse(r['narrative_and_table_final_agree'])
        self.assertFalse(r['upstream_asphuta_rounding_verified'])
        self.assertEqual(r['candidate_half_up_correction_degrees'],'-3.081')
