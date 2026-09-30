"""XX.14 favorable/adverse condition evidence; no automatic period outcome."""
from .debilitation_cancellation_candidates import _or


def period_disposition_gate(*,retrograde=None,own_sign=None,exaltation_sign=None,friendly_sign=None,good_house=None,inimical_sign=None,fall_sign=None,overpowered_rays=None,input_profile):
    flags=locals().copy();flags.pop('input_profile')
    if not isinstance(input_profile,str) or not input_profile.strip():raise ValueError('Named grounded input profile required')
    if any(v is not None and type(v) is not bool for v in flags.values()):raise ValueError('Condition bool or unknown required')
    def OR(keys):
        value=False
        for k in keys:value=_or(value,flags[k])
        return value
    favorable=OR(('retrograde','own_sign','exaltation_sign','friendly_sign','good_house'))
    dusthana=None if good_house is None else not good_house
    adverse=_or(OR(('inimical_sign','fall_sign','overpowered_rays')),dusthana)
    return {'supplied_flags':flags,'input_profile':input_profile,
        '1937_favorable_disjunction':favorable,'shared_adverse_disjunction':adverse,
        'opposed_conditions_active':True if favorable is True and adverse is True else None if favorable is None or adverse is None else False,
        'later_friendly_sign_omission':True,'later_favorable_connective_selected':None,
        'sources':[{'url':'https://archive.org/details/in.ernet.dli.2015.92117','pdf_page':241,'printed_page':204,'chapter':'XX','sloka':14,'verified_against_page_image':True},
            {'url':'https://jyotishvidya.com/HTMLobj-9415/Mantreswara_s__Phaladeeplka_.pdf','pdf_pages':[183,184],'chapter':'XX','sloka':14,'verified_against_page_image':True}],
        'selected_polarity':None,'personal_outcome':None,'global_precedence':None,
        'notice':'Original translation lists retrograde/own/exaltation/friendly/good-house alternatives before favorable lord-period descriptions and inimical/fall/rays/dusthana before adverse descriptions. Kapoor omits friendly in favorable list and its favorable connective wording is not selected here. Simultaneous favorable/adverse evidence remains a conflict, not resolved by one boolean. This gates condition evidence only, not chapter outcomes, strength completeness or active calendar.'}
