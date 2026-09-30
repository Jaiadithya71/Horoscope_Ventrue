"""Page-verified solar mean-centre candidate for one historical fixture."""
from decimal import Decimal as D
from .ketkar_motion_input_audit import SOURCE_URL
from .ketkar_solar_lookup_audit import solar_lookup_audit
from .ketkar_solar_example_reconstruction import reconstruct_solar_example


def mean_sun_lookup_audit():
    true_lookup = solar_lookup_audit()
    fixture = reconstruct_solar_example()
    fraction = D(true_lookup['fraction_between_rows'])
    mean_centre = D('90.673') + fraction * (D('92.646') - D('90.673'))
    apsis = D(fixture['computed_apsis_degrees'])
    mean_longitude = (apsis + mean_centre) % D(360)
    true_centre = D(true_lookup['computed_true_centre_degrees'])
    return {
        'source': {'url': SOURCE_URL, 'pdf_pages': [173, 179, 200, 201],
                   'printed_pages': [106, 112, 133, 134],
                   'verified_against_page_image': True},
        'scope': fixture['scope'],
        'printed_mean_sun_rule': 'madhyama Ravi = nicha + madhyama kendra',
        'printed_manda_correction_rule': 'true manda centre minus mean centre',
        'lower_row': {'centre_days': '92', 'mean_centre_degrees': '90.673'},
        'upper_row': {'centre_days': '94', 'mean_centre_degrees': '92.646'},
        'input_centre_days': true_lookup['input_centre_days'],
        'fraction_between_rows': str(fraction),
        'candidate_interpolation': 'linear_between_printed_adjacent_rows',
        'computed_mean_centre_degrees': str(mean_centre),
        'supplied_fixture_apsis_degrees': str(apsis),
        'candidate_mean_sun_longitude_degrees': str(mean_longitude),
        'candidate_true_minus_mean_centre_degrees': str(true_centre - mean_centre),
        'printed_true_longitude_minus_candidate_mean_degrees':
            str(D(fixture['printed_solar_longitude_degrees']) - mean_longitude),
        'true_centre_rounding_difference_degrees':
            str(true_centre - D(true_lookup['rounded_true_centre_degrees'])),
        'printed_independent_mean_sun_for_fixture': None,
        'source_selects_unique_interpolation_and_rounding': False,
        'epoch_utc_timestamp': None,
        'mean_to_sripati_input_mapping': None,
        'sighrochcha_assignments': None,
        'selected_revolution_branches': None,
        'arbitrary_date_mean_ephemeris_verified': False,
        'selected_natal_strength': None,
        'notice': 'Table11 contains a separate mean-centre column and an explicit '
                  'mean-Sun rule. This bounded candidate uses the same printed day '
                  'input and supplied apsis as the audited true-Sun example. Linear '
                  'interpolation is a candidate, not uniquely source-selected. The '
                  'result has no independent printed mean-Sun comparison here. '
                  'Do not replace this column with true centre, impose a modern '
                  'clock/frame, generalize to arbitrary dates, or infer Sripati '
                  'Sighrochcha inputs or revolution branches.'}


if __name__ == '__main__':
    import json
    print(json.dumps(mean_sun_lookup_audit(), indent=2))
