"""Validate supplied chart labels before source-scoped evidence computation."""
import math
from .forecast import sign_index


def validate_sign_longitude(placements):
    if not isinstance(placements,dict):raise ValueError('Placement object required')
    for pos in placements.values():
        if not isinstance(pos,dict):raise ValueError('Each placement must be an object')
        s=pos.get('sign');lon=pos.get('longitude')
        si=None if s is None else sign_index(s)
        if lon is not None:
            if type(lon) not in (int,float) or not math.isfinite(lon) or not 0<=lon<360:
                raise ValueError('Finite numeric longitude in [0,360) required')
            if si is not None and si!=int(lon//30):raise ValueError('Supplied sign disagrees with longitude')
    # Missing labels remain missing; do not fill them from another field here.
