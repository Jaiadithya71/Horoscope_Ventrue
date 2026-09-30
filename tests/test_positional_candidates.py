import unittest
from engine.natal import natal_chart
from engine.positional_candidates import positional_candidates

class PositionalCandidateTests(unittest.TestCase):
 def test_integrated_separate_coherent_base_profiles(self):
  n=natal_chart('2000-01-01','14:30','Asia/Kolkata',13.08,80.27,'synthetic fixture')
  x=n['natal_factors']['base_positional_candidates']
  self.assertIsNone(x['selected_positional_total'])
  self.assertEqual(len(x['planets']),7)
  for p in x['planets']:
   self.assertIsNone(p['selected_positional_total'])
   self.assertIsNone(p['full_strength_total'])
   for c in p['candidates']:
    self.assertAlmostEqual(c['base_five_piece_sum_rupa'],sum(c['pieces_rupa'].values()))
    self.assertEqual(c['unresolved_pieces'],[])
    self.assertEqual(len(c['not_included']),2)
  # Same longitudes, absent degree house relations: no Rasi substitution.
  placements={p:dict(v) for p,v in n['placements'].items()}
  for p in placements.values():p.pop('sripati_degree_house',None)
  y=positional_candidates(placements)
  for p in y['planets']:
   a,b=p['candidates']
   self.assertIsNotNone(a['base_five_piece_sum_rupa'])
   self.assertIsNone(b['base_five_piece_sum_rupa'])
   self.assertIn('house_category',b['unresolved_pieces'])

 def test_independent_axes_not_silently_coupled(self):
  n=natal_chart('2000-01-01','14:30','Asia/Kolkata',13.08,80.27,'synthetic fixture')
  x=positional_candidates(n['placements'])
  for row in x['planets']:
   matrix=row['independent_profile_matrix']
   self.assertEqual(len(matrix),4)
   self.assertEqual(len({(c['relation_profile'],c['house_category_profile']) for c in matrix}),4)
   for c in matrix:
    self.assertEqual(c['house_category_school']['sripati_commentator_and_balabhadra'],'sripati_degree_bhava')
    self.assertAlmostEqual(c['base_five_piece_sum_rupa'],sum(c['pieces_rupa'].values()))
   self.assertIsNone(row['selected_positional_total'])
 def test_missing_bhava_axis_blocks_only_dependent_components(self):
  n=natal_chart('2000-01-01','14:30','Asia/Kolkata',13.08,80.27,'synthetic fixture')
  placements={p:{k:v for k,v in row.items() if k!='sripati_degree_house'} for p,row in n['placements'].items()}
  for row in positional_candidates(placements)['planets']:
   m=row['independent_profile_matrix']
   self.assertIsNotNone(m[0]['base_five_piece_sum_rupa'])
   self.assertIsNone(m[1]['base_five_piece_sum_rupa'])
   self.assertIsNone(m[2]['pieces_rupa']['house_category'])
   self.assertIsNotNone(m[2]['pieces_rupa']['seven_varga_direct_owner'])
   self.assertIsNotNone(m[3]['pieces_rupa']['house_category'])
   self.assertIsNone(m[3]['pieces_rupa']['seven_varga_direct_owner'])
