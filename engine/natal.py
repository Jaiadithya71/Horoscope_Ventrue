"""Natal coordinates and Vimshottari-style period arithmetic for research, not prediction.

The period boundaries are expressed in solar-year units, not invented UTC dates.
Swiss Ephemeris license gate in engine/README.md applies.
"""
import datetime as dt
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
import json
from pathlib import Path
from .forecast import swe, julian_day, position, FLAGS, SIGNS

STARS = ('Ashwini','Bharani','Krittika','Rohini','Mrigashira','Ardra','Punarvasu','Pushya','Ashlesha',
         'Magha','Purva Phalguni','Uttara Phalguni','Hasta','Chitra','Swati','Vishakha','Anuradha','Jyeshtha',
         'Mula','Purva Ashadha','Uttara Ashadha','Shravana','Dhanishta','Shatabhisha','Purva Bhadrapada',
         'Uttara Bhadrapada','Revati')
STAR_SOURCE = {'slug':'astrological-self-instructor-1893','pdf_pages':[86,88],
               'printed_pages':[72,74], 'verified_against_page_image':True}
PERIODS = (('Sun', 6), ('Moon', 10), ('Mars', 7), ('Rahu', 18),
           ('Jupiter', 16), ('Saturn', 19), ('Mercury', 17), ('Ketu', 7), ('Venus', 20))
STAR_ARC = 360 / 27
PERIOD_SOURCE = {'slug': 'phaladeepika-1937', 'pdf_page': 229,
                 'chapter': 'XIX', 'sloka': '2-3', 'verified_against_page_image': True}


def birth_utc(date, time, timezone):
    """Reject missing, nonexistent and ambiguous local clock times (DST fold)."""
    try:
        zone = ZoneInfo(timezone)
        naive = dt.datetime.fromisoformat(f'{date}T{time}')
        if naive.tzinfo is not None:
            raise ValueError('Use a local clock time without an offset, with separate IANA timezone')
        candidates = [naive.replace(tzinfo=zone, fold=i) for i in (0, 1)]
        valid = [x for x in candidates if x.astimezone(dt.timezone.utc).astimezone(zone).replace(tzinfo=None) == naive]
        if not valid:
            raise ValueError('Birth clock time did not exist in that timezone (DST gap)')
        if len(valid) == 2 and valid[0].utcoffset() != valid[1].utcoffset():
            raise ValueError('Birth clock time is ambiguous in that timezone (DST fold): supply an unambiguous time')
        return valid[0].astimezone(dt.timezone.utc)
    except (ZoneInfoNotFoundError, TypeError) as exc:
        raise ValueError(f'Invalid IANA timezone: {timezone}') from exc


def natal_chart(date, time, timezone, latitude, longitude, place):
    """Coordinates are explicit input, not guessed from a place-name."""
    if not place or not place.strip():
        raise ValueError('Birth place label is required with verified coordinates')
    latitude, longitude = float(latitude), float(longitude)
    if not (-90 < latitude < 90 and -180 <= longitude <= 180):
        raise ValueError('Latitude must be strictly between -90 and 90; longitude between -180 and 180')
    utc = birth_utc(date, time, timezone)
    jd = julian_day(utc)
    # Swiss Ephemeris explicitly requests sidereal houses, with Lahiri set in forecast.py.
    cusps, axes = swe.houses_ex(jd, latitude, longitude, b'W', swe.FLG_SIDEREAL)
    asc = axes[0] % 360
    asc_index = int(asc // 30)
    moon_precise=swe.calc_ut(jd,swe.MOON,FLAGS)[0][0] % 360
    positions = {name: position(utc, name) for name in ('Sun','Moon','Mercury','Venus','Mars','Jupiter','Saturn','Rahu')}
    placements = {name: {**p, 'whole_sign_house_from_ascendant': (int(p['longitude'] // 30) - asc_index) % 12 + 1}
                  for name, p in positions.items()}
    from .synthesis import structural_factors
    return {'birth_utc': utc.isoformat(), 'birth_place': place, 'latitude': latitude,
            'longitude': longitude, 'ascendant': {'longitude': round(asc, 5), 'sign': SIGNS[asc_index]},
            'placements': placements, 'moon_nakshatra': nakshatra(moon_precise),
            'moon_periods': moon_periods(moon_precise),
            'reference_rules': natal_references(placements),
            'structural_factors_from_ascendant': structural_factors(SIGNS[asc_index],placements),
            'model': 'Lahiri sidereal Swiss Ephemeris/Moshier; W house calculation used for ascendant, whole-sign houses reported; mean Rahu',
            'notice': 'Time/location uncertainty can change ascendant and period boundaries. Historical astrology is not validated prediction.'}


def moon_periods(moon_longitude):
    """First 120 solar-year units from birth; birth's initial period is only its remainder."""
    if not 0 <= moon_longitude < 360:
        raise ValueError('Moon longitude must be in [0, 360)')
    star = int(moon_longitude / STAR_ARC)
    initial_index = (star + 7) % 9  # Ashwini=Ketu; Krittika (index 2)=Sun
    fraction_remaining = (star + 1 - moon_longitude / STAR_ARC)
    initial_name, initial_years = PERIODS[initial_index]
    remaining = fraction_remaining * initial_years
    entries = []
    start = 0.0
    for i in range(10):  # first partial period, then nine complete successors
        name, years = PERIODS[(initial_index + i) % 9]
        length = remaining if i == 0 else float(years)
        entries.append({'lord': name, 'start_solar_years_after_birth': round(start, 7),
                        'end_solar_years_after_birth': round(start + length, 7)})
        start += length
    return {'birth_star_index_1_based': star + 1, 'initial_lord': initial_name,
            'initial_remaining_solar_years': round(remaining, 7),
            'periods': entries, 'source': PERIOD_SOURCE,
            'date_limit': 'Offsets only: XIX.4 (PDF p. 230) defines a solar year by the Sun returning to its natal longitude. No calendar dates are asserted here.',
            'method_note': 'Equal 13°20′ stellar sectors and linear fractional balance are computational approximations to XIX.2-3. Verify astronomical convention before precise timing.'}


def subperiods(lord, starting_solar_years=0.0):
    """Nine antardashas, using the explicitly page-checked 120-year proportion."""
    years = dict(PERIODS)
    if lord not in years:
        raise ValueError(f'Unknown period lord: {lord}')
    idx = [name for name, _ in PERIODS].index(lord)
    elapsed = float(starting_solar_years)
    result = []
    for i in range(9):
        name = PERIODS[(idx + i) % 9][0]
        duration = years[lord] * years[name] / 120
        result.append({'lord': name, 'start_solar_years': round(elapsed, 7),
                       'end_solar_years': round(elapsed + duration, 7)})
        elapsed += duration
    return {'parent_lord': lord, 'subperiods': result,
            'source': {'slug': 'astrological-self-instructor-1893', 'pdf_page': 111,
                       'printed_page': 97, 'verified_against_page_image': True},
            'illustration': {'pdf_page': 112, 'printed_page': 98},
            'unit': 'solar-year fraction; no calendar date claim'}


def natal_references(placements):
    """Only reversible house-reference math, not outcome claims."""
    records = json.loads((Path(__file__).parent / 'natal_rules.json').read_text())
    by_id = {record['id']: record for record in records}
    def derived_sign(sign, house):
        return SIGNS[(SIGNS.index(sign) + house - 1) % 12]
    relatives = {}
    for planet, relative in by_id['phaladeepika-15-21-karaka-reference']['mappings'].items():
        if planet in placements:
            relatives[relative] = {'reference_planet': planet, 'reference_sign': placements[planet]['sign'],
                                   'second_sign': derived_sign(placements[planet]['sign'], 2),
                                   'source': by_id['phaladeepika-15-21-karaka-reference']['source']}
    return {'derived_bhava_source': by_id['phaladeepika-15-20-derived-bhava']['source'],
            'relatives': relatives,
            'notice': 'These are reference signs only. No event, health, or lifespan is inferred.'}


def nakshatra(longitude):
    """27 equal sidereal sectors, each quartered into padas; no interpretation."""
    if not 0 <= longitude < 360:
        raise ValueError('Longitude must be in [0,360)')
    # Whole integer quarter avoids rounding a boundary into the previous pada.
    quarter=int(longitude/(360/108))
    star, pada=divmod(quarter,4)
    return {'name':STARS[star], 'index_1_based':star+1,'pada':pada+1,
            'sign':SIGNS[quarter//9], 'source':STAR_SOURCE,
            'convention':'27 equal Lahiri sidereal sectors, 4 equal quarters each'}


def sign_audience_padas(sign):
    """Nine possible Moon-star padas in a rashi; not a person's birth star."""
    idx=SIGNS.index(sign)
    result=[]
    for quarter in range(idx*9,idx*9+9):
        star,pada=divmod(quarter,4)
        result.append({'nakshatra':STARS[star], 'pada':pada+1})
    return {'moon_sign':sign,'possible_nakshatra_padas':result,'source':STAR_SOURCE,
            'notice':'Audience segmentation only; unknown birth data cannot select an individual pada or forecast.'}
