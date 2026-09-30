"""Jha28 worked phase and Ayana arithmetic, no universal multiplier selection."""
from fractions import Fraction as F
from .bphs_jha_general_aspect import SOURCE_URL,dms


def jha_luminary_component_audit():
 sun=dms(2,5,25,15);moon=dms(9,25,37,45)
 phase=(moon-sun)%360;folded=min(phase,360-phase);benefic=folded/3;malefic=60-benefic
 printed_benefic=dms(0,43,15,50);printed_malefic=dms(0,16,44,10)
 # Source Sun starts2;28;32;10 but next operand prints28;12;10.
 residual_initial=dms(0,28,32,10);residual_next=dms(0,28,12,10)
 printed_product=dms(0,342,26,0);printed_quotient=dms(0,11,14,40)
 printed_accumulation=dms(0,89,14,40);printed_ayana=dms(0,59,34,53)
 exact_initial=(90+78+residual_initial*F(12,30))/3
 return {'profile':'jha_sudha28_worked_phase_ayana_source_audit',
  'paksha_worked':{'sun_degrees_rational':str(sun),'moon_degrees_rational':str(moon),
   'directed_phase_rational':str(phase),'exact_benefic_virupa_rational':str(benefic),
   'exact_malefic_virupa_rational':str(malefic),
   'printed_benefic_virupa_rational':str(printed_benefic),'printed_malefic_virupa_rational':str(printed_malefic),
   'exact_minus_printed_benefic_seconds_rational':str((benefic-printed_benefic)*3600),
   'exact_minus_printed_malefic_seconds_rational':str((malefic-printed_malefic)*3600),
   'printed_benefic_planets':['Moon','Mercury','Venus','Jupiter'],
   'moon_and_mercury_worked_classification':'Printed fixed-benefic workedgroup despite waningphase',
   'worked_moon_multiplier':1,'universal_moon_multiplier_verified':False},
  'ayana_worked':{'printed_initial_sayana_degrees_rational':str(dms(2,28,32,10)),
   'printed_next_residual_degrees_rational':str(residual_next),
   'printed_residual_change_arcseconds':int((residual_next-residual_initial)*3600),
   'next_operand_times12_minus_printed_product_arcseconds_rational':str((residual_next*12-printed_product)*3600),
   'printed_product_div30_minus_printed_quotient_arcseconds_rational':str((printed_product/30-printed_quotient)*3600),
   'printed_quotient_plus78_minus_printed_accumulation_arcseconds_rational':str((78+printed_quotient-printed_accumulation)*3600),
   'printed_accumulation_plus90_div3_minus_printed_ayana_arcseconds_rational':str(((90+printed_accumulation)/3-printed_ayana)*3600),
   'exact_initial_operand_ayana_virupa_rational':str(exact_initial),
   'printed_ayana_virupa_rational':str(printed_ayana),'worked_sun_multiplier':1,
   'universal_sun_multiplier_verified':False},
  'source':{'url':SOURCE_URL,'pdf_pages':[188,189],'printed_pages':[156,157],'chapter':28,'slokas':'10-11,15-18',
   'verified_against_page_image':True},
  'selected_strength_profile':None,'selected_multiplier_policy':None,'full_strength':None,
  'notice':'Named printed workedprofile and exact arithmetic only. Checked passages do not print the Santhanam commentary dark-half/association/doubling choices; absence here is not proof of universal exclusion. Jha Ayana explicitly uses residualthree-khanda, not the23.45degreedeclination shortcut. Multiple printedSun intermediate errors remain, no repairedvalue or mixedwholechart selected.'}
