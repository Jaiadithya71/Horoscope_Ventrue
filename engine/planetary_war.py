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


def chart_war_evidence(placements,*,coordinate_profile):
    """Audit all classical non-luminary pairs, never discard missing evidence."""
    from itertools import combinations
    rows=[];missing=[]
    for a,b in combinations(NON_LUMINARIES,2):
        if any(p not in placements or placements[p].get('longitude') is None for p in (a,b)):
            missing.append([a,b]);continue
        x,y=placements[a],placements[b]
        rows.append(planetary_war_evidence(a,b,x['longitude'],y['longitude'],
                    latitude_a=x.get('ecliptic_latitude_degrees'),latitude_b=y.get('ecliptic_latitude_degrees'),
                    coordinate_profile=coordinate_profile))
    return {'pairs':rows,'missing_coordinate_pairs':missing,'selected_winners':None,
            'adjusted_total_strength':None,'notice':'All pair evidence retained, not a filtered winner list. Modern coordinate model is explicit; physical overlap, minute-bin rule, complete totals and winner profile remain unresolved.'}


def supplied_war_adjustment(a,b,total_a,total_b,*,winner,war_condition_confirmed,
                            complete_prewar_totals,adjustment_profile,
                            latitude_a=None,latitude_b=None,latitude_unit=None,
                            total_unit='rupa'):
    """Explicit candidate arithmetic only; never detect war or certify totals.

    Absolute strength difference is a named candidate interpretation. Different
    latitude units change the divided candidate, so none is silently converted.
    """
    from decimal import Decimal
    if a not in NON_LUMINARIES or b not in NON_LUMINARIES or a==b:
        raise ValueError('Distinct classical non-luminaries required')
    if winner not in (a,b) or war_condition_confirmed is not True or complete_prewar_totals is not True:
        raise ValueError('Explicit winner, confirmed condition and complete supplied prewar totals required')
    if total_unit not in ('rupa','virupa'):
        raise ValueError('Named total unit required')
    x,y=Decimal(str(total_a)),Decimal(str(total_b))
    if not all(v.is_finite() and v>=0 for v in (x,y)):
        raise ValueError('Nonnegative finite supplied prewar strengths required')
    difference=abs(x-y)
    if adjustment_profile=='quoted_parashara_absolute_difference_candidate':
        amount=difference;reference=source('war commentary',70,56)
    elif adjustment_profile=='sripati_absolute_difference_per_supplied_latitude_unit_candidate':
        if latitude_unit not in ('degrees','arcminutes') or latitude_a is None or latitude_b is None:
            raise ValueError('Both latitudes in one explicit unit required')
        la,lb=Decimal(str(latitude_a)),Decimal(str(latitude_b))
        limit=Decimal(90 if latitude_unit=='degrees' else 5400)
        if not all(v.is_finite() and abs(v)<=limit for v in (la,lb)) or la==lb:
            raise ValueError('Finite distinct latitudes in stated unit range required')
        north=a if la>lb else b
        if winner!=north:
            raise ValueError('Supplied winner conflicts with Sripati north candidate')
        amount=difference/abs(la-lb);reference=source('15.5-16.5',69,55)
    else:raise ValueError('Explicit known candidate adjustment profile required')
    adjusted={a:x+(amount if winner==a else -amount),b:y+(amount if winner==b else -amount)}
    return {'planets':[a,b],'supplied_prewar_totals':{a:str(x),b:str(y)},
        'supplied_winner':winner,'adjustment_profile':adjustment_profile,
        'difference_interpretation':'absolute_magnitude_candidate','total_unit':total_unit,
        'latitude_unit':latitude_unit,'transfer_amount':str(amount),
        'candidate_adjusted_totals':{p:str(v) for p,v in adjusted.items()},
        'negative_candidate_totals':[p for p,v in adjusted.items() if v<0],
        'source':reference,
        'independent_transfer_corroboration':{
            'url':'https://archive.org/details/bmmv_brihat-parashar-hora-shastra-of-parashar-muni-with-sudha-commentary-by-pt.-dev-c',
            'pdf_page':190,'printed_page':158,'chapter':28,'sloka':20,
            'verified_against_page_image':True,
            'scope':'Full sixfold strength difference added to winner and subtracted from loser',
            'trigger_verified':False,'winner_rule_verified':False,
            'absolute_difference_interpretation_selected':False
        } if adjustment_profile=='quoted_parashara_absolute_difference_candidate' else None,
        'selected_winner':None,'engine_certified_total':None,
        'notice':'Arithmetic on explicit externally supplied complete prewar totals and confirmed condition. Candidate absolute-difference interpretation only; source latitude unit and minute-agreement rule unselected. Degree/arcminute denominators differ by60. No clipping negative results, automatic natal adjustment or double inclusion in temporal/base strength.'}
