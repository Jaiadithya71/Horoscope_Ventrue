"""Jha4 printed Sun daily interpolation arithmetic, not reconstructed ephemeris."""
from fractions import Fraction as F
from .bphs_jha_general_aspect import SOURCE_URL


def jha_daily_interpolation_audit():
 elapsed=F(1)+F(32,60)+F(3,3600)
 daily=F(59,60);arc=elapsed*daily;printed_arc=F(1)+F(30,60)+F(31,3600)
 anchor=F(11*30+22)+F(28,60)+F(31,3600)
 printed_final=F(11*30+20)+F(58,60)
 return {'profile':'jha_sudha4_printed_sun_daily_interpolation_audit',
  'printed_elapsed_days_ghatikas_palas':[1,32,3],'elapsed_days_rational':str(elapsed),
  'elapsed_hours_rational':str(elapsed*24),'printed_daily_sun_degrees_rational':str(daily),
  'exact_traversal_arcseconds_rational':str(arc*3600),
  'printed_traversal_arcseconds_rational':str(printed_arc*3600),
  'exact_minus_printed_traversal_arcseconds_rational':str((arc-printed_arc)*3600),
  'printed_anchor_degrees_rational':str(anchor),'exact_interpolated_degrees_rational':str(anchor-arc),
  'printed_final_degrees_rational':str(printed_final),
  'exact_minus_printed_final_arcseconds_rational':str((anchor-arc-printed_final)*3600),
  'printed_arc_subtraction_matches_printed_final':anchor-printed_arc==printed_final,
  'printed_clock_label_conflict':{'narrative_earlier_weekday_index':3,'parenthesized_earlier_weekday_index':4,
   'printed_later_weekday_index':5,'selected_clock_labels':None},
  'mean_true_speed_boundary':{'worked_speed_labeled':'true daily speed',
   'commentary_prefers':'mean speed for proportional interpolation',
   'moon_daily_speed_shortcut_endorsed':False,'selected_physical_speed_profile':None},
  'raman_helper_reused':False,'raman_previous_noon_24hour_domain_match':False,
  'source':{'url':SOURCE_URL,'pdf_pages':[52,53],'printed_pages':[20,21],'chapter':4,
   'slokas':'1-4 plus worked commentary','verified_against_page_image':True},
  'arbitrary_date_ephemeris_verified':False,'selected_historical_longitude':None,
  'notice':'Arithmetic on the printed1day32ghatika3pala interval, not a repaired weekdayclock. Interval36.82hours lies outside Raman preceding-noon24hour helper; that helper is not widened or mislabeled Jha. Printed roundedarc gives printedSunexactly, while exactfractiondiffers0.05arcsecond. Source commentary itself distinguishes meanspeed from workedtrue-speed approximation and uses timefractionMoon instead. No universalprecisionpolicy, historicalpanchanga generation or sourcewinner.'}
