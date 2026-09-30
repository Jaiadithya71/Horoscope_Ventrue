"""Printed tableIV candidate lookup; raw discrepancies never auto-corrected."""
from decimal import Decimal as D
from .raman_motion_source_audit import SOURCE_URL

TABLE={1:['.9856','98.5602','265.6026','146.0265'],2:['1.9712','197.1205','71.2053','272.0531'],3:['2.9568','295.6808','76.8080','48.0796'],4:['3.9524','34.2411','342.4106','184.1062'],5:['4.9280','132.8013','248.0133','320.1327'],6:['5.9136','231.3616','153.6159','96.1593'],7:['6.8992','329.9218','59.2186','232.1868'],8:['7.8848','68.4821','324.8212','8.2124'],9:['8.8704','167.0424','230.4239','144.2389']}


def raman_mean_sun_from_elapsed_days(elapsed_days,*,epoch_clock_profile):
    if not isinstance(epoch_clock_profile,str) or not epoch_clock_profile.strip():raise ValueError('Explicit elapsed-day clock/epoch profile required')
    if isinstance(elapsed_days,bool):raise ValueError('Finite elapsed days required')
    days=D(str(elapsed_days))
    if not days.is_finite() or abs(days)>=100000:raise ValueError('Finite elapsed days below100000 absolute table span required')
    n=int(abs(days));fraction=abs(days)-n;pieces=[]
    for place in (10000,1000,100,10,1):
        digit=n//place%10
        if digit:
            index={1:0,10:0,100:1,1000:2,10000:3}[place]
            value=D(TABLE[digit][index])*(10 if place==10 else 1)
            pieces.append({'day_place':place,'digit':digit,'printed_entry':TABLE[digit][index],'value_degrees':str(value)})
    fractional_motion=fraction*D(TABLE[1][0]);motion=sum((D(p['value_degrees']) for p in pieces),D(0))+fractional_motion
    if days<0:motion=-motion
    candidates=[]
    for profile,constant in [('repeated_prose_and_worked_constant','257.4568'),('tableIV_header_constant','257.4558')]:
        total=D(constant)+motion
        candidates.append({'constant_profile':profile,'epoch_constant':constant,'sum_before_normalization':str(total),'mean_sun_degrees':str((total%360+360)%360)})
    return {'supplied_elapsed_days':str(days),'epoch_clock_profile':epoch_clock_profile,'table_pieces':pieces,
        'fractional_day_motion_degrees':str(fractional_motion),'candidates':candidates,
        'source':{'url':SOURCE_URL,'pdf_pages':[76,77,117,118],'printed_pages':[71,72,112,113],'verified_against_page_image':True},
        'raw_four_day_unit_entry':TABLE[4][0],'four_times_one_day_diagnostic':str(4*D(TABLE[1][0])),
        'selected_mean_sun':None,'modern_date_bridge':None,'historical_ephemeris_verified':False,
        'notice':'Raw printed-table digit lookup candidate. Tens use unit-column times10 as described in adjoining mean-planet exposition; fractions use row1 times fraction. Constants remain separate. Rounded independent columns and incorrect4-day entry are not repaired or smoothed into one daily rate. Supplied elapsed days are not certified birth-time/epoch conversion. Table span is a computational limit, not astronomical validity. No selected mean Sun, true longitude, Sighra triple or natal total.'}


def raman_mean_sun_example_audit():
    x=raman_mean_sun_from_elapsed_days('4602.5',epoch_clock_profile='Printed1912-08-08 noon76E mean-time fixture')
    return {'table_lookup':x,'printed_example_mean_sun':'113.6930',
        'repeated_constant_candidate_matches_example':D(x['candidates'][0]['mean_sun_degrees'])==D('113.6930'),
        '1918_fourteen_hours_fraction':str(D(14)/24),'1918_printed_fraction':'.581',
        '1918_printed_fraction_matches_fourteen_hours':D('.581')==D(14)/24,
        '1918_printed_fractional_solar_motion':'.5656','motion_from_printed_fraction':str(D('.581')*D('.9856')),
        'selected_epoch_conversion':None,
        'notice':'1912 worked example reproduces one table route, not proof of universal epoch/rounding accuracy.1918 clock-fraction and motion discrepancy stays exposed.'}
