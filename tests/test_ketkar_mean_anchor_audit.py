import unittest
from decimal import Decimal as D
from engine.ketkar_mean_anchor_audit import ketkar_mean_anchor_audit


class KetkarMeanAnchorTests(unittest.TestCase):
    def test_source_and_comparison_columns_distinct(self):
        r = ketkar_mean_anchor_audit()
        self.assertEqual(r['printed_jyotirganita_anchors_degrees_minutes']['Sun'], (11, 13))
        self.assertEqual(r['comparison_sun_anchor_degrees_minutes'], (11, 40))
        self.assertEqual(D(r['difference_between_printed_solar_anchors_degrees']), D('.45'))
        self.assertEqual(D(r['difference_between_printed_solar_daily_rates_arcseconds']), D('.0015'))
        self.assertEqual(D(r['sun_daily_motion_degrees']), D('3548.3377')/3600)

    def test_mean_anchors_exist_but_mapping_not_inferred(self):
        r = ketkar_mean_anchor_audit()
        self.assertEqual(len(r['printed_jyotirganita_anchors_degrees_minutes']), 7)
        self.assertFalse(r['all_mean_quantities_absent'])
        self.assertFalse(r['arbitrary_date_mean_ephemeris_verified'])
        for key in ('epoch_utc_timestamp', 'epoch_local_clock_profile', 'subyear_precession_profile',
                    'mean_to_sripati_input_mapping', 'sighrochcha_assignments',
                    'selected_revolution_branches', 'selected_natal_strength'):
            self.assertIsNone(r[key])
