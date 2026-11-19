import unittest
from engine.extra_topics_conditional import children_conditional, foreign_conditional, love_conditional


def chart(asc_sign,signs):
    """signs: planet -> sign index 0..11 (Aries=0); longitude mid-sign."""
    return {'ascendant':{'longitude':asc_sign*30+10},
            'placements':{p:{'longitude':i*30+15,'whole_sign_house_from_ascendant':(i-asc_sign)%12+1}
                          for p,i in signs.items()}}


BASE={'Sun':4,'Moon':3,'Mars':0,'Mercury':5,'Jupiter':8,'Venus':1,'Saturn':9,'Rahu':2}


def rule(r,rid):return next(x for x in r['rows'] if x['rule_id']==rid)


class ChildrenConditionalTests(unittest.TestCase):
    def test_lords_together(self):
        # Aries Lagna: lagna lord Mars, 5th (Leo) lord Sun. Same sign -> together.
        c=chart(0,{**BASE,'Sun':0})
        self.assertEqual(rule(children_conditional(c),'phaladeepika-xii-1-lagna-lord-with-5th-lord')['status'],'met')
        self.assertEqual(rule(children_conditional(chart(0,BASE)),'phaladeepika-xii-1-lagna-lord-with-5th-lord')['status'],'not_met')

    def test_exchange(self):
        # Mars in Leo (Sun's sign), Sun in Aries (Mars's sign) -> exchange.
        c=chart(0,{**BASE,'Mars':4,'Sun':0})
        self.assertEqual(rule(children_conditional(c),'phaladeepika-xii-1-lagna-5th-exchange')['status'],'met')
        self.assertEqual(rule(children_conditional(chart(0,BASE)),'phaladeepika-xii-1-lagna-5th-exchange')['status'],'not_met')

    def test_mutual_aspect(self):
        # Mars in Cancer (house 4) aspects Capricorn (7th aspect); Sun in Capricorn aspects Cancer -> mutual.
        c=chart(0,{**BASE,'Mars':3,'Sun':9})
        self.assertEqual(rule(children_conditional(c),'phaladeepika-xii-1-lagna-5th-mutual-aspect')['status'],'met')
        self.assertEqual(rule(children_conditional(chart(0,BASE)),'phaladeepika-xii-1-lagna-5th-mutual-aspect')['status'],'not_met')

    def test_benefic_aspect_on_5th(self):
        # BASE: Jupiter in house 9 (Sagittarius) aspects house 5 (5th-from aspect) -> definite benefic.
        self.assertEqual(rule(children_conditional(chart(0,BASE)),'phaladeepika-xii-1-benefic-aspect-on-5th')['status'],'met')
        # Move Jupiter away and let only Mercury aspect the 5th: Mercury in house 11 aspects house 5 (7th aspect).
        c=chart(0,{**BASE,'Jupiter':2,'Mercury':10})
        self.assertEqual(rule(children_conditional(c),'phaladeepika-xii-1-benefic-aspect-on-5th')['status'],'possibly_met')

    def test_malefic_owner_in_5th(self):
        # Aries Lagna: 5th is Leo, owned by Sun (malefic); Sun in Leo owns and occupies the 5th.
        self.assertEqual(rule(children_conditional(chart(0,BASE)),'phaladeepika-xii-3-malefic-owner-in-5th')['status'],'met')
        c=chart(0,{**BASE,'Sun':0})
        self.assertEqual(rule(children_conditional(c),'phaladeepika-xii-3-malefic-owner-in-5th')['status'],'not_met')


class ForeignConditionalTests(unittest.TestCase):
    def test_saturn_in_2nd(self):
        c=chart(0,{**BASE,'Saturn':1})
        self.assertEqual(rule(foreign_conditional(c),'phaladeepika-viii-21-saturn-in-2nd')['status'],'met')
        self.assertEqual(rule(foreign_conditional(chart(0,BASE)),'phaladeepika-viii-21-saturn-in-2nd')['status'],'not_met')

    def test_ketu_in_4th(self):
        # BASE Rahu in Gemini -> Ketu in Sagittarius -> house 9 from Aries: not met.
        self.assertEqual(rule(foreign_conditional(chart(0,BASE)),'phaladeepika-viii-29-ketu-in-4th')['status'],'not_met')
        # Rahu in Capricorn -> Ketu in Cancer -> house 4: met.
        c=chart(0,{**BASE,'Rahu':9})
        self.assertEqual(rule(foreign_conditional(c),'phaladeepika-viii-29-ketu-in-4th')['status'],'met')
        # Without Rahu the Ketu point cannot be derived.
        c=chart(0,{k:v for k,v in BASE.items() if k!='Rahu'})
        self.assertEqual(rule(foreign_conditional(c),'phaladeepika-viii-29-ketu-in-4th')['status'],'unresolved')


class LoveConditionalTests(unittest.TestCase):
    def test_benefic_touch_7th(self):
        # BASE: no benefic touches house 7. Venus in Libra occupies it -> met.
        self.assertEqual(rule(love_conditional(chart(0,BASE)),'phaladeepika-xv-1-benefic-touch-7th')['status'],'not_met')
        c=chart(0,{**BASE,'Venus':6})
        self.assertEqual(rule(love_conditional(c),'phaladeepika-xv-1-benefic-touch-7th')['status'],'met')

    def test_own_lord_touch_7th(self):
        # 7th lord Venus: in Libra it occupies the 7th -> met; BASE Venus in Taurus -> not_met.
        c=chart(0,{**BASE,'Venus':6})
        self.assertEqual(rule(love_conditional(c),'phaladeepika-xv-1-own-lord-touch-7th')['status'],'met')
        self.assertEqual(rule(love_conditional(chart(0,BASE)),'phaladeepika-xv-1-own-lord-touch-7th')['status'],'not_met')

    def test_free_of_malefics(self):
        # BASE: Mars in house 1 aspects house 7 -> not_met.
        self.assertEqual(rule(love_conditional(chart(0,BASE)),'phaladeepika-xv-1-7th-free-of-malefics')['status'],'not_met')
        # Move Mars and Saturn so no malefic occupies or aspects house 7.
        c=chart(0,{**BASE,'Mars':1,'Saturn':8})
        self.assertEqual(rule(love_conditional(c),'phaladeepika-xv-1-7th-free-of-malefics')['status'],'met')

    def test_venus_karaka_needs_strength(self):
        c=chart(0,BASE)
        self.assertEqual(rule(love_conditional(c),'phaladeepika-xv-17-venus-karaka-strong')['status'],'unresolved')
        self.assertEqual(rule(love_conditional(c,strength_verdicts={'Venus':'meets_sripati_minimum_in_all_variants'}),'phaladeepika-xv-17-venus-karaka-strong')['status'],'met')
        self.assertEqual(rule(love_conditional(c,strength_verdicts={'Venus':'below_sripati_minimum_in_all_variants'}),'phaladeepika-xv-17-venus-karaka-strong')['status'],'not_met')


if __name__=='__main__':
    unittest.main()
