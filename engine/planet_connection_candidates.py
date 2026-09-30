"""XV.30 five connection candidates, preserving sign/degree interpretations."""
from .debilitation_cancellation_candidates import _and,_or
from .synthesis import LORDS,aspects
from .forecast import sign_index
from .friendship import CLASSICAL
from .chart_evidence_inputs import validate_sign_longitude


def planet_connection_candidates(placements,first,second):
    validate_sign_longitude(placements)
    a=placements.get(first,{});b=placements.get(second,{})
    sa=a.get('sign');sb=b.get('sign');la=a.get('longitude');lb=b.get('longitude')
    same=first==second;bothsign=sa is not None and sb is not None
    ia=None if sa is None else sign_index(sa);ib=None if sb is None else sign_index(sb)
    exchange=None if not bothsign or first not in CLASSICAL or second not in CLASSICAL else LORDS[ia]==second and LORDS[ib]==first and ia!=ib
    mutual=None
    if bothsign and first in CLASSICAL and second in CLASSICAL:
        ab=any(sign_index(t['target_sign'])==ib for t in aspects(first,sa,sa)['targets'])
        ba=any(sign_index(t['target_sign'])==ia for t in aspects(second,sb,sb)['targets'])
        mutual=_and(ab,ba)
    delta=None if la is None or lb is None else (lb-la)%360
    sign_house=None if not bothsign else (ib-ia)%12+1
    profiles=[('whole_sign_categories_full_classical_aspects',{
        'exchange':exchange,'conjunction':None if not bothsign else ia==ib,
        'mutual_aspect':mutual,'kendra':None if sign_house is None else sign_house in (1,4,7,10),
        'trikona':None if sign_house is None else sign_house in (1,5,9)}),
        ('literal_exact_degree_90_120_with_aspect_unresolved',{
        'exchange':exchange,'conjunction':None if delta is None else delta==0,
        'mutual_aspect':None,'kendra':None if delta is None else delta in (90,270),
        'trikona':None if delta is None else delta in (120,240)})]
    rows=[]
    for name,flags in profiles:
        related=False
        for value in flags.values():related=_or(related,value)
        rows.append({'profile':name,'condition_flags':flags,'related_candidate':None if same else related,
            'self_pair_not_evaluated_as_two_planet_connection':same})
    return {'first':first,'second':second,'sign_house_second_from_first':sign_house,
        'directed_degree_difference':delta,'candidates':rows,'selected_related':None,
        'source':{'url':'https://archive.org/details/in.ernet.dli.2015.92117','pdf_page':200,'printed_page':163,'chapter':'XV','sloka':30,'verified_against_page_image':True},
        'comparison_source':{'url':'https://jyotishvidya.com/HTMLobj-9415/Mantreswara_s__Phaladeeplka_.pdf','pdf_page':154,'chapter':'XV','sloka':30,'verified_against_page_image':True},
        'notice':'Sign categories and literal exact90/120-degree wording retained separately. Same sign is only a conjunction hypothesis; literal zero separation has no inferred orb. Whole-sign mutual full classical aspects are a hypothesis under II.23/IV.9, not universal efficacy. Exact-degree mutual-aspect qualifier and node ownership/aspects remain unknown; no positive-degree-amount cutoff inferred. A self-pair does not establish a two-planet relation. No school selection, similarly-circumstanced class or personal outcome.'}
