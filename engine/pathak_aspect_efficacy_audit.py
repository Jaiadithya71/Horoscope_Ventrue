"""Independent IV.9 efficacy alternatives, distinct from aspect geometry."""
from .pathak_solar_target_audit import SOURCE_URL


def pathak_aspect_efficacy_audit():
    return {'profile': 'pathak_phaladeepika4_aspect_efficacy_reading_audit',
            'primary_reading': {'seventh_aspect_most_effective': True,
                                'other_aspects_equal_efficacy_asserted': False},
            'attributed_other_teachers_reading': {
                'special_aspects_equally_important_in_yogas': True,
                'scope': 'Yoga and related results, not every possible aspect condition',
                'named_special_aspects': {'Jupiter': [5, 9], 'Mars': [4, 8], 'Saturn': [3, 10]}},
            'english_1937_other_teachers_not_less_efficacious_reading_corroborated': True,
            'hindi_source': {'url': SOURCE_URL, 'chapter': 4, 'slokas': '9',
                             'pdf_pages': [68], 'printed_pages': [48],
                             'verified_against_page_image': True},
            'english_source': {'url': 'https://archive.org/details/in.ernet.dli.2015.92117',
                               'chapter': 4, 'slokas': '9', 'pdf_pages': [74],
                               'printed_pages': [37], 'verified_against_page_image': True},
            'sanskrit_lower_result_phrase_with_negation_observed': True,
            'distinct_textual_school_readings_retained': True,
            'selected_reading': None, 'numeric_efficacy_weights': None,
            'universal_qualifying_aspect_definition': None,
            'global_outcome_precedence': None,
            'notice': 'Primary and attributed other-teachers views are separate. Their '
                      'efficacy discussion does not deny geometric special aspects or '
                      'automatically choose full-classical versus seventh-only qualifying '
                      'aspect hypotheses in other verses. No numeric result weights, '
                      'degree-aspect cutoff, yoga activation algorithm or universal school '
                      'winner is inferred. Existing aspect geometry and app outputs unchanged.'}
