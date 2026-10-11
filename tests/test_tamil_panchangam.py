import unittest,datetime as dt,json
from engine.natal import natal_chart
from engine.tamil_panchangam import tamil_panchangam,_sexagesimal
from api.calculate import response_body
from api.geocode import parse_candidates
B=dict(date='2026-01-01',time='12:00',timezone='Asia/Kolkata',latitude=9+55/60,longitude=78+7/60,place='Synthetic Madurai')
class TamilSheetTests(unittest.TestCase):
 def sheet(self,**changes):
  b={**B,**changes};return tamil_panchangam(b,natal_chart(**b))
 def test_site_sample_independent_angles(self):
  p=self.sheet();self.assertEqual(p['tamil_solar_date']['day'],17);self.assertEqual(p['tamil_solar_date']['month'],'மார்கழி');self.assertEqual(p['tithi_index_1_based'],13);self.assertEqual(p['pada'],2);self.assertEqual(p['tamil_solar_date']['year_name'],'விசுவாசுவ');self.assertEqual(len(p['chart_signs']),10);self.assertAlmostEqual(p['ayanamsa_degrees'],24.221835,places=5)
 def test_true_node_explicit_mean_preserved(self):
  a=natal_chart(**B);b=natal_chart(**B,node_mode='true');self.assertEqual(a['node_mode'],'mean');self.assertAlmostEqual(b['placements']['Rahu']['longitude'],316.6923074,places=6);self.assertNotEqual(a['placements']['Rahu']['longitude'],b['placements']['Rahu']['longitude']);self.assertEqual(a['placements']['Moon'],b['placements']['Moon'])
 def test_pre_sunrise_uses_previous_actual_event(self):
  p=self.sheet(time='03:00');self.assertTrue(p['sunrise_anchor'].startswith('2025-12-31'));self.assertGreater(p['udayadi_nazhikai'],40);self.assertLess(p['udayadi_nazhikai'],60)
 def test_polar_no_fake_events(self):
  p=self.sheet(date='2026-06-21',latitude=80.,longitude=20.,timezone='Europe/Oslo');self.assertIsNone(p['sunrise']);self.assertIsNone(p['udayadi_nazhikai']);self.assertEqual(p['tamil_solar_date']['status'],'unavailable')
 def test_london_offset_birth_date(self):
  p=self.sheet(date='2000-01-01',timezone='Europe/London',latitude=51.5,longitude=-7/60);self.assertEqual(p['utc_offset_seconds'],0);self.assertEqual(p['birth_local'],'2000-01-01T12:00:00+00:00')
 def test_local_dates_do_not_use_utc_day(self):
  p=self.sheet(date='2000-01-01',time='00:30');self.assertTrue(p['birth_local'].startswith('2000-01-01'));self.assertEqual(p['weekday'],'சனி')
 def test_sidereal_clock_wrap(self):
  self.assertEqual(_sexagesimal(23.9999999),'00:00:00');self.assertEqual(_sexagesimal(-1),'23:00:00')
 def test_zone_hint_not_fixed_offset(self):
  candidates=parse_candidates([{'lat':'51.50853','lon':'-0.12574','display_name':'London'}]);self.assertEqual(candidates[0]['timezone'],'Europe/London')
 def test_api_opt_in_and_bad_options(self):
  status,data=response_body(json.dumps({'birth':B,'tamil_view':True,'node_mode':'true'}).encode());p=json.loads(data);self.assertEqual(status,200);self.assertEqual(p['tamil_panchangam']['node_mode'],'true');self.assertIsNone(p['selected_calendar_profile'])
  for bad in [{'node_mode':'not-a-node'},{'tamil_view':'yes'},{'arbitrary':'field'}]:self.assertEqual(response_body(json.dumps({'birth':B,**bad}).encode())[0],400)
 def test_sunrise_external_chennai_minute_reference(self):
  # Drik Chennai 11 Oct 2026 fetched 12 Oct: sunrise 05:59, sunset17:52, minute precision.
  p=self.sheet(date='2026-10-11',latitude=13.08784,longitude=80.27847)
  for key,clock in [('sunrise','05:59'),('sunset','17:52')]:
   actual=dt.datetime.fromisoformat(p[key]);expected=dt.datetime.fromisoformat('2026-10-11T'+clock+'+05:30');self.assertLess(abs((actual-expected).total_seconds()),120)

 def test_tamil_year_boundary(self):
  early=self.sheet(date='2026-04-13')['tamil_solar_date'];late=self.sheet(date='2026-04-15')['tamil_solar_date'];self.assertEqual(early['year_name'],'விசுவாசுவ');self.assertEqual(late['year_name'],'பராபவ');self.assertEqual(late['month'],'சித்திரை')
