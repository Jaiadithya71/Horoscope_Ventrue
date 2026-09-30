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


class AngularSolarCalendar(SolarCalendar):
    """Explicit modern true-sidereal angular-time alternative.

    Uses Sun's angular progress, not elapsed UTC interpolation. Developer
    documentation supports this kind of calendar, not identical settings,
    a byte-for-byte software replica, or a uniquely mandated book map.
    """
    def at_offset(self,offset):
        if not math.isfinite(offset) or not -150<=offset<=150:
            raise ValueError('Solar offset must be finite and within +/-150 years')
        lower=math.floor(offset);fraction=offset-lower
        start=self.annual_return(lower)
        if fraction==0:return start
        end=self.annual_return(lower+1)
        wanted=360*fraction
        lo,hi=start,end
        while (hi-lo).total_seconds()>0.1:
            mid=lo+(hi-lo)/2
            progress=(self._sun(mid)-self.target)%360
            if progress<wanted:lo=mid
            else:hi=mid
        return lo+(hi-lo)/2

    def offset_at(self,instant):
        if not isinstance(instant,dt.datetime) or instant.tzinfo is None or instant.utcoffset() is None:
            raise ValueError('Query instant must be timezone-aware')
        instant=instant.astimezone(UTC)
        # Shared return roots establish revolution count, not fractional time.
        rough=super().offset_at(instant)
        lower=math.floor(rough)
        start=self.annual_return(lower)
        if abs((instant-start).total_seconds())<0.1:return float(lower)
        progress=(self._sun(instant)-self.target)%360
        return lower+progress/360


class Fixed36525Calendar:
    """Published vendor comparison profile, not a solar-return calculation."""
    def __init__(self,birth):
        if not isinstance(birth,dt.datetime) or birth.tzinfo is None or birth.utcoffset() is None:
            raise ValueError('Birth must be timezone-aware')
        self.birth=birth.astimezone(UTC)

    def at_offset(self,offset):
        if not math.isfinite(offset) or not -150<=offset<=150:
            raise ValueError('Offset must be finite and within +/-150 years')
        return self.birth+dt.timedelta(days=offset*365.25)

    def offset_at(self,instant):
        if not isinstance(instant,dt.datetime) or instant.tzinfo is None or instant.utcoffset() is None:
            raise ValueError('Query instant must be timezone-aware')
        value=(instant.astimezone(UTC)-self.birth).total_seconds()/(365.25*86400)
        if not -150<=value<=150:raise ValueError('Query outside supported calendar horizon')
        return round(value,12)


def dated_hierarchy(birth, moon_longitude, instant, *, balance_method=None, calendar_profile='elapsed_utc_return_interpolation'):
    """Nested lord intervals with UTC estimates under a named convention."""
    calendars={'elapsed_utc_return_interpolation':SolarCalendar,'sidereal_solar_angular_progress':AngularSolarCalendar,'fixed_365_25_day_software_comparison':Fixed36525Calendar}
    if calendar_profile not in calendars:raise ValueError('Unknown calendar profile')
    calendar = calendars[calendar_profile](birth)
    offset = calendar.offset_at(instant)
    balance=None
    evidence=None
    if balance_method is not None:
        from .period_evidence import lunar_traversal_evidence
        evidence=lunar_traversal_evidence(birth)
        if abs((evidence['birth_moon_longitude']-moon_longitude+180)%360-180)>0.000001:
            raise ValueError('Supplied Moon longitude disagrees with birth model')
        candidates={x['method']:x for x in evidence['balance_candidates']}
        if balance_method not in candidates:
            raise ValueError('Unknown birth balance method')
        balance=candidates[balance_method]['remaining_years']
    hierarchy = dasha_at_solar_offset(moon_longitude, offset,initial_remaining_years=balance)
    hierarchy['birth_balance_method']=balance_method or 'equal_sector_longitude_fraction'
    if evidence is not None:
        hierarchy['birth_balance_evidence']=evidence
    for row in hierarchy['hierarchy']:
        for key, target in (
            ('full_start_solar_years_after_birth','full_start_utc_estimate'),
            ('visible_start_solar_years_after_birth','visible_start_utc_estimate'),
            ('end_solar_years_after_birth','end_utc_estimate')):
            row[target] = calendar.at_offset(row[key]).isoformat()
    hierarchy['query_utc'] = instant.astimezone(UTC).isoformat()
    hierarchy['calendar_source'] = SOURCE if calendar_profile!='fixed_365_25_day_software_comparison' else {'source_url':'https://astrology.mathrubhumi.com/downloads/samples-pdf/saturnrep_eng.pdf','pdf_pages':[3,4,5],'verified_against_page_images':True,'scope':'Published vendor software365.25-day convention, not XIX.4 true solar-return mandate'}
    hierarchy['calendar_profile']=calendar_profile
    hierarchy['calendar_convention'] = 'Lahiri/Moshier integer solar returns; fractional years linearly interpolate elapsed UTC time between adjacent returns' if calendar_profile=='elapsed_utc_return_interpolation' else 'Lahiri/Moshier true sidereal solar angular progress; fractional years solve360*fraction degrees after each natal return'
    if calendar_profile=='fixed_365_25_day_software_comparison':
        hierarchy['calendar_convention']='Fixed365.25-day years, source-labeled vendor software comparison; no true solar-return root'
    hierarchy['modern_angular_profile_sources']=['https://www.vedicastrologer.org/jh/features.htm','https://www.vedicastrologer.org/jh/update_7.65.htm'] if calendar_profile=='sidereal_solar_angular_progress' else []
    hierarchy['date_limit'] = 'Calendar estimates under an explicitly named calendar convention, not uniquely book-defined exact dasha dates. Birth balance is chosen explicitly from separately sourced methods; disagreements remain exposed.'
    hierarchy['solar_return_tolerance_seconds'] = None if calendar_profile=='fixed_365_25_day_software_comparison' else 0.1
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
    parser.add_argument('--calendar-profile',choices=('elapsed_utc_return_interpolation','sidereal_solar_angular_progress','fixed_365_25_day_software_comparison'),default='elapsed_utc_return_interpolation')
    parser.add_argument('--balance-method',choices=('equal_sector_longitude_fraction','normalized_actual_traversal_fraction','printed_XIX_3_fixed_60_divisor'),default=None)
    args=parser.parse_args()
    birth=birth_utc(args.birth_date,args.birth_time,args.birth_tz)
    moon=swe.calc_ut(julian_day(birth),swe.MOON,FLAGS)[0][0]%360
    try:
        result=dated_hierarchy(birth,moon,dt.datetime.fromisoformat(args.at),balance_method=args.balance_method,calendar_profile=args.calendar_profile)
    except ValueError as exc:
        parser.error(str(exc))
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
