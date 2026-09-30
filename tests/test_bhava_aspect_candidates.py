import unittest
from engine.bhava_aspect_candidates import bhava_aspect_adjustment as b
from engine.degree_aspects import CLASSICAL

class BhavaAspectTests(unittest.TestCase):
 def test_extra_is_full_addition_not_quarter_replacement(self):
  ps={p:{'longitude':0} for p in CLASSICAL}
  kinds={p:'benefic' for p in CLASSICAL}
  x=b(1,180,ps,kinds,classification_profile='explicit synthetic classes')
  rs={r['planet']:r for r in x['pairs']}
  self.assertEqual(rs['Jupiter']['combined_aspect_adjustment_rupa'],1.25)
  self.assertEqual(rs['Mercury']['combined_aspect_adjustment_rupa'],1.25)
  self.assertEqual(x['aspect_adjustment_rupa'],3.75)
  kinds['Mercury']='malefic'
  y=b(1,180,ps,kinds,classification_profile='explicit synthetic classes')
  self.assertEqual(next(r for r in y['pairs'] if r['planet']=='Mercury')['combined_aspect_adjustment_rupa'],.75)
  self.assertIsNone(y['total_bhava_strength']);self.assertIsNone(y['personal_outcome'])
 def test_missing_class_or_coordinate_is_not_zero(self):
  ps={p:{'longitude':0} for p in CLASSICAL};kinds={p:'malefic' for p in CLASSICAL}
  del kinds['Moon']
  x=b(12,180,ps,kinds,classification_profile='incomplete synthetic classes')
  self.assertIsNone(x['aspect_adjustment_rupa'])
  self.assertIn({'planet':'Moon','field':'classification'},x['missing_evidence'])
  del ps['Mars']
  y=b(12,180,ps,kinds,classification_profile='incomplete synthetic classes')
  self.assertIn({'planet':'Mars','field':'longitude'},y['missing_evidence'])
  with self.assertRaises(ValueError):b(1,180,ps,kinds,classification_profile='')
