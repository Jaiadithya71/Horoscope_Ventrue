"""Exploratory same-library tropical Sun check, not historical timing validation."""
from datetime import datetime, timedelta, timezone
import swisseph as swe
from .ketkar_longitude_frame_audit import longitude_frame_audit
from .forecast import julian_day

SOURCE_URL='https://www.astro.com/swisseph/swephprg.htm'


def solar_window_check():
    start=datetime(1928,4,5,tzinfo=timezone.utc)
    flags=swe.FLG_MOSEPH | swe.FLG_SPEED  # Tropical, geocentric apparent of date.
    samples=[]
    for hour in range(0,25,6):
        instant=start+timedelta(hours=hour)
        vector, returned=swe.calc_ut(julian_day(instant),swe.SUN,flags)
        if returned & swe.FLG_SIDEREAL or not returned & swe.FLG_MOSEPH:
            raise ValueError('Unexpected returned frame/ephemeris flags')
        samples.append({'utc':instant.isoformat(),'longitude_degrees':vector[0],
                        'speed_degrees_per_day':vector[3],'returned_flags':returned})
    candidate=float(longitude_frame_audit()['source_sayana_solar_candidate_degrees'])
    low=min(x['longitude_degrees'] for x in samples)
    high=max(x['longitude_degrees'] for x in samples)
    return {'source_url':SOURCE_URL,'book_source':longitude_frame_audit()['source'],
        'comparison_kind':'same_library_exploratory_date_window',
        'library_version':swe.version,'requested_flags':flags,
        'frame':'tropical geocentric apparent ecliptic longitude of date',
        'utc_window':[start.isoformat(),(start+timedelta(days=1)).isoformat()],
        'samples':samples,'sampled_longitude_range_degrees':[low,high],
        'source_sayana_candidate_degrees':candidate,
        'candidate_within_sampled_range':low <= candidate <= high,
        'exact_historical_instant_verified':False,'independent_ephemeris_validation':False,
        'chosen_timestamp':None,'fitted_offset':None,'outcome_accuracy':None,
        'notice':'UTC April5 is an exploratory window, not an established conversion of the source local day. Candidate lies within a daily range but no longitude-fit timestamp is selected. Samples are not a proof about all instants or exact agreement. Swiss/Moshier is already an engine dependency, not a second independent astronomical source. Clock origin, source frame conventions and supplied-input provenance remain unresolved.'}
