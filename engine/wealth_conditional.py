"""Source-conditioned wealth-level readings (whole sign), never an income verdict.

Rules are from the scan-checked wealth research file: Phaladeepika VI (yogas)
and VIII (planets in the 2nd and 11th). Effects are own-words paraphrase of
the translator's English, wealth content only. Each rule returns met /
possibly_met / not_met / unresolved with reasons. 'Benefic' is undefined in
these sentences: Jupiter and Venus are definite, Mercury and the Moon only
possible. Held out: Kemadruma (cancellation wording not transcribed),
Srikantha/Srinatha/Virinchi/Parvata (conditions not transcribed), bad-yoga
(Nisswa/Daridra) wording, node placements, and any income amount.
"""
from .forecast import SIGNS
from .synthesis import LORDS
from .marriage_conditional import (DEFINITE_BENEFIC, CONDITIONAL_BENEFIC, _house, _lord_of_house,
                                   _tri, _sign_index, PLANETS)

PHALA='https://archive.org/details/in.ernet.dli.2015.92117'
PLAIN=('Sun','Moon','Mars','Mercury','Jupiter','Venus','Saturn')


def src(chapter,sloka,pdf,printed):
    return {'book':'phaladeepika-1937','chapter':chapter,'sloka':sloka,'pdf_pages':pdf,'printed_pages':printed,
            'verified_against_page_image':True,'url':PHALA}


def _from(ref_house,n):return (ref_house+n-2)%12+1


def _row(rid,source,condition,effect,status,detail,*,unresolved=None,adverse=False,needs=None):
    return {'rule_id':rid,'source':source,'condition':condition,'effect_paraphrase':effect,'status':status,
            'detail':detail,'unresolved':unresolved or [],'needs':needs or [],
            'adverse_text':adverse,'ship_default':not adverse}


def _occupants(chart,house,pool):
    return [p for p in pool if _house(chart,p)==house]


# Phaladeepika VIII, wealth clause only. (house, planet): (effect, pdf pages)
PLACEMENT={
 ('Sun',2):('is without riches (marital/learning clause not used)',[120,121]),
 ('Sun',11):('is very wealthy',[120,121]),
 ('Moon',2):('is rich',[122,123]),('Moon',11):('has riches',[122,123]),
 ('Mars',2):('is without wealth',[123,124]),('Mars',11):('has riches and happiness',[123,124]),
 ('Mercury',2):('earns wealth by his or her own talents',[125,126]),('Mercury',11):('is very rich',[125,126]),
 ('Jupiter',2):('is wealthy',[126,127]),('Jupiter',11):('is wealthy',[126,127]),
 ('Venus',2):('has riches of various kinds',[128,129]),('Venus',11):('is rich',[128,129]),
 ('Saturn',2):('is without wealth, and gains wealth later abroad',[129,131]),
 ('Saturn',11):('has lasting wealth and good income',[131,132]),
}


def wealth_conditional(chart,*,strength_verdicts=None):
    sv=strength_verdicts or {}
    rows=[]
    moon=_house(chart,'Moon')
    # B1/B2: Sunapha, Anapha, Durudhara (planet other than Sun in 2nd/12th from Moon).
    s2=_occupants(chart,_from(moon,2),[p for p in PLAIN if p not in ('Sun','Moon')])
    s12=_occupants(chart,_from(moon,12),[p for p in PLAIN if p not in ('Sun','Moon')])
    rows.append(_row('phaladeepika-vi-5-7-sunapha',src('VI','5-7',[85,86],[48,49]),'A planet other than the Sun in the 2nd from the Moon',
        'The text links this with self-earned wealth.','met' if s2 else 'not_met',f'planets: {s2}'))
    rows.append(_row('phaladeepika-vi-5-7-anapha',src('VI','5-7',[85,86],[48,49]),'A planet other than the Sun in the 12th from the Moon',
        'The text links this with comforts.','met' if s12 else 'not_met',f'planets: {s12}'))
    rows.append(_row('phaladeepika-vi-5-7-durudhara',src('VI','5-7',[85,86],[48,49]),'Planets other than the Sun in both the 2nd and 12th from the Moon',
        'The text links this with an abundance of wealth and vehicles.','met' if s2 and s12 else 'not_met',f'2nd: {s2}; 12th: {s12}'))
    # B4: Subhakartari (benefics in 12th and 2nd from Lagna).
    b12=_occupants(chart,12,DEFINITE_BENEFIC|CONDITIONAL_BENEFIC);b2=_occupants(chart,2,DEFINITE_BENEFIC|CONDITIONAL_BENEFIC)
    d12=[p for p in b12 if p in DEFINITE_BENEFIC];d2=[p for p in b2 if p in DEFINITE_BENEFIC]
    rows.append(_row('phaladeepika-vi-8-13-subhakartari',src('VI','8-13',[87,88],[50,51]),'Benefics in both the 12th and 2nd from Lagna',
        'The text calls the person rich.',_tri(d12 and d2,b12 and b2),f'12th: {b12}; 2nd: {b2}'))
    # B5: Vasumat, Amala.
    up=lambda ref:[(ref,n,_occupants(chart,_from(ref,n),DEFINITE_BENEFIC|CONDITIONAL_BENEFIC)) for n in (3,6,10,11)]
    detail={};dall=False;pall=False
    for label,ref in (('Lagna',1),('Moon',moon)):
        occ=up(ref);detail[label]={n:o for _,n,o in occ}
        dall|=any(p in DEFINITE_BENEFIC for _,_,o in occ for p in o);pall|=any(o for _,_,o in occ)
    rows.append(_row('phaladeepika-vi-19-vasumat',src('VI','19-20',[91],[54]),'Benefics in the 3rd, 6th, 10th or 11th from Lagna or from the Moon',
        'The text links this with plenty of money.',_tri(dall,pall),str(detail),
        unresolved=['text wording on whether one or several benefics are needed is not transcribed in the research file']))
    ten=_occupants(chart,10,DEFINITE_BENEFIC|CONDITIONAL_BENEFIC)
    rows.append(_row('phaladeepika-vi-19-amala',src('VI','19-20',[91],[54]),'A benefic in the 10th from Lagna',
        'The text calls the person wealthy.',_tri([p for p in ten if p in DEFINITE_BENEFIC],ten),f'10th: {ten}',
        unresolved=['Amala is stated for the 10th from Lagna; whether the Moon reference also applies is not stated here']))
    # B12: Adhiyoga.
    ad={}
    for label,ref in (('Lagna',1),('Moon',moon)):
        ad[label]={n:_occupants(chart,_from(ref,n),DEFINITE_BENEFIC|CONDITIONAL_BENEFIC) for n in (6,7,8)}
    full=any(all(v for v in x.values()) for x in ad.values())
    some=any(any(v for v in x.values()) for x in ad.values())
    rows.append(_row('phaladeepika-vi-42-43-adhiyoga',src('VI','42-43',[100,101],[63,64]),'Benefics in the 6th, 7th and 8th from Lagna or the Moon',
        'The text links this with wealth.','met' if full and all(any(p in DEFINITE_BENEFIC for p in v) for x in ad.values() if all(x.values()) for v in x.values()) else 'possibly_met' if full else 'unresolved' if some else 'not_met',str(ad),
        unresolved=['whether benefics must occupy all three houses or any of them is not settled in the research file']))
    # B9: Parivartana of 2nd lord (and 10th-11th Maha).
    def exchange(a,b):
        if a==b:return False
        return LORDS[_sign_index(chart,a)]==b and LORDS[_sign_index(chart,b)]==a
    l2=_lord_of_house(chart,2);l1=_lord_of_house(chart,1);l10=_lord_of_house(chart,10);l11=_lord_of_house(chart,11)
    ex2=[n for n in (4,5,7,9,10,11) if exchange(l2,_lord_of_house(chart,n))]
    ex1=[n for n in (2,4,5,7,9,10,11) if exchange(l1,_lord_of_house(chart,n))]
    rows.append(_row('phaladeepika-vi-32-34-parivartana-wealth',src('VI','32-34',[96,98],[59,61]),
        'Sign exchange between the 2nd lord and the lord of the 4th, 5th, 7th, 9th, 10th or 11th; or Lagna lord with the lord of the 2nd, 4th, 5th, 7th, 9th, 10th or 11th',
        'The text links such exchanges with wealth.','met' if ex2 or ex1 else 'not_met',f'2nd-lord exchanges with houses {ex2}; Lagna-lord with houses {ex1}'))
    rows.append(_row('phaladeepika-vi-32-34-maha-yoga',src('VI','32-34',[96,98],[59,61]),'Sign exchange between the 10th lord and the 11th lord',
        'The text calls this a Maha yoga and links it with wealth.','met' if exchange(l10,l11) else 'not_met',f'10th lord {l10}, 11th lord {l11}'))
    # C: planets in 2nd and 11th.
    for (p,h),(eff,pdf) in PLACEMENT.items():
        here=_house(chart,p)==h
        verdict=sv.get(p)
        rows.append(_row(f'phaladeepika-viii-{p.lower()}-in-{h}',src('VIII',str(h),pdf,[x-37 for x in pdf]),f'{p} in the {h}th house from Lagna',
            f'The text says the person {eff}.','met' if here else 'not_met',f'{p} in house {_house(chart,p)}',
            unresolved=['effect is scaled by the planet\'s position within the bhava (VIII.34-35) and by house strength (XV); not computed here'] if here else None,
            adverse=eff.startswith('is without') and here,
            needs=['shadbala verdict'] if here else []))
        rows[-1]['planet_strength_verdict']=verdict
    return {'status':'conditional_source_readings_not_selected_personal_forecast','house_model':'whole_sign_lagna_and_moon_references',
        'rows':rows,'income_level':None,'selected_outcome':None,
        'held_out':['Kemadruma and its cancellation','Srikantha, Srinatha, Virinchi, Parvata yogas (conditions not transcribed)',
                    'Nisswa and Daridra bad-yoga wording','Rahu and Ketu placements','any income amount or ranking'],
        'notice':'Wealth conditions evaluated on chart geometry. Not an income prediction. Phaladeepika V.9 (Navamsa-owner wealth ease) stays in life_aspect_candidates.'}
