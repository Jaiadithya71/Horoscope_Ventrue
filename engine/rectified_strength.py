"""IV.7 historical multiplication of explicitly complete supplied Shadbala."""
import math
from .continuous_strength import source
from .degree_aspects import CLASSICAL


def rectify_supplied_total(planet,total_rupa,ishta,kashta,*,complete,total_profile,factor_profile):
    if planet not in CLASSICAL:raise ValueError('Classical planet required')
    if not isinstance(complete,bool):raise ValueError('Complete flag must be boolean')
    if not total_profile or not factor_profile:raise ValueError('Named grounded total/factor profiles required')
    if not math.isfinite(total_rupa) or total_rupa<0:raise ValueError('Finite nonnegative total required')
    for x in (ishta,kashta):
        if not math.isfinite(x) or not 0<=x<=1:raise ValueError('Normalized supplied factors required')
    return {'planet':planet,'supplied_total_rupa':total_rupa,'supplied_ishta':ishta,'supplied_kashta':kashta,
            'complete':complete,'total_profile':total_profile,'factor_profile':factor_profile,
            'rectified_ishta_rupa':total_rupa*ishta if complete else None,
            'rectified_kashta_rupa':total_rupa*kashta if complete else None,
            'source':dict(source('7',86,72),chapter='IV'),
            'worked_sources':[dict(source('7 worked products',87,73),chapter='IV'),dict(source('7 continued',88,74),chapter='IV')],
            'engine_computed_full_strength':None,'aspect_rectification':None,
            'notice':'Historical multiplication only. Caller-supplied completeness/model provenance is not verified by this helper; engine partial components cannot qualify. No natal profile selection, probability, predicted event or personal priority. Aspect-factor attribution remains separately unresolved.'}
