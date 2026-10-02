import unittest
from engine.marriage_conditional import marriage_conditional as m


def chart(asc_sign,signs):
    """signs: planet -> sign index 0..11 (Aries=0); longitude mid-sign."""
    return {'ascendant':{'longitude':asc_sign*30+10},
            'placements':{p:{'longitude':i*30+15,'whole_sign_house_from_ascendant':(i-asc_sign)%12+1}
                          for p,i in signs.items()}}


BASE={'Sun':4,'Moon':3,'Mars':0,'Mercury':5,'Jupiter':8,'Venus':1,'Saturn':9}


def rule(r,rid):return next(x for x in r['rows'] if x['rule_id']==rid)


class MarriageConditionalTests(unittest.TestCase):
    def test_malefic_owner_in_seventh(self):
        # Aries Lagna: 7th is Libra, owned by Venus. Use Libra Lagna: 7th Aries, Mars owns it.
        c=chart(6,{**BASE,'Mars':0})
        self.assertEqual(rule(m(c),'phaladeepika-x-6-malefic-owner-in-7th')['status'],'met')
        c=chart(6,{**BASE,'Mars':3})
        self.assertEqual(rule(m(c),'phaladeepika-x-6-malefic-owner-in-7th')['status'],'not_met')

    def test_strong_benefic_seventh_lord_needs_strength(self):
        # Aries Lagna, 7th Libra, lord Venus.
        c=chart(0,BASE)
        self.assertEqual(rule(m(c),'phaladeepika-x-6-strong-benefic-7th-lord')['status'],'unresolved')
        self.assertEqual(rule(m(c,strength_verdicts={'Venus':'meets_sripati_minimum_in_all_variants'}),'phaladeepika-x-6-strong-benefic-7th-lord')['status'],'met')
        self.assertEqual(rule(m(c,strength_verdicts={'Venus':'below_sripati_minimum_in_all_variants'}),'phaladeepika-x-6-strong-benefic-7th-lord')['status'],'not_met')
        self.assertEqual(rule(m(c,strength_verdicts={'Venus':'unresolved_across_variants'}),'phaladeepika-x-6-strong-benefic-7th-lord')['status'],'unresolved')

    def test_benefic_in_seventh_unless_lord_of_6_8_12(self):
        # Aries Lagna: Jupiter in Libra (7th); Jupiter owns 9th and 12th -> excluded.
        c=chart(0,{**BASE,'Jupiter':6})
        self.assertEqual(rule(m(c),'phaladeepika-x-6-benefics-in-7th')['status'],'not_met')
        c=chart(0,{**BASE,'Venus':6})  # Venus owns 2nd and 7th
        self.assertEqual(rule(m(c),'phaladeepika-x-6-benefics-in-7th')['status'],'met')

    def test_mercury_only_benefic_is_possibly_met_not_met(self):
        c2=chart(2,{**BASE,'Mercury':8,'Jupiter':0})  # Gemini Lagna: 7th Sagittarius; Mercury in Sag = 7th, owns 1st/4th
        self.assertEqual(rule(m(c2),'phaladeepika-x-6-benefics-in-7th')['status'],'possibly_met')

    def test_moon_saturn_needs_native_sex(self):
        c=chart(0,{**BASE,'Moon':6,'Saturn':6})
        self.assertEqual(rule(m(c),'phaladeepika-x-8-and-brihat-23-1-moon-saturn-7th')['status'],'unresolved')
        r=rule(m(c,native_sex='female'),'phaladeepika-x-8-and-brihat-23-1-moon-saturn-7th')
        self.assertEqual(r['status'],'met');self.assertTrue(r['adverse_marital_status_text']);self.assertFalse(r['ship_default'])
        with self.assertRaises(ValueError):m(c,native_sex='x')

    def test_cautionary_rules_not_shipped_by_default(self):
        r=m(chart(0,{**BASE,'Sun':6}))
        row=rule(r,'phaladeepika-viii-3-sun-in-7')
        self.assertEqual(row['status'],'met');self.assertFalse(row['ship_default'])

    def test_no_selected_outcome_and_holdouts_listed(self):
        r=m(chart(0,BASE))
        self.assertIsNone(r['selected_outcome']);self.assertIn('"wicked/evil spouse" wording',r['held_out'])
        for row in r['rows']:self.assertIn(row['status'],{'met','possibly_met','not_met','unresolved'})

    def test_period_candidates_include_owner_occupant_and_aspecter(self):
        c=chart(0,{**BASE,'Venus':6,'Mars':3})  # Mars in 4th aspects 7th (4th from itself)
        d=rule(m(c),'phaladeepika-x-13-period-candidate-lords')['detail']
        self.assertIn('Venus',d);self.assertIn('Mars',d)


if __name__=='__main__':unittest.main()


class ReportWiringTests(unittest.TestCase):
    def test_report_carries_strength_and_marriage_and_is_json_serialisable(self):
        import json
        from engine.research_input_report import research_input_report
        x=research_input_report({'date':'1990-05-15','time':'10:30:00','timezone':'Asia/Calcutta',
                                 'latitude':13.08,'longitude':80.27,'place':'Chennai'})
        json.dumps(x)
        self.assertEqual(len(x['shadbala_working_profile']['planets']),7)
        self.assertIsNone(x['marriage_conditional']['selected_outcome'])
