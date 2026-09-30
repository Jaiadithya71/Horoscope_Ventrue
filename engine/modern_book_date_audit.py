"""Independently check PVR Example50 arithmetic, not pick a universal calendar."""
import datetime as dt
from fractions import Fraction
from .solar_dates import SolarCalendar,AngularSolarCalendar

SOURCE='https://vedicastrologer.org/articles/vedic_astro_textbook.pdf'


def audit_example50():
    zone=dt.timezone(dt.timedelta(hours=-4))
    birth=dt.datetime(2000,4,28,5,50,tzinfo=zone)
    remaining_fraction=Fraction(257,800)
    remaining_years=7*remaining_fraction
    savana=birth+dt.timedelta(days=float(remaining_years*360))
    printed_approx=dt.datetime(2002,7,15,19,tzinfo=zone)
    elapsed=SolarCalendar(birth).at_offset(float(remaining_years)).astimezone(zone)
    angular=AngularSolarCalendar(birth).at_offset(float(remaining_years)).astimezone(zone)
    return {'source_url':SOURCE,'source_pdf_pages':[24,222,223,224],
            'verified_against_page_images':True,'published_birth_fixed_offset':birth.isoformat(),
            'balance_fraction':str(remaining_fraction),'remaining_years':str(remaining_years),
            'stated_nakshatra_example_year_profile':'360-day savana; PDF223 explicitly overrides general solar calendar for these examples',
            'computed_360_day_endpoint':savana.isoformat(),
            'published_approximate_endpoint':printed_approx.isoformat(),
            'computed_minus_published_approx_hours':(savana-printed_approx).total_seconds()/3600,
            'solar_elapsed_interpolation_comparison':elapsed.isoformat(),
            'solar_angular_comparison':angular.isoformat(),
            'selected_calendar':None,
            'notice':'Book Example50 balance arithmetic is correct but its stated360-day profile gives July16 rather than printed approximate July15. Rounded Moon input and approximate output are not exact-time truth. General PDF24 angular calendar does not override PDF223 explicit savana convention. No fitted year, Balaji setting, event-accuracy or universal classic interpretation.'}


if __name__=='__main__':
    import json
    print(json.dumps(audit_example50(),indent=2))
