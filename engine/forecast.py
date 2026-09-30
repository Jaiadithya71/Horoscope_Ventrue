"""Reproducible research prototype for Moon-sign transit readings. Not an accuracy claim.

Requires pyswisseph, whose Swiss Ephemeris dependency has AGPL/professional licensing.
Do not serve publicly or redistribute this implementation until rights are resolved.
"""
import argparse
import datetime as dt
import json
from pathlib import Path

try:
    import swisseph as swe
except ImportError as exc:
    raise SystemExit('Install pyswisseph in a research environment; review AGPL/professional licensing before public use.') from exc

ROOT = Path(__file__).resolve().parent
PLANETS = {'Sun': swe.SUN, 'Moon': swe.MOON, 'Mercury': swe.MERCURY,
           'Venus': swe.VENUS, 'Mars': swe.MARS, 'Jupiter': swe.JUPITER,
           'Saturn': swe.SATURN, 'Rahu': swe.MEAN_NODE}
SIGNS = ('Aries','Taurus','Gemini','Cancer','Leo','Virgo','Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces')
swe.set_sid_mode(swe.SIDM_LAHIRI)
# Moshier built-in planetary model avoids fetching an untracked ephemeris file.
FLAGS = swe.FLG_MOSEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED


def julian_day(utc):
    return swe.julday(utc.year, utc.month, utc.day,
                      utc.hour + utc.minute/60 + (utc.second + utc.microsecond/1e6)/3600)


def position(utc, planet):
    lon, lat, distance, speed, *_ = swe.calc_ut(julian_day(utc), PLANETS[planet], FLAGS)[0]
    return {'longitude': lon, 'longitude_display_5dp': round(lon,5), 'sign': SIGNS[int(lon // 30)],
            'retrograde': speed < 0}


def sign_index(sign):
    try: return SIGNS.index(sign.title())
    except ValueError: raise ValueError(f'Unknown sign: {sign}. Choose {", ".join(SIGNS)}')


def moon_sign(birth_date, birth_time, birth_tz):
    """Birth data must include real IANA timezone; no guessed birth hour."""
    from .natal import birth_utc
    return position(birth_utc(birth_date,birth_time,birth_tz), 'Moon')['sign']


def forecast(date, moon_rashi, planet_names=None):
    utc = dt.datetime.fromisoformat(date).replace(tzinfo=dt.timezone.utc)
    moon = sign_index(moon_rashi)
    names = planet_names or list(PLANETS)
    placements = {}
    from .transit_phase import transit_phase
    for name in names:
        p = position(utc, name)
        placements[name] = {**p, 'transit_phase_evidence':transit_phase(name,p['longitude']), 'house_from_moon': (sign_index(p['sign'])-moon)%12+1}
    rules = json.loads((ROOT/'rules.json').read_text())
    findings = [{**rule, 'trigger': {'planet': rule['planet'], **placements[rule['planet']]}}
                for rule in rules if rule['planet'] in placements and placements[rule['planet']]['house_from_moon']==rule['house_from_moon']]
    from .natal import sign_audience_padas
    from .synthesis import structural_factors
    return {'as_of_utc': utc.isoformat(), 'natal_moon_sign': SIGNS[moon],
            'structural_factors_from_moon': structural_factors(SIGNS[moon],placements),
            'audience_nakshatra_padas': sign_audience_padas(SIGNS[moon]),
            'model': 'Swiss Ephemeris/Moshier + Lahiri sidereal; mean Rahu node; whole-sign Moon houses',
            'placements': placements, 'findings': findings,
            'notice': 'Historical astrological interpretations, not validated prediction or medical/financial advice. Only visually checked page excerpts are enabled.'}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--date', required=True, help='YYYY-MM-DD (UTC midnight sample)')
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument('--moon-sign',help='known Moon rashi, for like-for-like sign-video comparisons')
    g.add_argument('--birth-date',help='YYYY-MM-DD, requires birth time and IANA timezone')
    p.add_argument('--birth-time',help='HH:MM, never defaulted');p.add_argument('--birth-tz',help='IANA timezone')
    p.add_argument('--birth-place', help='birth place label; provide verified latitude and longitude')
    p.add_argument('--birth-lat', type=float); p.add_argument('--birth-lon', type=float)
    a=p.parse_args()
    if a.birth_date and not (a.birth_time and a.birth_tz):p.error('--birth-date requires --birth-time and --birth-tz')
    if a.moon_sign and any(x is not None for x in (a.birth_place,a.birth_lat,a.birth_lon)):
        p.error('birth-place/coordinates require birth-date, birth-time and birth-tz')
    coords=(a.birth_place,a.birth_lat,a.birth_lon)
    if any(x is not None for x in coords) and not all(x is not None for x in coords):
        p.error('birth-place, birth-lat and birth-lon must be supplied together')
    if all(x is not None for x in coords) and not a.birth_date:
        p.error('birth-place/coordinates require birth-date')
    try:
        sign=a.moon_sign or moon_sign(a.birth_date,a.birth_time,a.birth_tz)
        result=forecast(a.date,sign)
        if a.birth_date:
            from .natal import nakshatra, birth_utc
            exact_moon=swe.calc_ut(julian_day(birth_utc(a.birth_date,a.birth_time,a.birth_tz)),swe.MOON,FLAGS)[0][0]
            result['natal_moon_nakshatra']=nakshatra(exact_moon)
        if all(x is not None for x in coords):
            from .natal import natal_chart
            result['natal_chart']=natal_chart(a.birth_date,a.birth_time,a.birth_tz,a.birth_lat,a.birth_lon,a.birth_place)
    except ValueError as exc: p.error(str(exc))
    print(json.dumps(result,indent=2))

if __name__=='__main__': main()
