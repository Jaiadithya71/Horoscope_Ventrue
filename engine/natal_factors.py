"""Checked partial natal factors, not Shadbala or predictions."""
from .forecast import SIGNS, sign_index
from .synthesis import LORDS, LORD_SOURCE

SOURCE_DIGNITY={'slug':'phaladeepika-1937','pdf_page':40,'printed_page':3,'chapter':'I','sloka':6,'verified_against_page_image':True}
SOURCE_POSITION={'slug':'phaladeepika-1937','pdf_page':73,'printed_page':36,'chapter':'IV','sloka':7,'verified_against_page_image':True}
SOURCE_SIXFOLD={'slug':'phaladeepika-1937','pdf_pages':[70,71],'printed_pages':[33,34],'chapter':'IV','sloka':1,'verified_against_page_image':True}
SOURCE_MOOLA={'slug':'phaladeepika-1937','pdf_page':41,'printed_page':4,'chapter':'I','sloka':7,'verified_against_page_image':True}
SOURCE_YOGA={'slug':'phaladeepika-1937','pdf_pages':[83,84],'printed_pages':[46,47],
             'chapter':'VI','sloka':1,'verified_against_page_image':True}
SOURCE_EXCHANGE={'slug':'phaladeepika-1937','pdf_page':96,'printed_page':59,
                 'chapter':'VI','sloka':32,'verified_against_page_image':True}
# Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, in I.6 order.
EXALTATION={'Sun':'Aries','Moon':'Taurus','Mars':'Capricorn','Mercury':'Virgo',
            'Jupiter':'Cancer','Venus':'Pisces','Saturn':'Libra'}
YOGA_NAMES={'Mars':'Ruchaka','Mercury':'Bhadra','Jupiter':'Hamsa',
            'Venus':'Malavya','Saturn':'Sasa'}


MOOLATRIKONA={'Sun':('Leo',0,20),'Moon':('Taurus',3,30),
               'Mars':('Aries',0,12),'Mercury':('Virgo',16,20),
               'Jupiter':('Sagittarius',0,10),'Venus':('Libra',0,5),
               'Saturn':('Aquarius',0,20)}


def dignity(planet, sign, longitude=None):
    """Candidate IV.7 positional fractions only; conflicting conditions remain unresolved."""
    sign_i=sign_index(sign)
    if planet not in EXALTATION:
        return {'planet':planet,'sign':sign,'status':'not_scored',
                'reason':'Node dignity and full strength not covered by this narrow rule.'}
    if longitude is not None and not 0 <= longitude < 360:
        raise ValueError('Longitude must be in [0,360)')
    if longitude is not None and sign_i!=int(longitude//30):
        raise ValueError('Supplied sign disagrees with sidereal longitude')
    exalt=EXALTATION[planet]
    fall=SIGNS[(sign_index(exalt)+6)%12]
    own=LORDS[sign_i]==planet
    msign,begin,end=MOOLATRIKONA[planet]
    moola=sign==msign and longitude is not None and begin<=longitude%30<end
    possible_moola=sign==msign and longitude is None
    flags={'exaltation_sign':sign==exalt,'own_sign':own,'fall_sign':sign==fall,
           'moolatrikona_portion':moola if longitude is not None else None}
    candidates=[]
    if flags['exaltation_sign']:candidates.append({'condition':'exaltation_sign','rupa':1.0})
    if moola:candidates.append({'condition':'moolatrikona_portion','rupa':0.75})
    if own:candidates.append({'condition':'own_sign','rupa':0.5})
    if flags['fall_sign']:candidates.append({'condition':'fall_sign','rupa':0.0})
    # Moolatrikona is a portion of the owned sign; the text does not specify how
    # to combine it with own or overlapping exaltation conditions. Do not decide.
    return {'planet':planet,'sign':sign,'flags':flags,'positional_rupa_candidates':candidates,
            'candidate_conflict':len(candidates)>1 or possible_moola,
            'sources':[SOURCE_DIGNITY,SOURCE_MOOLA,SOURCE_POSITION,LORD_SOURCE],
            'notice':'Unadjusted IV.7 candidates, not a resolved score. Sixfold strength, combustion, and overlapping-condition precedence are not computed.'}


def exchanges(placements):
    """Distinct pair of classical planets each occupying the other's sign."""
    result=[]
    classical=EXALTATION.keys()
    for i,a in enumerate(classical):
        if a not in placements: continue
        for b in list(classical)[i+1:]:
            if b not in placements: continue
            sa,sb=placements[a]['sign'],placements[b]['sign']
            if sa!=sb and LORDS[sign_index(sa)]==b and LORDS[sign_index(sb)]==a:
                result.append({'planets':[a,b],'occupied_signs':[sa,sb],
                               'source':SOURCE_EXCHANGE,
                               'notice':'Mutual sign ownership only; no Dainya/Khala/Maha classification or outcome asserted.'})
    return result


def mahapurusha(reference_sign, placements):
    """The five Kendra plus own/exaltation geometric yoga conditions only."""
    i=sign_index(reference_sign)
    found=[]
    for planet,name in YOGA_NAMES.items():
        if planet not in placements:continue
        sign=placements[planet]['sign']
        house=(sign_index(sign)-i)%12+1
        d=dignity(planet,sign,placements[planet].get('longitude'))
        if house in (1,4,7,10) and (d['flags']['own_sign'] or d['flags']['exaltation_sign']):
            found.append({'name':name,'planet':planet,'sign':sign,'house_from_ascendant':house,
                          'dignity':d['flags'],'source':SOURCE_YOGA,
                          'notice':'Condition detected. Textual outcome and degree/strength qualifiers not evaluated.'})
    return found


def natal_factors(ascendant_sign, placements):
    from .strength_components import components
    from .friendship import relationship_evidence
    return {'relationship_evidence':relationship_evidence(placements),
            'strength_components':components(ascendant_sign,placements),
            'dignity':{p:dignity(p,x['sign'],x.get('longitude')) for p,x in placements.items()},
            'sign_exchanges':exchanges(placements),
            'maha_purusha_conditions':mahapurusha(ascendant_sign,placements),
            'missing_strength_components':['temporal','numeric motional (retrograde condition only)','numeric directional (whole-sign condition only)','declination','six-varga positional detail','combustion','exaltation/own/moola precedence','house boundary'],
            'sixfold_source':SOURCE_SIXFOLD,
            'notice':'No total strength score, comparative rank, or outcome is justified by these partial factors.'}
