"""Original war-condition evidence, not automatic winner or strength adjustment."""
import math
from .continuous_strength import source,valid_longitude,folded_distance
from .motional_strength import NON_LUMINARIES


def planetary_war_evidence(a,b,longitude_a,longitude_b,*,latitude_a=None,latitude_b=None,coordinate_profile):
    if a not in NON_LUMINARIES or b not in NON_LUMINARIES or a==b:raise ValueError('Distinct classical non-luminaries required')
    if not coordinate_profile:raise ValueError('Grounded supplied coordinate profile required')
    valid_longitude(longitude_a);valid_longitude(longitude_b)
    for lat in (latitude_a,latitude_b):
        if lat is not None and (not math.isfinite(lat) or not -90<=lat<=90):raise ValueError('Supplied latitude must be finite in [-90,90]')
    arc=folded_distance(longitude_a,longitude_b)
    north=None if latitude_a is None or latitude_b is None or latitude_a==latitude_b else a if latitude_a>latitude_b else b
    return {'planets':[a,b],'coordinate_profile':coordinate_profile,
            'longitude_separation_degrees':arc,
            'commentary_less_than_one_degree_condition':arc<1,
            'main_verse_exact_longitude_agreement':arc==0,
            'within_one_arcminute':arc<=1/60,
            'minute_agreement_interpretation':'Verse says agree even to a minute; exact equality and angular closeness are separate indicators, not a chosen rounded-minute bin rule.',
            'supplied_latitudes':{a:latitude_a,b:latitude_b},'north_planet':north,
            'winner_candidates':[{'profile':'sripati_north_rule','winner':north,'source':source('15.5-16.5',69,55)},
                                 {'profile':'quoted_parashara_disc_brightness_size_rule','winner':None,'source':source('war commentary',70,56)}],
            'adjustment_profiles':[{'profile':'sripati_strength_difference_divided_by_latitude_difference','status':'not_calculated','source':source('15.5-16.5',69,55),
                                    'notice':'Latitude-unit interpretation, minute-agreement interpretation and complete strength must be grounded before division.'},
                                   {'profile':'quoted_parashara_strength_difference','status':'not_calculated','source':source('war commentary',70,56)}],
            'selected_winner':None,'adjusted_total_strength':None,
            'notice':'Longitude closeness is not certified physical disc overlap. Northern placement, brightness and disc-size rules can disagree; latitude equality cannot select a winner. No Sun/Moon/node war, automatic total adjustment or outcome.'}
