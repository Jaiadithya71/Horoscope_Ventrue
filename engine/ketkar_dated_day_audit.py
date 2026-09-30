"""KetkarIII dated ahargana example; no automatic modern epoch conversion."""
from decimal import Decimal
import datetime


def dated_day_audit():
 mean=Decimal('-7.817');sun=Decimal('.173');moon=Decimal('-.227')
 tithi_end=mean+sun+moon
 weekday_fraction=Decimal('.106')
 ujjain=tithi_end-weekday_fraction
 kashi=ujjain-Decimal('.020')
 return {'source':{'url':'https://archive.org/details/jyotir-ganita-venkatesh-ramakrishna-kethkar-dattatreya-ketkar-surakant-jha',
    'pdf_pages':[168,169,170],'chapter':'III','printed_pages':[101,102,103],
    'verified_against_page_image':True},
  'printed_example':{'saka_year':1850,'lunar_label':'Chaitra bright15 full moon',
    'gregorian_date':'1928-04-05','weekday':'Thursday','location':'Ujjain','time_reference':'dawn'},
  'calculated_gregorian_weekday':datetime.date(1928,4,5).strftime('%A'),
  'supplied_mean_tithi_end_days':str(mean),'solar_correction_days':str(sun),
  'lunar_correction_days':str(moon),'computed_true_tithi_end_days':str(tithi_end),
  'printed_true_tithi_end_days':'-7.871','tithi_end_arithmetic_matches':tithi_end==Decimal('-7.871'),
  'printed_weekday_value':'5.106','weekday_fraction_removed':str(weekday_fraction),
  'computed_ujjain_dawn_days':str(ujjain),'printed_ujjain_dawn_days':'-7.977',
  'ujjain_arithmetic_matches':ujjain==Decimal('-7.977'),
  'supplied_kashi_rekhantara_days':'.020','computed_kashi_dawn_days':str(kashi),
  'printed_kashi_dawn_days':'-7.997','kashi_arithmetic_matches':kashi==Decimal('-7.997'),
  'utc_dawn_timestamp':None,'mean_planet_longitudes':None,'total_strength':None,
  'notice':'Exact arithmetic of printed three-decimal day inputs, not reproduction of preceding tables/epoch. Negative elapsed days are valid before its reference transition. Rekhantara is source-local correction, not a current longitude/timezone inference. No modern dawn model or universal Saka conversion selected. Date/weekday agreement is calendar consistency, not ephemeris or predictive accuracy.'}


if __name__=='__main__':
 import json
 print(json.dumps(dated_day_audit(),indent=2))


def solar_centre_day_audit():
 base=Decimal('100.741');motion=Decimal('365.093')
 ingress=base+motion
 dawn=ingress+Decimal(dated_day_audit()['computed_ujjain_dawn_days'])
 cycle=Decimal('365.260');reduced=dawn%cycle
 supplied_true_centre=Decimal('93.172');supplied_apsis=Decimal('258.995')
 return {'source':{'url':dated_day_audit()['source']['url'],'pdf_pages':[171,172,173,192,198],
  'printed_pages':[104,105,106,125,131],'verified_against_page_image':True},
  'base_centre_days':str(base),'supplied_50_year_motion_days':str(motion),
  'computed_ingress_centre_days':str(ingress),'printed_ingress_centre_days':'465.834',
  'computed_dawn_centre_days':str(dawn),'printed_dawn_centre_days':'457.857',
  'cycle_days':str(cycle),'computed_reduced_centre_days':str(reduced),
  'printed_reduced_centre_days':'92.597',
  'centre_day_chain_matches':(ingress,dawn,reduced)==tuple(map(Decimal,['465.834','457.857','92.597'])),
  'supplied_true_centre_degrees':str(supplied_true_centre),'supplied_apsis_degrees':str(supplied_apsis),
  'computed_solar_longitude_degrees':str((supplied_true_centre+supplied_apsis)%Decimal(360)),
  'printed_solar_longitude_degrees':'352.167',
  'table11_true_centre_lookup_reconstructed':False,'table7_apsis_reconstructed':False,
  'selected_solar_longitude':None,'total_strength':None,
  'notice':'Printed arithmetic bridge only. Source centre-day cycle365.260 is not a selected dasha calendar year. True centre and apsis are supplied printed example values; table11 interpolation and table7 epoch chain remain unverified. No modern ephemeris, exact UTC dawn or selected strength profile inferred.'}
