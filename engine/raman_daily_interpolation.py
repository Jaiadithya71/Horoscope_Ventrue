"""Manual art100 supplied daily-arc interpolation, not an ephemeris generator."""
from decimal import Decimal as D
from .raman_manual_geometry_audit import SOURCE_URL


def raman_daily_interpolation(previous_noon_tropical_degrees,daily_arc_magnitude_degrees,elapsed_hours,ayanamsa_degrees,*,motion_direction,ephemeris_profile,clock_profile,frame_profile):
    if motion_direction not in ('direct','retrograde'):raise ValueError('Explicit direct or retrograde direction required')
    if not all(isinstance(s,str) and s.strip() for s in (ephemeris_profile,clock_profile,frame_profile)):raise ValueError('Named source, clock and frame profiles required')
    values=[]
    for x in (previous_noon_tropical_degrees,daily_arc_magnitude_degrees,elapsed_hours,ayanamsa_degrees):
        if isinstance(x,bool):raise ValueError('Finite numeric inputs required')
        y=D(str(x))
        if not y.is_finite():raise ValueError('Finite numeric inputs required')
        values.append(y)
    before,arc,hours,aya=values
    if not 0<=before<360 or not 0<=arc<360 or not 0<=hours<=24 or not 0<=aya<360:raise ValueError('Input outside supplied longitude/day domain')
    traversed=arc*hours/24;delta=traversed if motion_direction=='direct' else -traversed
    tropical=before+delta;nirayana=tropical-aya
    return {'supplied_previous_noon_tropical_degrees':str(before),'supplied_daily_arc_magnitude_degrees':str(arc),
        'supplied_elapsed_hours':str(hours),'supplied_ayanamsa_degrees':str(aya),'motion_direction':motion_direction,
        'signed_traversal_degrees':str(delta),'interpolated_tropical_unwrapped_degrees':str(tropical),
        'interpolated_nirayana_unwrapped_degrees':str(nirayana),'interpolated_nirayana_normalized_degrees':str((nirayana%360+360)%360),
        'ephemeris_profile':ephemeris_profile,'clock_profile':clock_profile,'frame_profile':frame_profile,
        'source':{'url':SOURCE_URL,'pdf_pages':[120,121,122],'printed_pages':[80,81,82],'article':'100','verified_against_page_image':True},
        'selected_historical_true_longitude':None,'arbitrary_date_ephemeris_verified':False,
        'notice':'Linear supplied signed daily-arc candidate. Caller grounds the preceding-noon anchor, daily arc/direction and frame; endpoints do not infer station crossings or a shortest path. No log-table rounding fit, modern ayanamsa identity or universal mean/true averaging branch. Unwrapped output is local to the supplied noon anchor, not physical revolution recovery.'}
