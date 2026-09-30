import unittest
from engine.precedence_inventory import precedence_inventory
from engine.validation_report import validation_report

class PrecedenceInventoryTests(unittest.TestCase):
 def test_local_coverage_not_global_rank(self):
  x=precedence_inventory()
  self.assertEqual(len(x['scope_records']),18)
  self.assertEqual(len({r['id'] for r in x['scope_records']}),18)
  self.assertTrue(all(r['input_dependent_applicability'] is None for r in x['scope_records']))
  self.assertIsNone(x['global_rank']);self.assertIsNone(x['personal_outcome'])
  self.assertIsNone(x['selected_school'])
  self.assertTrue(all(r['source']['pdf_pages'] for r in x['scope_records']))
 def test_validation_still_closed(self):
  x=validation_report()
  self.assertIn('scoped_precedence_inventory',x)
  self.assertFalse(x['global_outcome_precedence_verified'])
  self.assertIsNone(x['empirical_outcome_accuracy'])
