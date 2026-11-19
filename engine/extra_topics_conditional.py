"""Source-conditioned children, foreign-residence and partnership readings.

Rules come from Phaladeepika (1937 translation) Adhyaya XII (children),
Adhyaya VIII (planets in houses; foreign residence clauses) and Adhyaya XV
(bhava welfare, read for the 7th house of partnership). Effects are own-words
paraphrase of the translator's English; distressing clauses (loss of children,
bodily or character remarks, living at another's cost) are held out, matching
the marriage module's hold-out policy. Every rule reports 'met',
'possibly_met', 'not_met' or 'unresolved' and says why; 'benefic' is not
defined by these sentences, so a rule is 'met' only if it holds with Jupiter
and Venus alone, 'possibly_met' if it needs Mercury or the Moon.
"""
from .marriage_conditional import (DEFINITE_BENEFIC, CONDITIONAL_BENEFIC, MALEFIC,
                                   _aspects, _benefic_touch, _house, _lord_of_house,
                                   _owned_houses, _row, _sign_index, _tri, src)

PHALA = 'phaladeepika-1937'


def _ketu_house(chart):
    rahu = chart['placements'].get('Rahu')
    if not rahu:
        return None
    asc = int(chart['ascendant']['longitude'] // 30)
    ketu_sign = int(((rahu['longitude'] + 180) % 360) // 30)
    return (ketu_sign - asc) % 12 + 1


def children_conditional(chart, *, strength_verdicts=None):
    """Phaladeepika Adh. XII: conditions the text links with having children."""
    rows = []
    lagna_lord = _lord_of_house(chart, 1)
    fifth_lord = _lord_of_house(chart, 5)
    # XII.1: lagna lord and 5th lord posited together.
    together = _house(chart, lagna_lord) == _house(chart, fifth_lord)
    rows.append(_row('phaladeepika-xii-1-lagna-lord-with-5th-lord', src(PHALA, 'XII', '1', [153], [116]),
        'The lords of the Lagna and the 5th house sit together in one house',
        'The text counts this among the conditions under which the acquisition of children is assured.',
        'met' if together else 'not_met',
        f'Lagna lord {lagna_lord} in house {_house(chart, lagna_lord)}; 5th lord {fifth_lord} in house {_house(chart, fifth_lord)}'))
    # XII.1: they occupy each other's places (sign exchange).
    exchange = (_house(chart, lagna_lord) in _owned_houses(chart, fifth_lord)
                and _house(chart, fifth_lord) in _owned_houses(chart, lagna_lord))
    rows.append(_row('phaladeepika-xii-1-lagna-5th-exchange', src(PHALA, 'XII', '1', [153], [116]),
        'The lords of the Lagna and the 5th house occupy each other\'s signs',
        'The text counts this among the conditions under which the acquisition of children is assured.',
        'met' if exchange else 'not_met',
        f'{lagna_lord} in house {_house(chart, lagna_lord)}, {fifth_lord} in house {_house(chart, fifth_lord)}'))
    # XII.1: mutual aspect between them.
    mutual = (_aspects(chart, lagna_lord, _house(chart, fifth_lord))
              and _aspects(chart, fifth_lord, _house(chart, lagna_lord)))
    rows.append(_row('phaladeepika-xii-1-lagna-5th-mutual-aspect', src(PHALA, 'XII', '1', [153], [116]),
        'The lords of the Lagna and the 5th house aspect each other',
        'The text counts this among the conditions under which the acquisition of children is assured.',
        'met' if mutual else 'not_met',
        f'mutual whole-sign aspect between {lagna_lord} and {fifth_lord}: ' + ('present' if mutual else 'absent')))
    # XII.1: aspect of a benefic, or of a planet owning an auspicious house, on the 5th.
    d = [p for p in DEFINITE_BENEFIC if _aspects(chart, p, 5)]
    cond = [p for p in CONDITIONAL_BENEFIC if _aspects(chart, p, 5)]
    auspicious_owner = [p for p in ('Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn')
                        if p not in d and p not in cond and _aspects(chart, p, 5)
                        and not set(_owned_houses(chart, p)) & {6, 8, 12}]
    status = 'met' if d else 'possibly_met' if (cond or auspicious_owner) else 'not_met'
    rows.append(_row('phaladeepika-xii-1-benefic-aspect-on-5th', src(PHALA, 'XII', '1', [153], [116]),
        'The 5th house receives the aspect of a benefic, or of a planet owning an auspicious house',
        'The text counts this among the conditions under which the acquisition of children is assured.',
        status,
        f'aspecting benefics: {d}; conditional: {cond}; auspicious-house owners: {auspicious_owner}',
        unresolved=['benefic classification of Mercury/Moon']))
    # XII.3: a malefic owning the 5th sits in the 5th.
    occ = [p for p in MALEFIC if _house(chart, p) == 5 and 5 in _owned_houses(chart, p)]
    rows.append(_row('phaladeepika-xii-3-malefic-owner-in-5th', src(PHALA, 'XII', '3', [154], [117]),
        'A malefic that owns the 5th house sits in it',
        'The text says the person will have children under this condition.',
        'met' if occ else 'not_met',
        f'owner-occupants: {occ}' if occ else 'no malefic owns and occupies the 5th'))
    return {'rows': rows}


def foreign_conditional(chart):
    """Phaladeepika Adh. VIII: the two verses that mention living in a foreign place."""
    rows = []
    # VIII.21: Saturn in the 2nd.
    s2 = _house(chart, 'Saturn') == 2
    rows.append(_row('phaladeepika-viii-21-saturn-in-2nd', src(PHALA, 'VIII', '21', [129], [92]),
        'Saturn occupies the 2nd house',
        'The text says the person lives in a foreign country at a later age, with vehicles, wealth and enjoyments. Its other clauses are held out.',
        'met' if s2 else 'not_met',
        f'Saturn in house {_house(chart, "Saturn")}'))
    # VIII.29: Ketu in the 4th.
    kh = _ketu_house(chart)
    if kh is None:
        status, detail = 'unresolved', 'Rahu is missing from the placements, so the Ketu point cannot be derived'
    else:
        status, detail = ('met' if kh == 4 else 'not_met'), f'Ketu (the point opposite Rahu) falls in house {kh}'
    rows.append(_row('phaladeepika-viii-29-ketu-in-4th', src(PHALA, 'VIII', '29', [133], [96]),
        'Ketu occupies the 4th house',
        'The text says the person leaves the native country and dwells in a foreign place. Its other clauses are held out.',
        status, detail,
        unresolved=['Ketu is derived as the point opposite Rahu, matching the app\'s Tamil sheet']))
    return {'rows': rows}


def love_conditional(chart, *, strength_verdicts=None):
    """Phaladeepika Adh. XV read for the 7th house (partnership); Venus as 7th karaka (XV.17)."""
    sv = strength_verdicts or {}
    rows = []
    seventh_lord = _lord_of_house(chart, 7)
    # XV.1: benefics occupy or aspect the 7th.
    d, a = _benefic_touch(chart, 7)
    rows.append(_row('phaladeepika-xv-1-benefic-touch-7th', src(PHALA, 'XV', '1', [189], [152]),
        'Benefics occupy or aspect the 7th house',
        'The text says a bhava gives its good results fully when benefics occupy or aspect it; here the 7th house is read for partnership.',
        _tri(d, a),
        f'definite benefic touch: {d}; with Mercury/Moon: {a}',
        unresolved=['benefic classification of Mercury/Moon']))
    # XV.1: the 7th's own lord occupies or aspects it.
    own = _house(chart, seventh_lord) == 7 or _aspects(chart, seventh_lord, 7)
    rows.append(_row('phaladeepika-xv-1-own-lord-touch-7th', src(PHALA, 'XV', '1', [189], [152]),
        'The 7th lord occupies or aspects the 7th house',
        'The text says a bhava gives its good results fully when its own lord occupies or aspects it.',
        'met' if own else 'not_met',
        f'7th lord {seventh_lord} in house {_house(chart, seventh_lord)}'))
    # XV.1: the 7th is free from malefic association or aspect.
    malefic_touch = [p for p in MALEFIC if _house(chart, p) == 7 or _aspects(chart, p, 7)]
    rows.append(_row('phaladeepika-xv-1-7th-free-of-malefics', src(PHALA, 'XV', '1', [189], [152]),
        'The 7th house is free from association or aspect of malefics',
        'The text asks for this freedom as part of a bhava giving its good results fully.',
        'met' if not malefic_touch else 'not_met',
        f'malefic contact: {malefic_touch}' if malefic_touch else 'no malefic occupies or aspects the 7th'))
    # XV.17 + XV.25: Venus is the karaka of the 7th; bhava with strong karaka yields good effects.
    verdict = sv.get('Venus')
    if verdict is None:
        status, why = 'unresolved', 'Venus strength verdict not supplied'
    elif verdict.startswith('meets'):
        status, why = 'met', 'Venus meets the Sripati minimum in all variants'
    elif verdict.startswith('below'):
        status, why = 'not_met', 'Venus is below the Sripati minimum in all variants'
    else:
        status, why = 'unresolved', 'Venus strength is unresolved across school variants'
    rows.append(_row('phaladeepika-xv-17-venus-karaka-strong', src(PHALA, 'XV', '17, 25', [196, 198], [159, 161]),
        'Venus, the karaka of the 7th house, is strong',
        'The text names Venus as the karaka of the 7th bhava and says a bhava whose lord and karaka are strong yields good effects.',
        status, why, needs=['shadbala verdict'],
        unresolved=['meaning of strength not defined in the sloka']))
    return {'rows': rows}
