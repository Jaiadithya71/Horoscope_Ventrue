import datetime as dt
import unittest
from engine.timing_conditional import _timeline, timing_conditional, YEAR_LENGTHS
from engine.natal import natal_chart


class TimingConditionalTests(unittest.TestCase):
    def test_brihat_jataka_worked_balance_example(self):
        # Krittika: Moon crosses it in 64gh42v, 24gh16v elapsed -> 3.7496 years of the Sun's 6 remain (printed 7278/1941).
        f=(24*60+16)/(64*60+42)
        tl=_timeline(dt.datetime(2000,1,1,tzinfo=dt.timezone.utc),f,2,360.0)
        first=tl[0]
        self.assertEqual(first['lord'],'Sun')
        self.assertAlmostEqual((first['_e']-first['_s']),7278/1941,places=9)

    def test_brihat_jataka_antardasa_example_venus_in_jupiter(self):
        # Punarvasu starts Jupiter (index 6). Venus antardasa in Jupiter dasa = 16*20/120 = 8/3 years.
        tl=_timeline(dt.datetime(2000,1,1,tzinfo=dt.timezone.utc),0.0,6,360.0)
        order=[a['lord'] for a in tl[0]['antardasas']]
        self.assertEqual(order,['Jupiter','Saturn','Mercury','Ketu','Venus','Sun','Moon','Mars','Rahu'])
        venus=tl[0]['antardasas'][4]
        self.assertAlmostEqual(venus['_e']-venus['_s'],8/3,places=9)
        self.assertAlmostEqual(tl[0]['antardasas'][-1]['_e'],16.0,places=9)

    def test_year_lengths_are_the_two_source_constants(self):
        self.assertEqual(YEAR_LENGTHS,{'savana_360':360.0,'soura_365_242264':365.242264})

    def test_chart_gives_four_unselected_timelines(self):
        c=natal_chart('1990-05-15','10:30:00','Asia/Calcutta',13.08,80.27,'Chennai')
        r=timing_conditional(c)
        self.assertEqual(len(r['timelines']),4);self.assertIsNone(r['selected_timeline'])
        a=r['birth_balance_alternatives']
        self.assertLess(a['difference_fraction'],0.05)
        for t in r['timelines'].values():
            self.assertGreater(len(t['mahadasas']),5)
            for m in t['mahadasas']:self.assertTrue(all(k in m for k in ('lord','start','end')))


if __name__=='__main__':unittest.main()
