"""Scoped Phaladeepika XV.10-11 ownership emphasis, not outcome arbitration."""
from .synthesis import lordship
from .natal_factors import MOOLATRIKONA

SOURCE={'slug':'phaladeepika-1937','chapter':'XV','sloka':'10-11','pdf_pages':[193,194],
        'printed_pages':[156,157],'verified_against_page_image':True,
        'url':'https://archive.org/details/in.ernet.dli.2015.92117'}


def lordship_precedence(ascendant_sign):
    houses=lordship(ascendant_sign)['houses'];lagna_lord=houses[0]['lord'];rows=[]
    for p in MOOLATRIKONA:
        owned=[h for h in houses if h['lord']==p]
        if len(owned)!=2:continue
        moola=next(h for h in owned if h['sign']==MOOLATRIKONA[p][0])
        other=next(h for h in owned if h!=moola)
        # A dusthana may be the Moolatrikona house rather than the other house.
        dusthana=[h['house'] for h in owned if h['house'] in (6,8,12)]
        exception=p==lagna_lord and bool(dusthana)
        rows.append({'planet':p,'owned_houses':owned,
            'moolatrikona_sign_house':moola['house'],'other_owned_house':other['house'],
            'general_rule':{'primary_house':moola['house'],'other_house_relative_effect':.5,'sloka':11},
            'lagna_dusthana_exception':{'primary_house':1,'secondary_dusthana_house':dusthana[0],
                                      'sloka':10,'scope':'Lagna ownership predominates, not the other dusthana ownership'} if exception else None,
            'scope_overlap':exception,'selected_effect_weights':None,
            'notice':'Ownership emphasis only, not dignity at actual longitude, house favorability, timing, occurrence probability, or full outcome score. XV.10 exception and XV.11 general rule both retained when they overlap.'})
    return {'ascendant_sign':houses[0]['sign'],'dual_owner_evidence':rows,'source':SOURCE,
            'global_outcome_precedence':None,
            'dasha_order_disagreement':{'sources':[SOURCE,{'slug':'phaladeepika-kapoor','chapter':'XV','sloka':11,'pdf_page':150,'verified_against_page_image':True,'url':'https://jyotishvidya.com/HTMLobj-9415/Mantreswara_s__Phaladeeplka_.pdf'}],
                'notice':'1937 says odd/even house, Kapoor says sign;1937 even reading says first half while Kapoor says second. First-in-order alternative also recorded by both. No half-dasha scheduler inferred.'}}
