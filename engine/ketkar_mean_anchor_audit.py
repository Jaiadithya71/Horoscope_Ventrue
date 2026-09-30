"""Printed tropical mean anchors, not an inferred historical motion ephemeris."""
from decimal import Decimal as D
from .ketkar_motion_input_audit import SOURCE_URL


def ketkar_mean_anchor_audit():
    anchors = {'Sun': (11, 13), 'Moon': (17, 25), 'Mercury': (74, 38),
               'Venus': (217, 36), 'Mars': (91, 20), 'Jupiter': (279, 48),
               'Saturn': (0, 30)}
    values = {p: str(D(degrees) + D(minutes)/60) for p, (degrees, minutes) in anchors.items()}
    source_rate = D('3548.3377')
    comparison_rate = D('3548.3362')
    return {
        'source': {'url': SOURCE_URL, 'pdf_pages': [36, 37], 'printed_pages': [13, 14],
                   'verified_against_page_image': True},
        'printed_epoch_label': 'Saka1800 Chaitra bright1',
        'printed_coordinate_label': 'sayana madhyama bhoga (tropical mean longitude)',
        'printed_jyotirganita_anchors_degrees_minutes': anchors,
        'exact_decimal_anchor_candidates_degrees': values,
        'sun_daily_motion_arcseconds': str(source_rate),
        'sun_daily_motion_degrees': str(source_rate/3600),
        'grahalaghava_comparison_sun_daily_motion_arcseconds': str(comparison_rate),
        'difference_between_printed_solar_daily_rates_arcseconds': str(source_rate-comparison_rate),
        'comparison_sun_anchor_degrees_minutes': (11, 40),
        'difference_between_printed_solar_anchors_degrees': str(D(27)/60),
        'all_mean_quantities_absent': False,
        'epoch_utc_timestamp': None,
        'epoch_local_clock_profile': None,
        'subyear_precession_profile': None,
        'mean_to_sripati_input_mapping': None,
        'sighrochcha_assignments': None,
        'selected_revolution_branches': None,
        'arbitrary_date_mean_ephemeris_verified': False,
        'selected_natal_strength': None,
        'notice': 'These introductory comparison tables explicitly contain tropical mean '
                  'positions and day motions. The author preface replacing mean-motion '
                  'tables in the true-planet route does not erase these mean anchors. '
                  'The adjacent Grahalaghava columns are comparison data, not alternate '
                  'Ketkar constants to mix. Decimal division is displayed arithmetic, '
                  'not recovered hidden precision. No civil/UTC epoch, uniform long-range '
                  'propagation, ayanamsa, superior/inferior Sighra assignment or Sripati '
                  'coordinate branch is inferred from this header alone.'}


if __name__ == '__main__':
    import json
    print(json.dumps(ketkar_mean_anchor_audit(), indent=2))
