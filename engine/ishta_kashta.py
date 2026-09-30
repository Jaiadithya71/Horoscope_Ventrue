"""Historical Sripati IV.5-6 component transformation, not outcome likelihood."""
import math
from .continuous_strength import source


def ishta_kashta(uchcha_rupa,cheshta_rupa,*,component_profile):
    if not component_profile:raise ValueError('Named grounded component profile required')
    for x in (uchcha_rupa,cheshta_rupa):
        if not math.isfinite(x) or not 0<=x<=1:raise ValueError('Supplied normalized components must be in [0,1]')
    root_good=math.sqrt(uchcha_rupa*cheshta_rupa)
    root_adverse=math.sqrt((1-uchcha_rupa)*(1-cheshta_rupa))
    average=(uchcha_rupa+cheshta_rupa)/2
    return {'component_profile':component_profile,'supplied_uchcha_rupa':uchcha_rupa,
            'supplied_cheshta_rupa':cheshta_rupa,
            'sripati_root_profile':{'historical_ishta':root_good,'historical_kashta':root_adverse,
                'sources':[dict(source('5-6',84,70),chapter='IV'),dict(source('6',85,71),chapter='IV')]},
            'quoted_parashara_average_profile':{'historical_ishta':average,'historical_kashta':1-average,
                'source':dict(source('6 commentary alternative',86,72),chapter='IV'),
                'notice':'Normalized arithmetic implied by rays=1+6*component from PDF83. The PDF86 Sun example uses Cheshta rays5.317, not PDF85 component.810; its numeric example is not used as an identical-input fixture.'},
            'selected_profile':None,'total_strength':None,
            'notice':'Two source-labeled historical transformation profiles, not probabilities, calibrated weights, promised benefits/harms or event forecasts. Caller must ground normalized Uchcha/Cheshta; Sun/Moon motion definitions and complete total are not supplied here. No automatic rectified-strength or aspect weighting.'}
