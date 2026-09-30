"""Independent IV.21-23 thresholds, not proof a supplied total is coherent."""
from .pathak_solar_target_audit import SOURCE_URL
from .strength_precedence import check_supplied_total


def pathak_strength_threshold_audit():
    printed = {'Sun': 6.5, 'Moon': 6.0, 'Mars': 5.0, 'Mercury': 7.0,
               'Jupiter': 6.5, 'Venus': 5.5, 'Saturn': 5.0}
    rows = []
    for planet, required in printed.items():
        probe = check_supplied_total(planet, required, complete=True)
        incomplete = check_supplied_total(planet, required, complete=False)
        rows.append({'planet': planet, 'printed_required_total_rupa': required,
                     'existing_required_total_rupa': probe['required_total_rupa'],
                     'matches': probe['required_total_rupa'] == required,
                     'synthetic_exact_threshold_accepted': probe['meets_book_threshold'],
                     'incomplete_threshold_classification': incomplete['meets_book_threshold']})
    return {'profile': 'pathak_phaladeepika4_strength_threshold_corroboration',
            'rows': rows, 'all_existing_thresholds_corroborated': all(r['matches'] for r in rows),
            'component_emphasis': {'Moon': 'paksha', 'other_planets': 'positional'},
            'source': {'url': SOURCE_URL, 'chapter': 4, 'slokas': '21-23',
                       'pdf_pages': [72, 73], 'printed_pages': [52, 53],
                       'verified_against_page_image': True},
            'selected_natal_total': None, 'selected_composition': None,
            'global_precedence': None, 'personal_outcome': None,
            'notice': 'Seven synthetic threshold probes corroborate the existing complete-'
                      'supplied-total gate, not an actual planet strength. Component emphasis '
                      'does not turn one component into a complete total. Caller completeness '
                      'is unverified; source composition and Jha threshold disagreements '
                      'remain separate. No natal total, numeric assembly, school winner or '
                      'app defaults changed.'}
