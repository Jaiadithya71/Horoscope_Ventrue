"""Explicit modern meridian transits for supplied Natonnata clock hypotheses."""
import datetime as dt
import math
from .forecast import swe,julian_day
from .continuous_strength import natonnatabala,NEECHA

PROFILE='moshier_modern_solar_meridian_transits_zero_altitude'
UTC=dt.timezone.utc


def solar_meridian_clock(instant,latitude,longitude,*,meridian_profile):
 if meridian_profile!=PROFILE:raise ValueError('Explicit supported meridian profile required')
 if not isinstance(instant,dt.datetime) or instant.tzinfo is None or instant.utcoffset() is None:
  raise ValueError('Timezone-aware instant required')
 if not all(math.isfinite(v) for v in (latitude,longitude)) or not -90<latitude<90 or not -180<=longitude<=180:
  raise ValueError('Finite geographic coordinates required')
 instant=instant.astimezone(UTC);jd=julian_day(instant);events=[]
 for kind,flag in (('noon',swe.CALC_MTRANSIT),('midnight',swe.CALC_ITRANSIT)):
  cursor=jd-2
  for _ in range(5):
   res,t=swe.rise_trans(cursor,swe.SUN,flag,(longitude,latitude,0),0,0,swe.FLG_MOSEPH)
   if res==-2:break
   if res!=0:raise ArithmeticError('Unverified meridian event status')
   root=t[0]
   if root>jd+2:break
   events.append((root,kind));cursor=root+1e-5
 events.sort();past=[e for e in events if e[0]<=jd];future=[e for e in events if e[0]>jd]
 base={'meridian_profile':PROFILE,'geographic_inputs':{'latitude':latitude,'longitude':longitude,'altitude_meters':0},
    'source_url':'https://astrorigin.com/pyswisseph/pydoc/index.html',
    'flag_semantics_source_url':'https://raw.githubusercontent.com/aloistr/swisseph/3186eed405bd2b4ff520c91d0b27bb25e9d75106/swephexp.h',
    'selected_clock_profile':None,'total_strength':None}
 if not past or not future:return {**base,'status':'unavailable','candidates':[],'notice':'No bracketing transits; no civil-clock fallback.'}
 start,kind=past[-1];end,next_kind=future[0]
 if kind==next_kind:raise ArithmeticError('Alternating meridian interval not established')
 epoch=dt.datetime(2000,1,1,12,tzinfo=UTC)
 stamp=lambda v:(epoch+dt.timedelta(days=v-2451545)).isoformat()
 fraction=(jd-start)/(end-start)
 boundary=min(jd-start,end-jd)*86400<=.1
 # Two defensible numerical bridges, not a silently selected solar-clock definition.
 normalized=(0 if kind=='midnight' else 12)+12*fraction
 elapsed=(0 if kind=='midnight' else 12)+(jd-start)*24
 profiles=[('normalized_meridian_half_interval',normalized),('elapsed_hours_since_last_half_anchor',elapsed)]
 candidates=[]
 for name,hour in profiles:
  supported=0<=hour<24
  candidates.append({'clock_profile':name,'hours_after_model_solar_midnight':hour,
     'status':'boundary_unresolved' if boundary else 'outside_clock_domain' if not supported else 'explicit_model_clock',
     'components':None if boundary or not supported else {p:natonnatabala(p,hour) for p in NEECHA}})
 return {**base,'status':'boundary_unresolved' if boundary else 'explicit_meridian_candidates',
   'interval_start_kind':kind,'interval_start_utc':stamp(start),'interval_end_utc':stamp(end),
   'interval_duration_hours':(end-start)*24,'elapsed_fraction':fraction,'boundary_tolerance_seconds':.1,
   'candidates':candidates,
   'notice':'Modern meridian transit hypotheses only, not historic rising tables, exact observational solar time or civil timezone clock. Actual elapsed hours and normalized12hour half interval can differ. No clipping at24, boundary ownership, unique clock, whole temporal total or outcome selected.'}
