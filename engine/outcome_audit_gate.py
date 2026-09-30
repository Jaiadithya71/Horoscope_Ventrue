"""Do not score caption-only hindsight as a verified pre-event prediction."""
REQUIRED=('original_audio_verified','publication_before_result_verified','candidate_identity_verified','result_read_live')


def audit_gate(record):
 missing=[k for k in REQUIRED if record.get(k) is not True]
 return {'id':record['id'],'missing_verification':missing,
   'eligible_for_reviewed_single_case_scoring':not missing,
   'scored_predictive_outcome':None,
   'notice':'Eligibility is a source-review gate, not an automatic correctness score. Never infer model/private-reading accuracy from a selected external public prediction case.'}
