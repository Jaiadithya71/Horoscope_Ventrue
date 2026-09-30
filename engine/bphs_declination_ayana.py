"""Named BPHS commentary declination shortcut, not Sripati's fixed24 model."""
import math
from .friendship import CLASSICAL
from .luminary_motion_identity import SOURCE,supplied_luminary_motion_identity


def supplied_bphs_declination_ayana(planet,signed_declination,*,declination_profile):
    if planet not in CLASSICAL:raise ValueError('Classical planet required')
    if isinstance(signed_declination,bool) or not isinstance(signed_declination,(int,float)) or not math.isfinite(signed_declination):raise ValueError('Finite signed declination required')
    if not isinstance(declination_profile,str) or not declination_profile.strip():raise ValueError('Named declination model/profile required')
    if abs(signed_declination)>23.45:raise ValueError('Declination exceeds named23deg27min shortcut bound; no clipping or unverified extrapolation')
    d=abs(signed_declination) if planet=='Mercury' else -signed_declination if planet in ('Moon','Saturn') else signed_declination
    base=(23.45+d)/46.9
    value=base*(2 if planet=='Sun' else 1)
    return {'planet':planet,'supplied_signed_declination_degrees':signed_declination,
        'declination_profile':declination_profile,'maximum_declination_degrees':23.45,
        'undoubled_ayana_rupa':base,'multiplier':2 if planet=='Sun' else 1,
        'ayana_rupa':value,'ayana_virupa':value*60,
        'source':dict(SOURCE,pdf_page=228,printed_page=218,sloka='15-17 commentary'),
        'sun_motion_identity':supplied_luminary_motion_identity('Sun',value,component_profile='BPHS23deg27min Ayana commentary; '+declination_profile) if planet=='Sun' else None,
        'selected_sripati_ayana':None,'total_strength':None,
        'notice':'Explicit commentary shortcut from separately supplied signed declination, not equinox-longitude reconstruction or a chosen modern/historical ephemeris. Inputs outside the stated bound are rejected, not clipped. Full precision46.9 denominator used, not rounded1.2793 Virupa coefficient. Sun multiplier applied once before identity; no extra motion double, Moon Paksha fill, mixed-book full total or personal effect.'}
