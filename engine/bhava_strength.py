"""Sripati III.21-23 supplied-category degree Bhava direction only."""
from .continuous_strength import source,valid_longitude,folded_distance

WEAKEST={'human':7,'quadruped':4,'reptile':1,'watery':10}


def bhava_digbala(house,category,bhava_centres,*,category_profile):
    if type(house) is not int or not 1<=house<=12:raise ValueError('House1..12 required')
    if category not in WEAKEST:raise ValueError('Grounded symbolic sign category required')
    if not category_profile:raise ValueError('Named externally grounded category profile required')
    weakest=WEAKEST[category]
    if house not in bhava_centres or weakest not in bhava_centres:raise ValueError('Required centres missing')
    centre=bhava_centres[house];anchor=bhava_centres[weakest]
    valid_longitude(centre);valid_longitude(anchor)
    arc=folded_distance(centre,anchor)
    return {'house':house,'supplied_category':category,'category_profile':category_profile,
            'weakest_house':weakest,'distance_degrees':arc,'rupa':arc/180,
            'sources':[source('21-23',76,62),source('22-23',77,63)],
            'classification_disagreements':{'source':source('23 commentary',78,64),
                'notice':'Aquarius human versus split quadruped/watery; Cancer watery versus reptile. Supplied named profile required; no automatic classification.'},
            'total_bhava_strength':None,
            'notice':'Direction subcomponent only. Complete lord strength, source-defined cross-sign lord weighting, signed aspects and extra full Mercury/Jupiter aspects remain separate. Historical animal/human categories describe symbolic signs, not people.'}
