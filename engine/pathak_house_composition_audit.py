"""IV.24 corroborated term list, not assembly of mismatched house components."""
from .pathak_solar_target_audit import SOURCE_URL


def pathak_house_composition_audit():
    return {'profile': 'pathak_phaladeepika4_house_strength_composition_audit',
            'named_additive_terms': ['house_lord_strength', 'one_rupa',
                                     'house_directional_strength', 'house_aspect_strength'],
            'fixed_addition_rupa': 1,
            'independent_hindi_and_english_term_list_matches': True,
            'english_commentator_refers_to_sripati_chapters_2_and_3': True,
            'referral_is_blanket_compatibility_proof': False,
            'hindi_source': {'url': SOURCE_URL, 'chapter': 4, 'slokas': '24',
                             'pdf_pages': [73], 'printed_pages': [53],
                             'verified_against_page_image': True},
            'english_source': {'url': 'https://archive.org/details/in.ernet.dli.2015.92117',
                               'chapter': 4, 'slokas': '24', 'pdf_pages': [79, 80],
                               'printed_pages': [42, 43], 'verified_against_page_image': True},
            'existing_separate_research_lanes': ['bhava_lord_candidates', 'bhava_strength',
                                                'bhava_aspect_candidates'],
            'unresolved_assembly_inputs': [
                'Source-consistent complete lord strength and cross-sign weighting',
                'Grounded house directional category and centre geometry',
                'House aspect geometry/classifications and extra-term compatibility',
                'Whether quoted Sripati occupant adjustments are already included or separate'],
            'selected_house_total': None, 'selected_component_profile': None,
            'global_precedence': None, 'personal_outcome': None,
            'notice': 'Independent term-list corroboration, not a computed natal total. '
                      'The English commentary points to Sripati for detail; that referral '
                      'does not certify every existing source candidate as compatible. '
                      'No incomplete lord total, whole-sign centre or aspect class is '
                      'invented, and no occupant/aspect term is double-added. Existing '
                      'separate lanes and app outputs unchanged.'}
