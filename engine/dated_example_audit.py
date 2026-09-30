"""Consistency check of a secondary worked date example, not adopted convention."""
import datetime as dt
from fractions import Fraction

SOURCE='https://saravali.github.io/astrology/dasa_balance.html'


def secondary_example_audit():
    u=dt.timezone.utc
    birth=dt.datetime(1935,7,6,5,38,16,tzinfo=u)
    entry=dt.datetime(1935,7,5,14,52,14,tzinfo=u)
    exit=dt.datetime(1935,7,6,17,54,4,tzinfo=u)
    time_elapsed=Fraction(int((birth-entry).total_seconds()),int((exit-entry).total_seconds()))
    longitude_elapsed=Fraction(437,800) # 140deg37min minus133deg20min over800minutes
    published={'time':dt.datetime(1944,8,1,8,49,8,tzinfo=u),
               'longitude':dt.datetime(1944,8,1,4,52,15,tzinfo=u)}
    rows=[]
    for method,elapsed in (('time',time_elapsed),('longitude',longitude_elapsed)):
        remaining=20*(1-elapsed)
        end=birth+dt.timedelta(days=float(remaining)*365.25)
        rows.append({'method':method,'elapsed_fraction':float(elapsed),'remaining_years':float(remaining),
                     'published_end_utc':published[method].isoformat(),
                     'computed_fixed_365_25_end_utc':end.isoformat(),
                     'published_minus_computed_hours':(published[method]-end).total_seconds()/3600,
                     'implied_fixed_days_per_year':(published[method]-birth).total_seconds()/86400/float(remaining)})
    return {'source_url':SOURCE,'rows':rows,'source_type':'secondary software explanatory page',
            'same_monotone_calendar_order_conflict':time_elapsed>longitude_elapsed and published['time']>published['longitude'],
            'adopted_calendar_profile':None,
            'notice':'Source elapsed-time arithmetic verified, but published endpoints have reversed order relative to remaining fractions and do not share a fixed year. Not an exact dasha oracle or new book convention. Historical person birth data is only a published numerical fixture; no event claim evaluated.'}
