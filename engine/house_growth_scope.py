"""XV.18-19 house growth is not automatically benefit to the person."""
SOURCE={'url':'https://archive.org/details/in.ernet.dli.2015.92117','slug':'phaladeepika-1937','chapter':'XV','sloka':'18-19','pdf_page':196,'printed_page':159,'verified_against_page_image':True}
COMPARISON={'url':'https://jyotishvidya.com/HTMLobj-9415/Mantreswara_s__Phaladeeplka_.pdf','pdf_page':151,'chapter':'XV','sloka':'18-19','verified_against_page_image':True}


def house_growth_scope(house,supplied_class,*,classification_profile,house_profile):
    if house is not None and (type(house) is not int or not 1<=house<=12):raise ValueError('House1..12 or unknown required')
    if supplied_class not in (None,'benefic','malefic'):raise ValueError('Supplied benefic/malefic class or unknown required')
    if not isinstance(classification_profile,str) or not classification_profile.strip():raise ValueError('Named supplied classification profile required')
    if not isinstance(house_profile,str) or not house_profile.strip():raise ValueError('Named house profile required')
    dusthana=None if house is None else house in (6,8,12)
    growth=None;evil=None
    if house is not None and supplied_class is not None:
        growth=('decay' if supplied_class=='benefic' else 'growth') if dusthana else ('growth' if supplied_class=='benefic' else 'decay')
        if dusthana:evil='reduced' if supplied_class=='benefic' else 'intensified'
    return {'house':house,'house_profile':house_profile,'supplied_class':supplied_class,
        'classification_profile':classification_profile,'dusthana':dusthana,
        'xv18_satyacharya_house_effect':growth,'xv19_dusthana_evil_effect':evil,
        'shared_dusthana_direction_consistent':True if evil is not None else None,
        'source':SOURCE,'comparison_source':COMPARISON,
        'personal_benefit':None,'global_precedence':None,
        'notice':'XV.18 explicitly reverses house growth/decay in6/8/12. XV.19 describes growth of evil versus its reduction there. These are consistent scoped directions, not a demonstrated school conflict or personal forecast. Good for a house is not necessarily good for its person. Supplied classification, dignity, strength, owned-house effects and timing are not certified by this helper.'}


def chart_house_growth_candidates(house,reference_sign,placements,classifications,*,classification_profile):
    from .forecast import sign_index
    from .friendship import CLASSICAL
    if type(house) is not int or not 1<=house<=12:raise ValueError('Target house1..12 required')
    from .chart_evidence_inputs import validate_sign_longitude
    validate_sign_longitude(placements)
    if not isinstance(classifications,dict) or any(p not in CLASSICAL or c not in ('benefic','malefic') for p,c in classifications.items()):raise ValueError('Classical supplied benefic/malefic classes required')
    rows=[]
    for profile in ('whole_sign','sripati_degree_bhava'):
        evidence=[];unknown=[]
        for planet in CLASSICAL:
            pos=placements.get(planet,{})
            if profile=='whole_sign':
                h=None if pos.get('sign') is None else (sign_index(pos['sign'])-sign_index(reference_sign))%12+1
            else:
                h=pos.get('sripati_degree_house');h=h.get('house') if isinstance(h,dict) else h
            x=house_growth_scope(h,classifications.get(planet),classification_profile=classification_profile,house_profile=profile)
            if h is None:unknown.append(planet)
            elif h==house:evidence.append({'planet':planet,'condition_evidence':x})
        rows.append({'house_profile':profile,'occupant_evidence':evidence,'unchecked_occupation':unknown,
            'combined_house_effect':None})
    return {'house':house,'candidates':rows,'personal_outcome':None,'global_precedence':None,
        'notice':'Per-occupant scope only; mixed occupants are not voted or summed. Empty evidence with unchecked occupation is not clearance. Degree geometry never falls back to whole sign.'}
