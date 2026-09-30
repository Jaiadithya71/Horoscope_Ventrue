import unittest
from engine.strength_profile_inventory import strength_profile_inventory

class InventoryTests(unittest.TestCase):
 def test_inventory_does_not_certify_total(self):
  r=strength_profile_inventory()
  self.assertFalse(r['input_dependent_full_total_available']);self.assertIsNone(r['selected_profile'])
  self.assertEqual(next(x for x in r['components'] if x['component']=='natural')['remaining_gates'],[])
  self.assertTrue(next(x for x in r['components'] if x['component']=='motion_excluding_ayana')['remaining_gates'])
  self.assertTrue(all(x['input_dependent_complete_status'] is None for x in r['components']))
