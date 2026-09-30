"""Scoped IV.4/7 evidence, not a general rule or total Shadbala calculator."""
import math
from .strength_components import source
from .friendship import CLASSICAL
from .natal_factors import dignity

THRESHOLDS={'Sun':6.5,'Moon':6.0,'Mars':5.0,'Mercury':7.0,'Jupiter':6.5,'Venus':5.5,'Saturn':5.0}


def condition_precedence(planet,sign,longitude=None,retrograde=None,overpowered_rays=None):
    for flag in (retrograde,overpowered_rays):
        if flag is not None and not isinstance(flag,bool):
            raise ValueError('Conditions must be bool or None')
    d=dignity(planet,sign,longitude)
    if planet not in CLASSICAL:
        return {'status':'not_scored','reason':'Node conditions not resolved by this checked slice'}
    rows=[]
    if retrograde is True and planet not in ('Sun','Moon'):
        rows.append({'condition':'retrograde','qualitative_evidence':'strength despite depression or enemy placement',
                     'source':source('4',72,35),'scope':'dignity versus retrograde condition, not numeric total'})
    if overpowered_rays is True:
        rows.append({'condition':'overpowered_rays','qualitative_evidence':'weak despite exaltation, own or friendly placement',
                     'source':source('4',72,35),'scope':'dignity versus overpowered rays'})
        rows.append({'condition':'overpowered_by_sun_rays','positional_rupa_candidate':0.0,
                     'source':source('7',73,36),'scope':'positional component only'})
    return {'status':'conditional_evidence_only','dignity':d,'condition_evidence':rows,
            'input_conditions':{'retrograde':retrograde,'overpowered_sun_rays':overpowered_rays},
            'unresolved_conflict':retrograde is True and overpowered_rays is True,
            'global_outcome_precedence':None,'total_strength':None,
            'component_emphasis':{'kind':'paksha' if planet=='Moon' else 'positional',
                                  'source':source('21',79,42)},
            'notice':'No automatic combustion threshold is inferred. Simultaneous motion/ray conditions remain exposed. No global priority or personal outcome.'}


def check_supplied_total(planet,total_rupa,complete=False):
    """Checks an explicitly complete externally supplied total, never partial sums."""
    if planet not in THRESHOLDS:raise ValueError('Classical planet required')
    if not math.isfinite(total_rupa) or total_rupa<0:raise ValueError('Total must be finite and nonnegative')
    if not isinstance(complete,bool):raise ValueError('Complete must be boolean')
    return {'planet':planet,'supplied_total_rupa':total_rupa,'complete':complete,
            'required_total_rupa':THRESHOLDS[planet],
            'meets_book_threshold':total_rupa>=THRESHOLDS[planet] if complete else None,
            'source':source('22-23',79,42),
            'notice':'Threshold test only. The engine does not calculate or verify the supplied total; incomplete totals cannot classify a planet.'}
