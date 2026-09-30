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

COMPOUND_SOURCE={'slug':'phaladeepika-kapoor','chapter':'II','sloka':'23 commentary',
                 'pdf_pages':[22,23],'printed_pages':[22,23],
                 'verified_against_page_image':True,
                 'url':'https://jyotishvidya.com/HTMLobj-9415/Mantreswara_s__Phaladeeplka_.pdf'}


def compound_relation(natural,other_house):
    """Explicit Kapoor commentary mapping; house convention belongs to caller."""
    if natural not in ('friend','neutral','enemy'):raise ValueError('Natural relation required')
    if type(other_house) is not int or not 1<=other_house<=12:raise ValueError('Relative house must be1..12')
    temporal='friend' if other_house in (2,3,4,10,11,12) else 'enemy'
    mapping={('friend','friend'):'very_friend',('friend','enemy'):'neutral',
             ('neutral','friend'):'friend',('neutral','enemy'):'enemy',
             ('enemy','friend'):'neutral',('enemy','enemy'):'very_enemy'}
    return {'natural_relation':natural,'temporal_relation':temporal,
            'compound_relation':mapping[(natural,temporal)],'other_house':other_house,
            'source':COMPOUND_SOURCE,
            'notice':'Source-labeled compound relation, not an outcome or overall strength. Caller must identify the house-count convention.'}


def compound_relationship_candidates(placements):
    rows=[]
    for a in CLASSICAL:
        for b in CLASSICAL:
            if a==b or a not in placements or b not in placements:continue
            rasi=(sign_index(placements[b]['sign'])-sign_index(placements[a]['sign']))%12+1
            candidates=[{'house_profile':'rasi_relative',**compound_relation(natural_relation(a,b),rasi)}]
            ha=placements[a].get('sripati_degree_house',{}).get('house')
            hb=placements[b].get('sripati_degree_house',{}).get('house')
            if ha is not None and hb is not None:
                candidates.append({'house_profile':'lagna_bhava_relative',**compound_relation(natural_relation(a,b),(hb-ha)%12+1)})
            rows.append({'planet':a,'other':b,'candidates':candidates,
                         'candidate_conflict':len({x['compound_relation'] for x in candidates})>1})
    return {'directed_pairs':rows,'selected_profile':None,
            'house_convention_source':{'slug':'sripatipaddhati-sastri-archive-203510','chapter':'III','sloka':'3 commentary','pdf_pages':[41,43],'printed_pages':[27,29],'verified_against_page_image':True,'url':'https://archive.org/details/dli.ernet.203510'},
            'notice':'No winner chosen between Rasi and Lagna-Bhava. Planet-specific recast Bhava convention discussed by Sripati is not calculated. No seven-varga total selected automatically.'}
