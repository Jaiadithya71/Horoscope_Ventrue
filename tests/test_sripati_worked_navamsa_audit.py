import unittest
from engine.sripati_worked_navamsa_audit import worked_navamsa_audit

class WorkedNavamsaAuditTests(unittest.TestCase):
    def test_earlier_table_is_not_geometry_oracle(self):
        audit=worked_navamsa_audit()
        self.assertEqual(audit['1919_geometry_matches'],6)
        self.assertEqual(audit['later_geometry_matches_for_1919_longitudes'],7)
        failures=[r for r in audit['rows'] if not r['1919_matches_named_geometry']]
        self.assertEqual([r['planet'] for r in failures],['Jupiter'])
        row=failures[0]
        self.assertEqual(row['printed_longitude_dms'],[8,1,25,1])
        self.assertEqual(row['calculated_navamsa']['part_1_based'],1)
        self.assertEqual(row['calculated_navamsa']['owner'],'Mars')
        self.assertFalse(row['calculated_navamsa']['own_owner'])
        self.assertIsNone(audit['selected_seven_varga_total'])

    def test_all_owner_cells_and_missing_handle(self):
        from engine.sripati_worked_navamsa_audit import worked_seven_varga_owner_audit
        x=worked_seven_varga_owner_audit()
        self.assertEqual(len(x['rows']),49)
        self.assertEqual(x['1919_owner_matches'],47)
        self.assertEqual(x['later_comparable_owners'],48)
        self.assertEqual(x['later_owner_matches'],48)
        failed=[(r['planet'],r['varga']) for r in x['rows'] if not r['1919_matches_named_geometry']]
        self.assertEqual(failed,[('Jupiter','navamsa'),('Saturn','dwadasamsa')])
        saturn=next(r for r in x['rows'] if r['planet']=='Saturn' and r['varga']=='dwadasamsa')
        self.assertEqual(saturn['calculated_owner'],'Jupiter')
        self.assertIsNone(saturn['later_matches_named_geometry'])
        self.assertIsNone(x['selected_strength_total'])
