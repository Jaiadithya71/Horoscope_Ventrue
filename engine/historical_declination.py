"""Supplied equinox-referenced longitude, fixed24-degree historical table only."""
from .continuous_strength import valid_longitude,source,ayanabala_candidates

INCREMENTS_ARCMINUTES=(362,341,299,236,150,52)


def historical_declination(tropical_longitude):
    """III.15-16 commentary table, not modern 3D equatorial declination.

    The caller grounds longitude measured from equinox. No current ayanamsa
    or planetary ecliptic latitude is silently supplied by this method.
    """
    valid_longitude(tropical_longitude)
    quadrant=tropical_longitude%180
    distance=min(quadrant,180-quadrant)
    count=min(int(distance//15),6)
    minutes=sum(INCREMENTS_ARCMINUTES[:count])
    if count<6:minutes+=(distance-count*15)/15*INCREMENTS_ARCMINUTES[count]
    sign=1 if tropical_longitude<180 else -1
    return {'supplied_equinox_referenced_longitude':tropical_longitude,
            'nearest_equinox_distance_degrees':distance,
            'declination_degrees':sign*minutes/60,
            'increments_arcminutes':list(INCREMENTS_ARCMINUTES),
            'source':source('15-16 commentary historical six-part table',67,53),
            'worked_example_notice':'PDF67 prints892.737 arcminutes for39-31-08; exact table arithmetic gives892.743185, differing by.006185 arcminutes. Printed number is not substituted.',
            'notice':'Historical fixed24-degree, piecewise-linear ecliptic-longitude table. Not modern equatorial declination; no ecliptic-latitude correction or model replacement is claimed.'}


def historical_ayana_from_longitude(planet,tropical_longitude,*,longitude_profile):
    if not longitude_profile:raise ValueError('Grounded supplied longitude profile required')
    d=historical_declination(tropical_longitude)
    return {'longitude_profile':longitude_profile,'historical_declination':d,
            'ayana_candidates':ayanabala_candidates(planet,d['declination_degrees']),
            'total_strength':None,'notice':'Historical table input only. Sun double/undoubled candidates remain separate. Do not mix with modern declination or silently select a complete strength profile.'}


def ayana_zero_point_consistency_audit():
    """III.15-16 equator sentence versus explicit zero-point arithmetic."""
    from decimal import Decimal
    rows=[]
    for planet in ('Sun','Moon','Mars','Mercury','Jupiter','Venus','Saturn'):
        candidate=ayanabala_candidates(planet,0)
        base=Decimal(str(candidate['candidates'][0]['rupa']))
        sentence=Decimal('0.5')
        rows.append({'planet':planet,'supplied_declination_degrees':0,
                     'base_zero_point_rupa':str(base),'equator_sentence_rupa':str(sentence),
                     'base_matches_equator_sentence':base==sentence,
                     'explicit_multiplier_rupa':str(base*2) if planet=='Sun' else None,
                     'source_candidates':candidate,'selected_ayana_rupa':None})
    return {'rows':rows,'equator_sentence_source':source('15-16 commentary equator sentence',66,52),
            'zero_point_source':source('15-16 Kesava zero-point/48 method',67,53),
            'worked_sun_source':source('15-16 worked Sun declination/undoubled result',67,53),
            'clearer_1919_cross_check':{'url':'https://archive.org/details/ksu.h1304.sripatipaddhati0000vsub','pdf_page':30,'printed_page':14,'verified_against_page_image':True},
            'prior_fraction_loss_corrected':True,
            'source_selected_profile':None,'total_strength':None,
            'notice':'The small fraction in PDF66 is1/2, confirmed by clearer1919 PDF30/14 and enlarged1934 crop. The equator sentence agrees with base zero-point/48 arithmetic for all seven planets. Prior supposed endpoint conflict was a fraction-reading error and is corrected, not retained as a classical alternative. Separate Sun-only doubling and worked-table allocation remain open; no global double or selected natal total.'}
