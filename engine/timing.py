"""Model-relative sidereal ingress and stationary-point search (research only).

Reports UTC roots to one-second tolerance, not a promise of observational or
forecast accuracy. Swiss Ephemeris licensing and Moshier precision limits apply.
"""
import datetime as dt
from .forecast import swe, FLAGS, PLANETS, SIGNS, julian_day

UTC = dt.timezone.utc


def state(utc, planet):
    if utc.tzinfo is None:
        raise ValueError('UTC-aware datetime required')
    if planet not in PLANETS:
        raise ValueError('Unknown planet')
    v = swe.calc_ut(julian_day(utc.astimezone(UTC)), PLANETS[planet], FLAGS)[0]
    return v[0] % 360, v[3]


def _bisect(left, right, changed):
    # A one-second bracket is finer than published forecast windows, and does
    # not imply one-second physical/ayanamsha accuracy.
    for _ in range(50):
        if (right-left).total_seconds() <= 1:
            break
        mid=left+(right-left)/2
        if changed(mid): right=mid
        else: left=mid
    return right


def transitions(start, end, planet, step_hours=12):
    """Scan a bounded UTC interval; find sign crossings and speed reversals.

    The half-open [start,end) window prevents duplicate events in adjoining
    searches. Step at most 12h; slower planets may be searched efficiently,
    but more than one unobserved crossing inside a step is not certified.
    """
    if start.tzinfo is None or end.tzinfo is None or start >= end:
        raise ValueError('Provide increasing timezone-aware start/end')
    if not 0 < step_hours <= 12:
        raise ValueError('step_hours must be in (0,12]')
    start, end=start.astimezone(UTC),end.astimezone(UTC)
    if (end-start).days > 366:
        raise ValueError('Search spans at most 366 days')
    events=[]
    left=start
    prev_lon,prev_speed=state(left,planet)
    while left < end:
        right=min(end,left+dt.timedelta(hours=step_hours))
        lon,speed=state(right,planet)
        a,b=int(prev_lon//30),int(lon//30)
        if a!=b:
            root=_bisect(left,right,lambda t:int(state(t,planet)[0]//30)!=a)
            if root < end:
                before=state(root-dt.timedelta(seconds=2),planet)[0]
                after=state(root+dt.timedelta(seconds=2),planet)[0]
                events.append({'kind':'sign_ingress','planet':planet,'at_utc':root.isoformat(),
                               'from_sign':SIGNS[int(before//30)],'to_sign':SIGNS[int(after//30)],
                               'motion':'retrograde' if state(root,planet)[1]<0 else 'direct'})
        # Exact zero at a sample is itself a station; avoid duplicate when the
        # next segment shares this sample as its left boundary.
        if (prev_speed < 0 <= speed) or (prev_speed > 0 >= speed):
            positive=prev_speed>0
            root=_bisect(left,right,lambda t:(state(t,planet)[1] <= 0) if positive else (state(t,planet)[1] >= 0))
            if root < end:
                events.append({'kind':'station','planet':planet,'at_utc':root.isoformat(),
                               'to_motion':'retrograde' if positive else 'direct',
                               'longitude':round(state(root,planet)[0],5)})
        left,prev_lon,prev_speed=right,lon,speed
    return {'planet':planet,'start_utc':start.isoformat(),'end_utc':end.isoformat(),
            'method':'Swiss Ephemeris/Moshier Lahiri sidereal sign boundaries and longitude-speed zeros; at most 12h sample, root bracket <=1s',
            'events':sorted(events,key=lambda e:e['at_utc'])}


def main():
    import argparse, json
    p=argparse.ArgumentParser(description='Research sidereal ingress and station UTC times')
    p.add_argument('--planet',required=True,choices=list(PLANETS))
    p.add_argument('--start',required=True,help='ISO UTC date/time, e.g. 2026-01-01T00:00:00+00:00')
    p.add_argument('--end',required=True,help='exclusive ISO UTC end')
    a=p.parse_args()
    try: print(json.dumps(transitions(dt.datetime.fromisoformat(a.start),dt.datetime.fromisoformat(a.end),a.planet),indent=2))
    except ValueError as exc: p.error(str(exc))

if __name__=='__main__': main()
