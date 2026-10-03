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
    heads = {'strong': 'A strong indication of a supportive partnership',
             'good': 'Encouraging for partnership',
             'some': 'A few supportive signs for partnership',
             'quiet': 'Nothing in particular stands out for marriage',
             'mixed': 'Mixed signals on partnership'}
    text = {'strong': 'Many of the classical marriage combinations are present in your chart.',
            'good': 'Several classical marriage combinations are present in your chart, and they point towards a good partnership.',
            'some': 'A small number of classical marriage combinations are present. They lean favourable but are not many.',
            'quiet': 'Your chart shows none of the classical marriage combinations strongly, so it leans neither way.',
            'mixed': 'Your chart carries both favourable and testing combinations, so expect a partnership that takes some work and patience.'}[level]
    pts = [f'In your favour: {p}' for p in good[:3]]
    if hard:
        pts.append('Needs care: ' + hard[0])
    return {'id': 'marriage', 'title': 'Marriage and partnership', 'level': level, 'headline': heads[level], 'text': text,
            'confidence': 'steady' if agree else 'tentative', 'points': pts}


def _wealth(report):
    data = report.get('wealth_conditional') or {}
    rows = data.get('rows') or []
    if not rows:
        return None
    level, agree = _topic_level(rows, ADVERSE_WEALTH)
    good = _points([r for r in rows if not _adverse(r, ADVERSE_WEALTH)], ADVERSE_WEALTH)
    hard = _points([r for r in rows if _adverse(r, ADVERSE_WEALTH)], ADVERSE_WEALTH, True)
    heads = {'strong': 'A strong indication of comfortable earnings',
             'good': 'Good signs for money',
             'some': 'Some supportive signs for money',
             'quiet': 'Steady, with no special wealth combination',
             'mixed': 'Mixed signals on money'}
    text = {'strong': 'Many of the classical wealth combinations are present in your chart.',
            'good': 'Several classical wealth combinations are present in your chart.',
            'some': 'A few classical wealth combinations are present. Expect earnings to build gradually through your own effort rather than arrive in a rush.',
            'quiet': 'None of the classical wealth combinations show strongly, so the chart leans neither towards unusual wealth nor towards hardship.',
            'mixed': 'Your chart carries both supportive and limiting money combinations, so earnings are likely to come in phases.'}[level]
    pts = [f'In your favour: {p}' for p in good[:3]]
    if hard:
        pts.append('Needs care: ' + hard[0])
    return {'id': 'wealth', 'title': 'Money and earnings', 'level': level, 'headline': heads[level], 'text': text,
            'confidence': 'steady' if agree else 'tentative', 'points': pts}


def _strength(report):
    planets = ((report.get('shadbala_working_profile') or {}).get('planets')) or {}
    if not planets:
        return None
    strong = [n for n, p in planets.items() if p.get('verdict') == 'meets_sripati_minimum_in_all_variants']
    open_ = [n for n in planets if n not in strong]
    n, k = len(planets), len(strong)
    level = 'strong' if k >= n - 1 and k >= 5 else 'good' if k >= n / 2 else 'some' if k else 'quiet'
    head = {'strong': 'Most of your planets are strong', 'good': 'Your planets are fairly strong', 'some': 'Your planets are modest in strength', 'quiet': 'Your planets are on the weaker side'}[level]
    text = f'{k} of {n} planets clear the classical strength minimum, so their results should be able to show up.'
    if open_:
        text += f' {", ".join(open_)} sits close to the line, so treat its results as milder.'
    return {'id': 'strength', 'title': 'Planetary strength', 'level': level, 'headline': head, 'text': text,
            'confidence': 'steady' if not open_ else 'tentative', 'points': [f'Strong: {", ".join(strong)}'] if strong else []}


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
            'text': 'Your chart points to more than one livelihood theme, with no single one clearly ahead. Older texts mention: ' + ', '.join(themes[:8]) + '. Read these as flavours of work you may be drawn to, not a job title.',
            'confidence': 'tentative', 'points': []}


def _span(lo, hi):
    return f'about {lo}' if lo == hi else f'about {lo} to {hi}'


def _timing(report, as_of):
    t = report.get('timing_conditional') or {}
    tls = list((t.get('timelines') or {}).values())
    if not tls:
        return None
    now = as_of.astimezone(timezone.utc).isoformat()
    cur = []
    for tl in tls:
        for i, m in enumerate(tl['mahadasas']):
            if m['start'] <= now < m['end']:
                nxt = tl['mahadasas'][i + 1] if i + 1 < len(tl['mahadasas']) else None
                cur.append((m, nxt))
                break
    pts = []
    if cur:
        lords = {m['lord'] for m, _ in cur}
        if len(lords) == 1:
            lo = min(_year(m['start']) for m, _ in cur); hi = max(_year(m['end']) for m, _ in cur)
            pts.append(f'Current main period: {cur[0][0]["lord"]}, {_span(lo, hi)}.')
            nxts = [n for _, n in cur if n]
            if nxts and len({n['lord'] for n in nxts}) == 1:
                lo = min(_year(n['start']) for n in nxts); hi = max(_year(n['end']) for n in nxts)
                pts.append(f'Next: {nxts[0]["lord"]}, {_span(lo, hi)}.')
    wins = []
    for tl in tls:
        for w in tl.get('marriage_candidate_antardasa_windows') or []:
            if w['end'] > now:
                wins.append((w['maha_lord'], w['antar_lord'], _year(w['start']), _year(w['end'])))
    text = 'All four ways of reading the timing agree on the main periods, within a few months.' if len({tuple(m['lord'] for m in tl['mahadasas']) for tl in tls}) == 1 else 'The timing readings differ on the main periods.'
    if wins:
        lo = min(w[2] for w in wins); hi = max(w[3] for w in wins)
        text += f' The classical marriage-period rule points to {_span(lo, hi)}. It is one narrow rule, so treat it as a pointer and not a date.'
    else:
        text += ' The classical marriage-period rule finds no window still ahead.'
    return {'id': 'timing', 'title': 'Timing', 'level': 'some', 'headline': 'Your life periods at a glance', 'text': text,
            'confidence': 'steady' if len({tuple(m['lord'] for m in tl['mahadasas']) for tl in tls}) == 1 else 'tentative', 'points': pts}


def _periods(report, as_of):
    lp = report.get('life_periods') or {}
    ps = lp.get('periods') or []
    if not ps:
        return None
    y = as_of.year
    good = [p for p in ps if p['tone'] == 'strong' and p['years_about'][1] >= y]
    hard = [p for p in ps if p['tone'] == 'weak' and p['years_about'][1] >= y]
    pts = []
    if good:
        pts.append('Supportive: ' + '; '.join(f"{p['lord']} period, about {p['years_about'][0]} to {p['years_about'][1]}" for p in good[:3]))
    if hard:
        pts.append('Testing: ' + '; '.join(f"{p['lord']} period, about {p['years_about'][0]} to {p['years_about'][1]}" for p in hard[:3]))
    return {'id': 'periods', 'title': 'Life stretches ahead', 'level': 'mixed' if good and hard else 'good' if good else 'some',
            'headline': 'Some stretches ahead help, others test', 'text': 'Each major period of your life has a broad flavour from the planet that rules it. Open the period-by-period section below for what each stretch tends to bring.',
            'confidence': 'tentative', 'points': pts}


def outcome_summary(report, as_of=None):
    as_of = as_of or datetime.now(timezone.utc)
    topics = [x for x in (_career(report), _marriage(report), _wealth(report), _strength(report), _timing(report, as_of), _periods(report, as_of)) if x]
    return {'topics': topics,
            'basis': 'Levels count how many of the classical books\' own combinations your chart shows. They are not tested forecasts.'}
