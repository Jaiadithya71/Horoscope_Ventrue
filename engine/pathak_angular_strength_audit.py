"""Independent IV.8 corroboration and attributed order, not a new strength total."""
from .pathak_solar_target_audit import SOURCE_URL
from .strength_components import KENDRA_REFINEMENT


def pathak_angular_strength_audit():
    expected = {4: .25, 10: .5, 7: .75, 1: 1.0}
    rows = []
    for house, amount in expected.items():
        implemented = KENDRA_REFINEMENT[house]
        rows.append({'house': house, 'printed_fraction_rupa': amount,
                     'existing_candidate_rupa': implemented, 'matches': amount == implemented,
                     'existing_constant_check_not_natal_chart': True})
    return {'profile': 'pathak_phaladeepika4_angular_strength_order_audit',
            'rows': rows, 'existing_kendra_refinement_corroborated': all(r['matches'] for r in rows),
            'phaladeepika_increasing_order': [4, 10, 7, 1],
            'commentary_attributed_laghu_parashari_increasing_order': [1, 4, 7, 10],
            'attributed_order_independently_verified_against_laghu_parashari': False,
            'quoted_alternate_verse_mentions_kendra_lords': True,
            'alternate_order_numeric_fractions_explicit': False,
            'alternate_order_applied_to_occupants': False,
            'source': {'url': SOURCE_URL, 'chapter': 4, 'slokas': '8 commentary',
                       'pdf_pages': [68], 'printed_pages': [48],
                       'verified_against_page_image': True},
            'selected_school': None, 'selected_house_component': None,
            'total_strength': None, 'global_precedence': None,
            'notice': 'Independent commentary corroborates existing IV.8 fractions, not a '
                      'new calculator. Its attributed Laghu Parashari order is retained as '
                      'commentary evidence, not an independently verified competing occupant '
                      'formula: the quoted verse mentions Kendra lords. No copied fractions '
                      'for the alternative order, category/refinement addition, house-frame '
                      'selection, total strength or app default change.'}
