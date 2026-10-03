import unittest
from engine.research_input_report import research_input_report
from engine.period_aspects import ASPECTS, HOUSE_ASPECT, PLANET_ASPECT, GUIDE

BIRTH = {'date': '1990-05-15', 'time': '10:30:00', 'timezone': 'Asia/Calcutta', 'latitude': 13.08, 'longitude': 80.27, 'place': 'Chennai'}
JARGON = ('rahu', 'ketu', 'saturn', 'jupiter', 'mars', 'venus', 'mercury', 'dasa', 'lord', 'house', 'lagna', 'planet', 'exalt', 'nakshatra')
BANNED = ('death', 'demise', 'wicked', 'gemstone', 'mantra', 'donat', 'ritual', 'puja')


class PeriodAspectsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lp = research_input_report(BIRTH)['life_periods']

    def test_every_period_has_all_six_areas_and_a_depth(self):
        for p in self.lp['periods']:
            self.assertEqual(list(p['aspects']), ASPECTS)
            self.assertIn(p['depth'], ('full', 'short'))
        full = [p['when'] for p in self.lp['periods'] if p['depth'] == 'full']
        self.assertEqual(full, ['now', 'next'])

    def test_quiet_areas_are_marked_not_padded(self):
        for p in self.lp['periods']:
            for a in p['aspects'].values():
                if a['status'] == 'quiet':
                    self.assertEqual(a['items'], [])
                    self.assertIsNone(a['guidance'])
                else:
                    self.assertTrue(a['items'] and a['guidance'])

    def test_surface_text_has_no_jargon_remedies_or_death_wording(self):
        texts = [v[0] for h in HOUSE_ASPECT.values() for a in h.values() for v in [a] for v in v if v] if False else []
        for h in HOUSE_ASPECT.values():
            for pair in h.values(): texts += [t for t in pair if t]
        for pl in PLANET_ASPECT.values():
            for t, _ in pl.values(): texts.append(t)
        for g in GUIDE.values(): texts += list(g.values())
        for p in self.lp['periods']:
            for a in p['aspects'].values(): texts.append(a['text'])
        for t in texts:
            low = t.lower()
            for w in JARGON + BANNED:
                self.assertNotIn(w, low, (t, w))

    def test_phase_areas_labelled_extension_data(self):
        for p in self.lp['periods']:
            for b in p['bhuktis']: self.assertIsInstance(b['phase_areas'], list)


if __name__ == '__main__':
    unittest.main()
