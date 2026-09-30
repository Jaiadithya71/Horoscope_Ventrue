"""Reproducible scoped checks, never a single misleading accuracy percentage."""
import json
from .benchmark import score,DATA
from .calendar_benchmark import run_benchmark
from .positional_table_audit import audit_printed_positional_table
from .seven_varga_table_audit import audit_printed_seven_varga_table
from .full_strength_table_audit import audit_printed_full_strength_table


def validation_report():
 transcript=score(json.loads(DATA.read_text()))
 calendar=run_benchmark()
 positional=audit_printed_positional_table()
 varga=audit_printed_seven_varga_table()
 total=audit_printed_full_strength_table()
 return {'status':'research_prototype_not_complete_predictor',
    'public_transcript_agreement':transcript,
    'calendar_convention_agreement':calendar,
    'printed_source_internal_arithmetic':{'positional':positional,'seven_varga':varga,'aggregate':total},
    'empirical_outcome_accuracy':None,
    'balaji_personal_consultation_replication_verified':False,
    'unique_calendar_profile_verified':False,
    'source_selected_natal_strength_total_available':False,
    'global_outcome_precedence_verified':False,
    'public_release_rights_cleared':False,
    'blocking_requirements':['Independently recorded personalized readings/outcomes for an actual predictive benchmark',
       'Resolve calendar/birth-balance convention and exact endpoint reference, not date-only software fit',
       'Source-selected coherent full positional/temporal/motional/aspect/war/combustion model',
       'Verified conditional outcome precedence and timing rules',
       'Compatible Swiss Ephemeris license and source-edition rights review'],
    'notice':'Metrics are different tasks with different denominators. Do not pool source arithmetic, same-library numerical consistency, chart mechanics, date conventions and empirical outcomes into one accuracy percentage. More passing tests do not demonstrate Balaji replication or predictive validity.'}


if __name__=='__main__':print(json.dumps(validation_report(),indent=2))
