import unittest
from engine.research_input_report import research_input_report
from engine.who_you_are import TRAITS, who_you_are

BIRTH = {'date': '1990-05-15', 'time': '10:30:00', 'timezone': 'Asia/Calcutta', 'latitude': 13.08, 'longitude': 80.27, 'place': 'Chennai'}
JARGON = ('rahu', 'ketu', 'saturn', 'jupiter', 'mars', 'venus', 'mercury', 'dasa', 'lord', 'house', 'lagna', 'ascendant', 'sign ', 'exalt', 'nakshatra', 'planet')
BANNED = ('hypocrite', 'shameless', 'sinful', 'wicked', 'covetous', 'death', 'demise', 'false')


class WhoYouAreTest(unittest.TestCase):
    def test_all_twelve_signs_cover_slokas_1_to_12(self):
        self.assertEqual(sorted(v[0] for v in TRAITS.values()), list(range(1, 13)))

    def test_surface_text_has_no_jargon_or_held_out_verdicts(self):
        for sign, (n, text, pointers) in TRAITS.items():
            low = (text + ' ' + ' '.join(pointers)).lower()
            for w in JARGON + BANNED:
                self.assertNotIn(w, low, (sign, w))

    def test_report_carries_sourced_reading(self):
        w = research_input_report(BIRTH)['who_you_are']
        self.assertEqual(w['status'], 'temperament_not_tested_forecast')
        for k in ('outer_you', 'inner_you'):
            self.assertTrue(w[k]['text'] and w[k]['rules'])
            self.assertTrue(all(r['source']['verified_against_page_image'] for r in w[k]['rules']))
        self.assertEqual(w['outer_you']['rules'][0]['sign'], 'Cancer')


if __name__ == '__main__':
    unittest.main()
