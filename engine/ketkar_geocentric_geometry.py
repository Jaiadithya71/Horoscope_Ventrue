"""Supplement42-49 direct geometry using supplied ecliptic-projected radii."""
import math


def geocentric_from_heliocentric(sun_longitude,planet_longitude,sun_radius,
                                 planet_ecliptic_radius,heliocentric_latitude=0):
    """Book's inner/outer formula in signed Cartesian form, avoiding tan quadrants.

    planet_ecliptic_radius is the radius projected onto the ecliptic, not a
    spatial radius. Caller must establish that input. No ephemeris inferred.
    """
    vals=[sun_longitude,planet_longitude,sun_radius,planet_ecliptic_radius,heliocentric_latitude]
    if not all(math.isfinite(float(x)) for x in vals):
        raise ValueError('Inputs must be finite')
    if sun_radius <= 0 or planet_ecliptic_radius <= 0 or abs(heliocentric_latitude)>=90:
        raise ValueError('Positive radii and latitude strictly between-90and90 required')
    s=math.radians(sun_longitude);p=math.radians(planet_longitude)
    x=sun_radius*math.cos(s)+planet_ecliptic_radius*math.cos(p)
    y=sun_radius*math.sin(s)+planet_ecliptic_radius*math.sin(p)
    horizontal=math.hypot(x,y)
    if horizontal <= 1e-12*max(sun_radius,planet_ecliptic_radius):
        raise ValueError('Degenerate geocentric direction')
    z=planet_ecliptic_radius*math.tan(math.radians(heliocentric_latitude))
    return {'longitude_degrees':math.degrees(math.atan2(y,x))%360,
            'latitude_degrees':math.degrees(math.atan2(z,horizontal)),
            'ecliptic_distance':horizontal,'spatial_distance':math.hypot(horizontal,z)}


def geometry_example():
    result=geocentric_from_heliocentric(352.167,261.814,1000.7,450.4)
    return {'source':{'url':'https://archive.org/details/jyotir-ganita-venkatesh-ramakrishna-kethkar-dattatreya-ketkar-surakant-jha',
       'pdf_pages':[267,268,269],'printed_pages':[200,201,202],
       'rule':'publisher-inserted supplement42-49, direct tangent geometry',
       'verified_against_page_image':True},
       'formula_profile':'direct_signed_geometry_supplied_ecliptic_projected_radii',
       'supplied_inputs':{'sun_longitude':352.167,'planet_longitude':261.814,
                          'sun_radius':1000.7,'planet_ecliptic_radius':450.4},
       'computed_zero_latitude_candidate':result,
       'narrative_table_candidate_longitude':'327.879',
       'nyasa5_table_candidate_longitude':'327.878',
       'difference_from_narrative_degrees':result['longitude_degrees']-327.879,
       'physical_radius_vs_ecliptic_projection_verified':False,
       'full_historical_ephemeris_verified':False,
       'notice':'Source supplement explicitly provides a direct geometric route and notes alternative ordinary trigonometry. This implementation uses Cartesian sums equivalent to its signed tangent/quadrant rules. Fixture uses printed rounded radius as an explicitly assumed ecliptic projection with zero latitude, not an established physical Mercury radius.327.876015 differs from the table-correction candidates. No profile selected, no claim of external ephemeris accuracy or resolved source rounding.'}
