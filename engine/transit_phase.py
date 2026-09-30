"""Phaladeepika XXVI.25 sign-third timing condition, not an outcome gate."""
from .continuous_strength import valid_longitude

THIRDS={'Sun':0,'Mars':0,'Jupiter':1,'Venus':1,'Moon':2,'Saturn':2}
SOURCE={'slug':'phaladeepika-1937','chapter':'XXVI','sloka':25,'pdf_page':333,
        'printed_page':296,'verified_against_page_image':True,
        'url':'https://archive.org/details/in.ernet.dli.2015.92117'}


def transit_phase(planet,longitude):
    valid_longitude(longitude)
    degree=longitude%30
    if planet=='Ketu':
        return {'planet':planet,'status':'not_covered','active_condition':None,'source':SOURCE,
                'notice':'No Ketu timing rule supplied by this passage. Rahu rule is not copied.'}
    if planet not in THIRDS and planet not in ('Mercury','Rahu'):raise ValueError('Planet not covered')
    throughout=planet in ('Mercury','Rahu')
    boundary=not throughout and degree in (10,20)
    active=True if throughout else None if boundary else int(degree//10)==THIRDS[planet]
    return {'planet':planet,'degree_in_sign':degree,'third_1_based':None if boundary else int(degree//10)+1,
            'specified_third_1_based':None if throughout else THIRDS[planet]+1,
            'throughout_passage':throughout,'active_condition':active,
            'boundary_unresolved':boundary,'source':SOURCE,
            'notice':'Historical transit timing evidence only. Degree, not chronological first/middle/last of retrograde visit. Does not suppress existing verse readings, certify a date, infer an event or establish Balaji practice.'}
