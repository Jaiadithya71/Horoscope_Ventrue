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
