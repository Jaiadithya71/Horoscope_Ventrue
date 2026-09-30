"""Reproduce a published software date profile, not evaluate predictions.

Sample PDF pages 3-5 checked as images; date precision only, seven complete
major boundaries. The last Ketu row is truncated and excluded.
"""
import datetime as dt
from fractions import Fraction
from zoneinfo import ZoneInfo
from .solar_dates import SolarCalendar

SOURCE='https://astrology.mathrubhumi.com/downloads/samples-pdf/saturnrep_eng.pdf'
REFERENCE_ENDS=('1997-04-02','2007-04-02','2014-04-02','2032-04-01','2048-04-01','2067-04-02','2084-04-01')
TERMS=(('Sun',None),('Moon',10),('Mars',7),('Rahu',18),('Jupiter',16),('Saturn',19),('Mercury',17))


def run_benchmark():
    # Vendor-published sample fixture, not owner's birth data. No sample name.
    zone=ZoneInfo('Asia/Kolkata')
    birth=dt.datetime(1992,7,5,18,30,tzinfo=zone).astimezone(dt.timezone.utc)
    # Moon 149d27m59s in Uttara Phalguni, whose lower limit is146d40m.
    moon=Fraction(149)+Fraction(27,60)+Fraction(59,3600)
    initial=(Fraction(160)-moon)/Fraction(40,3)*6
    calendar=SolarCalendar(birth)
    offset=initial
    rows=[]
    for (lord,years),expected in zip(TERMS,REFERENCE_ENDS):
        if years is not None:offset+=years
        fixed=birth+dt.timedelta(days=float(offset)*365.25)
        true_return=calendar.at_offset(float(offset))
        fixed_date=fixed.astimezone(zone).date().isoformat()
        return_date=true_return.astimezone(zone).date().isoformat()
        rows.append({'lord':lord,'published_local_end_date':expected,
                     'fixed_365_25_local_end_date':fixed_date,'fixed_profile_match':fixed_date==expected,
                     'solar_return_local_end_date':return_date,'return_profile_match':return_date==expected})
    return {'source_url':SOURCE,'source_pdf_pages':[3,4,5],'verified_against_page_images':True,
            'rows':rows,'fixed_profile_date_matches':sum(x['fixed_profile_match'] for x in rows),
            'return_profile_date_matches':sum(x['return_profile_match'] for x in rows),
            'reference_profile':'Published Moon longitude, longitude birth balance, fixed365.25-day year, Asia/Kolkata date-only endpoints',
            'notice':'Software convention agreement only. Not an exact-time reference, universal book mandate, Balaji agreement, or event-prediction accuracy. Printed truncated Ketu endpoint excluded.'}


def main():
    import json
    print(json.dumps(run_benchmark(),indent=2))


if __name__=='__main__':main()
