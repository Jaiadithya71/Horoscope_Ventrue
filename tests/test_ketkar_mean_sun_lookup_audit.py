import unittest
from decimal import Decimal as D
from engine.ketkar_mean_sun_lookup_audit import mean_sun_lookup_audit


class MeanSunLookupTests(unittest.TestCase):
    def test_separate_mean_column_and_supplied_apsis(self):
        r = mean_sun_lookup_audit()
        self.assertEqual(r['computed_mean_centre_degrees'], '91.2619405')
        self.assertEqual(r['candidate_mean_sun_longitude_degrees'], '350.2569405')
        self.assertEqual(r['candidate_true_minus_mean_centre_degrees'], '1.9105075')
        self.assertEqual(r['printed_true_longitude_minus_candidate_mean_degrees'], '1.9100595')
        self.assertEqual(D(r['candidate_true_minus_mean_centre_degrees']) -
                         D(r['printed_true_longitude_minus_candidate_mean_degrees']),
                         D(r['true_centre_rounding_difference_degrees']))

    def test_no_mapping_or_precision_certification(self):
        r = mean_sun_lookup_audit()
        self.assertFalse(r['source_selects_unique_interpolation_and_rounding'])
        self.assertFalse(r['arbitrary_date_mean_ephemeris_verified'])
        for key in ('printed_independent_mean_sun_for_fixture', 'epoch_utc_timestamp',
                    'mean_to_sripati_input_mapping', 'sighrochcha_assignments',
                    'selected_revolution_branches', 'selected_natal_strength'):
            self.assertIsNone(r[key])
