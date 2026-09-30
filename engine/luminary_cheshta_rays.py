"""Sripati IV.3-4 ray inputs, not automatic III Shadbala motion."""
import math
from .continuous_strength import source,valid_longitude


def luminary_cheshta_rays(sun_sidereal_longitude,moon_sidereal_longitude,ayanamsa_degrees,
                          *,coordinate_profile):
    if not coordinate_profile:raise ValueError('Named grounded coordinate profile required')
    for a in (sun_sidereal_longitude,moon_sidereal_longitude):valid_longitude(a)
    if not math.isfinite(ayanamsa_degrees):raise ValueError('Finite supplied ayanamsa required')
    angles={'Sun':(sun_sidereal_longitude+ayanamsa_degrees+90)%360,
            'Moon':(moon_sidereal_longitude-sun_sidereal_longitude)%360}
    rows={}
    for planet,angle in angles.items():
        folded=min(angle,360-angle)
        rows[planet]={'cheshtakendra_degrees':angle,'folded_degrees':folded,
                      'cheshta_rays':1+folded/30,
                      'equivalent_normalized_ray_input':folded/180,
                      'source':dict(source('3-4',83,69),chapter='IV')}
    return {'coordinate_profile':coordinate_profile,
            'supplied_sun_sidereal_longitude':sun_sidereal_longitude,
            'supplied_moon_sidereal_longitude':moon_sidereal_longitude,
            'supplied_ayanamsa_degrees':ayanamsa_degrees,'luminaries':rows,
            'angle_source':dict(source('3',82,68),chapter='IV'),
            'selected_shadbala_motion_component':None,'total_strength':None,
            'notice':'IV rays used in historical transformations. Not an automatic III Sun Ayana/Moon Paksha selection, physical speed or calibrated probability. PDF83 Sun rays5.317 and Moon4.107 reproduced within.001 from printed sexagesimal inputs. Printed Moon subtraction differs by one arcsecond between lines; no printed value is substituted.'}
