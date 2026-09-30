"""Directional natural friendship and a narrowly sourced IV.10 preference.

This is not a general priority between outcome rules or a numeric score.
"""
from .forecast import sign_index

CLASSICAL=('Sun','Moon','Mars','Mercury','Jupiter','Venus','Saturn')
FRIENDS={'Sun':{'Moon','Mars','Jupiter'},'Moon':{'Sun','Mercury'},
         'Mars':{'Sun','Moon','Jupiter'},'Mercury':{'Sun','Venus'},
         'Jupiter':{'Sun','Moon','Mars'},'Venus':{'Mercury','Saturn'},
         'Saturn':{'Mercury','Venus'}}
ENEMIES={'Sun':{'Venus','Saturn'},'Moon':set(),'Mars':{'Mercury'},
         'Mercury':{'Moon'},'Jupiter':{'Venus','Mercury'},
         'Venus':{'Sun','Moon'},'Saturn':{'Sun','Moon','Mars'}}
NATURAL_SOURCE={'slug':'phaladeepika-1937','pdf_page':54,'printed_page':17,
                'chapter':'II','sloka':'21-22','verified_against_page_image':True}
TEMPORAL_SOURCE={'slug':'phaladeepika-1937','pdf_page':55,'printed_page':18,
                 'chapter':'II','sloka':'23','verified_against_page_image':True}
PREFERENCE_SOURCE={'slug':'phaladeepika-1937','pdf_page':74,'printed_page':37,
                   'chapter':'IV','sloka':'10','verified_against_page_image':True}


def natural_relation(planet, other):
    if planet not in CLASSICAL or other not in CLASSICAL or planet==other:
        raise ValueError('Relationship requires two distinct classical planets')
    if other in FRIENDS[planet]:return 'friend'
    if other in ENEMIES[planet]:return 'enemy'
    return 'neutral'


def relationship_evidence(placements):
    rows=[]
    for planet in CLASSICAL:
        if planet not in placements:continue
        for other in CLASSICAL:
            if other==planet or other not in placements:continue
            house=(sign_index(placements[other]['sign'])-sign_index(placements[planet]['sign']))%12+1
            natural=natural_relation(planet,other)
            # II.23 only explicitly lists temporal friendship. Do not invent
            # an enemy classification for unlisted positions in this slice.
            temporal_friend=house in (2,3,4,10,11,12)
            rows.append({'planet':planet,'other':other,'natural_relation':natural,
                         'other_house_from_planet':house,
                         'temporal_friend_condition':temporal_friend,
                         'preferred_relation_evidence':{'kind':'natural','relation':natural,
                              'source':PREFERENCE_SOURCE},
                         'sources':[NATURAL_SOURCE,TEMPORAL_SOURCE],
                         'notice':'IV.10 prefers natural relationship evidence; temporal facts retained. No compound relationship, overall strength or personal outcome is inferred.'})
    return {'directed_pairs':rows,'scope':'natural versus temporal relationship evidence only',
            'outcome_precedence':None,'notice':'Natural friendship is directional, not necessarily mutual. This preference never resolves unrelated outcome conflicts.'}
