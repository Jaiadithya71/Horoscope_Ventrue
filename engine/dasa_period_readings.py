"""Period-by-period readings from Phaladeepika Adhyayas XIX and XX (page-checked).

Own-words paraphrase of the translator's English, scan checked at PDF 229-237
(Adh. XIX slokas 5-26, planet Dasa results) and PDF 238-248 (Adh. XX slokas 1-30,
Dasa of each house lord, strong versus weak). Held out: death and demise clauses
(XX.31-32, XX.18, XX.8th-lord wording), character and 'wicked' wording, the
birth-star sub-period rule XX.23, the dangerous-ordinal rule XX.24 and Kendra
or combustion strength details the pages do not define.

What this module does and does not do:
* It classifies each Mahadasa lord as strong, weak or mixed with XX.14 and XX.15-20:
  strong = retrograde, in own, exaltation or a friend's sign, or in a house other
  than the 6th, 8th, 12th; weak = in depression, an enemy's sign or the 6th, 8th, 12th.
  Both kinds present -> mixed. The classification is computed under whole-sign and
  Sripati degree houses; if they differ the period is mixed.
* The result is a broad theme per period, never an event or a date of an event.
* Antardasa (bhukti) tone uses XX.28-29 only: the position of the Bhukti lord from
  the Dasa lord (6th/8th/12th = unhappy, else good) and natural enmity.
* Dates are the union of the four timing conventions, rounded to years.
"""
from datetime import datetime, timedelta
from .forecast import SIGNS
from .synthesis import LORDS
from .friendship import natural_relation

PHALA = 'https://archive.org/details/in.ernet.dli.2015.92117'
SRC19 = {'book': 'phaladeepika-1937', 'chapter': 'XIX', 'sloka': '5-26', 'pdf_pages': list(range(229, 238)), 'verified_against_page_image': True, 'url': PHALA}
SRC20_STRONG = {'book': 'phaladeepika-1937', 'chapter': 'XX', 'sloka': '2-14', 'pdf_pages': [238, 239, 240, 241], 'verified_against_page_image': True, 'url': PHALA}
SRC20_WEAK = {'book': 'phaladeepika-1937', 'chapter': 'XX', 'sloka': '15-20', 'pdf_pages': [242, 243, 244], 'verified_against_page_image': True, 'url': PHALA}
SRC20_SUB = {'book': 'phaladeepika-1937', 'chapter': 'XX', 'sloka': '28-29', 'pdf_pages': [247], 'verified_against_page_image': True, 'url': PHALA}
YEARS = {'Sun': 6, 'Moon': 10, 'Mars': 7, 'Rahu': 18, 'Jupiter': 16, 'Saturn': 19, 'Mercury': 17, 'Ketu': 7, 'Venus': 20}
ORDER = ['Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 'Rahu', 'Jupiter', 'Saturn', 'Mercury']
BAD_HOUSES = (6, 8, 12)

# House-lord rules: (strong reading, weak reading), tags. XX.2-13 and XX.15-20.
HOUSE = {
 1: ('Rising standing, good health and a brightening life.', 'Setbacks to standing and health, a withdrawn or unsettled stretch.', 'status health'),
 2: ('Family comfort, good food, money from speech or teaching, a respected voice.', 'Poor judgement in speech, money drained or lost, friction with family.', 'wealth family'),
 3: ('Support from siblings, good news, courage and recognition.', 'Trouble around siblings, bad advice, hidden opposition and loss of confidence.', 'family status'),
 4: ('Help from relatives, home and vehicle gains, property, a better position.', 'Strain around the mother or home, worries over property and friends.', 'property family'),
 5: ('Children, honour from elders and authority, good learning, merit.', 'Worry over children, confused thinking, wandering and stomach trouble.', 'children status'),
 6: ('Enemies are overcome, good health, strength and confidence.', 'Opposition, setbacks and illness, a stretch of service and low standing.', 'conflict health'),
 7: ('Comforts, pleasant company, a happy partnership and social events.', 'Strain in partnership, separation from loved ones, trouble through the opposite sex.', 'partnership'),
 8: ('Debts cleared, quarrels end, livestock and helpers gained.', 'Money worries, health strain and reputation trouble.', 'wealth health'),
 9: ('Family prosperity, merit, royal favour and respect for the learned.', 'Bad luck, family strain and money trouble, especially around elders.', 'fortune family'),
 10: ('Work succeeds, a lasting position and wide renown.', 'Efforts come to little, loss of honour and time away from home.', 'career status'),
 11: ('A steady flow of income, domestic happiness and good service.', 'Bad news, trouble to siblings or children, and money friction.', 'wealth family'),
 12: ('Money goes out on good causes, merit is earned and past errors are worked off.', 'Illness, dishonour and loss of savings.', 'wealth health'),
}
# Planet's own Dasa nature, Adh. XIX slokas 18-26 (general results).
NATURE = {
 'Sun': ('money through risky or forceful routes, quarrels with authority, strain with seniors and some loss of property', 'conflict wealth'),
 'Moon': ('money through devotion and favour, comforts and ornaments, though some friction with difficult people', 'wealth'),
 'Mars': ('money through land and disputes, more cattle and land, quarrels with brothers, heat-related ailments', 'property conflict'),
 'Rahu': ('unsettled mind and trouble from authority and enemies, with danger of loss in family matters', 'conflict'),
 'Jupiter': ('status, children, wealth and friends, with respect for the way you speak', 'status children wealth'),
 'Saturn': ('money through effort and strife, servants and cattle gained, worry over children and spouse, windy ailments', 'wealth conflict'),
 'Mercury': ('learned and spiritual guidance, money through the learned, land and cattle, wealth that builds', 'wealth status'),
 'Ketu': ('sorrow and confusion, trouble from powerful people and time away from home', 'conflict'),
 'Venus': ('a partner, jewels, comforts, trade and travel gains, with anxiety and separation from elders', 'partnership wealth'),
}
DOMAIN = {2: 'money', 11: 'money', 10: 'career', 7: 'partnership', 5: 'children', 4: 'home', 9: 'luck'}


def _dt(s):
    return datetime.fromisoformat(s)


def _house(placement, model):
    return placement['whole_sign_house_from_ascendant'] if model == 'whole_sign' else placement['sripati_degree_house']['house']


def _nodes(chart):
    pl = dict(chart['placements'])
    if 'Rahu' in pl and 'Ketu' not in pl:
        r = pl['Rahu']
        lon = (r['longitude'] + 180) % 360
        deg = r.get('sripati_degree_house')
        pl['Ketu'] = {'longitude': lon, 'sign': SIGNS[int(lon // 30)], 'retrograde': True,
                      'whole_sign_house_from_ascendant': (r['whole_sign_house_from_ascendant'] + 5) % 12 + 1,
                      'sripati_degree_house': {'house': (deg['house'] + 5) % 12 + 1} if deg else None}
    return pl


def _owned(chart, planet):
    asc = int(chart['ascendant']['longitude'] // 30)
    return [h for h in range(1, 13) if LORDS[(asc + h - 1) % 12] == planet]


def _ord(n):
    return f"{n}{'th' if 10 <= n % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')}"


def _classify(planet, pl, model):
    p = pl[planet]
    strong, weak = [], []
    house = _house(p, model)
    if house in BAD_HOUSES: weak.append(f'in the {_ord(house)} house')
    elif house: strong.append(f'in the {_ord(house)} house')
    if planet in ('Rahu', 'Ketu'):
        # XIX.14-17 and XIX.21 give node periods as testing. XIX.15 makes an exception: a benefic
        # joins the node and it sits in a house other than the 6th, 8th, 12th. XIX.16 gives honour
        # that is lost at the end for Rahu in Virgo, Pisces or Scorpio, so that is mixed.
        strong, weak = [], []
        joined = [q for q in ('Jupiter', 'Venus') if q in pl and _house(pl[q], model) == house]
        if joined and house not in BAD_HOUSES: strong.append('joined by ' + ' and '.join(joined) + f' in the {_ord(house)} house')
        elif p['sign'] in ('Virgo', 'Pisces', 'Scorpio') and planet == 'Rahu': strong.append(f"in {p['sign']}"); weak.append('honour lost at the end of the period')
        else: weak.append('node periods read as testing unless a benefic joins in a good house')
        return strong, weak, house
    from .natal_factors import EXALTATION
    sign_i = int(p['longitude'] // 30)
    if p.get('retrograde'): strong.append('retrograde')
    if LORDS[sign_i] == planet: strong.append('in its own sign')
    elif EXALTATION.get(planet) == p['sign']: strong.append('exalted')
    elif sign_i == (SIGNS.index(EXALTATION[planet]) + 6) % 12: weak.append('in its fall')
    else:
        rel = natural_relation(planet, LORDS[sign_i])
        if rel == 'friend': strong.append("in a friend's sign")
        elif rel == 'enemy': weak.append("in an enemy's sign")
    return strong, weak, house


def _class(strong, weak):
    return 'mixed' if strong and weak else 'weak' if weak else 'strong' if strong else 'mixed'


def _tone(planet, chart, pl):
    out = {}
    detail = {}
    for m in ('whole_sign', 'sripati_degree_bhava'):
        mm = 'whole_sign' if m == 'whole_sign' else 'sripati'
        s, w, h = _classify(planet, pl, mm)
        out[m] = _class(s, w); detail[m] = (s, w, h)
    final = out['whole_sign'] if out['whole_sign'] == out['sripati_degree_bhava'] else 'mixed'
    return final, out, detail


def _antardasas(start, end, lord, yl_days):
    full = timedelta(days=YEARS[lord] * yl_days)
    t0 = end - full
    i = ORDER.index(lord)
    seq = ORDER[i:] + ORDER[:i]
    out, cur = [], t0
    for b in seq:
        dur = full * YEARS[b] / 120
        a, z = cur, cur + dur
        if z > start:
            out.append((b, max(a, start), min(z, end)))
        cur = z
    return out


def _span(vals):
    lo = min(v[0] for v in vals); hi = max(v[1] for v in vals)
    return [lo, hi]


def _good_house_from(dasa_house, bhukti_house):
    return ((bhukti_house - dasa_house) % 12) + 1


def life_periods(report, today=None):
    chart = report['natal_chart']; timing = report.get('timing_conditional') or {}
    tls = list((timing.get('timelines') or {}).values())
    if not tls: return None
    pl = _nodes(chart)
    shadbala = ((report.get('shadbala_working_profile') or {}).get('planets')) or {}
    cand = set(timing.get('marriage_candidate_lords') or [])
    periods = []
    for idx, m0 in enumerate(tls[0]['mahadasas'][:9]):
        lord = m0['lord']
        tone, by_model, detail = _tone(lord, chart, pl)
        owned = _owned(chart, lord) if lord not in ('Rahu', 'Ketu') else []
        rules = [{'rule_id': f'phaladeepika-xix-nature-{lord.lower()}', 'source': SRC19, 'effect': NATURE[lord][0]}]
        themes = set(NATURE[lord][1].split())
        reads = []
        for h in owned:
            strong_txt, weak_txt, tags = HOUSE[h]
            use = [('strong', strong_txt)] if tone == 'strong' else [('weak', weak_txt)] if tone == 'weak' else [('strong', strong_txt), ('weak', weak_txt)]
            for cls, txt in use:
                reads.append(txt)
                rules.append({'rule_id': f'phaladeepika-xx-house{h}-lord-{cls}', 'source': SRC20_STRONG if cls == 'strong' else SRC20_WEAK, 'effect': txt})
            themes |= set(tags.split())
        s, w, hse = detail['whole_sign']
        basis = []
        if s: basis.append('supportive: ' + ', '.join(s))
        if w: basis.append('testing: ' + ', '.join(w))
        sv = (shadbala.get(lord) or {}).get('verdict')
        conf = 'steady' if by_model['whole_sign'] == by_model['sripati_degree_bhava'] and sv != 'unresolved_across_variants' else 'tentative'
        # per-timeline dates
        spans, sub = [], {}
        for tl in tls:
            m = next(x for x in tl['mahadasas'] if x['lord'] == lord)
            a, z = _dt(m['start']), _dt(m['end'])
            spans.append((a.year, z.year))
            for b, ba, bz in _antardasas(a, z, lord, tl['year_length_days']):
                sub.setdefault(b, []).append((ba.year, bz.year))
        bhuktis = []
        dh = _house(pl[lord], 'whole_sign')
        dh2 = _house(pl[lord], 'sripati')
        for b in [x for x in ORDER[ORDER.index(lord):] + ORDER[:ORDER.index(lord)] if x in sub]:
            bh, bh2 = _house(pl[b], 'whole_sign'), _house(pl[b], 'sripati')
            pos1, pos2 = _good_house_from(dh, bh), _good_house_from(dh2, bh2)
            bad1, bad2 = pos1 in BAD_HOUSES, pos2 in BAD_HOUSES
            btone = 'testing' if bad1 and bad2 else 'supportive' if not bad1 and not bad2 else 'mixed'
            enemy = b != lord and natural_relation(b, lord) == 'enemy' if b in YEARS and lord in YEARS and b not in ('Rahu', 'Ketu') and lord not in ('Rahu', 'Ketu') else False
            if enemy and btone == 'supportive': btone = 'mixed'
            note = []
            for h in (_owned(chart, b) if b not in ('Rahu', 'Ketu') else []):
                if h in DOMAIN: note.append(DOMAIN[h])
            kind = []
            if btone != 'testing' and tone != 'weak':
                kind = sorted({d for d in note if d in ('money', 'career', 'partnership', 'children')})
            if lord in cand and b in cand and 'partnership' not in kind: kind.append('partnership')
            bhuktis.append({'lord': b, 'years_about': _span(sub[b]), 'tone': btone, 'highlights': kind,
                            'basis': ((f'{b} sits in the {_ord(pos1)} from {lord}' if b != lord else f'{b} is the period lord itself') + (', an unhappy position' if bad1 else ', a good position' if b != lord else '') + ('; natural enemy of the period lord' if enemy else ''))})
        pdk = sorted({d for b in bhuktis for d in b['highlights']})
        lead = {'strong': 'A supportive period.', 'weak': 'A testing period.', 'mixed': 'A mixed period.'}[tone]
        if tone == 'mixed' and len(reads) >= 2:
            summary = f'{lead} Good side: {reads[0]} Hard side: {reads[1]}'
        else:
            summary = ' '.join([lead] + reads[:2]) if reads else lead
        summary += f' In general this planet\'s period brings {NATURE[lord][0]}.'
        periods.append({'lord': lord, 'summary': summary, 'years_about': _span(spans), 'tone': tone, 'confidence': conf,
                        'houses_owned': owned, 'basis': basis, 'themes': sorted(themes),
                        'reading': NATURE[lord][0], 'house_lord_reading': reads,
                        'rules': rules, 'bhuktis': bhuktis, 'highlight_kinds': sorted({DOMAIN[h] for h in owned if h in DOMAIN and DOMAIN[h] in ('money','career','partnership','children')}) if tone != 'weak' else [], 'bhukti_highlight_kinds': pdk,
                        'sub_rule_source': SRC20_SUB})
    return {'status': 'periods_broad_themes_not_events', 'periods': periods,
            'held_out': ['death and demise clauses', 'character and "wicked" wording', 'combustion strength (limits not defined on these pages)', 'XX.23 birth-star sub-period rule', 'XX.24 dangerous ordinal rule'],
            'notice': 'Each period is a broad theme from the Dasa lord (Adh. XIX, XX), not an event or a date of an event. Dates are the union of four timing conventions, rounded to years.'}
