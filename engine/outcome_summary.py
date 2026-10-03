"""Plain-language outcome layer built from the evidence layers.

This module weighs the condition rows, planet-strength ranges and dated
timelines already in the report and states one reading per topic. It uses two
fixed rules, nothing else:

* A row that is met counts 1 for the topic it supports (or 1 against, for an
  adverse row). A row that holds under one house model but not the other, or is
  only possibly met, counts 0.5. Unresolved rows count 0. A rule that is not met
  adds nothing: the books list favourable combinations, so a missing one is
  silence, not a bad sign.
* The score is worked out under each house model separately. If the two models
  land on different levels, the lower level is stated and confidence drops.

The level names describe how many of the books' own combinations the chart
shows. They are not measured accuracy. empirical_accuracy stays unvalidated.
"""
from datetime import datetime, timezone

LEVELS = ['quiet', 'some', 'good', 'strong']  # ordered low to high
ADVERSE_WEALTH = {'phaladeepika-viii-sun-in-2', 'phaladeepika-viii-mars-in-2', 'phaladeepika-viii-saturn-in-2'}
NOT_NATAL = {'phaladeepika-x-13-period-candidate-lords'}
WEIGHT = {'met': 1.0, 'possibly_met': 0.5, 'house_model_dependent': 0.5}


def _adverse(row, adverse_ids):
    return bool(row.get('adverse_marital_status_text') or row.get('adverse_text')) or row['rule_id'] in adverse_ids


def _status(row, model):
    if model is None:
        return row['status']
    return (row.get('status_by_house_model') or {}).get(model, row['status'])


def _score(rows, model, adverse_ids):
    sup = adv = 0.0
    for r in rows:
        if r['rule_id'] in NOT_NATAL:
            continue
        w = WEIGHT.get(_status(r, model), 0.0)
        if w:
            if _adverse(r, adverse_ids): adv += w
            else: sup += w
    return sup, adv


def _level(sup, adv):
    if adv and adv >= sup:
        return 'mixed'
    net = sup - adv
    if net >= 5: return 'strong'
    if net >= 3: return 'good'
    if net >= 1: return 'some'
    return 'quiet'


def _topic_level(rows, adverse_ids):
    models = ['whole_sign', 'sripati_degree_bhava']
    levels = [_level(*_score(rows, m, adverse_ids)) for m in models]
    order = ['mixed', 'quiet', 'some', 'good', 'strong']
    agree = levels[0] == levels[1]
    final = min(levels, key=order.index)
    return final, agree


def _clean(text):
    t = text.strip().rstrip('.')
    first = t.split(' ', 1)[0]
    return t[0].lower() + t[1:] if first in ('A', 'An', 'The', 'Benefics', 'Malefics') else t


def _points(rows, adverse_ids, want_adverse=False):
    out = []
    for r in rows:
        if r['rule_id'] in NOT_NATAL or r.get('status') not in WEIGHT:
            continue
        if _adverse(r, adverse_ids) == want_adverse and _status(r, 'whole_sign') in WEIGHT or _adverse(r, adverse_ids) == want_adverse and _status(r, 'sripati_degree_bhava') in WEIGHT:
            out.append(_clean(r['condition']))
    return out


def _year(iso):
    return int(str(iso)[:4])


def _marriage(report):
    data = report.get('marriage_conditional') or {}
    rows = data.get('rows') or []
    if not rows:
        return None
    level, agree = _topic_level(rows, set())
    good = _points([r for r in rows if not _adverse(r, set())], set())
    hard = _points([r for r in rows if _adverse(r, set())], set(), True)
    heads = {'strong': 'Your chart strongly supports a happy partnership', 'good': 'Encouraging for partnership', 'some': 'A few supportive signs for partnership', 'quiet': 'Nothing in particular stands out for marriage', 'mixed': 'Mixed signals on partnership'}
    text = {'strong': 'Close relationships are a real source of happiness and support for you.', 'good': 'Partnership tends to bring you comfort, goodwill and support.', 'some': 'Expect warmth and goodwill in close relationships, without anything outsized promised.', 'quiet': 'Your chart leans neither way on partnership, so it rests largely on the choices you make.', 'mixed': 'Partnership brings both comfort and testing moments, so expect it to take some work and patience.'}[level]
    ev = [f'Supports: {p}' for p in good[:6]] + [f'Needs care: {p}' for p in hard[:3]]
    pts = []
    return {'id': 'marriage', 'evidence': ev, 'title': 'Marriage and partnership', 'level': level, 'headline': heads[level], 'text': text,
            'confidence': 'steady' if agree else 'tentative', 'points': pts}


def _wealth(report):
    data = report.get('wealth_conditional') or {}
    rows = data.get('rows') or []
    if not rows:
        return None
    level, agree = _topic_level(rows, ADVERSE_WEALTH)
    good = _points([r for r in rows if not _adverse(r, ADVERSE_WEALTH)], ADVERSE_WEALTH)
    hard = _points([r for r in rows if _adverse(r, ADVERSE_WEALTH)], ADVERSE_WEALTH, True)
    heads = {'strong': 'Comfortable earnings look likely', 'good': 'Good signs for money', 'some': 'Some supportive signs for money', 'quiet': 'Steady, with no special windfall', 'mixed': 'Mixed signals on money'}
    text = {'strong': 'Money tends to come readily and stay with you.', 'good': 'Money tends to come steadily, with several things working in your favour.', 'some': 'Expect earnings to build gradually through your own effort rather than arrive in a rush.', 'quiet': 'Nothing in your chart pushes money strongly up or down, so it follows your effort.', 'mixed': 'Earnings are likely to come in phases, with good and lean stretches.'}[level]
    ev = [f'Supports: {p}' for p in good[:6]] + [f'Needs care: {p}' for p in hard[:3]]
    pts = []
    return {'id': 'wealth', 'evidence': ev, 'title': 'Money and earnings', 'level': level, 'headline': heads[level], 'text': text,
            'confidence': 'steady' if agree else 'tentative', 'points': pts}


AREA = {'Sun': 'confidence and standing', 'Moon': 'emotional steadiness', 'Mars': 'drive and courage', 'Mercury': 'thinking and communication',
        'Jupiter': 'judgement and good fortune', 'Venus': 'relationships and comfort', 'Saturn': 'discipline and endurance'}


def _strength(report):
    planets = ((report.get('shadbala_working_profile') or {}).get('planets')) or {}
    if not planets:
        return None
    strong = [n for n, p in planets.items() if p.get('verdict') == 'meets_sripati_minimum_in_all_variants']
    open_ = [n for n in planets if n not in strong]
    n, k = len(planets), len(strong)
    level = 'strong' if k >= n - 1 and k >= 5 else 'good' if k >= n / 2 else 'some' if k else 'quiet'
    head = {'strong': 'You have a lot to draw on', 'good': 'You have solid inner resources', 'some': 'Some of your inner resources are modest', 'quiet': 'You may have to build your inner resources'}[level]
    text = 'Your strongest areas: ' + ', '.join(AREA[x] for x in strong[:5]) + '.' if strong else ''
    if open_:
        text += ' The softer side is ' + ' and '.join(AREA[x] for x in open_) + ', so give it some care.'
    ev = [f'{x}: meets the classical strength minimum in every variant' for x in strong] + [f'{x}: variants disagree' for x in open_]
    return {'id': 'strength', 'evidence': ev, 'title': 'Your inner resources', 'level': level, 'headline': head, 'text': text.strip(),
            'confidence': 'steady' if not open_ else 'tentative', 'points': []}


def _career(report):
    cands = (((report.get('life_aspect_candidates') or {}).get('career')) or {}).get('candidates') or []
    if not cands:
        return None
    themes = []
    for c in cands:
        for t in (c.get('historical_livelihood_examples') or [])[:4]:
            if t not in themes:
                themes.append(t)
    return {'id': 'career', 'title': 'Work and livelihood', 'level': 'mixed', 'headline': 'Several kinds of work show up',
            'text': 'Your chart points to more than one livelihood theme, with no single one clearly ahead. Traditional readings mention: ' + ', '.join(themes[:8]) + '. Read these as flavours of work you may be drawn to, not a job title.',
            'confidence': 'tentative', 'points': []}


def _span(lo, hi):
    return f'about {lo}' if lo == hi else f'about {lo} to {hi}'


def _timing(report, as_of):
    t = report.get('timing_conditional') or {}
    tls = list((t.get('timelines') or {}).values())
    if not tls:
        return None
    now = as_of.astimezone(timezone.utc).isoformat()
    wins = []
    for tl in tls:
        for w in tl.get('marriage_candidate_antardasa_windows') or []:
            if w['end'] > now:
                wins.append((_year(w['start']), _year(w['end'])))
    text = 'Years are rounded, because the traditional sources count them in more than one way.'
    if wins:
        text += f" The traditional rule for the time of marriage points to {_span(min(w[0] for w in wins), max(w[1] for w in wins))}. It is one narrow rule, so treat it as a pointer and not a date."
    else:
        text += ' The traditional rule for the time of marriage finds no window still ahead.'
    return {'id': 'timing', 'title': 'Timing', 'level': 'some', 'headline': 'Your life in stretches', 'text': text,
            'confidence': 'steady', 'points': [], 'evidence': ['Dated from the four timing conventions; marriage window from Phaladeepika X.13 with the sub-period rule.']}


def _periods(report, as_of):
    ps = ((report.get('life_periods') or {}).get('periods')) or []
    if not ps:
        return None
    y = as_of.year
    cur = next((p for p in ps if p['years_about'][0] <= y <= p['years_about'][1]), None)
    nxt = next((p for p in ps if p['years_about'][0] > (cur['years_about'][0] if cur else y)), None)
    word = lambda p: {'strong': 'a supportive stretch', 'weak': 'a testing stretch', 'mixed': 'a mixed stretch'}[p['tone']]
    pts = []
    if cur: pts.append(f"Right now (about {cur['years_about'][0]} to {cur['years_about'][1]}): {word(cur)}.")
    if nxt: pts.append(f"Next (about {nxt['years_about'][0]} to {nxt['years_about'][1]}): {word(nxt)}.")
    good = [p for p in ps if p['tone'] == 'strong' and p['years_about'][1] >= y]
    hard = [p for p in ps if p['tone'] == 'weak' and p['years_about'][1] >= y]
    return {'id': 'periods', 'title': 'Life stretches ahead', 'level': 'mixed' if good and hard else 'good' if good else 'some',
            'headline': 'Some stretches ahead help, others test', 'confidence': 'tentative',
            'text': 'Your life moves through long stretches, each with its own flavour. Open the section below to see what each one tends to bring for you.',
            'points': pts, 'evidence': [f"{p['years_about'][0]} to {p['years_about'][1]}: {p['lord']} period, {p['tone']}" for p in ps]}


def outcome_summary(report, as_of=None):
    as_of = as_of or datetime.now(timezone.utc)
    topics = [x for x in (_career(report), _marriage(report), _wealth(report), _strength(report), _timing(report, as_of), _periods(report, as_of)) if x]
    return {'topics': topics,
            'basis': 'Levels count how many of the classical books\' own combinations your chart shows. They are not tested forecasts.'}
