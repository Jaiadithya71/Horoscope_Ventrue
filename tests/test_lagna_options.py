import json
import unittest
from api.lagna import response_body
from engine.lagna_options import lagna_spans, lagna_for_known_sign
from engine.natal import natal_chart

CH = ('Asia/Kolkata', 13.08, 80.27)


class LagnaOptionsTest(unittest.TestCase):
    def test_spans_match_the_natal_chart_ascendant(self):
        r = lagna_spans('2000-01-01', *CH, '06:00', '10:00')
        self.assertEqual([s['lagna'] for s in r['spans']], ['Sagittarius', 'Capricorn', 'Aquarius'])
        for s in r['spans']:
            for t in (s['from'][11:], s['to'][11:], s['stand_in_time']):
                self.assertEqual(natal_chart('2000-01-01', t, CH[0], CH[1], CH[2], 'x')['ascendant']['sign'], s['lagna'])

    def test_spans_tile_the_window_without_gaps(self):
        r = lagna_spans('2000-01-01', *CH, '06:00', '10:00')
        self.assertEqual(sum(s['minutes'] for s in r['spans']), 241)
        self.assertTrue(r['spans'][0]['cut_by_window'] and not r['spans'][1]['cut_by_window'])

    def test_window_past_midnight(self):
        r = lagna_spans('2000-01-01', *CH, '23:00', '01:00')
        self.assertEqual(sum(s['minutes'] for s in r['spans']), 121)
        self.assertEqual(r['spans'][-1]['to'][:10], '2000-01-02')

    def test_known_lagna_gives_its_clock_span(self):
        r = lagna_for_known_sign('2000-01-01', *CH, 'Leo')
        self.assertTrue(r['spans'] and all(s['lagna'] == 'Leo' for s in r['spans']))
        s = r['spans'][0]
        self.assertEqual(natal_chart('2000-01-01', s['stand_in_time'], CH[0], CH[1], CH[2], 'x')['ascendant']['sign'], 'Leo')

    def test_known_lagna_orders_by_closeness_to_remembered_time(self):
        r = lagna_for_known_sign('2000-01-01', *CH, 'Taurus', around='23:30')
        self.assertTrue(len(r['spans']) >= 1)

    def test_rejections(self):
        for bad in ({'mode': 'window', 'date': '2000-01-01', 'timezone': 'Asia/Kolkata', 'latitude': 13, 'longitude': 80, 'start': '25:00', 'end': '10:00'},
                    {'mode': 'known', 'date': '2000-01-01', 'timezone': 'Asia/Kolkata', 'latitude': 13, 'longitude': 80, 'lagna': 'Dragon'},
                    {'mode': 'known', 'date': '2000-01-01', 'timezone': 'Nowhere/Land', 'latitude': 13, 'longitude': 80, 'lagna': 'Leo'},
                    {'mode': 'window', 'date': '2000-01-01', 'timezone': 'Asia/Kolkata', 'latitude': 80, 'longitude': 80, 'start': '06:00', 'end': '10:00'},
                    {'mode': 'x'}, {'mode': 'window', 'extra': 1}):
            self.assertEqual(response_body(json.dumps(bad).encode())[0], 400, bad)

    def test_api_ok(self):
        raw = json.dumps({'mode': 'window', 'date': '2000-01-01', 'timezone': 'Asia/Kolkata', 'latitude': 13.08, 'longitude': 80.27, 'start': '06:00', 'end': '10:00'}).encode()
        status, body = response_body(raw)
        self.assertEqual(status, 200)
        self.assertEqual(len(json.loads(body)['spans']), 3)


if __name__ == '__main__':
    unittest.main()
