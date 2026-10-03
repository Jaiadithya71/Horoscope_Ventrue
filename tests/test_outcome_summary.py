import unittest
from datetime import datetime, timezone
from engine.research_input_report import research_input_report
from engine.outcome_summary import outcome_summary

BIRTH = {'date': '1990-05-15', 'time': '10:30:00', 'timezone': 'Asia/Calcutta', 'latitude': 13.08, 'longitude': 80.27, 'place': 'Chennai'}
AS_OF = datetime(2026, 10, 3, tzinfo=timezone.utc)


class OutcomeSummaryTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = research_input_report(BIRTH)
        cls.out = outcome_summary(cls.report, AS_OF)

    def test_report_carries_summary(self):
        self.assertEqual([t['id'] for t in self.report['outcome_summary']['topics']], ['career', 'marriage', 'wealth', 'strength', 'timing', 'periods'])

    def test_each_topic_has_plain_fields_and_no_conditionals_in_headline(self):
        for t in self.out['topics']:
            self.assertIn(t['confidence'], ('steady', 'tentative'))
            self.assertTrue(t['headline'] and t['text'])
            self.assertNotIn(' if ', ' ' + t['headline'].lower() + ' ')
            self.assertNotIn('wicked', (t['text'] + ' '.join(t['points'])).lower())
            self.assertNotIn('wife', t['headline'].lower())

    def test_example_levels_are_stable(self):
        lv = {t['id']: t['level'] for t in self.out['topics']}
        self.assertEqual(lv['marriage'], 'some')
        self.assertEqual(lv['wealth'], 'some')
        self.assertEqual(lv['strength'], 'strong')

    def test_periods_topic_speaks_about_the_person(self):
        t = next(x for x in self.out['topics'] if x['id'] == 'periods')
        self.assertIn('Right now', t['points'][0])

    def test_surface_text_has_no_astrology_jargon(self):
        words = ('rahu', 'ketu', 'dasa', 'bhukti', 'lord', 'exalt', 'malefic', 'benefic', 'lagna', 'navamsa', 'classical', 'saturn', 'jupiter', 'mars', 'venus', 'mercury', 'moon ', 'sun ')
        for t in self.out['topics']:
            surface = (t['title'] + ' ' + t['headline'] + ' ' + t['text'] + ' ' + ' '.join(t['points'])).lower()
            for w in words:
                self.assertNotIn(w, surface, (t['id'], w))

    def test_house_model_disagreement_lowers_confidence_not_hides(self):
        import copy
        r = copy.deepcopy(self.report)
        for row in r['wealth_conditional']['rows']:
            row['status_by_house_model'] = {'whole_sign': 'met', 'sripati_degree_bhava': 'not_met'}
            row['status'] = 'house_model_dependent'
        w = next(x for x in outcome_summary(r, AS_OF)['topics'] if x['id'] == 'wealth')
        self.assertEqual(w['confidence'], 'tentative')
        self.assertEqual(w['level'], 'quiet')

    def test_adverse_rows_move_to_mixed(self):
        import copy
        r = copy.deepcopy(self.report)
        for row in r['marriage_conditional']['rows']:
            if row['rule_id'] == 'phaladeepika-viii-3-sun-in-7':
                row['status'] = 'met'; row['status_by_house_model'] = {'whole_sign': 'met', 'sripati_degree_bhava': 'met'}
        for row in r['marriage_conditional']['rows']:
            if not row.get('adverse_marital_status_text') and row['status'] in ('met', 'house_model_dependent'):
                row['status'] = 'not_met'; row['status_by_house_model'] = {'whole_sign': 'not_met', 'sripati_degree_bhava': 'not_met'}
        m = next(x for x in outcome_summary(r, AS_OF)['topics'] if x['id'] == 'marriage')
        self.assertEqual(m['level'], 'mixed')


if __name__ == '__main__':
    unittest.main()
