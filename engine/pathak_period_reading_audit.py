"""Independent Hindi readings, not majority voting or scope repairs."""
from .pathak_solar_target_audit import SOURCE_URL


def pathak_period_reading_audit():
    return {'profile': 'pathak_phaladeepika20_disposition_and_pair_reading_audit',
            'disposition': {
                'friendly_sign_term_retained': True,
                'favorable_connective_selected': None,
                'source': {'url': SOURCE_URL, 'chapter': 20, 'slokas': '14',
                           'pdf_pages': [237], 'printed_pages': [219],
                           'verified_against_page_image': True},
                'notice': 'Hindi favorable list retains friendly sign; not corroboration of its '
                          'omission in Kapoor. List syntax is not used to choose all-versus-any.'},
            'vargottama': {
                'fall_or_solar_obscuration_mixed_qualification_corroborated': True,
                'qualification_scope': 'This verse Vargottama period clause only',
                'source': {'url': SOURCE_URL, 'chapter': 20, 'slokas': '22',
                           'pdf_pages': [239], 'printed_pages': [221],
                           'verified_against_page_image': True}},
            'main_sub_pair': {
                'main_dusthana_set_explicit': [6, 8, 12],
                'separate_owner_pair_and_occupant_pair_wording_observed': True,
                'subperiod_hindi_scope_wording': 'Other house owner or other house occupant',
                'subperiod_other_house_restricted_to_dusthana_explicit': False,
                'subperiod_scope_selected': None,
                'existing_sastri_or_kapoor_boolean_selected': None,
                'source': {'url': SOURCE_URL, 'chapter': 20, 'slokas': '22 commentary',
                           'pdf_pages': [239], 'printed_pages': [221],
                           'verified_against_page_image': True},
                'notice': 'Other-house wording is unresolved here: it may refer back to the '
                          'dusthana set or a wider house set. No automatic new predicate or '
                          'repair to match an existing English candidate.'},
            'selected_translation': None, 'global_precedence': None, 'personal_outcome': None,
            'notice': 'Independent edition evidence preserves term, connective and scope '
                      'differences separately. Corroboration does not select a universal '
                      'translation, school or whole-chart outcome.'}
