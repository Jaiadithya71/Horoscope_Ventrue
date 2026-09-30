"""Explicit modern solar clocks plus optionally supplied historical day lords."""
from .solar_meridian_clock import solar_meridian_clock
from .solar_intervals import solar_interval_evidence
from .historical_day_count import historical_day_count
from .temporal_lords import positional_hora_candidates,lord_components


def temporal_evidence_report(instant,latitude,longitude,placements,ascendant,*,solar_event_profile,meridian_profile,historical_inputs=None):
 meridian=solar_meridian_clock(instant,latitude,longitude,meridian_profile=meridian_profile)
 thirds=solar_interval_evidence(instant,latitude,longitude,solar_event_profile=solar_event_profile)
 historic=None;hora=None;lord_variants=[]
 if historical_inputs is not None:
  expected={'elapsed_creation_solar_years','elapsed_solar_months','elapsed_lunar_days','epoch_profile'}
  if set(historical_inputs)!=expected:raise ValueError('All named historical inputs required, no extra epoch fields inferred')
  historic=historical_day_count(**historical_inputs)
  lords=historic['lord_evidence']['lords']
  if placements.get('Sun',{}).get('longitude') is not None and ascendant is not None:
   hora=positional_hora_candidates(lords['weekday'],ascendant,placements['Sun']['longitude'])
   for profile,lord in hora['candidates'].items():
    lord_variants.append({'hora_profile':profile,'components':lord_components(year=lords['year'],month=lords['month'],weekday=lords['weekday'],hora=lord)})
  else:lord_variants.append({'hora_profile':'unresolved_missing_coordinates','components':lord_components(year=lords['year'],month=lords['month'],weekday=lords['weekday'])})
 else:lord_variants.append({'hora_profile':'unresolved_epoch_and_origin','components':lord_components()})
 return {'modern_meridian_clock_candidates':meridian,'modern_solar_third_evidence':thirds,
    'supplied_historical_day_evidence':historic,'positional_hora_candidates':hora,
    'temporal_lord_component_candidates':lord_variants,
    'selected_temporal_profile':None,'total_temporal_strength':None,'total_strength':None,
    'remaining_model_gates':['phase complement/Moon multiplier','historical Ayana versus modern-coordinate model and Sun multiplier',
         'historic epoch/calendar validation','hora indexing/origin choice','meridian-clock definition','war adjustment and inclusive-versus-expanded motion layout consistency'],
    'notice':'Explicit mixed-source computational bridges, not a historically unified temporal model. Epoch counts never inferred from civil birth date. Modern solar intervals and supplied historical lord counts retain their distinct provenance. No summing partial components, selecting a winner, automatic full temporal score, planet ranking or outcome.'}
