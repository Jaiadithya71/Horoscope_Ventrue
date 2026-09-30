"""Jha46.14 normalized traversal and printed solar-target arithmetic audit."""
from fractions import Fraction as F
from .bphs_jha_general_aspect import SOURCE_URL


def decompose(years):
 y=int(years);q=(years-y)*12;m=int(q);q=(q-m)*30;d=int(q)
 q=(q-d)*60;g=int(q);q=(q-g)*60;p=int(q)
 return {'years':y,'months':m,'days':d,'ghatikas':g,'palas':p,'remaining_pala_fraction_rational':str(q-p)}


def encode(row):
 y,m,d,g,p=row
 return F(y)+F(m,12)+F(d,360)+F(g,21600)+F(p,1296000)


def jha_dasha_balance_audit():
 elapsed_pal=25*60+34;total_pal=56*60+40;expired=F(elapsed_pal*10,total_pal);remaining=10-expired
 printed_expired=(4,6,4,14,7);printed_remaining=(5,5,25,45,53)
 birth=F(4*30+25)+F(45,60)+F(55,3600)
 target=(birth+remaining*360)%360
 printed_target=F(10*30+21)+F(31,60)+F(48,3600)
 target_using_printed_balance=(birth+encode(printed_remaining)*360)%360
 return {'profile':'jha_sudha46_14_normalized_actual_traversal_worked_audit',
  'elapsed_traversal_pal':elapsed_pal,'total_traversal_pal':total_pal,'lord':'Moon','lord_years':10,
  'exact_expired_years_rational':str(expired),'exact_remaining_years_rational':str(remaining),
  'exact_expired_decomposition':decompose(expired),'exact_remaining_decomposition':decompose(remaining),
  'printed_expired_units':list(printed_expired),'printed_remaining_units':list(printed_remaining),
  'printed_expired_plus_remaining_years_rational':str(encode(printed_expired)+encode(printed_remaining)),
  'remaining_fixed60_diagnostic_years_rational':str(F((total_pal-elapsed_pal)*10,3600)),
  'solar_target_check':{'printed_birth_sun_degrees_rational':str(birth),
   'exact_balance_times360_added_target_degrees_rational':str(target),
   'printed_balance_times360_added_target_degrees_rational':str(target_using_printed_balance),
   'printed_later_sun_degrees_rational':str(printed_target),
   'exact_target_minus_printed_arcseconds_rational':str((target-printed_target)*3600),
   'printed_balance_target_minus_printed_arcseconds_rational':str((target_using_printed_balance-printed_target)*3600),
   'reading':'Named360degree-per-year solar-target arithmetic hypothesis; table alone does not establish exact fractional-year civil mapping'},
  'source':{'url':SOURCE_URL,'pdf_page':310,'printed_page':278,'chapter':46,'sloka':14,'verified_against_page_image':True},
  'selected_calendar_profile':None,'exact_civil_endpoint':None,'app_contract_changed':False,
  'notice':'Independent normalized elapsed/total traversal evidence. Printed subpala truncation/complement preserved, not universal roundingpolicy. Samvat/Sun table lacks complete civil timestamps and model; solar-target arithmetic is not proof of elapsed-return versus angular-progress calendar winner. Fixed60 diagnostic is a different sourceprofile and not silently substituted.'}
