"""Sripati III.21-23 quarter signed and extra full Mercury/Jupiter aspects."""
from .degree_aspects import CLASSICAL,degree_aspect
from .continuous_strength import valid_longitude,source


def bhava_aspect_adjustment(house,centre_longitude,placements,classifications,*,classification_profile):
 if type(house) is not int or not 1<=house<=12:raise ValueError('House1..12 required')
 if not classification_profile:raise ValueError('Named classification profile required')
 valid_longitude(centre_longitude)
 rows=[];missing=[]
 for planet in CLASSICAL:
  lon=placements.get(planet,{}).get('longitude');kind=classifications.get(planet)
  if kind is not None and kind not in ('benefic','malefic'):raise ValueError('Named benefic/malefic class or missing required')
  if lon is None:
   missing.append({'planet':planet,'field':'longitude'});continue
  a=degree_aspect(planet,lon,centre_longitude)
  quarter=None if kind is None else a['rupa']/4*(1 if kind=='benefic' else -1)
  extra=a['rupa'] if planet in ('Mercury','Jupiter') else 0
  if kind is None:missing.append({'planet':planet,'field':'classification'})
  rows.append({'planet':planet,'unsigned_degree_aspect':a,'supplied_classification':kind,
    'signed_quarter_rupa':quarter,'extra_full_aspect_rupa':extra,
    'combined_aspect_adjustment_rupa':None if quarter is None else quarter+extra})
 return {'house':house,'supplied_centre_longitude':centre_longitude,'classification_profile':classification_profile,
    'pairs':rows,'missing_evidence':missing,
    'aspect_adjustment_rupa':None if missing else sum(r['combined_aspect_adjustment_rupa'] for r in rows),
    'source':source('21-23 commentary',77,63),'quoted_corroboration_source':source('23 quoted Parashara',79,65),
    'total_bhava_strength':None,'personal_outcome':None,
    'notice':'Explicit centre-target degree aspect hypothesis: signed quarter plus extra full Jupiter/Mercury even when supplied class differs. All7classical positions/classes needed for net. Additional quoted occupant terms, complete/cross-sign lord strength and directional category are not combined. No automatic classification, final Bhava total, rank or outcome.'}
