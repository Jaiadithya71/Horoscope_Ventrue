"""Supplied-longitude Paksha component under Jha's named worked profile."""
from .bphs_jha_general_aspect import SOURCE_URL, number


def bphs_jha_paksha(sun_longitude, moon_longitude, *, coordinate_profile):
    if not isinstance(coordinate_profile, str) or not coordinate_profile.strip():
        raise ValueError('Named common coordinate provenance required')
    phase = (number(moon_longitude) - number(sun_longitude)) % 360
    folded = min(phase, 360 - phase)
    benefic = folded / 3
    malefic = 60 - benefic
    return {
        'profile': 'bphs_jha_sudha28_fixed_group_undoubled_worked_paksha_candidate',
        'coordinate_profile': coordinate_profile,
        'directed_phase_degrees_rational': str(phase),
        'folded_phase_degrees_rational': str(folded),
        'benefic_paksha_virupa_rational': str(benefic),
        'malefic_paksha_virupa_rational': str(malefic),
        'planet_paksha_virupa_rational': {
            p: str(benefic if p in ('Moon', 'Mercury', 'Jupiter', 'Venus') else malefic)
            for p in ('Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn')
        },
        'classification_profile': 'Jha28.10-11 printed fixed groups',
        'moon_multiplier': 1,
        'source': {'url': SOURCE_URL, 'pdf_pages': [188], 'printed_pages': [156],
                   'chapter': 28, 'slokas': '10-11', 'verified_against_page_image': True},
        'universal_multiplier_policy_verified': False,
        'selected_natal_strength_profile': None,
        'full_strength': None,
        'notice': 'Named Jha worked component only. Fixed benefic Moon/Mercury/Jupiter/Venus '
                  'and undoubled Moon match this printed worked example. No dark-half '
                  'classification switch, Mercury association test or Santhanam Moon doubling '
                  'is imported. This does not certify caller coordinates, universal multiplier '
                  'policy, a complete strength layout or any forecast.'
    }
