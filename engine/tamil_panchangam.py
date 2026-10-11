"""Modern Lahiri Tamil sheet, explicit local-sunset solar-date profile.

Not a Vakya calculator or an observational almanac. Model choices stay visible.
"""
import datetime as dt
import math
from zoneinfo import ZoneInfo
from .forecast import swe, FLAGS, julian_day
from .natal import birth_utc, STARS
UTC = dt.timezone.utc
MONTHS = ('சித்திரை','வைகாசி','ஆனி','ஆடி','ஆவணி','புரட்டாசி','ஐப்பசி','கார்த்திகை','மார்கழி','தை','மாசி','பங்குனி')
STARS_TA = ('அசுவினி','பரணி','கார்த்திகை','ரோகிணி','மிருகசீரிடம்','திருவாதிரை','புனர்பூசம்','பூசம்','ஆயில்யம்','மகம்','பூரம்','உத்திரம்','அஸ்தம்','சித்திரை','சுவாதி','விசாகம்','அனுஷம்','கேட்டை','மூலம்','பூராடம்','உத்திராடம்','திருவோணம்','அவிட்டம்','சதயம்','பூரட்டாதி','உத்திரட்டாதி','ரேவதி')
WEEKDAYS = ('திங்கள்','செவ்வாய்','புதன்','வியாழன்','வெள்ளி','சனி','ஞாயிறு')
YEARS_TA = ('பிரபவ','விபவ','சுக்ல','பிரமோதூத','பிரசோற்பத்தி','ஆங்கீரச','ஸ்ரீமுக','பவ','யுவ','தாது','ஈஸ்வர','வெகுதானிய','பிரமாதி','விக்கிரம','விஷு','சித்திரபானு','சுபானு','தாரண','பார்த்திப','விய','சர்வசித்து','சர்வதாரி','விரோதி','விக்ருதி','கர','நந்தன','விஜய','ஜய','மன்மத','துன்முகி','ஹேவிளம்பி','விளம்பி','விகாரி','சார்வரி','பிலவ','சுபகிருது','சோபகிருது','குரோதி','விசுவாசுவ','பராபவ','பிலவங்க','கீலக','சௌமிய','சாதாரண','விரோதகிருது','பரிதாபி','பிரமாதீச','ஆனந்த','ராட்சச','நள','பிங்கள','காளயுக்தி','சித்தார்த்தி','ரௌத்திரி','துன்மதி','துந்துபி','ருத்ரோத்காரி','ரக்தாட்சி','குரோதன','அட்சய')
SOURCE = 'https://ennkanitham.com/methodology/panchangam/'
SOLAR_PROFILE = 'Swiss Moshier apparent upper limb, standard refraction, sea level, 15 C; no terrain'
EPOCH = dt.datetime(2000,1,1,12,tzinfo=UTC)

def jd_datetime(jd):
    return EPOCH + dt.timedelta(days=jd-2451545.0)

def _event(day,zone,lat,lon,flag):
    # A civil day may be skipped by historical zone changes. Do not invent its sunrise.
    midnight = dt.datetime.combine(day,dt.time(),ZoneInfo(zone))
    if midnight.astimezone(UTC).astimezone(ZoneInfo(zone)).date()!=day:
        return None
    status,t = swe.rise_trans(julian_day(midnight.astimezone(UTC)),swe.SUN,flag,(lon,lat,0),0,15,swe.FLG_MOSEPH)
    if status == -2: return None
    if status != 0: raise ArithmeticError('Solar event not verified')
    value = jd_datetime(t[0]).astimezone(ZoneInfo(zone))
    return value if value.date()==day else None

def _sexagesimal(hours):
    seconds = int(round((hours%24)*3600)) % 86400
    return f'{seconds//3600:02d}:{seconds//60%60:02d}:{seconds%60:02d}'

def _solar_date(day,zone,lat,lon):
    sunset = _event(day,zone,lat,lon,swe.CALC_SET)
    if sunset is None:
        return {'status':'unavailable','reason':'Local sunset unavailable; no Tamil date inferred'}
    endjd = julian_day(sunset.astimezone(UTC))
    solar = swe.calc_ut(endjd,swe.SUN,FLAGS)[0][0]%360
    sign = int(solar//30); target=sign*30
    # The current month begins at its last ingress, assigned before/after local sunset.
    lo,hi=endjd-35,endjd
    for _ in range(55):
        mid=(lo+hi)/2; angle=((swe.calc_ut(mid,swe.SUN,FLAGS)[0][0]-target+180)%360)-180
        if angle >= 0: hi=mid
        else: lo=mid
    ingress=jd_datetime((lo+hi)/2).astimezone(ZoneInfo(zone))
    cutoff=_event(ingress.date(),zone,lat,lon,swe.CALC_SET)
    if cutoff is None:
        return {'status':'unavailable','reason':'Ingress-day sunset unavailable'}
    start=ingress.date()+dt.timedelta(days=1 if ingress>cutoff else 0)
    year_start=day.year-(1 if day.month<4 or (day.month==4 and sign!=0) else 0)
    return {'year_name':YEARS_TA[(year_start-1987)%60], 'cycle_year_start_gregorian':year_start,'status':'computed_profile','month':MONTHS[sign],'month_index_1_based':sign+1,
            'day':(day-start).days+1,'month_start_civil_date':start.isoformat(),
            'ingress_local':ingress.isoformat(),
            'profile':'Lahiri solar ingress, local-sunset cutoff, civil-date day count',
            'source_url':SOURCE,
            'notice':'Local-sunset profile, not guaranteed identical to Chennai-reference or Vakya calendars. Sixty-year names anchored to Prabhava beginning April 1987.'}

def tamil_panchangam(birth,chart):
    utc=birth_utc(birth['date'],birth['time'],birth['timezone'])
    zone=ZoneInfo(birth['timezone']); local=utc.astimezone(zone); day=local.date()
    lat,lon=birth['latitude'],birth['longitude']; jd=julian_day(utc)
    sun=swe.calc_ut(jd,swe.SUN,FLAGS)[0][0]%360;moon=swe.calc_ut(jd,swe.MOON,FLAGS)[0][0]%360
    elong=(moon-sun)%360; tithi=int(elong/12)+1; karana=int(elong/6)+1
    rise=_event(day,birth['timezone'],lat,lon,swe.CALC_RISE)
    sunset=_event(day,birth['timezone'],lat,lon,swe.CALC_SET)
    anchor=rise
    if rise is not None and utc<rise.astimezone(UTC):
        anchor=_event(day-dt.timedelta(days=1),birth['timezone'],lat,lon,swe.CALC_RISE)
    elapsed=None if anchor is None else (utc-anchor.astimezone(UTC)).total_seconds()
    nazhikai=None if elapsed is None or elapsed<0 else elapsed/1440
    star=chart['moon_nakshatra']['index_1_based']
    ayan=swe.get_ayanamsa_ex_ut(jd,swe.FLG_MOSEPH)[1]
    rahu=chart['placements']['Rahu']['longitude'];ketu=(rahu+180)%360
    from .vargas import six_vargas
    def navamsa(lon):
        return next(v['sign'] for v in six_vargas(lon)['vargas'] if v['varga']=='navamsa')
    signs={name:{'rasi':v['sign'],'navamsa':navamsa(v['longitude'])} for name,v in chart['placements'].items()}
    from .forecast import SIGNS
    signs['Ketu']={'rasi':SIGNS[int(ketu//30)],'navamsa':navamsa(ketu)}
    signs['Lagna']={'rasi':chart['ascendant']['sign'],'navamsa':navamsa(chart['ascendant']['longitude'])}
    return {'chart_signs':signs,'profile':'modern_lahiri_tamil_sheet_v1','birth_local':local.isoformat(),
        'timezone':birth['timezone'],'utc_offset_seconds':local.utcoffset().total_seconds(),
        'weekday':WEEKDAYS[local.weekday()],'tamil_solar_date':_solar_date(day,birth['timezone'],lat,lon),
        'sunrise':None if rise is None else rise.isoformat(),'sunset':None if sunset is None else sunset.isoformat(),
        'solar_event_profile':SOLAR_PROFILE,'sunrise_anchor':None if anchor is None else anchor.isoformat(),
        'udayadi_nazhikai':nazhikai,'udayadi_vinadi':None if nazhikai is None else (nazhikai%1)*60,
        'daylight_nazhikai':None if rise is None or sunset is None else (sunset.astimezone(UTC)-rise.astimezone(UTC)).total_seconds()/1440,
        'local_apparent_sidereal_time':_sexagesimal(swe.sidtime(jd)+lon/15),
        'sidereal_clock_notice':'Local apparent sidereal time (nakshatra clock); not planetary hora. Uses signed geographic longitude.',
        'ayanamsa_degrees':ayan,'nakshatra_tamil':STARS_TA[star-1],'pada':chart['moon_nakshatra']['pada'],
        'tithi_index_1_based':tithi,'tithi_in_paksha':(tithi-1)%15+1,
        'paksha':'வளர்பிறை' if tithi<=15 else 'தேய்பிறை',
        'yoga_index_1_based':int(((moon+sun)%360)/(360/27))+1,
        'karana_half_index_1_based':karana,
        'ketu_longitude':ketu,'node_mode':chart.get('node_mode','mean'),
        'source_urls':[SOURCE,'https://www.astro.com/swisseph/swephprg.htm','https://omtamilcalendar.com/tamil_new_year_names/index.html'],
        'notice':'Panchang angles are at the birth instant, not sunrise. Missing polar solar events stay unavailable. Modern arithmetic, not validated life predictions.'}
