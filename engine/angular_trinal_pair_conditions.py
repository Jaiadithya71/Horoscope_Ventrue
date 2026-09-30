"""XX.45-46 pair conditions, not automatic prosperity or global overrides."""
from .synthesis import lordship
from .friendship import CLASSICAL
from .debilitation_cancellation_candidates import _and


def angular_trinal_pair_conditions(reference_sign,first,second,*,related=None,kendra_lord_strong=None,evidence_profile=None):
    if first not in (*CLASSICAL,'Rahu','Ketu') or second not in (*CLASSICAL,'Rahu','Ketu'):raise ValueError('Known planet pair required')
    for flag in (related,kendra_lord_strong):
        if flag is not None and type(flag) is not bool:raise ValueError('Supplied bool or unknown required')
    if any(f is not None for f in (related,kendra_lord_strong)) and (not isinstance(evidence_profile,str) or not evidence_profile.strip()):raise ValueError('Named supplied evidence profile required')
    houses=lordship(reference_sign)['houses']
    def owned(p):return None if p not in CLASSICAL else [h['house'] for h in houses if h['lord']==p]
    rows=[]
    for k,t in ((first,second),(second,first)):
        kh=owned(k);th=owned(t)
        krole=None if kh is None else any(h in (1,4,7,10) for h in kh)
        trole=None if th is None else any(h in (5,9) for h in th)
        roles=_and(krole,trole)
        relation=_and(roles,related)
        rows.append({'kendra_lord_candidate':k,'trikona_lord_candidate':t,
            'kendra_candidate_owned_houses':kh,'trikona_candidate_owned_houses':th,
            'ownership_pair_condition':roles,'xx45_related_pair_condition':None if first==second else relation,
            'xx46_related_strong_kendra_condition':None if first==second else _and(relation,kendra_lord_strong),
            'extra_dusthana_ownership':None if kh is None or th is None else sorted({h for h in kh+th if h in (6,8,12)}),
            'selected_personal_effect':None})
    return {'first':first,'second':second,'evidence_profile':evidence_profile,
        'trikona_scope':'Explicit fifth/ninth pair candidate, not universal removal of Lagna from trines',
        'ownership_profile':'ascendant whole-sign lordship','candidates':rows,
        'sources':[{'url':'https://archive.org/details/in.ernet.dli.2015.92117','pdf_page':252,'printed_page':215,'chapter':'XX','sloka':'45-46','verified_against_page_image':True},
            {'url':'https://jyotishvidya.com/HTMLobj-9415/Mantreswara_s__Phaladeeplka_.pdf','pdf_page':191,'chapter':'XX','sloka':'45-46','verified_against_page_image':True}],
        'global_precedence':None,'personal_outcome':None,
        'notice':'XX.45 relates Kendra/Trikona lords despite extra adverse ownership; XX.46 separately requires a strong Kendra lord with fifth/ninth lord. External relation/strength unknowns stay unresolved. Opposite pair orientations are candidates, not assigned strength. One planet is not related to itself. No third-planet enhancement, automatic yogakaraka status, period date or global cancellation is inferred.'}
