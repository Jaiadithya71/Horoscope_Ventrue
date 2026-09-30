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
