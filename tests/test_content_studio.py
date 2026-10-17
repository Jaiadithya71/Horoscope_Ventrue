"""Content studio cards: shape, citations, and honesty-gate labels."""
import unittest

from engine.content_studio import (NAKSHATRA_DATA, PLANETS, SIGNS12, WEEKDAYS,
                                   studio_index, studio_report, TOOLS)


class WeekdayCardTests(unittest.TestCase):
    def test_all_seven_days_build(self):
        for day in WEEKDAYS:
            r = studio_report('weekday', day)
            self.assertEqual(r['tool'], 'weekday')
            self.assertTrue(r['hook_ta'])
            self.assertTrue(r['cta_ta'])
            self.assertEqual(r['choice'], day)
            self.assertIn(r['hook_ta'], r['caption_text'])

    def test_weekday_is_honest_about_missing_direct_rule(self):
        r = studio_report('weekday', 'Friday')
        notice = r['notices'][0]['en'].lower()
        self.assertIn('no book', notice)
        self.assertIn('weekday of birth', notice)
        kinds = [b['kind'] for b in r['bullets']]
        self.assertIn('derived', kinds)  # the day-lord nature chain is labelled
        # the only cited hop is the weekday-lord mapping itself
        for b in r['bullets']:
            if b['kind'] == 'cited':
                self.assertIn('hora', b['en'])

    def test_unknown_day_rejected(self):
        with self.assertRaises(ValueError):
            studio_report('weekday', 'Someday')


class NakshatraCardTests(unittest.TestCase):
    def test_all_27_build_with_lord_and_deity(self):
        self.assertEqual(len(NAKSHATRA_DATA), 27)
        for name in NAKSHATRA_DATA:
            r = studio_report('nakshatra', name)
            self.assertTrue(any('dasha lord' in b['en'] for b in r['bullets']), name)
            self.assertTrue(any('Presiding deity' in b['en'] for b in r['bullets']), name)

    def test_deity_is_labelled_derived_with_notice(self):
        r = studio_report('nakshatra', 'Rohini')
        deity = [b for b in r['bullets'] if 'Presiding deity' in b['en']][0]
        self.assertEqual(deity['kind'], 'derived')
        self.assertIn('no direct', r['notices'][0]['en'].lower())
        # traits stay cited with a page
        traits = [b for b in r['bullets'] if b['kind'] == 'cited']
        self.assertTrue(all('PDF p.' in (b['source'] or '') for b in traits))

    def test_rohini_deity_chain_is_sun_list(self):
        r = studio_report('nakshatra', 'Rohini')  # dasha lord Moon
        deity = [b for b in r['bullets'] if 'Presiding deity' in b['en']][0]
        self.assertIn('Moon', deity['en'])
        self.assertIn('Amba (Parvati)', deity['en'])


class GrahaCardTests(unittest.TestCase):
    def test_all_nine_build_with_shanti_rule(self):
        for p in PLANETS:
            r = studio_report('graha', p)
            self.assertTrue(any('Shantis' in b['en'] for b in r['bullets']), p)
            self.assertTrue(all(b['kind'] == 'cited' for b in r['bullets']), p)
            for b in r['bullets']:
                self.assertTrue(b['source'], p)

    def test_disagreements_kept_visible(self):
        r = studio_report('graha', 'Jupiter')
        metal = [b for b in r['bullets'] if 'Substance' in b['en']][0]
        self.assertIn('gold', metal['en'])   # Phaladeepika II.30
        self.assertIn('silver', metal['en'])  # Brihat Jataka II.12
        self.assertIn('disagree', r['notices'][0]['en'])

    def test_nodes_have_no_invented_colour(self):
        r = studio_report('graha', 'Rahu')
        self.assertFalse(any('colour' in b['en'].lower() and b['kind'] == 'cited' and 'Grain' not in b['en']
                             for b in r['bullets'] if 'colour' in b['en'].lower()))


class SignCardTests(unittest.TestCase):
    def test_all_12_build_with_caveat(self):
        for s in SIGNS12:
            r = studio_report('sign', s)
            self.assertTrue(any('Kalapurusha' in b['en'] for b in r['bullets']), s)
            self.assertTrue(any('only when the Moon' in b['en'] for b in r['bullets']), s)

    def test_capricorn_traits_from_bj17(self):
        r = studio_report('sign', 'Capricorn')
        body = ' '.join(b['en'] for b in r['bullets'])
        self.assertIn('ch. XVII', body)
        self.assertIn('wandering nature', body)


class DispatchTests(unittest.TestCase):
    def test_unknown_tool_rejected(self):
        with self.assertRaises(ValueError):
            studio_report('planet', 'Sun')

    def test_index_covers_all_tools(self):
        idx = studio_index()
        self.assertEqual({t['id'] for t in idx['tools']}, set(TOOLS))
        for t in idx['tools']:
            self.assertTrue(t['choices'])
            for ch in t['choices']:
                r = studio_report(t['id'], ch['id'])  # every picker choice must build
                self.assertEqual(r['choice'], ch['id'])

    def test_deterministic(self):
        self.assertEqual(studio_report('nakshatra', 'Mula'), studio_report('nakshatra', 'Mula'))


if __name__ == '__main__':
    unittest.main()
