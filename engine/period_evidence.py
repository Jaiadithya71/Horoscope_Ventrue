"""Checked period arithmetic and measured lunar traversal, with disagreement visible."""
import datetime as dt
from fractions import Fraction
from .forecast import swe, FLAGS, julian_day
from .natal import PERIODS, STAR_ARC, moon_periods

NESTED_SOURCE={'slug':'phaladeepika-1937','pdf_page':258,'printed_page':221,
               'chapter':'XXI','sloka':2,'verified_against_page_image':True}
BALANCE_SOURCE={'slug':'phaladeepika-1937','pdf_pages':[229,230],'printed_pages':[192,193],
                'chapter':'XIX','sloka':3,'verified_against_page_image':True}


def period_units(lords):
    """Exact rational years/months/days for a path of one to three lords.

    XXI.2 uses 12 months/year and 30 days/month as arithmetic units. These are
    not Gregorian months or proof that a solar year equals 360 civil days.
    """
    if not 1 <= len(lords) <= 3 or any(lord not in dict(PERIODS) for lord in lords):
        raise ValueError('Provide one to three known period lords')
    fraction=Fraction(dict(PERIODS)[lords[0]])
    for lord in lords[1:]:fraction*=Fraction(dict(PERIODS)[lord],120)
    years=fraction.numerator//fraction.denominator
    month_fraction=(fraction-years)*12
    months=month_fraction.numerator//month_fraction.denominator
    day_fraction=(month_fraction-months)*30
    days=day_fraction.numerator//day_fraction.denominator
    remainder=day_fraction-days
    return {'lords':list(lords),'years':years,'months':months,'days':days,
            'remaining_day_fraction':{'numerator':remainder.numerator,'denominator':remainder.denominator},
            'exact_year_fraction':{'numerator':fraction.numerator,'denominator':fraction.denominator},
            'source':NESTED_SOURCE,
            'unit_notice':'12 arithmetic months/year; 30 arithmetic days/month. Not Gregorian months or a fixed 360-civil-day year.'}


def lunar_traversal_evidence(birth):
    """Measure current sector entry/exit; expose, do not resolve balance methods.

    The checked English XIX.3 prints remaining ghatikas * lord years / 60.
    The actual traversal duration differs from 60 ghatikas. Show that literal
    candidate alongside longitude and normalized-time conventions. Only the
    first is the printed formula; normalization is not attributed to this verse.
    """
    if not isinstance(birth,dt.datetime) or birth.tzinfo is None or birth.utcoffset() is None:
        raise ValueError('Birth must be timezone-aware')
    birth=birth.astimezone(dt.timezone.utc)
    def moon(instant):return swe.calc_ut(julian_day(instant),swe.MOON,FLAGS)[0][0]%360
    lon=moon(birth)
    star=int(lon/STAR_ARC)
    def crossing(target):
        def error(instant):return (moon(instant)-target+180)%360-180
        lo,hi=birth-dt.timedelta(days=2),birth+dt.timedelta(days=2)
        if not error(lo)<0<error(hi):raise ArithmeticError('Moon crossing not bracketed')
        while (hi-lo).total_seconds()>0.1:
            mid=lo+(hi-lo)/2
            if error(mid)<0:lo=mid
            else:hi=mid
        return lo+(hi-lo)/2
    entry=crossing(star*STAR_ARC)
    exit=crossing(((star+1)*STAR_ARC)%360)
    total=(exit-entry).total_seconds()
    remaining=(exit-birth).total_seconds()
    initial=moon_periods(lon)
    years=dict(PERIODS)[initial['initial_lord']]
    # 1 ghatika = 24 minutes is explicitly checked separately in Row p.99.
    remaining_ghatikas=remaining/1440
    return {'birth_utc':birth.isoformat(),'birth_moon_longitude':lon,
            'star_index_1_based':star+1,'initial_lord':initial['initial_lord'],
            'sector_entry_utc':entry.isoformat(),'sector_exit_utc':exit.isoformat(),
            'total_traversal_ghatikas':total/1440,'remaining_traversal_ghatikas':remaining_ghatikas,
            'balance_candidates':[
                {'method':'printed_XIX_3_fixed_60_divisor','remaining_years':remaining_ghatikas*years/60,
                 'source':BALANCE_SOURCE,'warning':'Literal checked English formula. May exceed full lord years if actual traversal exceeds 60 ghatikas; not automatically adopted.'},
                {'method':'normalized_actual_traversal_fraction','remaining_years':remaining/total*years,
                 'source':None,'warning':'Explicit diagnostic convention, not the fixed-divisor instruction printed in this edition.'},
                {'method':'equal_sector_longitude_fraction','remaining_years':initial['initial_remaining_solar_years'],
                 'warning':'Existing prototype approximation; does not measure Moon traversal time.'}],
            'ghatika_source':{'slug':'astrological-self-instructor-1893','pdf_page':99,'printed_page':85,
                              'verified_against_page_image':True},
            'numerical_bracket_seconds':0.1,'status':'unresolved_source_convention',
            'notice':'Lahiri/Moshier equal-sector traversal roots, not certain dasha dates. No candidate changes the existing hierarchy or opens outcome gates.'}


def main():
    import argparse
    import json
    from .natal import birth_utc
    parser=argparse.ArgumentParser(description='Book arithmetic and unresolved birth-period balance evidence')
    parser.add_argument('--birth-date',required=True)
    parser.add_argument('--birth-time',required=True)
    parser.add_argument('--birth-tz',required=True)
    args=parser.parse_args()
    print(json.dumps(lunar_traversal_evidence(birth_utc(args.birth_date,args.birth_time,args.birth_tz)),indent=2))


if __name__=='__main__':main()
