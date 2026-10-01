import unittest
from copy import deepcopy
from engine.life_aspect_candidates import life_aspect_candidates, OCCUPATIONS
from engine.forecast import SIGNS
from engine.synthesis import LORDS

def chart(asc=0):
 return {'ascendant':{'longitude':asc,'sign':SIGNS[int(asc//30)]},
  'placements':{p:{'longitude':0,'sign':'Aries'} for p in set(LORDS)}}

class LifeAspectTests(unittest.TestCase):
 def test_three_alternatives_not_ranked_even_when_identical(self):
  r=life_aspect_candidates(chart())
  self.assertEqual([x['reference'] for x in r['career']['candidates']],['Lagna','Moon','Sun'])
  self.assertIsNone(r['career']['selected_reference'])
  self.assertIsNone(r['career']['selected_profession'])
  self.assertEqual({x['navamsa_owner'] for x in r['career']['candidates']},{'Mars'})
  for x in r['career']['candidates']:
   self.assertFalse(x['reference_selected']);self.assertIsNone(x['income_level']);self.assertIsNone(x['timing'])
   self.assertIn('If the',x['conditional_reading'])
 def test_navamsa_bands_and_exact_integer_boundaries(self):
  for degree,owner in [(0,'Mars'),(4,'Venus'),(7,'Mercury'),(10,'Moon'),(14,'Sun'),(17,'Mercury'),(20,'Venus'),(24,'Mars'),(27,'Jupiter')]:
   c=chart();c['placements']['Saturn']={'longitude':degree,'sign':'Aries'}
   row=life_aspect_candidates(c)['career']['candidates'][0]
   self.assertEqual(row['tenth_lord'],'Saturn');self.assertEqual(row['navamsa_owner'],owner)
   self.assertEqual(row['historical_livelihood_examples'],OCCUPATIONS[owner][2])
 def test_sun_and_moon_routes_can_differ(self):
  c=chart();c['placements']['Moon']={'longitude':30,'sign':'Taurus'}
  rows=life_aspect_candidates(c)['career']['candidates']
  self.assertEqual([x['tenth_sign'] for x in rows],['Capricorn','Aquarius','Capricorn'])
 def test_no_input_mutation(self):
  c=chart();before=deepcopy(c);life_aspect_candidates(c);self.assertEqual(c,before)
 def test_invalid_input_not_silently_read(self):
  for lon in [True,float('nan'),-1,360,'10']:
   c=chart();c['placements']['Mars']['longitude']=lon
   with self.assertRaises(ValueError):life_aspect_candidates(c)
  c=chart();c['placements']['Mars']['sign']='Leo'
  with self.assertRaises(ValueError):life_aspect_candidates(c)
 def test_other_topics_not_fabricated(self):
  r=life_aspect_candidates(chart())
  for k in ['marriage','health','timing']:self.assertIsNone(r[k]['reading'])
  self.assertIsNone(r['wealth']['selected_outcome']);self.assertIsNone(r['empirical_accuracy'])
 def test_integrated_birth_entry(self):
  from engine.research_input_report import research_input_report
  r=research_input_report(dict(date='2000-01-01',time='14:30',timezone='Asia/Kolkata',latitude=13.,longitude=80.,place='Synthetic example'))
  self.assertEqual(len(r['life_aspect_candidates']['career']['candidates']),3)
  self.assertIsNone(r['global_outcome']);self.assertIsNone(r['selected_complete_strength'])
  self.assertFalse(r['active_period_inferred'])

 def test_saturn_owner_and_wrap(self):
  c=chart();c['placements']['Saturn']={'longitude':30,'sign':'Taurus'}
  row=life_aspect_candidates(c)['career']['candidates'][0]
  self.assertEqual(row['navamsa_owner'],'Saturn')
  self.assertIn('wood work',row['historical_livelihood_examples'])
  self.assertEqual(life_aspect_candidates(chart(359))['career']['candidates'][0]['tenth_sign'],'Sagittarius')
