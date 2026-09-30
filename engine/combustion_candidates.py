"""Kapoor II.36 notes thresholds under an explicit modern-longitude hypothesis."""
from .continuous_strength import valid_longitude,folded_distance

THRESHOLDS={'Moon':12,'Mars':17,'Mercury':(14,12),'Jupiter':11,'Venus':(10,8),'Saturn':15}
SOURCE={'title':'Phaladeepika Kapoor reproduction, commentary notes to II.36',
 'chapter':'II','sloka':'36 notes','pdf_pages':[26,27],
 'url':'https://jyotishvidya.com/HTMLobj-9415/Mantreswara_s__Phaladeeplka_.pdf',
 'verified_against_page_image':True,'attribution':'Translator/commentary notes, not numerical orbs in the checked1937 verse'}


def combustion_candidates(planet,longitude,sun_longitude,retrograde=None):
 valid_longitude(longitude);valid_longitude(sun_longitude)
 if retrograde is not None and type(retrograde) is not bool:raise ValueError('Retrograde must be bool or None')
 if planet not in THRESHOLDS:
  if planet not in ('Sun','Rahu','Ketu'):raise ValueError('Known planet required')
  return {'planet':planet,'status':'not_covered','selected_overpowered_sun_rays':None,
          'notice':'No self-combustion or node threshold copied from these notes'}
 sep=folded_distance(longitude,sun_longitude);t=THRESHOLDS[planet]
 profiles=[('direct_or_not_motion_dependent',t)] if isinstance(t,int) else (
  [('direct',t[0]),('retrograde',t[1])] if retrograde is None else [('retrograde' if retrograde else 'direct',t[1 if retrograde else 0])])
 rows=[{'motion_profile':motion,'threshold_degrees':orb,
        'candidate_overpowered_sun_rays':None if sep==orb else sep<orb,
        'exact_threshold_boundary':sep==orb} for motion,orb in profiles]
 vals=[x['candidate_overpowered_sun_rays'] for x in rows]
 return {'planet':planet,'separation_in_ecliptic_longitude_degrees':sep,'supplied_retrograde':retrograde,
    'candidates':rows,'candidate_conflict':len(set(vals))>1,'selected_overpowered_sun_rays':None,
    'source':SOURCE,'status':'commentary_threshold_hypothesis',
    'notice':'Folded apparent geocentric ecliptic-longitude separation interpreted as strictly inside the note\'s distance; this application and exact-boundary abstention are explicit modeling conventions, not a claim of physical visibility, true eclipse, atmospheric conditions or universal combustion. No source-selected flag, strength adjustment or outcome is inferred.'}


def chart_combustion_candidates(placements):
 sun=placements.get('Sun',{}).get('longitude')
 rows={}
 for planet,p in placements.items():
  if sun is None or p.get('longitude') is None:
   rows[planet]={'status':'unresolved_coordinates','selected_overpowered_sun_rays':None}
  else:rows[planet]=combustion_candidates(planet,p['longitude'],sun,p.get('retrograde'))
 return {'planets':rows,'selected_profile':None,
         'notice':'Standalone natal candidate evidence; never sets placement overpowered_sun_rays or resolves source-selected strength and period gates.'}
