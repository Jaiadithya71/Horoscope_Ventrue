import unittest
from engine.house_model_sensitivity import dual_house_model, degree_chart
from engine.marriage_conditional import marriage_conditional
from tests.test_marriage_conditional import chart, BASE


def with_degree(c,houses):
    for p,h in houses.items():
        c['placements'][p]['sripati_degree_house']={'house':h,'at_sandhi':False}
    for p in c['placements']:
        c['placements'][p].setdefault('sripati_degree_house',{'house':c['placements'][p]['whole_sign_house_from_ascendant'],'at_sandhi':False})
    return c


class HouseModelTests(unittest.TestCase):
    def test_agreement_keeps_status(self):
        c=with_degree(chart(0,BASE),{})
        r=dual_house_model(marriage_conditional,c)
        self.assertEqual(r['house_model_sensitivity']['rows_that_differ'],0)

    def test_disagreement_becomes_model_dependent_with_both_statuses(self):
        c=with_degree(chart(0,{**BASE,'Venus':6}),{'Venus':8})  # whole-sign 7th, degree 8th
        r=dual_house_model(marriage_conditional,c)
        row=next(x for x in r['rows'] if x['rule_id']=='phaladeepika-viii-18-venus-in-7th')
        self.assertEqual(row['status'],'house_model_dependent')
        self.assertEqual(row['status_by_house_model'],{'whole_sign':'met','sripati_degree_bhava':'not_met'})

    def test_missing_degree_geometry_is_reported_not_guessed(self):
        r=dual_house_model(marriage_conditional,chart(0,BASE))
        self.assertEqual(r['house_model_sensitivity']['status'],'degree_model_unavailable')


if __name__=='__main__':unittest.main()
