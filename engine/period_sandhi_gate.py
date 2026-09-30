"""XV.13-14 exact geometric period-effect qualification, not event arbitration."""
from .bhava_effectiveness import bhava_effectiveness,SOURCE


def period_sandhi_gate(placements,main_lord,sub_lord,*,geometry=None,geometry_profile=None):
    from .chart_evidence_inputs import validate_sign_longitude
    validate_sign_longitude(placements)
    if geometry is not None and (not isinstance(geometry_profile,str) or not geometry_profile.strip()):
        raise ValueError('Named supplied degree-Bhava geometry profile required')
    rows=[]
    for lord in dict.fromkeys((main_lord,sub_lord)):
        longitude=placements.get(lord,{}).get('longitude')
        missing=[]
        if longitude is None:missing.append('longitude')
        if geometry is None:missing.append('degree_bhava_geometry')
        effect=None if missing else bhava_effectiveness(longitude,geometry)
        sandhi=None if effect is None else effect['membership']['at_sandhi']
        rows.append({'lord':lord,'missing_inputs':missing,'geometry_evidence':effect,
            'at_exact_sandhi':sandhi,'scoped_sandhi_override_active':sandhi,
            'scope':'Exact Bhava-Sandhi defeats exaltation/friendly-house/sixfold-strength evidence for this XV.13-14 effect, not general adverse event',
            'favorable_dignity_or_strength_can_remove_sandhi_clause':False if sandhi else None,
            'selected_period_outcome':None})
    return {'rows':rows,'geometry_profile':geometry_profile,'source':SOURCE,
        'comparison_source':{'url':'https://jyotishvidya.com/HTMLobj-9415/Mantreswara_s__Phaladeeplka_.pdf','pdf_page':150,'chapter':'XV','sloka':'13-14','verified_against_page_image':True},
        'status':'scoped_condition_evidence_only','global_precedence':None,
        'notice':'1937 translation says ineffective; Kapoor XV.13 says affliction, but both XV.14 say no effect at Sandhi. Retain shared zero-effect scope, not a harm prediction. Exact supplied degree geometry only; no whole-sign substitute, near-boundary orb, supplied total selection, active calendar or event conclusion.'}
