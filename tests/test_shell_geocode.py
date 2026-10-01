import json,unittest
from unittest import mock
from api.geocode import parse_candidates, geocode
PAYLOAD=[{'lat':'13.0827','lon':'80.2707','display_name':'Chennai, Tamil Nadu, India','category':'place','type':'city'},
         {'lat':'bad','lon':'1','display_name':'Broken row'},{'lat':'95','lon':'1','display_name':'Out of range'}]
class GeocodeTests(unittest.TestCase):
 def test_parse_filters_invalid(self):
  c=parse_candidates(PAYLOAD)
  self.assertEqual(len(c),1)
  self.assertEqual(c[0]['latitude'],13.0827)
  self.assertIn('Chennai',c[0]['display_name'])
 def test_geocode_empty_place(self):
  with self.assertRaises(ValueError):geocode('  ')
 def test_geocode_network_failure_is_friendly(self):
  with mock.patch('urllib.request.urlopen',side_effect=OSError('down')):
   with self.assertRaises(ValueError) as ctx:geocode('Chennai')
  self.assertIn('unavailable',str(ctx.exception))
class FakeResponse:
 def __enter__(self):return self
 def __exit__(self,*a):pass
 def read(self):return json.dumps(PAYLOAD).encode()
def test_live_shape(self=None):
 with mock.patch('urllib.request.urlopen',return_value=FakeResponse()):
  c=geocode('Chennai')
 assert c[0]['type']=='city'
class LiveShapeTest(unittest.TestCase):
 def test_geocode_parses_live_shape(self):
  with mock.patch('urllib.request.urlopen',return_value=FakeResponse()):
   c=geocode('Chennai')
  self.assertEqual(c[0]['type'],'city')
