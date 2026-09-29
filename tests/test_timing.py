import datetime as dt
import unittest
from engine.timing import transitions,state
from engine.natal import nakshatra, sign_audience_padas

UTC=dt.timezone.utc
class TimingTests(unittest.TestCase):
    def test_nakshatra_pada_sign_boundaries(self):
        self.assertEqual((nakshatra(0)['name'],nakshatra(0)['pada']),('Ashwini',1))
        self.assertEqual((nakshatra(10)['name'],nakshatra(10)['pada']),('Ashwini',4))
        self.assertEqual((nakshatra(30)['name'],nakshatra(30)['pada'],nakshatra(30)['sign']),('Krittika',2,'Taurus'))
        self.assertEqual((nakshatra(300)['name'],nakshatra(300)['pada'],nakshatra(300)['sign']),('Dhanishta',3,'Aquarius'))
        self.assertEqual((nakshatra(359.99)['name'],nakshatra(359.99)['pada']),('Revati',4))

    def test_audience_segmentation_not_personal_inference(self):
        segments=sign_audience_padas('Aquarius')
        self.assertEqual(len(segments['possible_nakshatra_padas']),9)
        self.assertEqual(segments['possible_nakshatra_padas'][0],{'nakshatra':'Dhanishta','pada':3})
        self.assertEqual(segments['possible_nakshatra_padas'][-1],{'nakshatra':'Purva Bhadrapada','pada':3})
        self.assertIn('unknown birth data',segments['notice'])

    def test_2026_jupiter_and_rahu_ingress_brackets(self):
        a=transitions(dt.datetime(2026,5,1,tzinfo=UTC),dt.datetime(2026,8,1,tzinfo=UTC),'Jupiter')
        ingress=[x for x in a['events'] if x['kind']=='sign_ingress' and x['to_sign']=='Cancer']
        self.assertEqual(len(ingress),1)
        instant=dt.datetime.fromisoformat(ingress[0]['at_utc'])
        self.assertLess(state(instant-dt.timedelta(minutes=1),'Jupiter')[0],90)
        self.assertGreaterEqual(state(instant+dt.timedelta(minutes=1),'Jupiter')[0],90)
        b=transitions(dt.datetime(2026,11,1,tzinfo=UTC),dt.datetime(2027,1,1,tzinfo=UTC),'Rahu')
        self.assertEqual([x['to_sign'] for x in b['events'] if x['kind']=='sign_ingress'],['Capricorn'])
        # Half-open adjoining windows should not duplicate the same crossing.
        cut=dt.datetime(2026,12,1,tzinfo=UTC)
        before=transitions(dt.datetime(2026,11,1,tzinfo=UTC),cut,'Rahu')['events']
        after=transitions(cut,dt.datetime(2027,1,1,tzinfo=UTC),'Rahu')['events']
        self.assertEqual([x for x in before+after if x['kind']=='sign_ingress'],[x for x in b['events'] if x['kind']=='sign_ingress'])

    def test_station_changes_speed_and_date_bound(self):
        a=transitions(dt.datetime(2026,1,1,tzinfo=UTC),dt.datetime(2027,1,1,tzinfo=UTC),'Jupiter')
        stations=[x for x in a['events'] if x['kind']=='station']
        self.assertGreaterEqual(len(stations),2)
        for x in stations:
            t=dt.datetime.fromisoformat(x['at_utc'])
            v0=state(t-dt.timedelta(hours=1),'Jupiter')[1]
            v1=state(t+dt.timedelta(hours=1),'Jupiter')[1]
            self.assertLess(v0*v1,0)
        with self.assertRaises(ValueError):
            transitions(dt.datetime(2026,1,1,tzinfo=UTC),dt.datetime(2027,2,1,tzinfo=UTC),'Jupiter')

if __name__=='__main__': unittest.main()
