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
    latitude_candidates={str(arcmin):geocentric_from_heliocentric(352.167,261.814,1000.7,450.4,arcmin/60) for arcmin in (-352.6,-353.4)}
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
       'source_labels_input_as_ecliptic_radius':True,
       'physical_radius_vs_ecliptic_projection_verified':False,
       'heliocentric_latitude_candidates_arcmin':latitude_candidates,
       'supplement_corrected_heliocentric_latitude_arcmin':-353.4,
       'supplement_printed_geocentric_latitude_arcmin':-145.8,
       'computed_corrected_geocentric_latitude_arcmin':latitude_candidates['-353.4']['latitude_degrees']*60,
       'full_historical_ephemeris_verified':False,
       'notice':"Source supplement explicitly provides a direct geometric route and notes alternative ordinary trigonometry. This implementation uses Cartesian sums equivalent to its signed tangent/quadrant rules. SupplementPDF268 explicitly labels450.4 an ecliptic manda radius, so the source-specific input convention is grounded. This is not independent certification of a physical Mercury radius. Zero-latitude fixture is retained as one candidate; supplied latitude alternatives-352.6 and supplement correction-353.4arcmin are separately computed. Corrected latitude gives-145.808054arcmin, reproducing printed-145.8 at one decimal without selecting the book's full precision policy.327.876015 differs from the table-correction candidates. No profile selected, no claim of external ephemeris accuracy or resolved source rounding."}
