"""Solar returns and explicitly convention-dependent dasha calendar estimates.

XIX.4 defines a year by a solar return. It does not uniquely fix a fractional
Gregorian mapping. Actual integer returns are solved; fractions interpolate
elapsed UTC time between adjacent returns. This is not an exact dasha claim.
"""
import datetime as dt
import math
from .forecast import swe, FLAGS, julian_day
from .natal import dasha_at_solar_offset

SOURCE = {'slug':'phaladeepika-1937','pdf_page':230,'printed_page':193,
          'chapter':'XIX','sloka':4,'verified_against_page_image':True}
UTC = dt.timezone.utc


class SolarCalendar:
    """Birth-anchored Lahiri solar returns, numerical bracket at most 0.1s.

    Offsets are limited to +/- 150 years to bound work. Returned datetimes are
    UTC. Model tolerance is not an astronomical accuracy guarantee.
    """
    def __init__(self, birth):
        if not isinstance(birth, dt.datetime) or birth.tzinfo is None or birth.utcoffset() is None:
            raise ValueError('Birth must be a timezone-aware datetime')
        self.birth = birth.astimezone(UTC)
        self.target = self._sun(self.birth)
        self.returns = {0:self.birth}

    @staticmethod
    def _sun(instant):
        return swe.calc_ut(julian_day(instant), swe.SUN, FLAGS)[0][0] % 360

    def _error(self, instant):
        return (self._sun(instant)-self.target+180)%360-180

    def annual_return(self, year):
        if isinstance(year, bool) or not isinstance(year, int) or not -150 <= year <= 150:
            raise ValueError('Return index must be an integer from -150 to 150')
        if year in self.returns:
            return self.returns[year]
        # Mean year only locates a wide bracket, never supplies the answer.
        guess = self.birth+dt.timedelta(days=365.25636*year)
        lo, hi = guess-dt.timedelta(days=4), guess+dt.timedelta(days=4)
        if not self._error(lo) < 0 < self._error(hi):
            raise ArithmeticError('Solar return not bracketed in the requested model')
        while (hi-lo).total_seconds() > 0.1:
            middle = lo+(hi-lo)/2
            if self._error(middle) < 0:
                lo = middle
            else:
                hi = middle
        self.returns[year] = lo+(hi-lo)/2
        return self.returns[year]

    def at_offset(self, offset):
        if not math.isfinite(offset) or not -150 <= offset <= 150:
            raise ValueError('Solar offset must be finite and within +/-150 years')
        lower = math.floor(offset)
        start = self.annual_return(lower)
        fraction = offset-lower
        if fraction == 0:
            return start
        end = self.annual_return(lower+1)
        return start+(end-start)*fraction

    def offset_at(self, instant):
        if not isinstance(instant, dt.datetime) or instant.tzinfo is None or instant.utcoffset() is None:
            raise ValueError('Query instant must be timezone-aware')
        instant = instant.astimezone(UTC)
        rough = (instant-self.birth).total_seconds()/86400/365.25636
        year = math.floor(rough)
        if not -149 <= year <= 149:
            raise ValueError('Query instant outside supported solar calendar horizon')
        start, end = self.annual_return(year), self.annual_return(year+1)
        if instant < start:
            year -= 1
            start, end = self.annual_return(year), start
        elif instant >= end:
            year += 1
            start, end = end, self.annual_return(year+1)
        # Datetime has microsecond resolution; remove sub-microsecond inverse noise.
        return round(year+(instant-start).total_seconds()/(end-start).total_seconds(),12)


def dated_hierarchy(birth, moon_longitude, instant):
    """Nested lord intervals with UTC estimates under a named convention."""
    calendar = SolarCalendar(birth)
    offset = calendar.offset_at(instant)
    hierarchy = dasha_at_solar_offset(moon_longitude, offset)
    for row in hierarchy['hierarchy']:
        for key, target in (
            ('full_start_solar_years_after_birth','full_start_utc_estimate'),
            ('visible_start_solar_years_after_birth','visible_start_utc_estimate'),
            ('end_solar_years_after_birth','end_utc_estimate')):
            row[target] = calendar.at_offset(row[key]).isoformat()
    hierarchy['query_utc'] = instant.astimezone(UTC).isoformat()
    hierarchy['calendar_source'] = SOURCE
    hierarchy['calendar_convention'] = 'Lahiri/Moshier integer solar returns; fractional years linearly interpolate elapsed UTC time between adjacent returns'
    hierarchy['date_limit'] = 'Calendar estimates under an explicit interpolation convention, not uniquely book-defined exact dasha dates. Birth balance still uses equal-sector longitude approximation, not measured stellar traversal time.'
    hierarchy['solar_return_tolerance_seconds'] = 0.1
    return hierarchy


def main():
    import argparse
    import json
    from .natal import birth_utc
    parser=argparse.ArgumentParser(description='Solar-return-based dasha calendar estimates, not exact predicted event dates')
    parser.add_argument('--birth-date',required=True)
    parser.add_argument('--birth-time',required=True)
    parser.add_argument('--birth-tz',required=True)
    parser.add_argument('--at',required=True,help='Timezone-aware ISO query instant')
    args=parser.parse_args()
    birth=birth_utc(args.birth_date,args.birth_time,args.birth_tz)
    moon=swe.calc_ut(julian_day(birth),swe.MOON,FLAGS)[0][0]%360
    try:
        result=dated_hierarchy(birth,moon,dt.datetime.fromisoformat(args.at))
    except ValueError as exc:
        parser.error(str(exc))
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
