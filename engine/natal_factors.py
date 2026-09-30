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


def natal_factors(ascendant_sign, placements, bhava_centres=None):
    from .strength_components import components
    from .friendship import relationship_evidence
    from .vargas import varga_owner_evidence,seven_varga_owner_evidence
    from .strength_precedence import condition_precedence
    from .continuous_strength import continuous_components
    from .degree_aspects import degree_aspect_evidence
    from .friendship import compound_relationship_candidates
    from .lordship_precedence import lordship_precedence
    from .planetary_war import chart_war_evidence
    from .seven_varga_strength import chart_direct_owner_candidates
    from .positional_candidates import positional_candidates
    return {'base_positional_candidates':positional_candidates(placements),
            'seven_varga_numeric_candidates':chart_direct_owner_candidates(placements),
            'planetary_war_coordinate_evidence':chart_war_evidence(placements,coordinate_profile='Lahiri sidereal Swiss Ephemeris/Moshier geocentric ecliptic coordinates'),
            'scoped_lordship_precedence':lordship_precedence(ascendant_sign),
            'compound_relationship_candidates':compound_relationship_candidates(placements),
            'degree_aspect_evidence':degree_aspect_evidence(placements),
            'continuous_strength_components':continuous_components(placements,bhava_centres),
            'scoped_strength_conditions':{p:condition_precedence(p,x['sign'],x.get('longitude'),x.get('retrograde'),x.get('overpowered_sun_rays')) for p,x in placements.items()},
            'seven_varga_owner_evidence':{p:seven_varga_owner_evidence(p,x['longitude']) for p,x in placements.items() if x.get('longitude') is not None},
            'six_varga_owner_evidence':{p:varga_owner_evidence(p,x['longitude']) for p,x in placements.items() if x.get('longitude') is not None},
            'relationship_evidence':relationship_evidence(placements),
            'strength_components':components(ascendant_sign,placements),
            'dignity':{p:dignity(p,x['sign'],x.get('longitude')) for p,x in placements.items()},
            'sign_exchanges':exchanges(placements),
            'maha_purusha_conditions':mahapurusha(ascendant_sign,placements),
            'missing_strength_components':['source-selected complete temporal profile (standalone solar-clock/declination/third/lord helpers available)','automatic traditional motional-angle generation (supplied Cheshtakendra helper available)','source-selected seven-varga component (distinct chart-derived direct-owner candidates available)','automatic combustion thresholds','source-selected planetary war/winner adjustment (supplied coordinate evidence helper available)','automatic signed aspect profile (explicit-classification adjustment helper available)','source-selected complete positional profile','source-selected total sixfold strength'],
            'unresolved_conventions':['phase complement and Sun/Moon multipliers','Rasi versus degree-Bhava house-category interpretation','exact Sandhi membership','global outcome precedence'],
            'sixfold_source':SOURCE_SIXFOLD,
            'notice':'No total strength score, comparative rank, or outcome is justified by these partial factors.'}
