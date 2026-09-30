import unittest
from engine.transit_phase import transit_phase,THIRDS

class TransitPhaseTests(unittest.TestCase):
    def test_all_planet_thirds(self):
        for p,wanted in THIRDS.items():
            for i in range(3):
                self.assertEqual(transit_phase(p,30*4+10*i+5)['active_condition'],i==wanted)
        for p in ('Mercury','Rahu'):
            for degree in (0,5,10,15,20,29.999):
                self.assertTrue(transit_phase(p,degree)['active_condition'])
        self.assertIsNone(transit_phase('Ketu',0)['active_condition'])

    def test_rotation_and_boundaries(self):
        for p in THIRDS:
            for degree in (10,20):
                self.assertIsNone(transit_phase(p,degree)['active_condition'])
            for sign in range(12):
                self.assertEqual(transit_phase(p,sign*30+5)['active_condition'],transit_phase(p,5)['active_condition'])
        self.assertTrue(transit_phase('Sun',0)['active_condition'])
        self.assertTrue(transit_phase('Saturn',359.99)['active_condition'])
        with self.assertRaises(ValueError):transit_phase('Sun',360)

    def test_forecast_evidence_does_not_filter_findings(self):
        from engine.forecast import forecast
        x=forecast('2026-01-01','Aquarius')
        self.assertIn('transit_phase_evidence',x['placements']['Jupiter'])
        self.assertTrue(any(f['planet']=='Jupiter' for f in x['findings']))
        self.assertNotIn('prediction_accuracy',x)
