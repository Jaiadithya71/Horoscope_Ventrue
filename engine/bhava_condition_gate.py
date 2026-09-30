"""Phaladeepika XV.25-26 condition audit; never a personal forecast."""
DISTRESS_ALTERNATIVE={'Sun':9,'Moon':4,'Mars':3,'Jupiter':5,'Venus':7,'Saturn':8}
SOURCE={'slug':'phaladeepika-1937','chapter':'XV','sloka':'25-26',
        'pdf_page':198,'printed_page':161,'verified_against_page_image':True,
        'url':'https://archive.org/details/in.ernet.dli.2015.92117'}


def audit_bhava_conditions(house,*,bhava_strong=None,lord_strong=None,karaka_strong=None,
                           strength_profile=None,planet_houses=None):
    """External grounded strength flags; missing data cannot imply a result.

    Explicit placement map is needed to check competing XV.26. It may be a
    documented complete or partial map; a partial map cannot rule out conflict.
    Caller names geometry; no whole-sign/degree-Bhava substitution is made.
    """
    if type(house) is not int or not 1<=house<=12:raise ValueError('House must be integer 1..12')
    flags={'bhava':bhava_strong,'lord':lord_strong,'karaka':karaka_strong}
    if any(x is not None and type(x) is not bool for x in flags.values()):raise ValueError('Strength flags must be bool or None')
    if any(x is not None for x in flags.values()) and not strength_profile:raise ValueError('Grounded supplied strength profile required')
    supplied=planet_houses if planet_houses is not None else {}
    for planet,h in supplied.items():
        if planet not in ('Sun','Moon','Mars','Mercury','Jupiter','Venus','Saturn','Rahu','Ketu'):raise ValueError('Unknown planet')
        if h is not None and (type(h) is not int or not 1<=h<=12):raise ValueError('Supplied house must be integer1..12 or None')
    missing_strength=[k for k,v in flags.items() if v is None]
    favorable=None if missing_strength else all(flags.values())
    alternative=[p for p,h in DISTRESS_ALTERNATIVE.items() if h==house and supplied.get(p)==house]
    # Only a planet named for this specific house can activate XV.26.
    relevant=[p for p,h in DISTRESS_ALTERNATIVE.items() if h==house]
    unchecked=[p for p in relevant if supplied.get(p) is None]
    conflict=True if favorable and alternative else None if favorable is None or unchecked else False
    return {'house':house,'strength_profile':strength_profile,'supplied_strength_flags':flags,
            'all_three_strength_condition':favorable,'missing_strength':missing_strength,
            'quoted_alternative_planets_matched':alternative,'unchecked_alternative_planets':unchecked,
            'conflict':conflict,'selected_polarity':None,'status':'abstain','source':SOURCE,
            'notice':'XV.25 all-three-strong condition and XV.26 explicitly quoted others-say alternative retained together. False condition is not an adverse forecast. No tie-break, degree geometry, karaka mapping, automatic strength classification, event or timing conclusion is inferred.'}
