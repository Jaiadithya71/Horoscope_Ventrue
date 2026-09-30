"""Explicit modern solar-event input profile for historical interval helpers."""
import datetime as dt
import math
from .forecast import swe,julian_day
from .temporal_lords import tribhaga

UTC=dt.timezone.utc
PROFILE='moshier_topocentric_solar_centre_no_refraction_zero_altitude'
SOURCE_URL='https://astrorigin.com/pyswisseph/pydoc/index.html'


def solar_interval_evidence(instant,latitude,longitude,*,solar_event_profile):
    """Sunrise/sunset-bounded interval, not civil clock thirds or full Kala bala.

    Explicit profile has no terrain, refraction, disc-limb or altitude estimate.
    It is not automatically chosen from historic text or owner's place label.
    """
    if solar_event_profile!=PROFILE:raise ValueError('Explicit supported solar-event profile required')
    if not isinstance(instant,dt.datetime) or instant.tzinfo is None or instant.utcoffset() is None:
        raise ValueError('Timezone-aware instant required')
    if not all(math.isfinite(v) for v in (latitude,longitude)) or not -90<latitude<90 or not -180<=longitude<=180:
        raise ValueError('Finite geographic coordinates required')
    instant=instant.astimezone(UTC);jd=julian_day(instant)
    epoch=dt.datetime(2000,1,1,12,tzinfo=UTC)
    events=[]
    for kind,flag in (('rise',swe.CALC_RISE),('set',swe.CALC_SET)):
        cursor=jd-2
        for _ in range(5):
            res,t=swe.rise_trans(cursor,swe.SUN,flag|swe.BIT_DISC_CENTER|swe.BIT_NO_REFRACTION,
                                 (longitude,latitude,0),0,0,swe.FLG_MOSEPH)
            if res==-2:break
            if res!=0:raise ArithmeticError('Unverified solar event status')
            root=t[0]
            if root>jd+2:break
            events.append((root,kind));cursor=root+1e-5
    events.sort()
    past=[e for e in events if e[0]<=jd];future=[e for e in events if e[0]>jd]
    if not past or not future:
        return {'status':'unavailable','solar_event_profile':PROFILE,'geographic_inputs':{'latitude':latitude,'longitude':longitude,'altitude_meters':0},'tribhaga_evidence':None,
                'source_url':SOURCE_URL,'flag_semantics_source_url':'https://github.com/aloistr/swisseph/blob/3186eed405bd2b4ff520c91d0b27bb25e9d75106/swephexp.h','notice':'No bracketing rise/set in bounded search, including polar day/night. No civil-time replacement or invented interval.'}
    start,kind=past[-1];end,next_kind=future[0]
    if kind==next_kind:raise ArithmeticError('Alternating solar interval not established')
    boundary_seconds=min(abs(jd-start),abs(end-jd))*86400
    fraction=(jd-start)/(end-start)
    # Rise/set and fractional-third ownership at model tolerance are held
    # unresolved, not claimed as exact second-level birth categorization.
    near_third=min(abs(fraction-1/3),abs(fraction-2/3))*(end-start)*86400<=.1
    boundary=boundary_seconds<=.1 or near_third
    return {'status':'boundary_unresolved' if boundary else 'explicit_model_interval',
            'solar_event_profile':PROFILE,'geographic_inputs':{'latitude':latitude,'longitude':longitude,'altitude_meters':0},'source_url':SOURCE_URL,'flag_semantics_source_url':'https://github.com/aloistr/swisseph/blob/3186eed405bd2b4ff520c91d0b27bb25e9d75106/swephexp.h',
            'period':'day' if kind=='rise' else 'night',
            'interval_start_utc':(epoch+dt.timedelta(days=start-2451545)).isoformat(),
            'interval_end_utc':(epoch+dt.timedelta(days=end-2451545)).isoformat(),
            'elapsed_fraction':fraction,'boundary_tolerance_seconds':.1,
            'tribhaga_evidence':None if boundary else tribhaga('day' if kind=='rise' else 'night',fraction),
            'total_strength':None,
            'notice':'Chosen modern solar-centre/no-refraction/zero-altitude events supply the historical third helper; not traditional-anchor identity, observational timing accuracy or full temporal strength. No automatic hora/day-origin/year/month or Noon/Midnight profile chosen.'}
