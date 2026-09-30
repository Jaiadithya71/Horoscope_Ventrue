"""Numerical Sripatipaddhati III.2/8 components. Never total strength."""
import math

NEECHA={'Sun':190.0,'Moon':213.0,'Mars':118.0,'Mercury':345.0,'Jupiter':275.0,'Venus':177.0,'Saturn':20.0}
WEAKEST_BHAVA={'Sun':4,'Mars':4,'Mercury':7,'Jupiter':7,'Venus':10,'Moon':10,'Saturn':1}

def source(verse,page,printed):
    return {'slug':'sripatipaddhati-sastri-archive-203510','chapter':'III','sloka':verse,
            'pdf_page':page,'printed_page':printed,'verified_against_page_image':True,
            'url':'https://archive.org/details/dli.ernet.203510',
            'edition_notice':'Scan lists fifth edition 1976; archive metadata says 2005. Not asserted as 1937 edition.'}


def valid_longitude(x):
    if not math.isfinite(x) or not 0<=x<360:raise ValueError('Longitude must be finite and in [0,360)')


def folded_distance(a,b):
    delta=(a-b)%360
    return min(delta,360-delta)


def uchchabala(planet,longitude):
    if planet not in NEECHA:raise ValueError('Classical planet required')
    valid_longitude(longitude)
    arc=folded_distance(longitude,NEECHA[planet])
    return {'planet':planet,'longitude':longitude,'neecha_longitude':NEECHA[planet],
            'distance_from_neecha_degrees':arc,'rupa':arc/180,'virupa':arc/3,
            'source':source('2',38,24),
            'degree_source':{'slug':'phaladeepika-1937','chapter':'I','sloka':6,
                             'pdf_pages':[40,41],'printed_pages':[3,4],'verified_against_page_image':True},
            'notice':'Continuous exaltation component only; not IV.7 sign dignity or total Shadbala.'}


def digbala(planet,longitude,bhava_centres):
    """Require actual centre longitudes. Whole-sign numbers are not centres."""
    if planet not in WEAKEST_BHAVA:raise ValueError('Classical planet required')
    valid_longitude(longitude)
    n=WEAKEST_BHAVA[planet]
    if n not in bhava_centres:raise ValueError('Required degree-based bhava centre missing')
    centre=bhava_centres[n];valid_longitude(centre)
    arc=folded_distance(longitude,centre)
    return {'planet':planet,'longitude':longitude,'weakest_bhava':n,'weakest_bhava_centre':centre,
            'distance_from_weakest_bhava_degrees':arc,'rupa':arc/180,'virupa':arc/3,
            'source':source('8',55,41),
            'notice':'Uses supplied degree-based bhava centre, not whole-sign house. Centre calculation/house-system verification remains caller responsibility.'}


def continuous_components(placements,bhava_centres=None):
    rows={}
    for planet,p in placements.items():
        if planet not in NEECHA or p.get('longitude') is None:continue
        rows[planet]={'uchchabala':uchchabala(planet,p['longitude']),
                      'digbala':digbala(planet,p['longitude'],bhava_centres) if bhava_centres is not None else None}
    return {'planets':rows,'status':'two_component_slice' if bhava_centres is not None else 'uchchabala_only',
            'total_strength':None,'notice':'Do not sum with IV.7 dignity candidates or infer a total or personal outcome. No bhava centres are fabricated from whole-sign labels.'}
