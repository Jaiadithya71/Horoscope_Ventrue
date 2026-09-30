"""Bounded historical Sun example chain, not a general-date ephemeris."""
from decimal import Decimal
from .ketkar_dated_day_audit import dated_day_audit,solar_centre_day_audit
from .ketkar_solar_lookup_audit import solar_lookup_audit


def reconstruct_solar_example():
 day=dated_day_audit();centre_days=solar_centre_day_audit();lookup=solar_lookup_audit()
 apsis_base=Decimal('258.831');motion=Decimal('.164');apsis=apsis_base+motion
 true_centre=Decimal(lookup['rounded_true_centre_degrees'])
 longitude=(apsis+true_centre)%Decimal(360)
 return {'source':{'url':day['source']['url'],'pdf_pages':[169,172,173,179,192,193,198,201],
  'verified_against_page_image':True,'apsis_rows':'table7 PDF193/126 and Nyasa3 PDF179/112 rows12-14'},
  'scope':'only supplied historical example 1928-04-05 Ujjain dawn, Saka1850',
  'local_day_chain':day,'centre_day_chain':centre_days,'table11_lookup_candidate':lookup,
  'apsis_base_saka_year':1800,'apsis_base_degrees':str(apsis_base),
  'supplied_50_year_apsis_motion_degrees':str(motion),'computed_apsis_degrees':str(apsis),
  'printed_apsis_degrees':'258.995','apsis_arithmetic_matches':apsis==Decimal('258.995'),
  'candidate_solar_longitude_degrees':str(longitude),'printed_solar_longitude_degrees':'352.167',
  'longitude_matches_at_printed_precision':longitude==Decimal('352.167'),
  'candidate_manda_radius':str(Decimal(1000)+Decimal(lookup['rounded_radius_residual'])),
  'printed_manda_radius':'1000.7',
  'table_inputs_reconstructed_from_year_alone':False,
  'utc_dawn_timestamp':None,'modern_tropical_longitude':None,'selected_natal_strength':None,
  'outcome_accuracy':None,
  'remaining_inputs':['derive tithi/solar/lunar corrections from tables rather than printed mean-day inputs',
   'derive year-motion rows with source rounding rather than supplied50year increments',
   'establish historical zero-longitude/ayanamsa and dawn/epoch convention',
   'verify interpolation/rounding across additional examples before generalizing',
   'independent ephemeris check after frame/time conventions are grounded'],
  'notice':'Composes page-verified printed day, centre-day, actual table11 candidate and apsis addition into a bounded historical fixture. Reproduces352.167 and1000.7 at printed precision, not external astronomical accuracy or a complete arbitrary-date engine. No contemporary ayanamsa or timezone imposed; no prediction claim.'}
