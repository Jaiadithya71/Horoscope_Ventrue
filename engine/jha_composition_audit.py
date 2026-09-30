"""Page-grounded natural ratios and luminary equalities, no composition choice."""
from fractions import Fraction as F
from .bphs_jha_general_aspect import SOURCE_URL
from .continuous_strength import naisargikabala


def jha_composition_audit():
    # Independent order printed in Jha28.14.
    order = ('Saturn', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Moon', 'Sun')
    rows = []
    for rank, planet in enumerate(order, 1):
        exact = F(60 * rank, 7)
        prior = naisargikabala(planet)
        rows.append({'planet': planet, 'jha_exact_virupa_rational': str(exact),
                     'existing_sripati_exact_virupa_rational': str(F(prior['rational_rupa']) * 60),
                     'exact_ratio_matches': exact == F(prior['rational_rupa']) * 60,
                     'quoted_integer_comparison_virupa': prior['quoted_comparison']['virupa'],
                     'exact_minus_quoted_integer_rational': str(exact - prior['quoted_comparison']['virupa'])})
    return {'profile': 'jha_sudha28_natural_and_luminary_identity_audit',
            'natural_rows': rows,
            'natural_source': {'url': SOURCE_URL, 'pdf_pages': [188], 'printed_pages': [156],
                               'chapter': 28, 'slokas': '14', 'verified_against_page_image': True},
            'luminary_equalities': [{'planet': 'Sun', 'equal_components': ['ayana', 'cheshta']},
                                    {'planet': 'Moon', 'equal_components': ['paksha', 'cheshta']}],
            'identity_source': {'url': SOURCE_URL, 'pdf_pages': [189], 'printed_pages': [157],
                                'chapter': 28, 'slokas': '18', 'verified_against_page_image': True},
            'sixfold_enumeration_source': {'url': SOURCE_URL, 'pdf_pages': [190], 'printed_pages': [158],
                                          'chapter': 28, 'slokas': '25.5', 'verified_against_page_image': True},
            'general_ayana_containment_selected': None,
            'luminary_double_counting_selected': None,
            'selected_composition_profile': None, 'full_strength': None,
            'notice': 'Natural 60/7 increments corroborate exact Sripati ratios, not rounded quoted '
                      'integers. Jha18 names equal luminary components; equality does not prescribe '
                      'adding the amount twice or general Ayana containment. Sixfold enumeration '
                      'alone does not settle that composition. No repaired table, multiplier or '
                      'full natal total selected.'}
