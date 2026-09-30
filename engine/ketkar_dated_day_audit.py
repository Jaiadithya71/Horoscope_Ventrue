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
