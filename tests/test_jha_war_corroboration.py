import unittest
from engine.planetary_war import supplied_war_adjustment

class JhaWarCorroborationTests(unittest.TestCase):
 def test_transfer_corroboration_does_not_certify_winner(self):
  x=supplied_war_adjustment('Mars','Mercury',300,280,winner='Mercury',war_condition_confirmed=True,
   complete_prewar_totals=True,adjustment_profile='quoted_parashara_absolute_difference_candidate',total_unit='virupa')
  self.assertEqual(x['transfer_amount'],'20');self.assertEqual(x['candidate_adjusted_totals'],{'Mars':'280','Mercury':'300'})
  c=x['independent_transfer_corroboration'];self.assertEqual(c['sloka'],20)
  self.assertFalse(c['trigger_verified']);self.assertFalse(c['winner_rule_verified'])
  self.assertFalse(c['absolute_difference_interpretation_selected']);self.assertIsNone(x['selected_winner'])
 def test_latitude_divisor_does_not_claim_jha_identity(self):
  x=supplied_war_adjustment('Mars','Mercury',300,280,winner='Mars',war_condition_confirmed=True,
   complete_prewar_totals=True,adjustment_profile='sripati_absolute_difference_per_supplied_latitude_unit_candidate',
   latitude_a=1,latitude_b=0,latitude_unit='degrees',total_unit='virupa')
  self.assertIsNone(x['independent_transfer_corroboration'])
