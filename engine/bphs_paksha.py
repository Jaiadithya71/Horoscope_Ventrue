"""BPHS27.10-11 commentary phase/classification, not Sripati replacement."""
from .friendship import CLASSICAL
from .luminary_motion_identity import SOURCE,supplied_luminary_motion_identity


def bphs_paksha_candidates(planet,sun_longitude,moon_longitude,*,mercury_with_malefic=None,association_profile=None):
    import math
    if planet not in CLASSICAL:raise ValueError('Classical planet required')
    for x in (sun_longitude,moon_longitude):
        if isinstance(x,bool) or not isinstance(x,(int,float)) or not math.isfinite(x) or not 0<=x<360:raise ValueError('Finite longitude in0..360 required')
    if mercury_with_malefic is not None and type(mercury_with_malefic) is not bool:raise ValueError('Supplied association bool or unknown required')
    if mercury_with_malefic is not None and (not isinstance(association_profile,str) or not association_profile.strip()):raise ValueError('Named external association profile required')
    elongation=(moon_longitude-sun_longitude)%360
    factor=min(elongation,360-elongation)/180
    if planet=='Moon':
        classifications=[True,False] if elongation in (0,180) else [elongation<180]
        origin='Moon dark-half commentary; exact0/180 classification unspecified'
    elif planet=='Mercury':
        classifications=[True,False] if mercury_with_malefic is None else [not mercury_with_malefic]
        origin='Externally supplied malefic association, not guessed geometry'
    else:classifications=[planet in ('Jupiter','Venus')];origin='Fixed benefic/malefic group in this profile'
    rows=[]
    for benefic in classifications:
        base=factor if benefic else 1-factor
        value=base*(2 if planet=='Moon' else 1)
        rows.append({'benefic_classification_candidate':benefic,'undoubled_paksha_rupa':base,
            'commentary_multiplier':2 if planet=='Moon' else 1,'paksha_rupa':value,
            'moon_motion_identity':supplied_luminary_motion_identity('Moon',value,component_profile='BPHS folded phase/classification commentary candidate') if planet=='Moon' else None})
    return {'planet':planet,'elongation_degrees':elongation,'folded_benefic_factor':factor,
        'classification_origin':origin,'mercury_with_malefic':mercury_with_malefic,'association_profile':association_profile,
        'candidates':rows,'selected_paksha_rupa':rows[0]['paksha_rupa'] if len(rows)==1 else None,
        'source':dict(SOURCE,pdf_page=222,printed_page=212,sloka='10-11 commentary'),
        'selected_sripati_component':None,'total_strength':None,
        'notice':'Named digital BPHS commentary candidate only. Moon dark-half malefic and Mercury association profile differ from Sripati fixed-benefic commentary. Exact lunar0/180 classification stays unresolved. No inferred Mercury conjunction orb/aggregate malefic status. Moon double occurs once before motion identity. A determinate scoped value is not a selected full natal model, historical ephemeris, strength rank or personal outcome.'}
