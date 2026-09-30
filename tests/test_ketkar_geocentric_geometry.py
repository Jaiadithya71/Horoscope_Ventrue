import unittest
from engine.ketkar_geocentric_geometry import geocentric_from_heliocentric,geometry_example

class GeometryTests(unittest.TestCase):
 def test_inner_quadrant_and_projection(self):
  r=geocentric_from_heliocentric(0,90,1,.5)
  self.assertAlmostEqual(r['longitude_degrees'],26.565051177)
  self.assertAlmostEqual(r['latitude_degrees'],0)
 def test_outer_and_wrap(self):
  r=geocentric_from_heliocentric(359,1,1,5)
  self.assertTrue(0<r['longitude_degrees']<1)
 def test_latitude_and_radius(self):
  r=geocentric_from_heliocentric(0,0,1,1,45)
  self.assertAlmostEqual(r['latitude_degrees'],26.565051177)
  self.assertGreater(r['spatial_distance'],r['ecliptic_distance'])
 def test_singular_and_invalid(self):
  with self.assertRaises(ValueError):geocentric_from_heliocentric(0,180,1,1)
  with self.assertRaises(ValueError):geocentric_from_heliocentric(0,0,1,-1)
 def test_example_not_validation(self):
  r=geometry_example()
  self.assertAlmostEqual(r['computed_zero_latitude_candidate']['longitude_degrees'],327.87601476)
  self.assertFalse(r['full_historical_ephemeris_verified'])
  self.assertFalse(r['physical_radius_vs_ecliptic_projection_verified'])

 def test_source_ecliptic_radius_and_corrected_latitude(self):
  r=geometry_example()
  self.assertTrue(r['source_labels_input_as_ecliptic_radius'])
  self.assertAlmostEqual(r['computed_corrected_geocentric_latitude_arcmin'],-145.80805395)
  self.assertEqual(round(r['computed_corrected_geocentric_latitude_arcmin'],1),-145.8)
  self.assertNotEqual(r['heliocentric_latitude_candidates_arcmin']['-352.6']['latitude_degrees'],r['heliocentric_latitude_candidates_arcmin']['-353.4']['latitude_degrees'])
