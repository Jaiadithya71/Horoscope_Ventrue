"""Runnable independent JhaSudha source checks, no horoscope or accuracy score."""
import json
from .bphs_jha_aspect_report import bphs_jha_source_validation
from .jha_strength_threshold_audit import jha_strength_threshold_audit
from .jha_dasha_balance_audit import jha_dasha_balance_audit
from .jha_traversal_moon import jha_traversal_moon_audit
from .jha_daily_interpolation_audit import jha_daily_interpolation_audit
from .precedence_inventory import precedence_inventory
from .jha_friendship_audit import jha_friendship_audit


def jha_validation_report():
 return {'status':'source_validation_not_forecast','checks':{
  'directed_geometry_and_supplied_drigbala':bphs_jha_source_validation(),
  'printed_strength_thresholds_and_layout':jha_strength_threshold_audit(),
  'normalized_birth_balance_and_solar_target':jha_dasha_balance_audit(),
  'supplied_timefraction_moon':jha_traversal_moon_audit(),
  'daily_sun_interpolation_clock_and_speed':jha_daily_interpolation_audit(),
  'direct_rasi_compound_friendship':jha_friendship_audit()},
  'local_precedence_scope':[r for r in precedence_inventory()['scope_records'] if r['id']=='same_house_yoga_strength'],
  'critical_source_disagreements':[
   'Saturn270degree adjacent endpoints60/30 and Jupiter270 endpoints0/15 remain unresolved',
   'Printed Saturn20;5;15 times2 product misses20virupa',
   'Total threshold prose/table differs forSun/Mercury/Venus; Hindi component headings reverse motion/temporal',
   'Daily Sun interpolation weekday labels conflict and commentary distinguishes mean from workedtrue speed'],
  'source_profile_boundaries':[
   'Jha chapter27 geometry/28 strength numbering differs from Santhanam26/27',
   'Corroborated quarterplusfullMercury/Jupiter term does not certify mixedbook fullstrength',
   'TimefractionMoon agrees with normalizedbalance by construction, not arbitrary moderntrueMoon',
   'Printed Sun target arithmetic does not establish complete civil endpoints or unique fractional-year mapping'],
  'remaining_execution_gates':[
   'Complete source-consistent natal ephemeris, input clocks/frames and classifications',
   'Ayana containment, threshold selection and complete strength layout',
   'Exact sign boundary convention and printed-source discrepancies without inferred repairs',
   'Same-house contributor roles/totals, tie handling and global outcome precedence',
   'Exact civil-date convention and independent personalized outcome evidence',
   'Source-edition rights and compatible ephemeris license before public release'],
  'selected_natal_total':None,'selected_calendar_profile':None,'global_precedence':None,
  'empirical_outcome_accuracy':None,'balaji_personal_consultation_replication_verified':False,
  'public_release_rights_cleared':False,
  'notice':'Six existing deterministic source checks collected without pooling them into an accuracy/readiness score. Whole validation retains its existing individual keys; this report does not duplicate another nested copy there. Actual page verification and arithmetic regressions do not certify full natal strength, historical ephemeris truth or prediction. Tonight birth-input contract remains unchanged.'}


if __name__=='__main__':print(json.dumps(jha_validation_report(),indent=2))
