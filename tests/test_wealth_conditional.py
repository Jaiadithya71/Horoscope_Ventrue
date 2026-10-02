import unittest
from engine.wealth_conditional import wealth_conditional as w
from tests.test_marriage_conditional import chart, BASE


def rule(r,rid):return next(x for x in r['rows'] if x['rule_id']==rid)


class WealthConditionalTests(unittest.TestCase):
    def test_sunapha_anapha_durudhara_exclude_sun_and_moon(self):
        # Aries Lagna; Moon in Cancer (house 4); 2nd from Moon = house 5 (Leo), 12th = house 3 (Gemini)
        c=chart(0,{**BASE,'Moon':3,'Mars':4,'Mercury':2,'Sun':4,'Jupiter':8,'Venus':8,'Saturn':9})
        r=w(c)
        self.assertEqual(rule(r,'phaladeepika-vi-5-7-sunapha')['status'],'met')
        self.assertEqual(rule(r,'phaladeepika-vi-5-7-anapha')['status'],'met')
        self.assertEqual(rule(r,'phaladeepika-vi-5-7-durudhara')['status'],'met')
        c=chart(0,{**BASE,'Moon':3,'Mars':8,'Mercury':8,'Sun':4,'Jupiter':8,'Venus':8,'Saturn':9})
        r=w(c);self.assertEqual(rule(r,'phaladeepika-vi-5-7-sunapha')['status'],'not_met')

    def test_sun_alone_in_second_from_moon_is_not_sunapha(self):
        c=chart(0,{**BASE,'Moon':3,'Sun':4,'Mars':8,'Mercury':8,'Jupiter':8,'Venus':8,'Saturn':9})
        self.assertEqual(rule(w(c),'phaladeepika-vi-5-7-sunapha')['status'],'not_met')

    def test_parivartana_between_second_lord_and_ninth_lord(self):
        # Aries Lagna: 2nd Taurus (Venus), 9th Sagittarius (Jupiter). Venus in Sag, Jupiter in Taurus.
        c=chart(0,{**BASE,'Venus':8,'Jupiter':1})
        self.assertEqual(rule(w(c),'phaladeepika-vi-32-34-parivartana-wealth')['status'],'met')
        c=chart(0,BASE)
        self.assertEqual(rule(w(c),'phaladeepika-vi-32-34-parivartana-wealth')['status'],'not_met')

    def test_subhakartari_needs_both_sides(self):
        c=chart(0,{**BASE,'Jupiter':11,'Venus':1})
        self.assertEqual(rule(w(c),'phaladeepika-vi-8-13-subhakartari')['status'],'met')
        c=chart(0,{**BASE,'Jupiter':11,'Venus':5})
        self.assertEqual(rule(w(c),'phaladeepika-vi-8-13-subhakartari')['status'],'not_met')

    def test_placement_rows_and_adverse_flag(self):
        c=chart(0,{**BASE,'Jupiter':1,'Mars':1})
        r=w(c)
        self.assertEqual(rule(r,'phaladeepika-viii-jupiter-in-2')['status'],'met')
        m=rule(r,'phaladeepika-viii-mars-in-2')
        self.assertEqual(m['status'],'met');self.assertFalse(m['ship_default'])
        self.assertTrue(rule(r,'phaladeepika-viii-jupiter-in-2')['ship_default'])

    def test_no_income_level_and_valid_statuses(self):
        r=w(chart(0,BASE));self.assertIsNone(r['income_level']);self.assertIsNone(r['selected_outcome'])
        for x in r['rows']:self.assertIn(x['status'],{'met','possibly_met','not_met','unresolved'})


if __name__=='__main__':unittest.main()
