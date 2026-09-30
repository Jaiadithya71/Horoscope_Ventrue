"""Supplied-input Sripati III.13-14 components, never Gregorian substitutes."""
import math
from .continuous_strength import source,valid_longitude,NATURAL_ORDER

WEEK_LORDS=('Sun','Moon','Mars','Mercury','Jupiter','Venus','Saturn')
HORA_CYCLE=('Jupiter','Mars','Sun','Venus','Mercury','Moon','Saturn')
THIRDS={'day':('Mercury','Sun','Saturn'),'night':('Moon','Venus','Mars')}


def tribhaga(period,elapsed_fraction):
    """Fraction of supplied sunrise/sunset-bounded day or night, not civil time."""
    if period not in THIRDS:raise ValueError('Day or night required')
    if not math.isfinite(elapsed_fraction) or not 0<=elapsed_fraction<1:
        raise ValueError('Finite fraction in [0,1) required')
    boundary=elapsed_fraction in (1/3,2/3)
    third=None if boundary else int(elapsed_fraction*3)
    lord=None if third is None else THIRDS[period][third]
    scores={p:(1.0 if p=='Jupiter' or p==lord else None if boundary and p in THIRDS[period] else 0.0) for p in NATURAL_ORDER}
    return {'period':period,'elapsed_fraction':elapsed_fraction,'third_index':third,
            'active_lord':lord,'rupa_by_planet':scores,'boundary_unresolved':boundary,
            'source':source('13',60,46),'total_strength':None,
            'notice':'Birth profile only. Exact internal-third ownership abstains; Jupiter always1. Supplied solar interval required.'}


def historical_lords(elapsed_terrestrial_days):
    if type(elapsed_terrestrial_days) is not int or elapsed_terrestrial_days<0:
        raise ValueError('Nonnegative integer historical terrestrial days required')
    n=elapsed_terrestrial_days;y=n//360;m=n//30
    remainders={'year':(3*y+1)%7,'month':(2*m+1)%7,'weekday':n%7}
    lords={k:WEEK_LORDS[(v-1)%7] for k,v in remainders.items()}
    return {'elapsed_terrestrial_days':n,'elapsed_360_day_years':y,'elapsed_30_day_months':m,
            'remainders':remainders,'lords':lords,'sources':[source('14 commentary',62,48),source('14 commentary',63,49)],
            'notice':'Sunday=1, Saturday=0. Historical elapsed-day epoch must be grounded by caller. No Gregorian year/month or modern weekday substitution.'}


def kala_hora(weekday_lord,elapsed_day_fraction):
    if weekday_lord not in WEEK_LORDS:raise ValueError('Classical weekday lord required')
    if not math.isfinite(elapsed_day_fraction) or not 0<=elapsed_day_fraction<1:
        raise ValueError('Finite elapsed whole-day fraction in [0,1) required')
    scaled=24*elapsed_day_fraction
    boundary=scaled>0 and scaled.is_integer()
    index=None if boundary else int(scaled)
    lord=None if index is None else HORA_CYCLE[(HORA_CYCLE.index(weekday_lord)+index)%7]
    return {'profile':'24_equal_parts_supplied_day_origin','weekday_lord':weekday_lord,
            'hora_index':index,'lord':lord,'boundary_unresolved':boundary,
            'source':source('14 commentary',64,50),
            'notice':'Requires grounded day origin and elapsed fraction; no civil-clock or unequal seasonal-hour substitution. Exact internal boundaries abstain.'}


def positional_hora_candidates(weekday_lord,ascendant_longitude,sun_longitude):
    if weekday_lord not in WEEK_LORDS:raise ValueError('Classical weekday lord required')
    valid_longitude(ascendant_longitude);valid_longitude(sun_longitude)
    doubled=((ascendant_longitude-sun_longitude)%360)*2
    signs=int(doubled//30);remainder=signs%7;base=HORA_CYCLE.index(weekday_lord)
    candidates={'completed_signs_zero_based':HORA_CYCLE[(base+remainder)%7],
                'remainder_one_based':HORA_CYCLE[(base+remainder-1)%7]}
    return {'doubled_arc_degrees':doubled,'completed_signs':signs,'remainder':remainder,
            'candidates':candidates,'selected_lord':None,'source':source('14 commentary',64,50),
            'original_sample_disagreement':None,
            'worked_sample_evidence':'Printed doubled arc23sign23deg36min32sec has completed-sign index23, hence 24th hora from Venus, Moon. Enlarged laterPDF64/50 and1919PDF106/90 confirm24th, not earlier mistaken4th. Zero-based candidate matches arithmetic, ordinal and planet; one-based remainder gives Mercury and fails this worked example.',
            'worked_sample_supported_profile':'completed_signs_zero_based',
            'notice':'Separate half-Rasi alternative, not merged into Kala hora. Exact half-Rasi boundary convention also remains unresolved.'}


def lord_components(*,year=None,month=None,weekday=None,hora=None):
    supplied={'year':year,'month':month,'weekday':weekday,'hora':hora}
    for lord in supplied.values():
        if lord is not None and lord not in WEEK_LORDS:raise ValueError('Classical lord or None required')
    weights={'year':.25,'month':.5,'weekday':.75,'hora':1.0}
    rows={p:{k:None if lord is None else weights[k] if lord==p else 0.0 for k,lord in supplied.items()} for p in NATURAL_ORDER}
    return {'supplied_lords':supplied,'rupa_components_by_planet':rows,
            'source':source('14',61,47),'total_strength':None,
            'notice':'Birth-only lord subcomponents. Missing lords remain None; no full temporal or Shadbala total.'}
