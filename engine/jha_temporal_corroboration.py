"""Independent Jha page corroboration of existing supplied temporal helpers."""
from .bphs_jha_general_aspect import SOURCE_URL
from .temporal_lords import tribhaga, lord_components


def jha_temporal_corroboration():
    # Expectations transcribed from actual Jha188/156, not imported THIRDS.
    expected = {'day': ('Mercury', 'Sun', 'Saturn'), 'night': ('Moon', 'Venus', 'Mars')}
    thirds = []
    for period, lords in expected.items():
        for index, lord in enumerate(lords):
            result = tribhaga(period, (index + .5) / 3)
            thirds.append({'period': period, 'third_index': index,
                           'jha_printed_lord': lord, 'existing_helper_lord': result['active_lord'],
                           'lord_matches': result['active_lord'] == lord,
                           'jupiter_always_virupa': result['rupa_by_planet']['Jupiter'] * 60,
                           'active_lord_virupa': result['rupa_by_planet'][lord] * 60})
    supplied = {'year': 'Sun', 'month': 'Moon', 'weekday': 'Mars', 'hora': 'Mercury'}
    rows = lord_components(**supplied)['rupa_components_by_planet']
    weights = [{'component': key, 'jha_printed_virupa': value,
                'existing_helper_virupa': rows[supplied[key]][key] * 60,
                'weight_matches': rows[supplied[key]][key] * 60 == value}
               for key, value in (('year', 15), ('month', 30), ('weekday', 45), ('hora', 60))]
    return {'profile': 'jha_sudha28_temporal_component_corroboration',
            'source': {'url': SOURCE_URL, 'pdf_pages': [188], 'printed_pages': [156],
                       'chapter': 28, 'slokas': '12-13', 'verified_against_page_image': True},
            'third_checks': thirds, 'supplied_lord_weight_checks': weights,
            'existing_helpers': ['temporal_lords.tribhaga', 'temporal_lords.lord_components'],
            'third_boundary_rule_corroborated': False,
            'historical_lord_algorithm_corroborated': False,
            'solar_event_model_corroborated': False,
            'selected_natal_strength_profile': None, 'full_strength': None,
            'notice': 'Jha independently confirms interior day/night third order, Jupiter always '
                      '60 virupa and supplied year/month/day/hour weights. These components were '
                      'already implemented under Sripati; no duplicate calculator is added. '
                      'This page does not establish exact third ownership, solar-event conventions '
                      'or historical lord derivation. Synthetic supplied lords only, not a natal chart.'}
