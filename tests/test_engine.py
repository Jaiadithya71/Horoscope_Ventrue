import datetime as dt
import unittest
from engine.forecast import forecast, moon_sign, position
from engine.benchmark import DATA, score
import json

class ForecastTests(unittest.TestCase):
    def test_jupiter_month_shift(self):
        self.assertEqual(forecast('2026-01-01','Aquarius')['placements']['Jupiter']['house_from_moon'],5)
        self.assertEqual(forecast('2026-07-01','Aquarius')['placements']['Jupiter']['house_from_moon'],6)

    def test_rahu_and_saturn(self):
        self.assertEqual(forecast('2026-12-10','Aquarius')['placements']['Rahu']['sign'],'Capricorn')
        self.assertEqual(forecast('2026-01-01','Leo')['placements']['Saturn']['house_from_moon'],8)

    def test_birth_moon_sign_requires_time(self):
        self.assertIn(moon_sign('2004-12-15','12:00','Asia/Kolkata'),[x for x in ('Aries','Taurus','Gemini','Cancer','Leo','Virgo','Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces')])

    def test_rule_source_citation(self):
        f=forecast('2026-01-01','Aquarius')['findings']
        self.assertTrue(any(x['source']=={'slug':'phaladeepika-1937','pdf_page':330,'chapter':'XXVI','sloka':19,'verified_against_page_image':True} for x in f))

    def test_benchmark_does_not_claim_unsupported_outcomes(self):
        s=score(json.loads(DATA.read_text()))
        self.assertEqual(s['counts'],{'chart_match':4,'unsupported':3})
        self.assertNotIn('accuracy',s)

if __name__=='__main__':unittest.main()
