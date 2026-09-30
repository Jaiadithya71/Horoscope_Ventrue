"""Runnable Raman source arithmetic checks, not a horoscope or accuracy score."""
import json
from .raman_motion_source_audit import raman_motion_source_audit
from .raman_mean_sun import raman_mean_sun_example_audit
from .raman_superior_mean import raman_superior_example_audit
from .raman_worked_motion_audit import raman_worked_motion_audit
from .raman_residential_audit import raman_residential_audit
from .raman_manual_geometry_audit import raman_manual_geometry_audit
from .raman_manual_frame_audit import raman_manual_frame_audit
from .raman_manual_precession import raman_manual_precession_audit
from .raman_temporal_audit import raman_temporal_audit
from .raman_strength_composition import raman_printed_composition_audit


def raman_validation_report():
 checks={
  'mean_sun_epoch_constants':raman_mean_sun_example_audit(),
  'motion_source_conditions':raman_motion_source_audit(),
  'superior_raw_tables':raman_superior_example_audit(),
  'rounded_vs_sexagesimal_motion_inputs':raman_worked_motion_audit(),
  'residential_ratios_and_geometry':raman_residential_audit(),
  'manual_geometry_anchors':raman_manual_geometry_audit(),
  'manual_1932_interpolation_and_frames':raman_manual_frame_audit(),
  'manual_year_precession':raman_manual_precession_audit(),
  'temporal_clock_phase_and_row_sums':raman_temporal_audit(),
  'printed_full_component_arithmetic':raman_printed_composition_audit()}
 return {'status':'source_validation_not_forecast','checks':checks,
  'critical_source_disagreements':[
   {'check':'manual_1932_interpolation_and_frames','issue':'Moon printed Nirayana differs by2degrees from its row subtraction and1degree from common ayanamsa; neither selected'},
   {'check':'manual_1932_interpolation_and_frames','issue':'Rahu anchor labeledMay1 but used asMay2; candidates differ3arcminutes'},
   {'check':'manual_geometry_anchors','issue':'Manual anchors differ from later strength example; printed seventh centre also disagrees with construction'},
   {'check':'superior_raw_tables','issue':'Jupiter raw table arithmetic disagrees with worked mean; no print-fit repair'},
   {'check':'temporal_clock_phase_and_row_sums','issue':'MethodA Mars21.68 versus formula/MethodB/final11.68; decimal and exact clocks differ'},
   {'check':'printed_full_component_arithmetic','issue':'Mars changesKala by3virupa; Mercury537.02/60 differs from8.85; SaturnDrik sign unmarked'}],
  'source_profile_boundaries':[
   'Manual illustrated1932 and standard1918 examples are distinct, not one coherent fixture',
   'Raman Ayana is insideKala; Sripati inclusiveCheshta containsAyana. Never add both layouts',
   'Raman partial-base disc-divisor war profile does not resolve Sripati latitude-divisor profile',
   'Raman worked MercuryPapa phase classification is not Sripati phase-specific MercuryBenefic'],
  'remaining_execution_gates':[
   'Grounded ephemeris/clock/frame for supplied mean,true,Sighra inputs and revolution branches',
   'Complete source-consistent positional, temporal, motion and signed-aspect inputs',
   'War trigger, circular-longitude winner, unit and composition profile selection',
   'Subyear precession convention and source discrepancies without inferred repairs',
   'Independent personalized outcome evidence and global precedence rules'],
  'selected_natal_total':None,'selected_chart_frame':None,'selected_war_winner':None,
  'coherent_full_chart_benchmark':False,'empirical_outcome_accuracy':None,
  'balaji_personal_consultation_replication_verified':False,
  'notice':'All checks are accessible in one deterministic report, with original source/page references nested in each check. Findings are not pooled into a percentage. Passing tests establish implementation regressions and source arithmetic only, not historical ephemeris truth, model completeness or forecast accuracy.'}


if __name__=='__main__':print(json.dumps(raman_validation_report(),indent=2))
