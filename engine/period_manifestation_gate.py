"""XX.43-44 separates owned-house effects from automatic own-subperiod output."""
from .debilitation_cancellation_candidates import _or


def period_manifestation_gate(main_lord,sub_lord,*,related=None,similarly_circumstanced=None,evidence_profile=None):
    from .natal import PERIODS
    if main_lord not in dict(PERIODS) or sub_lord not in dict(PERIODS):raise ValueError('Known period lords required')
    for flag in (related,similarly_circumstanced):
        if flag is not None and type(flag) is not bool:raise ValueError('Grounded bool or unknown required')
    if any(v is not None for v in (related,similarly_circumstanced)) and (not isinstance(evidence_profile,str) or not evidence_profile.strip()):raise ValueError('Named relation/circumstance evidence required')
    same=main_lord==sub_lord
    return {'main_lord':main_lord,'sub_lord':sub_lord,'same_lord_pair':same,
        'automatic_owned_house_effect_from_same_lord_pair':False,
        'supplied_related':related,'supplied_similarly_circumstanced':similarly_circumstanced,
        'xx44_supplied_activation_condition':None if same else _or(related,similarly_circumstanced),
        'evidence_profile':evidence_profile,'selected_personal_effect':None,
        'sources':[{'url':'https://archive.org/details/in.ernet.dli.2015.92117','pdf_page':252,'printed_page':215,'chapter':'XX','sloka':'43-44','verified_against_page_image':True},
            {'url':'https://jyotishvidya.com/HTMLobj-9415/Mantreswara_s__Phaladeeplka_.pdf','pdf_pages':[190,191],'chapter':'XX','sloka':'43-44','verified_against_page_image':True}],
        'relation_definition_reference':{'url':'https://archive.org/details/in.ernet.dli.2015.92117','pdf_page':200,'printed_page':163,'chapter':'XV','sloka':30,'verified_against_page_image':True},
        'global_precedence':None,
        'notice':'Own subperiod does not automatically establish all owned-house effects;1937 all-do-not versus Kapoor no-planet wording is not expanded into universal no-effects. XX.44 calls for related or similarly circumstanced planets; self-relation and the latter classification are not inferred. Kapoor XX.44 says Chapter25 verse30 while its own nearby notes and original point toXV.30, retained as cross-reference typo not new authority. No active dates, polarity or global priority follows.'}
