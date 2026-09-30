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


def chart_period_disposition_candidates(reference_sign,placements,main_lord,sub_lord):
    from .chart_evidence_inputs import validate_sign_longitude
    from .forecast import sign_index
    from .natal_factors import dignity
    from .friendship import CLASSICAL
    validate_sign_longitude(placements)
    asc=sign_index(reference_sign);rows=[]
    for lord in dict.fromkeys((main_lord,sub_lord)):
        p=placements.get(lord,{})
        sign=p.get('sign');longitude=p.get('longitude')
        d=None if sign is None or lord not in CLASSICAL else dignity(lord,sign,longitude)
        flags={} if d is None else d['flags']
        for frame in ('whole_sign','sripati_degree_bhava'):
            if frame=='whole_sign':h=None if sign is None else (sign_index(sign)-asc)%12+1
            else:
                h=p.get('sripati_degree_house');h=h.get('house') if isinstance(h,dict) else h
            if h is not None and (type(h) is not int or not 1<=h<=12):raise ValueError('House1..12 or unknown required')
            # Node chapter applicability is not established by this checked slice.
            classical=lord in CLASSICAL
            condition=period_disposition_gate(
                retrograde=p.get('retrograde') if classical else None,
                own_sign=flags.get('own_sign'),exaltation_sign=flags.get('exaltation_sign'),
                fall_sign=flags.get('fall_sign'),good_house=None if h is None or not classical else h not in (6,8,12),
                overpowered_rays=p.get('overpowered_sun_rays') if classical else None,
                input_profile='XX.14 supplied chart '+frame+' occupation and checked dignity candidate; relation flags unresolved')
            rows.append({'lord':lord,'occupation_profile':frame,'supplied_house':h,
                'classical_scope_applicability':classical,'condition_evidence':condition,
                'unresolved_flags':['friendly_sign','inimical_sign']})
    return {'rows':rows,'selected_profile':None,'personal_outcome':None,
        'notice':'Main/sub lord conditions only. Source-specific friendship class unselected; missing rays are unknown. Raw fall/own/exaltation are not cancelled or replaced by a total. Nodes retain unknown conditions. Whole-sign/degree occupation candidates are not a selected historical frame, active period or global arbitration.'}
