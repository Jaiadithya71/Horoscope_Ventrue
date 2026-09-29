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
    return {'longitude': round(lon, 5), 'sign': SIGNS[int(lon // 30)],
            'retrograde': speed < 0}


def sign_index(sign):
    try: return SIGNS.index(sign.title())
    except ValueError: raise ValueError(f'Unknown sign: {sign}. Choose {", ".join(SIGNS)}')


def moon_sign(birth_date, birth_time, birth_tz):
    """Birth data must include real IANA timezone; no guessed birth hour."""
    from zoneinfo import ZoneInfo
    local = dt.datetime.fromisoformat(f'{birth_date}T{birth_time}').replace(tzinfo=ZoneInfo(birth_tz))
    return position(local.astimezone(dt.timezone.utc), 'Moon')['sign']


def forecast(date, moon_rashi, planet_names=None):
    utc = dt.datetime.fromisoformat(date).replace(tzinfo=dt.timezone.utc)
    moon = sign_index(moon_rashi)
    names = planet_names or list(PLANETS)
    placements = {}
    for name in names:
        p = position(utc, name)
        placements[name] = {**p, 'house_from_moon': (sign_index(p['sign'])-moon)%12+1}
    rules = json.loads((ROOT/'rules.json').read_text())
    findings = [{**rule, 'trigger': {'planet': rule['planet'], **placements[rule['planet']]}}
                for rule in rules if rule['planet'] in placements and placements[rule['planet']]['house_from_moon']==rule['house_from_moon']]
    return {'as_of_utc': utc.isoformat(), 'natal_moon_sign': SIGNS[moon],
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
    a=p.parse_args()
    if a.birth_date and not (a.birth_time and a.birth_tz):p.error('--birth-date requires --birth-time and --birth-tz')
    sign=a.moon_sign or moon_sign(a.birth_date,a.birth_time,a.birth_tz)
    print(json.dumps(forecast(a.date,sign),indent=2))

if __name__=='__main__': main()
