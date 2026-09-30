"""XX.49 period-pair wording candidates, not a personal effect classification."""
from .synthesis import lordship
from .friendship import CLASSICAL
from .debilitation_cancellation_candidates import _and,_or


def angular_trinal_period_readings(reference_sign,main_lord,sub_lord,*,related=None,evidence_profile=None):
    if any(p not in (*CLASSICAL,'Rahu','Ketu') for p in (main_lord,sub_lord)):raise ValueError('Known planet pair required')
    if related is not None and type(related) is not bool:raise ValueError('Supplied bool or unknown required')
    if related is not None and (not isinstance(evidence_profile,str) or not evidence_profile.strip()):raise ValueError('Named supplied relation profile required')
    houses=lordship(reference_sign)['houses']
    def role(p,roles):return None if p not in CLASSICAL else any(h['lord']==p and h['house'] in roles for h in houses)
    rows=[]
    for name,trines in [('fifth_ninth_scope_candidate',(5,9)),('lagna_fifth_ninth_scope_candidate',(1,5,9))]:
        a=_and(role(main_lord,trines),role(sub_lord,(1,4,7,10)))
        b=_and(role(main_lord,(1,4,7,10)),role(sub_lord,trines))
        match=None if main_lord==sub_lord else _or(a,b)
        unrelated=_and(match,None if related is None else not related)
        rows.append({'trikona_scope_profile':name,'trikona_houses':list(trines),
            'trikona_main_kendra_sub_condition':a,'kendra_main_trikona_sub_condition':b,
            'distinct_pair_ownership_condition':match,'unrelated_pair_condition':unrelated,
            'unrelated_clause_readings':[
                {'translation':'Sastri1937','clause':'will not cause harm','condition':unrelated},
                {'translation':'Kapoor','clause':'productive of good effects','condition':unrelated}],
            'selected_effect':None})
    return {'main_lord':main_lord,'sub_lord':sub_lord,'evidence_profile':evidence_profile,'candidates':rows,
        'sources':[{'url':'https://archive.org/details/in.ernet.dli.2015.92117','pdf_page':253,'printed_page':216,'chapter':'XX','sloka':49,'verified_against_page_image':True},
            {'url':'https://jyotishvidya.com/HTMLobj-9415/Mantreswara_s__Phaladeeplka_.pdf','pdf_page':192,'chapter':'XX','sloka':49,'verified_against_page_image':True}],
        'selected_trikona_scope':None,'selected_translation':None,'personal_outcome':None,'global_precedence':None,
        'notice':'The base clause describes good effects for alternating Kendra/Trikona lord periods; the explicit unrelated clause differs between these English translations. No-harm is not automatically favorable. XX.49 does not enumerate Trikona houses, so fifth/ninth and Lagna-inclusive ownership candidates remain separate, not a source-selected profile. No self-pair extension, global cancellation, selected relation, active period date or forecast.'}
