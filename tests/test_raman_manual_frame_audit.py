import unittest
from fractions import Fraction as F
from decimal import Decimal as D
from engine.raman_manual_frame_audit import raman_manual_frame_audit

class ManualFrameTests(unittest.TestCase):
 def test_exact_traversals_and_independent_helper_agreement(self):
  audit=raman_manual_frame_audit()
  for row in audit['rows']:
   value=F(row['exact_traversal_arcseconds_rational'])
   helper=abs(D(row['interpolation_helper_candidate']['signed_traversal_degrees']))*3600
   self.assertLess(abs(helper-D(value.numerator)/D(value.denominator)),D('1e-20'))
  moon=audit['rows'][1]
  self.assertEqual(F(moon['exact_minus_printed_traversal_arcseconds_rational']),F(189,32))
  self.assertEqual(moon['row_subtraction_minus_printed_nirayana_arcseconds'],7200)
  self.assertEqual(moon['common_subtraction_minus_printed_nirayana_arcseconds'],3600)
 def test_ayanamsa_and_unknowns_are_not_selected(self):
  a=raman_manual_frame_audit();self.assertIsNone(a['selected_true_positions']);self.assertIsNone(a['selected_ayanamsa'])
  for row in a['rows']:
   if row['planet']!='Moon':self.assertIn(row['row_subtraction_minus_printed_nirayana_arcseconds'],(0,None))
  self.assertIsNone(a['rows'][6]['readable_printed_nirayana_dms'])
 def test_node_two_distinct_anchors_and_ketu_opposition(self):
  a=raman_manual_frame_audit();node=a['rahu_anchor_audit']
  self.assertEqual(F(node['may1_label_propagated_birth_sayana_arcseconds_rational'])-F(node['worked_anchor_birth_sayana_arcseconds_rational']),-180)
  self.assertIsNone(node['selected_anchor']);self.assertEqual(a['ketu_printed_frame_check']['opposition_to_printed_rahu_arcseconds'],648000)
