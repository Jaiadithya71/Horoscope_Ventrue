"""Explicit local mean-clock bridge to Raman's76E epoch, never civil time."""
from datetime import datetime,timedelta
from decimal import Decimal as D
import math
from .raman_mean_sun import raman_mean_sun_from_elapsed_days
from .raman_motion_source_audit import SOURCE_URL


def raman_local_mean_clock(local_mean_timestamp,longitude,*,clock_kind,clock_profile):
    if clock_kind!='local_mean_solar_time':raise ValueError('Explicit local mean solar time required, not civil/apparent time')
    if not isinstance(clock_profile,str) or not clock_profile.strip():raise ValueError('Named clock provenance required')
    if isinstance(longitude,bool) or not isinstance(longitude,(float,int)) or not math.isfinite(longitude) or not -180<=longitude<=180:raise ValueError('Finite east-positive longitude required')
    local=datetime.fromisoformat(local_mean_timestamp)
    if local.tzinfo is not None:raise ValueError('Local mean-clock label must be naive; do not pass civil offset/UTC')
    correction=D(str(longitude))-76
    seconds=correction*240
    reference=local-timedelta(seconds=float(seconds))
    delta=reference-datetime(1900,1,1)
    total_seconds=D(delta.days)*86400+D(delta.seconds)+D(delta.microseconds)/1000000
    elapsed=total_seconds/86400
    return {'supplied_local_mean_timestamp':local.isoformat(),'longitude_east_positive':longitude,
        'clock_kind':clock_kind,'clock_profile':clock_profile,'reference_meridian_degrees':76,
        'subtract_from_local_seconds':str(seconds),'reference_mean_timestamp':reference.isoformat(),
        'reference_epoch_label':'1900-01-01T00:00:00 at76E local mean clock, not UTC',
        'elapsed_reference_days':str(elapsed),
        'mean_sun_table_candidates':raman_mean_sun_from_elapsed_days(str(elapsed),epoch_clock_profile='Raman76E local mean epoch; '+clock_profile),
        'source':{'url':SOURCE_URL,'pdf_pages':[74,75,76],'printed_pages':[69,70,71],'verified_against_page_image':True},
        'selected_mean_sun':None,'utc_timestamp':None,
        'notice':'Explicit proleptic-Gregorian mean-clock arithmetic with day rollover. Clock-kind label is caller supplied, not certification that civil birth time was converted. No civil timezone, DST, equation-of-time, rounded6minute correction, UTC assertion or repaired1918 interval. Microsecond numerical representation is not source or observational time accuracy. Table lookup domain limit still applies; no selected historical ephemeris or full strength.'}
