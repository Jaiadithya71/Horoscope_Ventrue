import unittest
from engine.validation_report import validation_report

class ValidationReportTests(unittest.TestCase):
 def test_no_metric_laundering_or_readiness_from_printed_sums(self):
  x=validation_report()
  self.assertEqual(x['status'],'research_prototype_not_complete_predictor')
  self.assertIsNone(x['empirical_outcome_accuracy'])
  for k in ('balaji_personal_consultation_replication_verified','unique_calendar_profile_verified',
            'source_selected_natal_strength_total_available','global_outcome_precedence_verified','public_release_rights_cleared'):
   self.assertFalse(x[k])
  self.assertEqual(x['public_transcript_agreement']['counts'],{'chart_match':4,'unsupported':3})
  c=x['calendar_convention_agreement']
  self.assertEqual((c['fixed_profile_date_matches'],c['return_profile_date_matches'],c['angular_profile_date_matches']),(7,3,0))
  self.assertFalse(c['exact_reference_times_available'])
  a=x['printed_source_internal_arithmetic']
  self.assertEqual(a['positional']['internal_arithmetic_matches'],7)
  self.assertEqual(a['seven_varga']['decimal_sums_matching'],6)
  self.assertEqual(a['aggregate']['subtotal_matches'],6)
  self.assertEqual(a['aggregate']['aspect_equations_match'],7)
  self.assertNotIn('accuracy_percentage',x)
