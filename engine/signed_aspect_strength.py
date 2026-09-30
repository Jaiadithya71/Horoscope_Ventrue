"""Explicit-classification Sripati III.20 quarter-aspect adjustment only."""
from .degree_aspects import CLASSICAL,degree_aspect
from .continuous_strength import source,valid_longitude


def signed_aspect_adjustment(target,target_longitude,aspecting_placements,classifications,*,classification_profile):
    if target not in CLASSICAL:raise ValueError('Classical target required')
    if not classification_profile:raise ValueError('Named externally grounded classification profile required')
    valid_longitude(target_longitude)
    rows=[];missing=[]
    for p in CLASSICAL:
        if p==target:continue
        lon=aspecting_placements.get(p,{}).get('longitude')
        if lon is None:
            missing.append(p);continue
        aspect=degree_aspect(p,lon,target_longitude)
        kind=classifications.get(p)
        if kind is not None and kind not in ('benefic','malefic'):raise ValueError('Benefic, malefic or missing classification required')
        signed=None if kind is None else aspect['rupa']/4*(1 if kind=='benefic' else -1)
        if kind is None:missing.append(p)
        rows.append({'aspecting_planet':p,'supplied_classification':kind,'unsigned_aspect':aspect,'signed_rupa':signed})
    return {'target':target,'classification_profile':classification_profile,'pairs':rows,
            'missing_planets_or_classifications':missing,
            'signed_adjustment_rupa':None if missing else sum(r['signed_rupa'] for r in rows),
            'source':source('20',74,60),'total_strength':None,
            'notice':'Explicitly supplied benefic/malefic classes only. No phase-conditioned Moon or association-conditioned Mercury class inferred. All six other classical planets required before net adjustment. Not applied to incomplete five-bala sum; no Bhava extra Mercury/Jupiter rule here.'}
