"""Named year-only approximation from Manual1935 art49, not modern frame selection."""
from fractions import Fraction as F
from .raman_manual_geometry_audit import SOURCE_URL


def raman_manual_year_precession(year):
    if isinstance(year,bool) or not isinstance(year,int) or year<397:
        raise ValueError('Integer AD year at or after the named397epoch required')
    arc=F((year-397)*151,3)
    degrees=int(arc//3600);remainder=arc-degrees*3600
    minutes=int(remainder//60);seconds=remainder-minutes*60
    return {'year':year,'epoch_ad':397,'annual_rate_arcseconds_rational':'151/3',
        'precession_arcseconds_rational':str(arc),'precession_degrees_rational':str(arc/3600),
        'unwrapped_dms_rational':[str(degrees),str(minutes),str(seconds)],
        'profile':'raman_manual1935_art49_year_only_approximation',
        'source':{'url':SOURCE_URL,'pdf_pages':[62,63],'printed_pages':[22,23],
            'article':'49','verified_against_page_image':True},
        'selected_modern_ayanamsa':None,'odd_day_correction':None,
        'notice':'Source approximation using integer AD year and50⅓seconds/year after397AD. No fit to Moon output, modern ayanamsa identity, epoch proof, subyear convention, universal validity or exact historical ephemeris accuracy. Output is unwrapped; caller supplies any normalization and independently names the frame.'}


def raman_manual_precession_audit():
    rows=[]
    for year,printed in [(1912,76255),(1918,76557),(1932,77261)]:
        candidate=raman_manual_year_precession(year)
        rows.append({'year':year,'candidate':candidate,'printed_arcseconds':printed,
            'exact_minus_printed_arcseconds_rational':str(F(candidate['precession_arcseconds_rational'])-printed),
            'printed_provenance':'art49 example' if year!=1932 else 'art100 non-Moon rows; not a printed art49 example'})
    return {'rows':rows,'illustrated_1932_moon_aya_comparison':{
        'printed_row_dms':[20,27,41],'art49_minus_printed_moon_aya_arcseconds_rational':'10802/3',
        'printed_moon_output_explained':False},
        'illustrated_clock_evidence':{'local_mean_clock':'05:45','east_longitude_degrees':75,
            'greenwich_mean_clock':'00:45','preceding_noon_label':'2nd May1932',
            'elapsed_hours_rational':'51/4','source_url':SOURCE_URL,'pdf_pages':[118,119],
            'printed_pages':[78,79],'articles':[97,98],'verified_against_page_image':True},
        'selected_chart_frame':None,'notice':'Cross-table arithmetic only.1932 annual approximation differs2/3arcsecond from displayed common precession, and1degree2/3arcsecond from Moon row; neither explains printed Moon Nirayana. Clock conversion is the book example, not current timezone rules.'}
