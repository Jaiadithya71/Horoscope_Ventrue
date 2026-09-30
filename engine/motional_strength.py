"""Sripati III.16-18 supplied Cheshtakendra only, not modern-speed replacement."""
from .continuous_strength import source,valid_longitude

NON_LUMINARIES=('Mars','Mercury','Jupiter','Venus','Saturn')


def cheshtabala(planet,cheshtakendra_degrees):
    if planet not in NON_LUMINARIES:raise ValueError('Classical non-luminary required')
    valid_longitude(cheshtakendra_degrees)
    folded=min(cheshtakendra_degrees,360-cheshtakendra_degrees)
    return {'planet':planet,'supplied_cheshtakendra_degrees':cheshtakendra_degrees,
            'folded_degrees':folded,'rupa':folded/180,'virupa':folded/3,
            'sources':[source('16-18',71,57),source('18 commentary worked table',73,59)],
            'total_strength':None,
            'worked_table_notice':'PDF73 prints .795/.049/.062 for Jupiter/Venus/Saturn. Supplied rounded angles give .7957778/.0495278/.0626111, within .001 but not standard three-decimal rounding. Printed values are not substituted.',
            'notice':'Caller must ground traditional Cheshtakendra. Modern instantaneous speed or retrograde flag is not this angle. Mean/true/Sighrochcha angle generation remains unresolved; Sun/Moon are outside this helper.'}
