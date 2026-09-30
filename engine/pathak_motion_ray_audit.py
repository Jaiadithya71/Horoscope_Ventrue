"""Independent IV.4 connective evidence, not physical ray derivation or total strength."""
from .pathak_solar_target_audit import SOURCE_URL


def pathak_motion_ray_audit(retrograde=None, full_rays=None, solar_obscuration=None):
    """Evaluate the Hindi OR clause on supplied three-valued flags only."""
    for flag in (retrograde, full_rays, solar_obscuration):
        if flag is not None and not isinstance(flag, bool):
            raise ValueError('Conditions must be bool or None')
    positive = (True if retrograde is True or full_rays is True else
                False if retrograde is False and full_rays is False else None)
    return {'profile': 'pathak_phaladeepika4_motion_ray_connective_audit',
            'input_conditions': {'retrograde': retrograde, 'full_rays': full_rays,
                                 'solar_obscuration': solar_obscuration},
            'hindi_positive_connective': 'OR',
            'hindi_strength_clause_applies': positive,
            'hindi_weakness_clause_applies': solar_obscuration,
            'strength_scope': 'Strength despite fall or enemy sign/navamsa placement',
            'weakness_scope': 'Weakness despite exalted or friendly sign/navamsa placement',
            'sanskrit_retrograde_and_full_ray_descriptions_juxtaposed': True,
            'sanskrit_boolean_connective_selected': None,
            'simultaneous_strength_and_weakness_evidence':
                positive is True and solar_obscuration is True,
            'full_rays_and_obscuration_supplied_together':
                full_rays is True and solar_obscuration is True,
            'source': {'url': SOURCE_URL, 'chapter': 4, 'slokas': '4',
                       'pdf_pages': [65, 66], 'printed_pages': [45, 46],
                       'verified_against_page_image': True},
            'selected_universal_connective': None,
            'selected_physical_ray_definition': None,
            'numeric_strength': None, 'global_precedence': None,
            'personal_outcome': None,
            'notice': 'Supplied-condition audit only. Hindi explicitly separates retrograde '
                      'and full rays with OR; the Sanskrit descriptions do not establish a '
                      'selected Boolean algorithm here. No physical full-ray criterion, '
                      'automatic obscuration flag or combustion threshold is inferred. '
                      'Simultaneous flags remain exposed without a winner. False positive '
                      'clause is not an adverse conclusion. Existing IV.4/7 reports and '
                      'birth-input defaults are unchanged.'}
