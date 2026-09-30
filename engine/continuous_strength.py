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
                      'naisargikabala':naisargikabala(planet),
                      'pakshabala_candidates':pakshabala_candidates(planet,placements['Sun']['longitude'],placements['Moon']['longitude']) if placements.get('Sun',{}).get('longitude') is not None and placements.get('Moon',{}).get('longitude') is not None else None,
                      'digbala':digbala(planet,p['longitude'],bhava_centres) if bhava_centres is not None else None}
    return {'planets':rows,'status':'partial_numeric_components',
            'total_strength':None,'notice':'Do not sum with IV.7 dignity candidates or infer a total or personal outcome. No bhava centres are fabricated from whole-sign labels.'}

NATURAL_ORDER=('Saturn','Mars','Mercury','Jupiter','Venus','Moon','Sun')
QUOTED_NATURAL_VIRUPA={'Sun':60,'Moon':51,'Mars':17,'Mercury':26,'Jupiter':34,'Venus':43,'Saturn':9}


def naisargikabala(planet):
    if planet not in NATURAL_ORDER:raise ValueError('Classical planet required')
    rank=NATURAL_ORDER.index(planet)+1
    return {'planet':planet,'rupa':rank/7,'rational_rupa':f'{rank}/7',
            'virupa':60*rank/7,'source':source('19',73,59),
            'quoted_comparison':{'virupa':QUOTED_NATURAL_VIRUPA[planet],
                                 'notice':'Same page quotes integer Parashara values; not substituted for Sripati fractions.'},
            'notice':'Constant natural component, not whole-chart strength or rank.'}


def pakshabala_candidates(planet,sun_longitude,moon_longitude):
    if planet not in NATURAL_ORDER:raise ValueError('Classical planet required')
    valid_longitude(sun_longitude);valid_longitude(moon_longitude)
    elongation=(moon_longitude-sun_longitude)%360
    folded=min(elongation,360-elongation)/180
    benefic=planet in ('Moon','Mercury','Venus','Jupiter')
    commentary=folded if benefic else 1-folded
    # The translated main passage says to complement for the dark half,
    # unlike its folded-arc commentary. Keep the literal candidate visible.
    literal_benefic=folded if elongation<=180 else 1-folded
    literal=literal_benefic if benefic else 1-literal_benefic
    return {'planet':planet,'elongation_degrees':elongation,
            'phase':'bright_half' if elongation<=180 else 'dark_half',
            'candidates':[{'profile':'folded_arc_commentary','rupa':commentary,'source':source('11-12 commentary',59,45)},
                          {'profile':'literal_translated_dark_half_complement','rupa':literal,'source':source('11-12',58,44)}],
            'candidate_conflict':abs(commentary-literal)>1e-12,
            'classification_profile':'Moon/Mercury/Venus/Jupiter benefic for this component; Sun/Mars/Saturn malefic',
            'notice':'Source-specific candidates only. Commentary keeps Mercury benefic and Moon benefic while waning; other schools are mentioned. No automatic winner or Moon multiplier added.'}
