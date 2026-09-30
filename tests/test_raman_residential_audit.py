import unittest
from decimal import Decimal as D
from engine.raman_residential_audit import raman_residential_audit as audit

class ResidentialAuditTests(unittest.TestCase):
 def test_independent_geometry_membership_but_ratio_discrepancy(self):
  x=audit()
  for r in x['rows']:
   self.assertEqual(r['independent_geometry_evidence']['membership']['house'],r['printed_house'])
   self.assertNotEqual(D(r['anchor_route_difference_from_printed_arc_ratio']),D(0))
 def test_printed_errors_not_fitted(self):
  x=audit();rows={r['planet']:r for r in x['rows']}
  self.assertGreater(D(rows['Mars']['absolute_printed_difference']),D('.05'))
  self.assertGreater(D(rows['Moon']['absolute_printed_difference']),D('.02'))
  self.assertEqual(rows['Venus']['printed_arc_dms'],[3,38,26])
  self.assertIsNone(x['total_strength']);self.assertIsNone(x['selected_residential_fraction'])
