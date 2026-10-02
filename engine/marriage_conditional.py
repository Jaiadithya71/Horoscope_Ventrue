"""Source-conditioned marriage readings (whole-sign, Lagna reference), never a verdict.

Rules come from page-checked Phaladeepika Adh. VIII, X, XI and Brihat Jataka
Adh. XXIII-XXIV (research files by the marriage stream, scan-checked).
Effects are own-words paraphrase of the translator's English. Spouse-death,
body, character and similar clauses are held out. Every rule reports
'met', 'possibly_met', 'not_met' or 'unresolved' and says why; 'benefic'
is not defined by these sentences, so a rule is 'met' only if it holds with
Jupiter and Venus alone, 'possibly_met' if it needs Mercury or the Moon.
Strength-conditioned rules need a Shadbala verdict from shadbala_working_profile.
"""
from .forecast import SIGNS
from .synthesis import LORDS

PHALA='https://archive.org/details/in.ernet.dli.2015.92117'
DEFINITE_BENEFIC={'Jupiter','Venus'}
CONDITIONAL_BENEFIC={'Mercury','Moon'}
MALEFIC={'Sun','Mars','Saturn'}
PLANETS=('Sun','Moon','Mars','Mercury','Jupiter','Venus','Saturn')
SPECIAL_ASPECTS={'Mars':(4,7,8),'Jupiter':(5,7,9),'Saturn':(3,7,10)}


def src(book,chapter,sloka,pdf,printed):
    return {'book':book,'chapter':chapter,'sloka':sloka,'pdf_pages':pdf,'printed_pages':printed,
            'verified_against_page_image':True,'url':PHALA if book=='phaladeepika-1937' else None,
            'url_note':None if book=='phaladeepika-1937' else 'registry URL unverified'}


def _house(chart,p):
    return chart['placements'][p]['whole_sign_house_from_ascendant']


def _sign_index(chart,p):
    return int(chart['placements'][p]['longitude']//30)


def _aspects(chart,planet,house):
    """Whole-sign aspect of planet on a house number (1..12)."""
    d=(house-_house(chart,planet))%12+1
    return d in SPECIAL_ASPECTS.get(planet,(7,))


def _lord_of_house(chart,n):
    asc=int(chart['ascendant']['longitude']//30)
    return LORDS[(asc+n-1)%12]


def _owned_houses(chart,planet):
    asc=int(chart['ascendant']['longitude']//30)
    return [h for h in range(1,13) if LORDS[(asc+h-1)%12]==planet]


def _tri(definite,possible):
    if definite:return 'met'
    if possible:return 'possibly_met'
    return 'not_met'


def _row(rid,source,condition,effect,status,detail,*,needs=None,adverse=False,unresolved=None):
    return {'rule_id':rid,'source':source,'condition':condition,'effect_paraphrase':effect,
            'status':status,'detail':detail,'needs':needs or [],
            'adverse_marital_status_text':adverse,'ship_default':not adverse,
            'unresolved':unresolved or []}


def _benefics_in(chart,house,pool):
    return [p for p in pool if _house(chart,p)==house]


def _benefic_touch(chart,house):
    """Occupation or whole-sign aspect by benefics on a house: (definite, possible)."""
    def touch(pool):
        return [p for p in pool if p!=None and (_house(chart,p)==house or _aspects(chart,p,house))]
    d=touch(DEFINITE_BENEFIC);a=touch(DEFINITE_BENEFIC|CONDITIONAL_BENEFIC)
    return d,a


def marriage_conditional(chart,*,strength_verdicts=None,native_sex=None):
    """chart: natal_chart() result. strength_verdicts: planet -> shadbala verdict string."""
    if native_sex not in (None,'female','male'):raise ValueError('native_sex must be female, male or None')
    sv=strength_verdicts or {}
    rows=[]
    seventh_lord=_lord_of_house(chart,7)
    # Phaladeepika X.6(ii): strong benefic 7th lord.
    verdict=sv.get(seventh_lord)
    benefic_status='definite' if seventh_lord in DEFINITE_BENEFIC else 'conditional' if seventh_lord in CONDITIONAL_BENEFIC else 'malefic'
    if benefic_status=='malefic':status='not_met';why=f'7th lord {seventh_lord} is not a benefic here'
    elif verdict is None:status='unresolved';why='7th lord strength verdict not supplied'
    elif verdict.startswith('meets'):status='met' if benefic_status=='definite' else 'possibly_met';why=f'{seventh_lord} meets the Sripati minimum in all variants'
    elif verdict.startswith('below'):status='not_met';why=f'{seventh_lord} is below the Sripati minimum in all variants'
    else:status='unresolved';why=f'{seventh_lord} strength is unresolved across school variants'
    rows.append(_row('phaladeepika-x-6-strong-benefic-7th-lord',src('phaladeepika-1937','X','6',[144],[107]),
        '7th lord is a benefic and strong','The text links this with a good-natured partner and good children.',
        status,why,needs=['shadbala verdict'],unresolved=['benefic classification of Mercury/Moon','meaning of strength not defined in the sloka']))
    # X.6(iii): malefic owning and sitting in the 7th.
    occ=[p for p in MALEFIC if _house(chart,p)==7 and 7 in _owned_houses(chart,p)]
    rows.append(_row('phaladeepika-x-6-malefic-owner-in-7th',src('phaladeepika-1937','X','6',[144],[107]),
        'A malefic that owns the 7th house sits in it','The text says such a malefic does good to the partner.',
        'met' if occ else 'not_met',f'owner-occupants: {occ}' if occ else 'no malefic owns and occupies the 7th'))
    # X.6(iv): benefics in 7th good unless lords of 6, 8, 12.
    in7=[p for p in DEFINITE_BENEFIC|CONDITIONAL_BENEFIC if _house(chart,p)==7]
    spoiled=[p for p in in7 if set(_owned_houses(chart,p))&{6,8,12}]
    d=[p for p in in7 if p in DEFINITE_BENEFIC and p not in spoiled];a=[p for p in in7 if p not in spoiled]
    rows.append(_row('phaladeepika-x-6-benefics-in-7th',src('phaladeepika-1937','X','6',[144],[107]),
        'Benefics in the 7th that do not own the 6th, 8th or 12th','The text says they are productive of good for marriage.',
        _tri(d,a),f'benefics in 7th: {in7}; excluded as lords of 6/8/12: {spoiled}'))
    # X.7: 2nd and 7th touched by benefics.
    dd2,pp2=_benefic_touch(chart,2);dd7,pp7=_benefic_touch(chart,7)
    both_d=bool(dd2 and dd7);both_p=bool(pp2 and pp7);either=bool(pp2 or pp7)
    status='met' if both_d else 'possibly_met' if both_p else 'unresolved' if either else 'not_met'
    rows.append(_row('phaladeepika-x-7-second-seventh-benefic',src('phaladeepika-1937','X','7',[145],[108]),
        '2nd and 7th houses occupied or aspected by benefics','The text says the couple will be lucky and enjoy comforts.',
        status,f'2nd touched by {pp2}; 7th touched by {pp7}',
        unresolved=['text does not say whether both houses or either suffice','husband chart uses 7th and 8th, not 2nd and 7th']))
    # X.9: even 7th sign, 7th lord and Venus in even signs, 5th/7th lords strong, not combust.
    even=lambda i:i%2==1
    asc=int(chart['ascendant']['longitude']//30)
    geom=even((asc+6)%12) and even(_sign_index(chart,seventh_lord)) and even(_sign_index(chart,'Venus'))
    lords57=(_lord_of_house(chart,5),seventh_lord)
    strong=[sv.get(p) for p in lords57]
    if not geom:status='not_met';why='sign-parity conditions fail'
    elif any(s is None for s in strong):status='unresolved';why='strength verdicts for 5th and 7th lords not supplied'
    elif any(s.startswith('below') for s in strong):status='not_met';why='a lord is below the Sripati minimum in all variants'
    elif all(s.startswith('meets') for s in strong):status='unresolved';why='parity and strength hold, but the Sun-proximity limit for "overpowered by the Sun" is not defined in the source'
    else:status='unresolved';why='strength of 5th or 7th lord unresolved across variants'
    rows.append(_row('phaladeepika-x-9-even-signs-lords-strong',src('phaladeepika-1937','X','9',[145],[108]),
        '7th sign even, 7th lord and Venus in even signs, 5th and 7th lords strong and not overpowered by the Sun',
        'The text promises a spouse and children.',status,why,needs=['shadbala verdict','combustion orb'],
        unresolved=['orb for the Sun overpowering a planet is not stated']))
    # X.10 (a).
    lords=(_lord_of_house(chart,2),seventh_lord,_lord_of_house(chart,12))
    good=(1,4,5,7,9,10)
    ok_a=all(_house(chart,l) in good and (l=='Jupiter' or _aspects(chart,'Jupiter',_house(chart,l))) for l in lords)
    h7l=_house(chart,seventh_lord)
    ok_b=all(any(_house(chart,bn)==(h7l+k-2)%12+1 for bn in DEFINITE_BENEFIC) for k in (2,7,11))
    rows.append(_row('phaladeepika-x-10-wife-happiness',src('phaladeepika-1937','X','10',[145,146],[108,109]),
        '(a) lords of 2nd, 7th, 12th in kendra/trikona and aspected by Jupiter, or (b) benefics in 2nd, 7th and 11th from the 7th lord',
        'The text says the partner has happiness and children.',
        'met' if ok_a or ok_b else 'not_met',f'(a) holds: {ok_a}; (b) holds: {ok_b}',
        unresolved=['whether (a) and (b) are alternatives rests on the translator\'s "or"','Jupiter as one of the lords counts as aspected by itself (reading choice)']))
    # 5th and 7th from Lagna or Moon (Phaladeepika X.1 / BJ XXIII.1).
    moon_house=_house(chart,'Moon')
    def from_ref(offset,n):return (offset+n-2)%12+1
    refs={'Lagna':1,'Moon':moon_house};detail={}
    d_all=True;p_all=True
    for label,off in refs.items():
        for n in (5,7):
            h=from_ref(off,n);dd,pp=_benefic_touch(chart,h)
            detail[f'{label}:{n}th (house {h})']={'definite':dd,'possible':pp}
            d_all&=bool(dd);p_all&=bool(pp)
    rows.append(_row('phaladeepika-x-1-and-brihat-23-1-fifth-seventh-benefic',
        src('phaladeepika-1937','X','1',[142],[105]),'5th and 7th from Lagna and from Moon occupied or aspected by benefics (or their lords)',
        'The texts say the houses then bear fruit (wife and sons); otherwise not.',
        'met' if d_all else 'possibly_met' if p_all else 'unresolved' if any(v['possible'] for v in detail.values()) else 'not_met',str(json_safe(detail)),
        unresolved=['text does not say whether Lagna and Moon references both apply or either','"or by their lords" and the 9th-lord variant (Phaladeepika only) are not evaluated','Brihat Jataka XXIII.1 PDF 246-247 states the same condition']))
    # Single-planet 7th placements (favourable) plus cautionary ones.
    fav={'Mercury':('phaladeepika-viii-12',[125],[88],'The text links Mercury in the 7th with a wealthy spouse.'),
         'Jupiter':('phaladeepika-viii-15',[127],[90],'The text links Jupiter in the 7th with a good spouse and sons.'),
         'Venus':('phaladeepika-viii-18',[128],[91],'The text links Venus in the 7th with a good spouse.'),
         'Moon':('phaladeepika-viii-6',[122],[85],'The text links the Moon in the 7th with an attractive partner.')}
    for p,(rid,pdf,pr,eff) in fav.items():
        rows.append(_row(rid+'-'+p.lower()+'-in-7th',src('phaladeepika-1937','VIII',rid.split('-')[-1],pdf,pr),
            f'{p} in the 7th house',eff,'met' if _house(chart,p)==7 else 'not_met',f'{p} in house {_house(chart,p)}'))
    rows.append(_row('phaladeepika-viii-19-venus-in-9th',src('phaladeepika-1937','VIII','19',[129],[92]),
        'Venus in the 9th house','The text links Venus in the 9th with a spouse, friends and children.',
        'met' if _house(chart,'Venus')==9 else 'not_met',f'Venus in house {_house(chart,"Venus")}'))
    cautionary={('Sun',7):('phaladeepika-viii-3',[120,121],[83,84],'The text says without a wife, wandering and humiliated (marital part only).'),
                ('Mars',12):('phaladeepika-viii-10',[124],[87],'The text says without a wife (marital part only).'),
                ('Venus',3):('phaladeepika-viii-17',[128],[91],'The text says wifeless (marital part only).')}
    for (p,h),(rid,pdf,pr,eff) in cautionary.items():
        rows.append(_row(rid+f'-{p.lower()}-in-{h}',src('phaladeepika-1937','VIII',rid.split('-')[-1],pdf,pr),
            f'{p} in house {h}',eff,'met' if _house(chart,p)==h else 'not_met',f'{p} in house {_house(chart,p)}',adverse=True))
    # Moon with Saturn in 7th: needs sex.
    ms=_house(chart,'Moon')==7 and _house(chart,'Saturn')==7
    if not ms:status='not_met';why='Moon and Saturn are not both in the 7th'
    elif native_sex is None:status='unresolved';why='native sex needed; the texts differ by chart type'
    else:status='met';why='Moon and Saturn both in the 7th'
    eff={'female':'Phaladeepika: the woman is remarried.','male':'Phaladeepika: the man is wifeless or childless; Brihat Jataka: the wife leaves and marries another.',None:'Outcome differs by chart type and by book.'}[native_sex]
    rows.append(_row('phaladeepika-x-8-and-brihat-23-1-moon-saturn-7th',src('phaladeepika-1937','X','8',[145],[108]),
        'Moon and Saturn together in the 7th',eff,status,why,adverse=True,unresolved=['Brihat Jataka outcome differs from Phaladeepika for a man; both preserved']))
    # Husband's nature from 7th-house sign lord (BJ XXIV.11-12), whole-sign only.
    sign_lord=seventh_lord
    nature={'Mars':'quick temper but attached to the wife','Venus':'good-looking and fond of the wife','Mercury':'learned and intelligent',
            'Jupiter':'courageous with self-control','Sun':'very gentle and engaged in many works'}
    if sign_lord in nature:
        rows.append(_row('brihat-24-11-12-husband-nature-by-7th-sign-lord',src('brihat-jataka-1905','XXIV','11-12',[259],[215]),
            'Woman\'s chart: sign (or Navamsa) of the 7th house belongs to this planet','Brihat Jataka describes the husband as '+nature[sign_lord]+'.',
            'unresolved' if native_sex!='female' else 'possibly_met',f'7th sign lord {sign_lord}',
            unresolved=['sign vs Navamsa disagreement: the note says whichever is powerful','commentator assumes the 7th house is empty','Moon clause omitted']))
    # Marriage-period candidate lords (Phaladeepika X.13).
    cand=sorted({p for p in PLANETS if _house(chart,p)==7 or _aspects(chart,p,7) or 7 in _owned_houses(chart,p)})
    rows.append(_row('phaladeepika-x-13-period-candidate-lords',src('phaladeepika-1937','X','13',[146],[109]),
        'Period of a planet in, aspecting, or owning the 7th house (or Lagna lord transiting the 7th sign)','The text says acquisition of a wife may happen then.',
        'met',f'candidate lords: {cand}',needs=['dasa level and calendar convention'],
        unresolved=['dasa level (Maha or Antar) not stated','no rule when several planets qualify','dasa system and year length handled by the timing module']))
    return {'status':'conditional_source_readings_not_selected_personal_forecast','house_model':'whole_sign_lagna_reference',
        'rows':rows,'native_sex':native_sex,'selected_outcome':None,
        'held_out':['spouse-death and illness clauses','body and character wording','"wicked/evil spouse" wording','wife\'s birth sign and country direction (Ashtakavarga/strength method undefined)'],
        'notice':'Source conditions evaluated on chart geometry. Not a marriage prediction; no number of marriages, timing or spouse description is selected.'}


def json_safe(d):return {k:{kk:list(vv) for kk,vv in v.items()} for k,v in d.items()}
