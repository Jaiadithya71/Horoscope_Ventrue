from fractions import Fraction as F
import unittest
from engine.pathak_mean_partition_audit import pathak_mean_partition_audit


class PathakMeanPartitionTests(unittest.TestCase):
    def test_exact_partition_arithmetic(self):
        x = pathak_mean_partition_audit()
        self.assertEqual([r['parts_under_mean_3600_palas'] for r in x['rows']], ['60', '12', '36'])
        for row in x['rows']:
            self.assertEqual(F(row['parts_under_mean_3600_palas']) * F(row['exact_uniform_angular_width_arcseconds_rational']), 48000)
        self.assertEqual([r['printed_minus_exact_arcseconds_rational'] for r in x['rows']], ['0', '0', '-1/30'])
        self.assertEqual(x['hindi_source']['pdf_pages'], [69])

    def test_no_cross_chapter_or_boundary_selection(self):
        x = pathak_mean_partition_audit()
        for key in ('selected_integer_index_or_boundary_policy', 'selected_true_moon_traversal_mapping',
                    'selected_xix_dasha_balance_method', 'selected_calendar_profile', 'personal_outcome'):
            self.assertIsNone(x[key])
