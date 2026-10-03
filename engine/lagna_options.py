"""Which lagna fits an uncertain birth time, and which clock time fits a known lagna.

Pure arithmetic on the same Swiss Ephemeris call the natal chart uses (Lahiri, W houses).
It does not guess a birth time: it lists every lagna that occurs inside the window the
person can defend, with the clock span of each, and says whether the Moon stays in one
sign and one star across that span. A span midpoint is only a stand-in time for the
chart calculation, and is labelled that way."""
import datetime as dt
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from .forecast import swe, julian_day, SIGNS, FLAGS
from .natal import birth_utc, nakshatra

STEP_MINUTES = 1
MAX_WINDOW_MINUTES = 24 * 60


def _hhmm(text, what):
    try:
        h, m = text.split(':')
        h, m = int(h), int(m)
        if not (0 <= h <= 23 and 0 <= m <= 59):
            raise ValueError
        return h * 60 + m
    except (ValueError, AttributeError):
        raise ValueError(f'{what} must be a 24-hour HH:MM clock time')


def _local(date, minute_of_day):
    base = dt.datetime.fromisoformat(f'{date}T00:00')
    return base + dt.timedelta(minutes=minute_of_day)


def _sample(date, minute, timezone, lat, lon):
    local = _local(date, minute)
    try:
        utc = birth_utc(local.date().isoformat(), local.strftime('%H:%M'), timezone)
    except ValueError as exc:
        if 'Invalid IANA' in str(exc):
            raise
        return None  # DST gap or fold minute: skip rather than guess
    jd = julian_day(utc)
    _c, axes = swe.houses_ex(jd, lat, lon, b'W', swe.FLG_SIDEREAL)
    moon = swe.calc_ut(jd, swe.MOON, FLAGS)[0][0] % 360
    return local, SIGNS[int((axes[0] % 360) // 30)], moon


def _validate(date, timezone, lat, lon):
    try:
        dt.date.fromisoformat(date)
        ZoneInfo(timezone)
    except (ValueError, TypeError, ZoneInfoNotFoundError):
        raise ValueError('Supply a valid date (YYYY-MM-DD) and IANA timezone')
    for v in (lat, lon):
        if type(v) not in (int, float):
            raise ValueError('Latitude and longitude must be numbers')
    if not (-66 < lat < 66 and -180 <= lon <= 180):
        raise ValueError('Lagna spans are only offered between 66 degrees north and south')


def lagna_spans(date, timezone, latitude, longitude, start='00:00', end='23:59'):
    """All lagna spans between start and end (end earlier than start means past midnight)."""
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    _validate(date, timezone, latitude, longitude)
    a, b = _hhmm(start, 'Start'), _hhmm(end, 'End')
    if b < a:
        b += 24 * 60
    if b - a > MAX_WINDOW_MINUTES:
        raise ValueError('Window is longer than a day')
    spans, cur = [], None
    for minute in range(a, b + 1, STEP_MINUTES):
        s = _sample(date, minute, timezone, latitude, longitude)
        if s is None:
            continue
        local, sign, moon = s
        sign_m, star_m = int(moon // 30), nakshatra(moon)['name']
        if cur and cur['sign'] == sign:
            cur['to'] = local
            cur['signs'].add(sign_m)
            cur['stars'].add(star_m)
        else:
            cur = {'sign': sign, 'from': local, 'to': local, 'signs': {sign_m}, 'stars': {star_m}}
            spans.append(cur)
    out = []
    for s in spans:
        mins = int((s['to'] - s['from']).total_seconds() // 60) + 1
        mid = s['from'] + (s['to'] - s['from']) / 2
        out.append({'lagna': s['sign'], 'from': s['from'].strftime('%Y-%m-%d %H:%M'),
                    'to': s['to'].strftime('%Y-%m-%d %H:%M'), 'minutes': mins,
                    'stand_in_date': mid.date().isoformat(), 'stand_in_time': mid.strftime('%H:%M'),
                    'cut_by_window': s['from'] == _local(date, a) or s['to'] == _local(date, b),
                    'moon_sign_steady': len(s['signs']) == 1, 'moon_star_steady': len(s['stars']) == 1})
    return {'date': date, 'timezone': timezone, 'window': {'start': start, 'end': end},
            'spans': out,
            'notice': 'Each span is the clock stretch in which that lagna rises at this place. '
                      'The stand-in time is the middle of the span, not a claimed birth time.'}


def lagna_for_known_sign(date, timezone, latitude, longitude, lagna, around=None):
    """Clock spans on the date when the person's known lagna is rising; nearest first if `around` is given."""
    if lagna not in SIGNS:
        raise ValueError('Unknown lagna sign')
    res = lagna_spans(date, timezone, latitude, longitude)
    spans = [s for s in res['spans'] if s['lagna'] == lagna]
    if around:
        m = _hhmm(around, 'Time')
        def dist(s):
            lo = int(s['from'][11:13]) * 60 + int(s['from'][14:16])
            hi = int(s['to'][11:13]) * 60 + int(s['to'][14:16])
            return 0 if lo <= m <= hi else min(abs(m - lo), abs(m - hi))
        spans.sort(key=dist)
    return {**res, 'spans': spans, 'lagna': lagna}
