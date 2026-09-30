import unittest
from engine.period_relation_context import period_relation_context as context
from engine.period_condition_report import period_condition_report

class PeriodRelationContextTests(unittest.TestCase):
 def test_directional_relation_and_compound_not_selected(self):
  x=context({'Mercury':{'sign':'Cancer'},'Moon':{'sign':'Virgo'}},'Mercury','Moon')
  a,b=x['rows'];self.assertEqual(a['natural_relation_lord_to_owner'],'enemy')
  self.assertEqual(b['natural_relation_lord_to_owner'],'friend')
  self.assertEqual(a['rasi_relative_compound_candidate']['other_house'],3)
  self.assertIsNone(a['selected_friendly_sign']);self.assertIsNone(x['selected_relation_profile'])
 def test_self_owner_missing_owner_and_node_scope(self):
  x=context({'Sun':{'sign':'Leo'}},'Sun','Ketu');a,b=x['rows']
  self.assertEqual(a['status'],'own_sign_not_two_planet_relationship');self.assertIsNone(a['natural_relation_lord_to_owner'])
  self.assertEqual(b['status'],'node_relationship_applicability_unknown')
  x=context({'Jupiter':{'sign':'Gemini'}},'Jupiter','Jupiter')['rows'][0]
  self.assertEqual(x['natural_relation_lord_to_owner'],'enemy');self.assertIsNone(x['rasi_relative_compound_candidate'])
  self.assertIn('occupied_sign_owner_placement',x['missing_inputs'])
 def test_period_route_keeps_disposition_unknown(self):
  x=period_condition_report('Aries',{'Mercury':{'sign':'Cancer'},'Moon':{'sign':'Virgo'}},'Mercury','Moon')
  self.assertIn('occupied_sign_owner_relationship_context',x)
  for row in x['xx14_lord_disposition_candidates']['rows']:
   flags=row['condition_evidence']['supplied_flags'];self.assertIsNone(flags['friendly_sign']);self.assertIsNone(flags['inimical_sign'])
