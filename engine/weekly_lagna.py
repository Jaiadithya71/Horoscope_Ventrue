"""Week-by-lagna transit evidence: deterministic sky math plus page-cited structure.

One week (Monday 00:00 IST to the next Monday 00:00 IST) is sampled day by day.
For a chosen lagna (ascendant sign) the engine counts whole-sign houses from
that lagna for every planet, and lists sign ingresses and retrograde stations
that fall inside the week with their clock times. Ketu is derived geometry
(mean Rahu + 180 degrees), not a separately verified rule.

Outcome lines appear only where a verified, page-cited conditional rule exists.
The enabled transit rules (engine/rules.json, Phaladeepika XXVI) read the Moon
sign, not the lagna, so they are emitted only when a Moon sign is supplied, and
they are sampled once per day at 00:00 IST. Historical astrological
interpretations, not validated prediction or medical/financial advice.
"""
import datetime as dt
import json
from pathlib import Path

import swisseph as swe

from .forecast import PLANETS, SIGNS, FLAGS, julian_day, position, sign_index
from .synthesis import structural_factors
from .transit_phase import transit_phase

IST = dt.timezone(dt.timedelta(hours=5, minutes=30), 'IST')
RULES = json.loads((Path(__file__).resolve().parent / 'rules.json').read_text())
WEEKDAY_NAMES = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')
MODEL = 'Swiss Ephemeris/Moshier + Lahiri sidereal; mean Rahu node; whole-sign houses from lagna'
NOTICE = ('Historical astrological interpretations, not validated prediction or medical/financial advice. '
          'House counts, aspects and lordship are structure, not outcomes. Outcome lines come only from '
          'page-cited rules, and the enabled transit rules read the Moon sign, not the lagna.')


def week_bounds_ist(any_date):
    """The IST week (Mon 00:00 to next Mon 00:00) containing any_date, as UTC instants."""
    if not isinstance(any_date, dt.date) or isinstance(any_date, dt.datetime):
        raise ValueError('Supply a calendar date (YYYY-MM-DD).')
    monday = any_date - dt.timedelta(days=any_date.weekday())
    start = dt.datetime(monday.year, monday.month, monday.day, tzinfo=IST)
    end = start + dt.timedelta(days=7)
    return start.astimezone(dt.timezone.utc), end.astimezone(dt.timezone.utc)


def _speed(utc, planet):
    return swe.calc_ut(julian_day(utc), PLANETS[planet], FLAGS)[0][3]


def _bisect_ingress(planet, lo, hi, lo_sign, hi_sign):
    """First instant in (lo, hi] where the sidereal sign leaves lo_sign; ~1 minute precision."""
    for _ in range(12):
        mid = lo + (hi - lo) / 2
        if position(mid, planet)['sign'] == lo_sign:
            lo = mid
        else:
            hi = mid
    return hi


def _find_ingresses(planet, samples, signs):
    events = []
    for k in range(len(samples) - 1):
        lo, hi = samples[k], samples[k + 1]
        cur, nxt = signs[k], signs[k + 1]
        guard = 0
        while cur != nxt and guard < 3:
            crossing = _bisect_ingress(planet, lo, hi, cur, nxt)
            after = crossing + dt.timedelta(seconds=61)
            events.append({'kind': 'sign_ingress', 'planet': planet, 'at_utc': crossing.isoformat(),
                           'at_ist': crossing.astimezone(IST).strftime('%d %b %Y, %H:%M IST'),
                           'from_sign': cur, 'to_sign': position(after, planet)['sign'],
                           'precision': 'about one minute'})
            lo, cur, guard = after, events[-1]['to_sign'], guard + 1
    return events


def _find_stations(planet, samples, retro):
    if planet in ('Sun', 'Moon'):
        return []
    events = []
    for k in range(len(samples) - 1):
        if retro[k] == retro[k + 1]:
            continue
        lo, hi = samples[k], samples[k + 1]
        for _ in range(12):
            mid = lo + (hi - lo) / 2
            if (_speed(mid, planet) < 0) == retro[k]:
                lo = mid
            else:
                hi = mid
        events.append({'kind': 'station_retrograde' if not retro[k] else 'station_direct',
                       'planet': planet, 'at_utc': hi.isoformat(),
                       'at_ist': hi.astimezone(IST).strftime('%d %b %Y, %H:%M IST'),
                       'precision': 'about one minute'})
    return events


def _moon_findings(samples, per_planet_signs, moon_sign):
    """Daily-00:00-IST activation spans for the enabled cited transit rules."""
    ref = sign_index(moon_sign)
    findings = []
    for rule in RULES:
        planet = rule['planet']
        active = []
        for k, utc in enumerate(samples[:-1]):
            house = (sign_index(per_planet_signs[planet][k]) - ref) % 12 + 1
            if house == rule['house_from_moon']:
                day = (utc + dt.timedelta(hours=5, minutes=30)).date()
                active.append({'date': day.isoformat(), 'weekday': WEEKDAY_NAMES[day.weekday()]})
        if active:
            findings.append({'rule_id': rule['id'], 'planet': planet, 'topic': rule['topic'],
                             'outcome': rule['outcome'], 'source': rule['source'],
                             'house_from_moon': rule['house_from_moon'], 'active_days': active})
    return findings


def weekly_lagna_report(week_of, lagna, moon_sign=None):
    """week_of: dt.date (any day in the wanted week). lagna: English sign name."""
    ref = sign_index(lagna)
    if moon_sign is not None:
        sign_index(moon_sign)
    start_utc, end_utc = week_bounds_ist(week_of)
    samples = [start_utc + dt.timedelta(days=k) for k in range(8)]

    placements, events = {}, []
    for planet in PLANETS:
        pos = [position(utc, planet) for utc in samples]
        signs = [p['sign'] for p in pos]
        retro = [p['retrograde'] for p in pos]
        placements[planet] = {
            'signs_by_day': signs,
            'degrees_in_sign_by_day': [round(p['longitude'] % 30, 2) for p in pos],
            'retrograde_by_day': retro,
            'houses_from_lagna_by_day': [(sign_index(s) - ref) % 12 + 1 for s in signs],
            'transit_phase_evidence': transit_phase(planet, pos[0]['longitude']),
        }
        events += _find_ingresses(planet, samples, signs)
        events += _find_stations(planet, samples, retro)

    rahu_lon = position(samples[0], 'Rahu')['longitude']
    ketu_signs = [SIGNS[int(((position(utc, 'Rahu')['longitude'] + 180) % 360) // 30)] for utc in samples]
    placements['Ketu'] = {
        'signs_by_day': ketu_signs,
        'degrees_in_sign_by_day': [round((position(utc, 'Rahu')['longitude'] + 180) % 30, 2) for utc in samples],
        'retrograde_by_day': [p['retrograde'] for p in [position(utc, 'Rahu') for utc in samples]],
        'houses_from_lagna_by_day': [(sign_index(s) - ref) % 12 + 1 for s in ketu_signs],
        'transit_phase_evidence': transit_phase('Ketu', (rahu_lon + 180) % 360),
        'derived': 'Mean Rahu longitude + 180 degrees; geometry only, no separate verified rule.',
    }
    events.sort(key=lambda e: e['at_utc'])

    start_sign_placements = {p: {'sign': v['signs_by_day'][0]} for p, v in placements.items() if p != 'Ketu'}
    report = {
        'week_start_ist': samples[0].astimezone(IST).date().isoformat(),
        'week_end_ist_exclusive': samples[-1].astimezone(IST).date().isoformat(),
        'day_dates_ist': [(s + dt.timedelta(hours=5, minutes=30)).date().isoformat() for s in samples[:-1]],
        'lagna': SIGNS[ref],
        'moon_sign': moon_sign,
        'model': MODEL,
        'sampling': 'Daily 00:00 IST; ingress and station times refined to about one minute.',
        'placements': placements,
        'events': events,
        'structural_factors_from_lagna': structural_factors(SIGNS[ref], start_sign_placements),
        'moon_findings': None,
        'notice': NOTICE,
    }
    if moon_sign is not None:
        report['moon_findings'] = _moon_findings(samples, {p: v['signs_by_day'] for p, v in placements.items()}, moon_sign)
        report['moon_findings_notice'] = ('Enabled rules are Phaladeepika XXVI readings counted from the natal Moon sign, '
                                          'sampled once per day at 00:00 IST. They do not depend on the lagna pick.')
    return report


if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--week-of', required=True, help='Any YYYY-MM-DD inside the wanted week (IST weeks, Monday start)')
    p.add_argument('--lagna', required=True, help='Ascendant sign, e.g. Capricorn')
    p.add_argument('--moon-sign', default=None, help='Optional natal Moon sign; enables the cited transit rules')
    a = p.parse_args()
    print(json.dumps(weekly_lagna_report(dt.date.fromisoformat(a.week_of), a.lagna, a.moon_sign), indent=2))
