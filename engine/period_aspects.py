"""Per-aspect reads and practical guidance for each Dasa period.

Built only from rules already page-checked in dasa_period_readings: Phaladeepika Adh. XIX
slokas 5-26 (period of each planet, PLANET_ASPECT) and Adh. XX slokas 2-20 (period of each
house lord, strong versus weak, HOUSE_ASPECT). Each house sentence of those slokas is filed
under the life area it speaks about (own-words split, same content, nothing added).
Where the texts say nothing about an area for a period the area is marked 'quiet' and no
text is invented. Mind and health are thin in these chapters; both say so.

'Practical guidance' lines are generic coaching written by us from the sign of the read
(lean into good signs, take care where signs are hard). They are NOT text of the book and
no classical remedy is given. Smaller-phase area chips are an extension: the book gives the
good/bad tone of a phase (XX.28-29) and does not name areas; we read areas from the houses the
phase planet rules, and label that as an extension.
"""
ASPECTS = ['work', 'money', 'health', 'relationships', 'family', 'mind']
LABELS = {'work': 'Work and standing', 'money': 'Money', 'health': 'Health', 'relationships': 'Relationships', 'family': 'Family and home', 'mind': 'Mind and confidence'}

# house -> aspect -> (when the period lord is strong, when weak). None = the sentence does not speak to that case.
HOUSE_ASPECT = {
 1: {'health': ('Good health and a brightening life.', 'Health setbacks and a withdrawn or unsettled stretch.'), 'work': ('Your standing rises.', 'Your standing takes a knock.')},
 2: {'money': ('Money comes through speech or teaching, and your voice is respected.', 'Money drains or is lost through poor judgement in what you say.'), 'family': ('Family comfort and good food.', 'Friction with family.')},
 3: {'family': ('Support from brothers and sisters, and good news.', 'Trouble around brothers and sisters, and bad advice.'), 'mind': ('Courage, and recognition for it.', 'Hidden opposition and a loss of confidence.')},
 4: {'family': ('Help from relatives, and gains around home and vehicles.', 'Strain around the mother or home, and worry over friends.'), 'money': ('Property gains.', 'Worry over property.'), 'work': ('A better position.', None)},
 5: {'mind': ('Good learning, honour from elders and a sense of merit.', 'Confused thinking and a wandering mind.'), 'family': ('Children and respect from elders.', 'Worry over children.'), 'health': (None, 'Stomach trouble.')},
 6: {'health': ('Good health and strength.', 'Illness.'), 'work': ('Opponents are overcome.', 'Opposition, a stretch of service and low standing.'), 'mind': ('Confidence.', 'Setbacks that wear on you.')},
 7: {'relationships': ('Pleasant company, a happy partnership and social life.', 'Strain in partnership, distance from loved ones and trouble through the opposite sex.')},
 8: {'money': ('Debts clear.', 'Money worries.'), 'health': (None, 'Health strain.'), 'relationships': ('Quarrels end and helpers arrive.', 'Reputation trouble.')},
 9: {'family': ('Family prosperity.', 'Family strain, especially around elders.'), 'work': ('Favour from people in power and respect for the learned.', None), 'money': (None, 'Money trouble.'), 'mind': ('A sense of luck and merit.', 'A run of bad luck.')},
 10: {'work': ('Work succeeds, you hold a lasting position and become widely known.', 'Efforts come to little, standing is lost and you spend time away from home.')},
 11: {'money': ('A steady flow of income.', 'Money friction.'), 'family': ('Domestic happiness.', 'Trouble for brothers, sisters or children.'), 'work': ('Good service.', 'Bad news.')},
 12: {'money': ('Money goes out on good causes.', 'Loss of savings.'), 'health': (None, 'Illness.'), 'mind': ('Merit earned and old errors worked off.', 'Dishonour that wears on you.')},
}
# planet -> aspect -> (text, +1 good / -1 hard / 0 mixed). Adh. XIX 18-26.
PLANET_ASPECT = {
 'Sun': {'work': ('Friction with authority figures and seniors.', -1), 'money': ('Money can come, but through forceful or risky routes.', 0), 'family': ('Some loss of property.', -1)},
 'Moon': {'money': ('Money and comforts come through goodwill and trust.', 1), 'relationships': ('Some friction with difficult people.', -1)},
 'Mars': {'money': ('Income and land come through effort and disputes.', 0), 'family': ('Quarrels with brothers.', -1), 'health': ('Heat-related ailments.', -1)},
 'Rahu': {'mind': ('An unsettled, restless mind.', -1), 'work': ('Trouble from people in authority.', -1), 'relationships': ('Trouble from rivals and enemies.', -1), 'family': ('Risk of loss in family matters.', -1)},
 'Jupiter': {'work': ('Your standing improves and people respect how you speak.', 1), 'family': ('Children and friends bring happiness.', 1), 'money': ('Wealth improves.', 1)},
 'Saturn': {'money': ('Income through steady effort and strife, with helpers around you.', 0), 'family': ('Worry over children.', -1), 'relationships': ('Worry over spouse.', -1), 'health': ('Wind-type ailments.', -1)},
 'Mercury': {'mind': ('Learning and good advisers.', 1), 'money': ('Money through knowledgeable people, and wealth that builds.', 1), 'family': ('Land and cattle gained.', 1)},
 'Ketu': {'mind': ('Sorrow and confusion.', -1), 'work': ('Friction with powerful people.', -1), 'family': ('Time away from home.', -1)},
 'Venus': {'relationships': ('A partner and comforts.', 1), 'money': ('Gains from trade and travel.', 1), 'family': ('Anxiety and distance from elders.', -1)},
}
GUIDE = {
 'work': {'good': 'Lean into: put yourself forward, take visible work and build on your reputation.', 'hard': 'Take care: avoid big career bets and fights with seniors. Keep steady and let the results speak.', 'mixed': 'Lean into steady work you can finish. Take care with confrontations and quick moves.'},
 'money': {'good': 'Lean into: build savings and invest in your skills while the flow is good.', 'hard': 'Take care: keep a cushion, cut spending you do not need and avoid risky bets or lending.', 'mixed': 'Lean into slow, earned income. Take care with risk and large commitments.'},
 'health': {'good': 'Lean into: keep up good routines. This is a good window to build fitness.', 'hard': 'Take care: sleep, food and regular checkups matter more than usual. See a doctor for anything lasting.', 'mixed': 'Keep routines steady and do not ignore small signs.'},
 'relationships': {'good': 'Lean into: spend time with the people who matter and say yes to company.', 'hard': 'Take care: choose words slowly and give people room. Do not make big relationship decisions in a bad moment.', 'mixed': 'Lean into honest conversation, and avoid reacting in the heat of the moment.'},
 'family': {'good': 'Lean into: show up for family and use their support.', 'hard': 'Take care: expect friction and avoid fights over property or old grievances. Stay patient.', 'mixed': 'Lean into the family members who support you and go slowly on disputes.'},
 'mind': {'good': 'Lean into: learning and new ideas, while your head is clear.', 'hard': 'Take care: avoid big decisions when you feel unsettled. Routines, rest and a person to talk to help.', 'mixed': 'Lean into routines that steady you, and sleep on big decisions.'},
}
THIN = {'health': 'The period texts say very little about health. This is not a medical read.', 'mind': 'The period texts say little about mind and confidence beyond what is shown.'}
SRC_PLANET = {'book': 'phaladeepika-1937', 'chapter': 'XIX', 'sloka': '5-26'}
SRC_HOUSE = {'book': 'phaladeepika-1937', 'chapter': 'XX', 'sloka': '2-20'}


def _tone(items):
    s = sum(1 for _, v, _ in items if v > 0); h = sum(1 for _, v, _ in items if v < 0)
    if s and h: return 'mixed'
    return 'good' if s else 'hard' if h else 'mixed'


def period_aspects(lord, owned, tone):
    """Return {aspect: {...}} for a period. tone is strong, weak or mixed (period lord)."""
    out = {}
    for a in ASPECTS:
        items = []
        for t, v in [(PLANET_ASPECT.get(lord, {}).get(a, (None, 0)))]:
            if t: items.append((t, v, SRC_PLANET))
        for h in owned:
            pair = HOUSE_ASPECT.get(h, {}).get(a)
            if not pair: continue
            use = [(pair[0], 1)] if tone == 'strong' else [(pair[1], -1)] if tone == 'weak' else [(pair[0], 1), (pair[1], -1)]
            for t, v in use:
                if t: items.append((t, v, dict(SRC_HOUSE, house=h)))
        if not items:
            out[a] = {'label': LABELS[a], 'status': 'quiet', 'text': 'The texts say nothing specific about this area for this stretch, so the overall feel of the stretch applies.' + (' ' + THIN[a] if a in THIN else ''), 'items': [], 'guidance': None}
            continue
        t = _tone(items)
        text = ' '.join(x[0] for x in items)
        out[a] = {'label': LABELS[a], 'status': {'good': 'supportive', 'hard': 'testing', 'mixed': 'mixed'}[t], 'text': text + (' ' + THIN[a] if a in THIN else ''), 'guidance': GUIDE[a][t],
                  'items': [{'effect': x[0], 'source': x[2]} for x in items]}
    return out


def phase_chips(owned_b, btone):
    """Extension: areas for a smaller phase from the houses the phase planet rules."""
    chips = []
    for h in owned_b:
        for a, pair in HOUSE_ASPECT.get(h, {}).items():
            txt = pair[0] if btone == 'supportive' else pair[1] if btone == 'testing' else None
            if txt and a not in [c[0] for c in chips]: chips.append((a, txt))
    return [{'aspect': a, 'label': LABELS[a], 'text': t} for a, t in chips]
