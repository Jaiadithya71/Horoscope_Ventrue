import unittest
from engine.research_input_report import research_input_report
from engine.dasa_period_readings import life_periods, _ord

BIRTH = {'date': '1990-05-15', 'time': '10:30:00', 'timezone': 'Asia/Calcutta', 'latitude': 13.08, 'longitude': 80.27, 'place': 'Chennai'}


class DasaPeriodTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lp = research_input_report(BIRTH)['life_periods']

    def test_nine_periods_in_vimshottari_order(self):
        self.assertEqual([p['lord'] for p in self.lp['periods']], ['Sun', 'Moon', 'Mars', 'Rahu', 'Jupiter', 'Saturn', 'Mercury', 'Ketu', 'Venus'])

    def test_example_tones_follow_the_page_checked_rules(self):
        t = {p['lord']: p['tone'] for p in self.lp['periods']}
        self.assertEqual(t['Jupiter'], 'weak')    # 12th house and enemy sign
        self.assertEqual(t['Rahu'], 'weak')       # no benefic joins (XIX.15 exception unmet)
        self.assertEqual(t['Saturn'], 'strong')   # own sign, retrograde, 7th

    def test_every_period_cites_sources_and_has_bhuktis(self):
        for p in self.lp['periods']:
            self.assertTrue(p['rules'] and all(r['source']['verified_against_page_image'] for r in p['rules']))
            self.assertTrue(p['bhuktis'])
            self.assertTrue(p['summary'])
            self.assertLessEqual(p['years_about'][0], p['years_about'][1])

    def test_held_out_clauses_not_present(self):
        text = ' '.join(p['summary'] + ' '.join(p['house_lord_reading']) for p in self.lp['periods']).lower()
        for bad in ('death', 'demise', 'wicked'):
            self.assertNotIn(bad, text)

    def test_user_facing_period_text_has_no_planet_talk(self):
        for p in self.lp['periods']:
            low = (p['label'] + ' ' + p['you_text']).lower()
            for w in ('rahu', 'ketu', 'saturn', 'jupiter', 'mars', 'venus', 'mercury', 'sun ', 'moon ', 'dasa', 'lord', 'house'):
                self.assertNotIn(w, low, (p['lord'], w))

    def test_ordinal(self):
        self.assertEqual([_ord(n) for n in (1, 2, 3, 6, 11, 12)], ['1st', '2nd', '3rd', '6th', '11th', '12th'])


if __name__ == '__main__':
    unittest.main()
