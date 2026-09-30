"""IV.11 relative protective potency, not a Shadbala multiplier or cancellation."""
from .pathak_solar_target_audit import SOURCE_URL


def pathak_protective_potency_audit():
    return {'profile': 'pathak_phaladeepika4_protective_potency_scope_audit',
            'relative_potency_to_jupiter': {'Jupiter': '1', 'Mercury': '1/4', 'Venus': '1/2'},
            'potency_scope': 'Removing adverse effects and increasing favorable effects',
            'jupiter_greatest_in_this_scope': True,
            'moon_strength_described_as_basis_of_planet_strength': True,
            'moon_dependency_formula_explicit': False,
            'hindi_source': {'url': SOURCE_URL, 'chapter': 4, 'slokas': '11',
                             'pdf_pages': [68, 69], 'printed_pages': [48, 49],
                             'verified_against_page_image': True},
            'english_source': {'url': 'https://archive.org/details/in.ernet.dli.2015.92117',
                               'chapter': 4, 'slokas': '11', 'pdf_pages': [74, 75],
                               'printed_pages': [37, 38], 'verified_against_page_image': True},
            'same_relative_potency_and_moon_basis_corroborated': True,
            'selected_natal_applicability': None,
            'selected_strength_multiplier': None,
            'selected_adverse_cancellation': None,
            'global_outcome_precedence': None,
            'notice': 'Relative potency in this named protective/favorable scope is not '
                      'a numeric Shadbala component, total-strength ratio or instruction '
                      'to multiply Mercury/Venus/Moon totals. The Moon basis statement '
                      'does not specify a dependency equation. No placement, aspect, '
                      'relationship or sufficient-strength activation test is supplied '
                      'by this audit. Do not erase other adverse evidence or promise '
                      'personal protection. Existing strength and app defaults unchanged.'}
