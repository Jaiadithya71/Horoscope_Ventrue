"""Interval-valued Sripati-method Shadbala for a modern chart (working profile).

Every component whose source reading, school or modern input is unresolved is
carried as a [min, max] interval; nothing is silently selected. A planet is
called strong or weak against the Sripati III minima only when the verdict
holds at both ends of the summed interval. Otherwise it is 'unresolved'.
This is source arithmetic on modern inputs, not forecast accuracy.
Source: Sripatipaddhati (Sastri), Adhyaya III, pixel-checked pages PDF 38-80.
"""
import datetime as dt
import math
from zoneinfo import ZoneInfo
from .forecast import swe, julian_day
from .continuous_strength import (continuous_components, naisargikabala,
                                  pakshabala_candidates, source)
from .positional_candidates import positional_candidates
from .degree_aspects import CLASSICAL
from .signed_aspect_strength import signed_aspect_adjustment
from .temporal_lords import (WEEK_LORDS, HORA_CYCLE, tribhaga, kala_hora,
                             positional_hora_candidates)
from .solar_meridian_clock import solar_meridian_clock, PROFILE as MERIDIAN
from .solar_intervals import solar_interval_evidence, PROFILE as SOLAR

PROFILE = 'sripati_iii_interval_working_profile_modern_inputs_v1'
# Sripati III p66 (pixel-checked): minimum Shadbala in virupas.
MINIMUM_VIRUPA = {'Sun': 390, 'Moon': 360, 'Mars': 300, 'Mercury': 420,
                  'Jupiter': 390, 'Venus': 330, 'Saturn': 300}
SWE = {'Sun': swe.SUN, 'Moon': swe.MOON, 'Mercury': swe.MERCURY, 'Venus': swe.VENUS,
       'Mars': swe.MARS, 'Jupiter': swe.JUPITER, 'Saturn': swe.SATURN}
# Modern mean heliocentric longitudes, deg and deg/century from J2000 (JPL
# approximate-elements set). A modern stand-in for the traditional mean planet.
MEAN_HELIO = {'Mercury': (252.25032350, 149472.67411175), 'Venus': (181.97909950, 58517.81538729),
              'Mars': (-4.55343205, 19140.30268499), 'Jupiter': (34.39644051, 3034.74612775),
              'Saturn': (49.95424423, 1222.49362201)}
MEAN_EARTH = (100.46457166, 35999.37306329)
MAX_DECLINATION = 24.0  # Sripati III.15-16 fixed maximum


def _wrap180(x):
    return (x + 180) % 360 - 180


def _iv(values):
    values = [v for v in values if v is not None]
    return (min(values), max(values))


def _add(*ivs):
    return (sum(i[0] for i in ivs), sum(i[1] for i in ivs))


def _mean_longitudes(jd, ayanamsa):
    t = (jd - 2451545.0) / 36525
    sun_mean = (MEAN_EARTH[0] + MEAN_EARTH[1] * t + 180) % 360
    helio = {p: (a + b * t) % 360 for p, (a, b) in MEAN_HELIO.items()}
    return sun_mean, helio, ayanamsa


def cheshtabala_modern_mean(planet, true_sidereal, sun_mean_trop, helio_trop, ayanamsa):
    """Sripati III.16-18 / Kesava: kendra = sighrochcha - (mean+true)/2, folded, /180."""
    if planet in ('Mercury', 'Venus'):
        sighra, mean = helio_trop[planet], sun_mean_trop
    else:
        sighra, mean = sun_mean_trop, helio_trop[planet]
    sighra = (sighra - ayanamsa) % 360
    mean = (mean - ayanamsa) % 360
    d = _wrap180(true_sidereal - mean)
    kendra = (sighra - mean - d / 2) % 360
    folded = min(kendra, 360 - kendra)
    return {'cheshtakendra_degrees': kendra, 'rupa': folded / 180}


def _sunrise_before(jd, lat, lon):
    cursor = jd - 1.6
    last = None
    for _ in range(6):
        res, t = swe.rise_trans(cursor, swe.SUN, swe.CALC_RISE | swe.BIT_DISC_CENTER | swe.BIT_NO_REFRACTION,
                                (lon, lat, 0), 0, 0, swe.FLG_MOSEPH)
        if res != 0 or t[0] > jd + 1:
            break
        if t[0] <= jd:
            last = t[0]
        cursor = t[0] + 1e-4
    nxt = None
    res, t = swe.rise_trans(jd, swe.SUN, swe.CALC_RISE | swe.BIT_DISC_CENTER | swe.BIT_NO_REFRACTION,
                            (lon, lat, 0), 0, 0, swe.FLG_MOSEPH)
    if res == 0:
        nxt = t[0]
    return last, nxt


def _declination(planet, jd):
    return swe.calc_ut(jd, SWE[planet], swe.FLG_MOSEPH | swe.FLG_EQUATORIAL)[0][1]


def _ayana_rupa(planet, dec):
    sign = -1 if planet in ('Moon', 'Saturn') else 1
    if planet == 'Mercury':
        return (MAX_DECLINATION + abs(dec)) / 48
    return (MAX_DECLINATION + sign * dec) / 48


def shadbala_working_profile(chart, *, timezone):
    utc = dt.datetime.fromisoformat(chart['birth_utc'])
    lat, lon = chart['latitude'], chart['longitude']
    jd = julian_day(utc)
    pl = chart['placements']
    centres = chart['sripati_degree_geometry'].get('centres')
    if centres is None:
        raise ValueError('Degree bhava centres unavailable for this chart; no substitute geometry')
    cont = continuous_components(pl, centres)['planets']
    pos = {r['planet']: r for r in positional_candidates(pl)['planets']}
    ayanamsa = swe.get_ayanamsa_ex_ut(jd, swe.FLG_MOSEPH)[1]
    sun_mean, helio, _ = _mean_longitudes(jd, ayanamsa)

    # Natonnata (two meridian clock bridges) and day/night thirds.
    mer = solar_meridian_clock(utc, lat, lon, meridian_profile=MERIDIAN)
    clocks = [c for c in mer.get('candidates', []) if c.get('status') == 'explicit_model_clock']
    third = solar_interval_evidence(utc, lat, lon, solar_event_profile=SOLAR)
    third_rupa = (third.get('tribhaga_evidence') or {}).get('rupa_by_planet')
    # Weekday lord (sunrise-origin) and hora lords.
    sunrise, next_sunrise = _sunrise_before(jd, lat, lon)
    hora_lords, weekday_lord = [], None
    if sunrise is not None:
        local_date = (dt.datetime(2000, 1, 1, 12, tzinfo=dt.timezone.utc)
                      + dt.timedelta(days=sunrise - 2451545.0)).astimezone(ZoneInfo(timezone)).date()
        weekday_lord = WEEK_LORDS[(local_date.weekday() + 1) % 7]
        hours = (jd - sunrise) * 24
        hora_lords.append(HORA_CYCLE[(HORA_CYCLE.index(weekday_lord) + int(hours)) % 7])
        if next_sunrise is not None and next_sunrise > sunrise:
            frac = (jd - sunrise) / (next_sunrise - sunrise)
            if 0 <= frac < 1:
                lord = kala_hora(weekday_lord, frac)['lord']
                if lord:
                    hora_lords.append(lord)
        hora_lords += list(positional_hora_candidates(
            weekday_lord, chart['ascendant']['longitude'], pl['Sun']['longitude'])['candidates'].values())

    # Aspect classification variants (Moon benefic always per Sripati commentary).
    base_class = {'Sun': 'malefic', 'Mars': 'malefic', 'Saturn': 'malefic',
                  'Moon': 'benefic', 'Jupiter': 'benefic', 'Venus': 'benefic'}
    class_variants = [{**base_class, 'Mercury': 'benefic'}, {**base_class, 'Mercury': 'malefic'}]

    rows, notes = {}, []
    for p in CLASSICAL:
        lon_p = pl[p]['longitude']
        sthana = _iv([c['base_five_piece_sum_rupa'] for c in pos[p]['independent_profile_matrix']])
        dig = (cont[p]['digbala']['rupa'],) * 2
        nat = _iv([natonnata for natonnata in
                   [(1.0 if p == 'Mercury' else None)] +
                   [c['components'][p]['rupa'] for c in clocks if p in c.get('components', {})]
                   if natonnata is not None]) if clocks else (0.0, 1.0)
        paksha_c = [x['rupa'] for x in pakshabala_candidates(p, pl['Sun']['longitude'], pl['Moon']['longitude'])['candidates']]
        paksha = _iv(paksha_c)
        trib = (third_rupa[p],) * 2 if third_rupa and third_rupa.get(p) is not None else (0.0, 1.0)
        dina = (0.75 if weekday_lord == p else 0.0,) * 2 if weekday_lord else (0.0, 0.75)
        hora = _iv([1.0 if h == p else 0.0 for h in hora_lords]) if hora_lords else (0.0, 1.0)
        year_month = (0.0, 0.75)  # year/month lords need the unresolved historical epoch count
        kala = _add(nat, paksha, trib, dina, hora, year_month)
        dec = _declination(p, jd)
        ay = _ayana_rupa(p, dec)
        ayana = (ay, 2 * ay) if p == 'Sun' else (ay, ay)
        if p == 'Sun':
            cheshta = ayana  # worked table gives Sun's Cheshta as its Ayana value
        elif p == 'Moon':
            cheshta = (paksha[0], 2 * paksha[1])  # worked table: Paksha value; text mentions doubling
        else:
            cheshta = (cheshtabala_modern_mean(p, lon_p, sun_mean, helio, ayanamsa)['rupa'],) * 2
        naisarg = (naisargikabala(p)['rupa'],) * 2
        adjs = []
        for cv in class_variants:
            a = signed_aspect_adjustment(p, lon_p, pl, cv, classification_profile='sripati_commentary_variants')
            adjs.append(a['signed_adjustment_rupa'])
        aspect = _iv(adjs)
        total = _add(sthana, dig, kala, ayana, cheshta, naisarg, aspect)
        # Sripati's worked table counts Ayana inside Cheshta for Sun/Moon rows and separately otherwise:
        # keep the printed expanded layout (Ayana + Cheshta both added), as in III p61.
        minimum = MINIMUM_VIRUPA[p] / 60
        war = [q for q in ('Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn')
               if q != p and p in ('Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn')
               and abs(_wrap180(pl[q]['longitude'] - lon_p)) < 1.0]
        if war:
            verdict = 'unresolved_planetary_war'
        elif total[0] >= minimum:
            verdict = 'meets_sripati_minimum_in_all_variants'
        elif total[1] < minimum:
            verdict = 'below_sripati_minimum_in_all_variants'
        else:
            verdict = 'unresolved_across_variants'
        rows[p] = {'components_rupa_interval': {
            'sthana': sthana, 'dig': dig, 'kala': kala, 'ayana': ayana, 'cheshta': cheshta,
            'naisargika': naisarg, 'drishti_quarter_aspect': aspect},
            'total_rupa_interval': total, 'minimum_rupa': minimum, 'verdict': verdict,
            'war_with': war}
    return {'profile': PROFILE, 'planets': rows, 'weekday_lord': weekday_lord, 'hora_lord_candidates': hora_lords,
            'source': source('III whole chapter', 38, 24),
            'open_inputs': ['historical year and month lords (bounded 0..0.75)',
                            'Kendra rasi vs bhava, relation profile (4 positional variants)',
                            'Pakshabala folded vs literal complement', 'Natonnata two meridian-clock bridges',
                            'Sun Ayana doubled vs worked-table undoubled; Moon multiplier',
                            'Mercury benefic vs malefic for aspect sign',
                            'modern mean heliocentric elements stand in for the traditional mean planet',
                            'Yuddha (planetary war) adjustment not applied; flagged only'],
            'notice': 'Interval arithmetic on a named profile. Not a predictor of outcomes; verdicts only where every variant agrees.'}
