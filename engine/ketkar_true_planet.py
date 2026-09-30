"""III13-15 correction operations with explicit inputs and no table selection."""
from decimal import Decimal, ROUND_HALF_UP


def true_sighra_radius(mean_radius, planet_term, solar_term):
    values=[Decimal(str(x)) for x in (mean_radius,planet_term,solar_term)]
    result=sum(values)
    if result <= 0:
        raise ValueError('Sighra radius must be positive')
    return result


def corrected_inantara(asphuta_correction, mean_radius, true_radius):
    a,m,t=(Decimal(str(x)) for x in (asphuta_correction,mean_radius,true_radius))
    if m <= 0 or t <= 0:
        raise ValueError('Sighra radii must be positive')
    return a*m/t


def true_geocentric_longitude(provisional_longitude, correction):
    value=Decimal(str(provisional_longitude))+Decimal(str(correction))
    return (value % Decimal(360)+Decimal(360)) % Decimal(360)


def mercury_example():
    radius=true_sighra_radius('1069.9','22.8','.7')
    correction=corrected_inantara('-3.149','1069.9',radius)
    rounded=correction.quantize(Decimal('.001'),rounding=ROUND_HALF_UP)
    longitude=true_geocentric_longitude('330.960',rounded)
    return {'source':{'url':'https://archive.org/details/jyotir-ganita-venkatesh-ramakrishna-kethkar-dattatreya-ketkar-surakant-jha',
        'pdf_pages':[174,175,181,182],'printed_pages':[107,108,114,115],
        'rule':'III13-15, worked Mercury narrative and Nyasa5',
        'verified_against_page_image':True},
        'scope':'1928-04-05 supplied Mercury narrative inputs only',
        'supplied_mean_sighra_radius':'1069.9','supplied_radius_terms':['22.8','.7'],
        'computed_true_radius':str(radius),'printed_narrative_true_radius':'1093.4',
        'supplied_asphuta_correction_degrees':'-3.149',
        'computed_correction_degrees':str(correction),
        'candidate_half_up_correction_degrees':str(rounded),
        'printed_narrative_correction_degrees':'-3.081',
        'supplied_provisional_longitude_degrees':'330.960',
        'computed_longitude_at_narrative_precision':str(longitude),
        'printed_narrative_longitude_degrees':'327.879',
        'printed_nyasa5_final_longitude_degrees':'327.878',
        'narrative_final_matches':longitude==Decimal('327.879'),
        'narrative_and_table_final_agree':False,
        'upstream_asphuta_rounding_verified':False,'table14_lookup_reconstructed':False,
        'arbitrary_date_ephemeris_complete':False,'selected_natal_strength':None,
        'notice':'Implements signed correction times mean/true sighra-radius ratio and longitude addition. Radius contributions and provisional/asphuta values remain supplied. Narrative intermediate62.99 times-.050 gives-3.1495, but prints-3.149; no universal rounding inferred. Nyasa5 final327.878 differs from narrative327.879 by.001degree. Keep both, do not print-fit or select a corrected edition.'}
