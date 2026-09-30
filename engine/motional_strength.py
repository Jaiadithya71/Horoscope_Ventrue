"""Sripati III.16-18 supplied Cheshtakendra only, not modern-speed replacement."""
from .continuous_strength import source,valid_longitude

NON_LUMINARIES=('Mars','Mercury','Jupiter','Venus','Saturn')


def _finite_angle(value):
    import math
    if isinstance(value,bool) or not isinstance(value,(int,float)):
        raise ValueError('Numeric non-boolean angle required')
    try:
        finite=math.isfinite(value)
    except OverflowError:
        finite=False
    if not finite:
        raise ValueError('Finite representable angle required')


def cheshtabala(planet,cheshtakendra_degrees):
    if planet not in NON_LUMINARIES:raise ValueError('Classical non-luminary required')
    _finite_angle(cheshtakendra_degrees)
    valid_longitude(cheshtakendra_degrees)
    folded=min(cheshtakendra_degrees,360-cheshtakendra_degrees)
    return {'planet':planet,'supplied_cheshtakendra_degrees':cheshtakendra_degrees,
            'folded_degrees':folded,'rupa':folded/180,'virupa':folded/3,
            'sources':[source('16-18',71,57),source('18 commentary worked table',73,59)],
            'total_strength':None,
            'worked_table_notice':'PDF73 prints .795/.049/.062 for Jupiter/Venus/Saturn. Supplied rounded angles give .7957778/.0495278/.0626111, within .001 but not standard three-decimal rounding. Printed values are not substituted.',
            'notice':'Caller must ground traditional Cheshtakendra. Modern instantaneous speed or retrograde flag is not this angle. Mean/true/Sighrochcha angle generation remains unresolved; Sun/Moon are outside this helper.'}


def cheshta_from_supplied_mean_true(planet,mean_unwrapped_degrees,true_unwrapped_degrees,
                                  sighrochcha_degrees,*,input_profile,coordinate_branch):
    """III.16-18 algebra only; caller explicitly grounds the angle branch.

    Taking a circular average silently is not allowed. A mean359/true1
    pair differs from mean359/true361; the source does not fix a universal
    wrap rule here. Accept unwrapped finite inputs with named provenance.
    """
    import math
    if not isinstance(input_profile,str) or not input_profile.strip() or not isinstance(coordinate_branch,str) or not coordinate_branch.strip():
        raise ValueError('Grounded input profile and coordinate branch required')
    for angle in (mean_unwrapped_degrees,true_unwrapped_degrees,sighrochcha_degrees):
        _finite_angle(angle)
    valid_longitude(sighrochcha_degrees)
    corrected=sighrochcha_degrees+(mean_unwrapped_degrees-true_unwrapped_degrees)/2
    difference=corrected-mean_unwrapped_degrees
    if not math.isfinite(corrected) or not math.isfinite(difference):
        raise ValueError('Supplied angle branch overflows the motion algebra')
    kendra=difference%360
    return {'planet':planet,'supplied_mean_unwrapped_degrees':mean_unwrapped_degrees,
            'supplied_true_unwrapped_degrees':true_unwrapped_degrees,
            'supplied_sighrochcha_degrees':sighrochcha_degrees,
            'input_profile':input_profile,'coordinate_branch':coordinate_branch,
            'corrected_sighrochcha_unwrapped_degrees':corrected,
            'cheshtakendra_degrees':kendra,'cheshtabala':cheshtabala(planet,kendra),
            'source':source('16-18 supplied mean/true/Sighrochcha algebra',71,57),
            'total_strength':None,
            'notice':'Algebra from explicitly supplied historical inputs only. No modern instantaneous speed, helio longitude, automatically chosen mean model or coordinate branch. Does not reconstruct the Ketkar worked-table angles or select a natal strength profile.'}
