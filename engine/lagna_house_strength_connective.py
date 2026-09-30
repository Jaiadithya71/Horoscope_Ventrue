"""XV.27 translation connectives with supplied statuses, no strength inference."""
from .debilitation_cancellation_candidates import _and,_or


def lagna_house_strength_connective(lagna_link=None,*,bhava_status=None,lord_status=None,strength_profile=None):
    if lagna_link is not None and type(lagna_link) is not bool:raise ValueError('Grounded link bool or None required')
    for s in (bhava_status,lord_status):
        if s not in (None,'strong','weak'):raise ValueError('Explicit strong/weak/unknown status required')
    if any(s is not None for s in (bhava_status,lord_status)) and (not isinstance(strength_profile,str) or not strength_profile.strip()):raise ValueError('Named supplied strength profile required')
    b=None if bhava_status is None else bhava_status=='strong'
    l=None if lord_status is None else lord_status=='strong'
    earlier=_and(lagna_link,_or(b,l));later=_and(lagna_link,_and(b,l))
    return {'supplied_lagna_link':lagna_link,'supplied_bhava_status':bhava_status,
        'supplied_lord_status':lord_status,'strength_profile':strength_profile,
        'favorable_condition_candidates':[
            {'reading':'1937 Bhava OR lord strong','condition':earlier,
             'source':{'url':'https://archive.org/details/in.ernet.dli.2015.92117','pdf_page':199,'printed_page':162,'chapter':'XV','sloka':27,'verified_against_page_image':True}},
            {'reading':'Kapoor Bhava AND lord strong','condition':later,
             'source':{'url':'https://jyotishvidya.com/HTMLobj-9415/Mantreswara_s__Phaladeeplka_.pdf','pdf_page':153,'chapter':'XV','sloka':27,'verified_against_page_image':True}}],
        'favorable_connective_disagreement':None if earlier is None or later is None else earlier!=later,
        'adverse_condition':None,'selected_profile':None,'personal_outcome':None,
        'notice':'Translation connective candidates, not established Sanskrit schools. Link means Lagna lord occupies target house or conjoins its lord; caller must ground geometry. Explicit weak is not inferred from a failed strong flag, and mixed strength is not automatically adverse. Adverse weakness quantifier remains unselected. No complete total, timing or global winner is inferred.'}


def chart_lagna_strength_candidates(house,reference_sign,placements,*,bhava_strong=None,lord_strong=None,lord_status=None,strength_profile=None):
    """Labeled sign-conjunction hypothesis, not an automatic degree orb."""
    from .synthesis import LORDS
    from .forecast import sign_index
    if type(house) is not int or not 1<=house<=12:raise ValueError('Target house1..12 required')
    from .chart_evidence_inputs import validate_sign_longitude
    validate_sign_longitude(placements)
    for f in (bhava_strong,lord_strong):
        if f is not None and type(f) is not bool:raise ValueError('Supplied strength flags bool or unknown required')
    if lord_strong is True and lord_status=='weak':raise ValueError('Conflicting supplied lord strength declarations')
    if lord_strong is False and lord_status=='strong':raise ValueError('Conflicting supplied lord strength declarations')
    asc=sign_index(reference_sign);lagna_lord=LORDS[asc];target_lord=LORDS[(asc+house-1)%12]
    lagna=placements.get(lagna_lord,{});target=placements.get(target_lord,{})
    ls=lagna.get('sign');ts=target.get('sign')
    # The lord is not conjoined with a second planet when both roles name it.
    same=None if ls is None or ts is None else False if lagna_lord==target_lord else sign_index(ls)==sign_index(ts)
    bs='strong' if bhava_strong is True else None
    status=lord_status if lord_status is not None else 'strong' if lord_strong is True else None
    rows=[]
    for profile in ('whole_sign','sripati_degree_bhava'):
        if profile=='whole_sign':h=None if ls is None else (sign_index(ls)-asc)%12+1
        else:
            h=lagna.get('sripati_degree_house');h=h.get('house') if isinstance(h,dict) else h
        if h is not None and (type(h) is not int or not 1<=h<=12):raise ValueError('Degree house1..12 or unknown required')
        occupation=None if h is None else h==house
        link=_or(occupation,same)
        rows.append({'occupation_profile':profile,'lagna_lord_house':h,
            'occupation_matches_target':occupation,'same_sign_association_candidate':same,
            'association_profile':'two distinct lords in same sign, not a selected degree conjunction orb',
            'condition_evidence':lagna_house_strength_connective(link,bhava_status=bs,lord_status=status,strength_profile=strength_profile)})
    return {'house':house,'lagna_lord':lagna_lord,'target_lord':target_lord,'candidates':rows,
        'selected_profile':None,'personal_outcome':None,
        'notice':'Same-sign conjunction is a named hypothesis independent of occupation frame. A missing degree house stays unknown rather than whole-sign substitution. False strong flags are unknown, not weak; explicit supplied weak status is separate. No total, global arbitration or personal forecast.'}
