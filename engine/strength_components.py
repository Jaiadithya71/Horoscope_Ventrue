"""Partial IV.2-3/8 strength evidence, never total Shadbala or an outcome."""
from .forecast import SIGNS, sign_index


def source(verse,page,printed):
    return {'slug':'phaladeepika-1937','chapter':'IV','sloka':verse,
            'pdf_page':page,'printed_page':printed,'verified_against_page_image':True}

DIRECTION_HOUSES={'Sun':10,'Mars':10,'Venus':4,'Moon':4,'Mercury':1,'Jupiter':1,'Saturn':7}
NATURAL_ORDER=('Saturn','Mars','Mercury','Jupiter','Venus','Moon','Sun')


def components(ascendant_sign,placements):
    """Whole-sign house convention and supplied retrograde flags are explicit.

    IV.3 gives category fractions; IV.8 refines the Kendra fractions differently.
    Keep both as separate candidates rather than add them or choose a winner.
    IV.2 directional signs are evidence, not exact angular Digbala values.
    """
    reference=sign_index(ascendant_sign)
    rows={}
    for planet,p in placements.items():
        house=(sign_index(p['sign'])-reference)%12+1
        if planet not in DIRECTION_HOUSES:
            rows[planet]={'status':'not_scored','reason':'Node components outside this checked rule slice'}
            continue
        category = 'kendra' if house in (1,4,7,10) else 'panaphara' if house in (2,5,8,11) else 'apoklima'
        fraction={'kendra':1.0,'panaphara':0.5,'apoklima':0.25}[category]
        candidates=[{'rule':'bhava_category','rupa':fraction,'source':source('3',72,35)}]
        if category=='kendra':
            candidates.append({'rule':'kendra_refinement','rupa':{1:1.0,4:0.25,7:0.75,10:0.5}[house],
                               'source':source('8',74,37)})
        motion=None
        if planet not in ('Sun','Moon'):
            motion=p.get('retrograde')
            if motion is not None and not isinstance(motion,bool):
                raise ValueError('Retrograde flag must be boolean or absent')
        rows[planet]={
            'whole_sign_house_from_ascendant':house,
            'house_strength_candidates':candidates,
            'house_candidate_conflict':len({x['rupa'] for x in candidates})>1,
            'directional_house_condition':{'matched':house==DIRECTION_HOUSES[planet],
                 'target_house':DIRECTION_HOUSES[planet],'source':source('2',71,34),
                 'notice':'Whole-sign condition only, not continuous angular Digbala'},
            'retrograde_motional_condition':{'matched':motion,'source':source('2',71,34),
                 'notice':'Not a numerical Cheshtabala; Sun north-course and full Moon conditions unimplemented'},
            'natural_strength_order':{'ordinal':NATURAL_ORDER.index(planet)+1,'source':source('3',72,35),
                 'notice':'Book order only, not a numeric component or overall planet rank'}
        }
    return {'planets':rows,'house_convention':'whole-sign from supplied ascendant; not degree-based bhava boundaries',
            'status':'partial_evidence_only','total_strength':None,
            'notice':'Do not sum candidates, infer total strength, resolve dignity overlap, or unlock personal-outcome rules.'}
