"""Pathak XX.7/9/13 strength-qualified lord-period clauses, not global polarity."""
from .pathak_solar_target_audit import SOURCE_URL


def pathak_dusthana_lord_period(*, owned_house, main_period_is_owner=None,
                               lord_strong=None, strength_profile, ownership_profile):
    if type(owned_house) is not int or owned_house not in (6, 8, 12):
        raise ValueError('Scoped owned house6,8,12 required')
    for flag in (main_period_is_owner, lord_strong):
        if flag is not None and type(flag) is not bool:
            raise ValueError('Condition bool or unknown required')
    for profile in (strength_profile, ownership_profile):
        if not isinstance(profile, str) or not profile.strip():
            raise ValueError('Named supplied strength and ownership provenance required')
    applies = (False if main_period_is_owner is False or lord_strong is False
               else True if main_period_is_owner is True and lord_strong is True else None)
    clause = {6: ('7', 235, 217, 'Victory over enemies and increased courage'),
              8: ('9', 236, 218, 'Relief from debt and disputes'),
              12: ('13', 236, 218, 'Expenditure on good causes and favorable acts')}[owned_house]
    return {'profile': 'pathak_phaladeepika20_strong_dusthana_owner_main_period_clause',
            'owned_house': owned_house, 'main_period_is_owner': main_period_is_owner,
            'supplied_lord_strong': lord_strong, 'strength_profile': strength_profile,
            'ownership_profile': ownership_profile, 'scoped_favorable_clause_applies': applies,
            'source_clause_theme': clause[3],
            'sixth_owner_always_adverse_rejected_by_commentary': owned_house == 6,
            'source': {'url': SOURCE_URL, 'chapter': 20, 'slokas': clause[0],
                       'pdf_pages': [clause[1]], 'printed_pages': [clause[2]],
                       'verified_against_page_image': True},
            'global_polarity': None, 'personal_outcome': None, 'global_precedence': None,
            'notice': 'A source-qualified favorable main-period clause, not a prediction. '
                      'Ownership alone does not establish it; strength and active owner period '
                      'are explicitly supplied. False means this clause is not established, '
                      'not that an adverse outcome follows. Does not cancel occupied-dusthana, '
                      'other ownership, disposition, Sandhi or main/subperiod pair conditions.'}
