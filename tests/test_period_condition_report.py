import unittest
from engine.period_condition_report import period_condition_report
from engine.natal import natal_chart

class PeriodReportTests(unittest.TestCase):
 def test_integrated_scopes_do_not_vote_or_pick_calendar(self):
  n=natal_chart('2000-01-01','14:30','Asia/Kolkata',13.08,80.27,'synthetic fixture')
  x=period_condition_report(n['ascendant']['sign'],n['placements'],'Jupiter','Mercury')
  self.assertTrue(x['period_school_conflict']['unresolved_school_conflict'])
  for k in ('personal_outcome','global_precedence','selected_strength_total','selected_calendar'):self.assertIsNone(x[k])
  self.assertEqual(len(x['unfavorable_house_candidates']['candidates']),2)
  self.assertEqual(len(x['vargottama_qualification_candidates']),2)
  for r in x['vargottama_qualification_candidates']:self.assertIsNone(r['selected_result'])
  for r in n['placements'].values():self.assertNotIn('overpowered_sun_rays',r)
 def test_missing_nodes_and_no_conditionless_conclusion(self):
  x=period_condition_report('Aries',{},'Rahu','Ketu')
  self.assertFalse(x['period_school_conflict']['scope_match'])
  self.assertEqual(x['lordship_emphasis']['dual_owner_evidence'],[])
  for r in x['vargottama_qualification_candidates']:
   self.assertIsNone(r['base_qualification']);self.assertEqual(r['commentary_conditioned_candidates'],[])
  self.assertIsNone(x['personal_outcome'])
