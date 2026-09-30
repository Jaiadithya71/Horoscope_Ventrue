"""IV.12 mean-nakshatra partition arithmetic, never XIX balance arbitration."""
from fractions import Fraction as F
from .pathak_solar_target_audit import SOURCE_URL


def pathak_mean_partition_audit():
    rows = []
    for name, divisor, printed in (('chandra_kriya', 60, F(800)),
                                   ('chandra_avastha', 300, F(4000)),
                                   ('chandra_vela', 100, F(13333, 10))):
        count = F(3600, divisor)
        width = F(48000) / count
        rows.append({'name': name, 'elapsed_pala_divisor': divisor,
                     'parts_under_mean_3600_palas': str(count),
                     'exact_uniform_angular_width_arcseconds_rational': str(width),
                     'printed_angular_width_arcseconds_rational': str(printed),
                     'printed_minus_exact_arcseconds_rational': str(printed - width)})
    return {'profile': 'pathak_phaladeepika4_mean_nakshatra_partition_audit',
            'mean_traversal_ghatikas_explicit': 60,
            'mean_traversal_palas_explicit': 3600,
            'uniform_nakshatra_width_arcseconds': 48000,
            'rows': rows,
            'literal_elapsed_time_divisors_independently_corroborated': True,
            'uniform_time_to_angle_equivalence_assumption':
                'Mean3600-pala traversal and uniform progress within13degree20minute sector',
            'hindi_source': {'url': SOURCE_URL, 'chapter': 4, 'slokas': '12 commentary',
                             'pdf_pages': [69], 'printed_pages': [49],
                             'verified_against_page_image': True},
            'english_source': {'url': 'https://archive.org/details/in.ernet.dli.2015.92117',
                               'chapter': 4, 'slokas': '12', 'pdf_pages': [75],
                               'printed_pages': [38], 'verified_against_page_image': True},
            'selected_integer_index_or_boundary_policy': None,
            'selected_true_moon_traversal_mapping': None,
            'selected_xix_dasha_balance_method': None,
            'selected_calendar_profile': None, 'personal_outcome': None,
            'notice': 'Arithmetic evidence for this IV.12 commentary only. English independently '
                      'corroborates elapsed-time divisors, not the later mean-duration explanation. '
                      'The printed vela seconds13.3 are lower than exact13+1/3 by1/30 arcsecond. '
                      'Mean uniform angle equivalence is not true Moon traversal-time equality. '
                      'No integer quotient rounding, row index, endpoint convention or adverse '
                      'outcome list is activated. Do not transfer the mean60 assumption into '
                      'XIX dasha or select a civil calendar. App defaults unchanged.'}
