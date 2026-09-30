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
