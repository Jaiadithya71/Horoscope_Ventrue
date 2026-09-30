"""XV.29 own non-dusthana occupation exception, not general outcome selection."""
from .synthesis import lordship
from .forecast import sign_index

SOURCE={'url':'https://archive.org/details/in.ernet.dli.2015.92117','slug':'phaladeepika-1937','chapter':'XV','sloka':29,'pdf_pages':[199,200],'printed_pages':[162,163],'verified_against_page_image':True}
COMPARISON={'url':'https://jyotishvidya.com/HTMLobj-9415/Mantreswara_s__Phaladeeplka_.pdf','pdf_page':153,'chapter':'XV','sloka':29,'verified_against_page_image':True}


def dual_owner_occupation_exception(reference_sign,placements):
    from .chart_evidence_inputs import validate_sign_longitude
    validate_sign_longitude(placements)
    houses=lordship(reference_sign)['houses'];rows=[]
    for planet in ('Mars','Mercury','Jupiter','Venus','Saturn'):
        owned=[h for h in houses if h['lord']==planet]
        dust=[h for h in owned if h['house'] in (6,8,12)]
        other=[h for h in owned if h['house'] not in (6,8,12)]
        # Both owned houses being dusthana is not the other-house exception.
        eligible=len(dust)==1 and len(other)==1
        pos=placements.get(planet,{})
        s=pos.get('sign');active=None if s is None and eligible else False
        occupied=None if s is None else (sign_index(s)-sign_index(reference_sign))%12+1
        if eligible and s is not None:active=sign_index(s)==sign_index(other[0]['sign'])
        rows.append({'planet':planet,'owned_houses':owned,'occupation_house_whole_sign':occupied,
            'dual_ownership_condition':eligible,'own_other_house_occupation':active,
            'scoped_exception_active':active,
            'occupied_own_house_emphasized':other[0]['house'] if active else None,
            'dusthana_ownership_effect_excluded_in_this_clause':dust[0]['house'] if active else None,
            'source':SOURCE,'comparison_source':COMPARISON,
            'selected_personal_effect':None,
            'notice':'Scoped sign-ownership/occupation condition only. Not general cancellation of adverse occupation, aspects, weakness, other verses or other schools. No degree-Bhava substitution or dasha date is inferred.'})
    return {'reference_sign':reference_sign,'occupation_profile':'ascendant_whole_sign_candidate',
        'rows':rows,'global_precedence':None,'personal_outcome':None,
        'notice':'XV.29 other-owned-house exception retained separately from XV.10 Lagna exception and XV.11 Moolatrikona general emphasis. The latter can point at the dusthana, so no global weights are selected. Kapoor calls the other house auspicious; no independent numeric auspiciousness rule is invented.'}
