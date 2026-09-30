import unittest
from engine.natal import natal_chart, moon_periods, subperiods, birth_utc, natal_references

class NatalTests(unittest.TestCase):
    def test_star_boundaries_and_initial_remainder(self):
        self.assertEqual(moon_periods(0)['initial_lord'],'Ketu')
        self.assertEqual(moon_periods(2*360/27)['initial_lord'],'Sun')
        self.assertAlmostEqual(moon_periods(0)['initial_remaining_solar_years'],7)
        self.assertAlmostEqual(moon_periods(6*360/27+360/54)['initial_remaining_solar_years'],8)
        self.assertEqual(moon_periods(0)['periods'][1]['lord'],'Venus')

    def test_subperiods_proportional_and_ordered(self):
        rows=subperiods('Sun')['subperiods']
        self.assertEqual([x['lord'] for x in rows], ['Sun','Moon','Mars','Rahu','Jupiter','Saturn','Mercury','Ketu','Venus'])
        self.assertAlmostEqual(rows[0]['end_solar_years'],0.3)
        self.assertAlmostEqual(rows[-1]['end_solar_years'],6)

    def test_birth_place_coordinates_change_ascendant_not_moon(self):
        a=natal_chart('2000-01-01','14:30','Asia/Kolkata',13.0827,80.2707,'Chennai, India')
        b=natal_chart('2000-01-01','14:30','Asia/Kolkata',51.5072,-0.1276,'London, UK')
        self.assertNotEqual(a['ascendant']['longitude'],b['ascendant']['longitude'])
        self.assertEqual(a['placements']['Moon']['longitude'],b['placements']['Moon']['longitude'])
        self.assertEqual(a['birth_utc'],'2000-01-01T09:00:00+00:00')
        self.assertEqual(len(a['dasha_hierarchy_at_birth']['hierarchy']),3)
        self.assertEqual(a['dasha_hierarchy_at_birth']['hierarchy'][0]['lord'],a['moon_periods']['initial_lord'])

    def test_page_cited_relative_house_references_no_outcomes(self):
        positions={'Sun': {'sign': 'Aries'}, 'Moon': {'sign': 'Pisces'}}
        refs=natal_references(positions)
        self.assertEqual(refs['relatives']['father']['second_sign'],'Taurus')
        self.assertEqual(refs['relatives']['mother']['second_sign'],'Aries')
        self.assertEqual(refs['relatives']['father']['source']['pdf_page'],197)
        self.assertNotIn('outcome',refs)

    def test_dst_and_coordinates_fail_closed(self):
        with self.assertRaisesRegex(ValueError,'did not exist'):
            birth_utc('2026-03-08','02:30','America/New_York')
        with self.assertRaisesRegex(ValueError,'ambiguous'):
            birth_utc('2026-11-01','01:30','America/New_York')
        with self.assertRaisesRegex(ValueError,'Latitude'):
            natal_chart('2000-01-01','14:30','Asia/Kolkata',90,80,'somewhere')

if __name__=='__main__': unittest.main()

class DashaHierarchyTests(unittest.TestCase):
    def test_first_partial_and_nested_boundaries(self):
        from engine.natal import dasha_at_solar_offset
        at_birth=dasha_at_solar_offset(360/54,0)
        levels=at_birth['hierarchy']
        self.assertEqual([x['level'] for x in levels],['mahadasha','antardasha','antara'])
        self.assertEqual([x['lord'] for x in levels],['Ketu','Rahu','Mercury'])
        self.assertAlmostEqual(levels[0]['full_start_solar_years_after_birth'],-3.5)
        self.assertEqual(levels[0]['visible_start_solar_years_after_birth'],0)
        self.assertNotIn('calendar_dates',at_birth)
        # A boundary belongs to the next major lord, and nested intervals fit.
        boundary=dasha_at_solar_offset(360/54,3.5)
        self.assertEqual(boundary['hierarchy'][0]['lord'],'Venus')
        for outer,inner in zip(boundary['hierarchy'],boundary['hierarchy'][1:]):
            self.assertLessEqual(outer['full_start_solar_years_after_birth'],inner['full_start_solar_years_after_birth'])
            self.assertLessEqual(inner['end_solar_years_after_birth'],outer['end_solar_years_after_birth'])
        with self.assertRaises(ValueError):dasha_at_solar_offset(0,float('nan'))
        with self.assertRaises(ValueError):dasha_at_solar_offset(0,-1)
