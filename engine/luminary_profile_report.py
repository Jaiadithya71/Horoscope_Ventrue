"""Run separately labeled component profiles, never a mixed strength total."""
import math
from .continuous_strength import ayanabala_candidates,pakshabala_candidates
from .bphs_declination_ayana import supplied_bphs_declination_ayana
from .bphs_paksha import bphs_paksha_candidates


def luminary_profile_report(sun_longitude,moon_longitude,*,declinations=None,declination_profile=None,mercury_with_malefic=None,association_profile=None):
    declinations={} if declinations is None else declinations
    if set(declinations)-{'Sun','Moon','Mercury'}:raise ValueError('Only Sun/Moon/Mercury comparison declinations accepted')
    if declinations and (not isinstance(declination_profile,str) or not declination_profile.strip()):raise ValueError('Named supplied declination profile required')
    for d in declinations.values():
        if isinstance(d,bool) or not isinstance(d,(int,float)) or not math.isfinite(d) or abs(d)>90:raise ValueError('Finite physical signed declination required')
    rows=[]
    for p in ('Sun','Moon','Mercury'):
        d=declinations.get(p)
        def domain(bound):return 'missing_declination' if d is None else 'outside_named_formula_domain' if abs(d)>bound else 'available'
        sstatus=domain(24);bstatus=domain(23.45)
        rows.append({'planet':p,
            'sripati_paksha_candidates':pakshabala_candidates(p,sun_longitude,moon_longitude),
            'bphs_paksha_candidates':bphs_paksha_candidates(p,sun_longitude,moon_longitude,mercury_with_malefic=mercury_with_malefic,association_profile=association_profile),
            'sripati_declination_domain_status':sstatus,
            'sripati_ayana_candidates':ayanabala_candidates(p,d) if sstatus=='available' else None,
            'bphs_declination_domain_status':bstatus,
            'bphs_ayana_component':supplied_bphs_declination_ayana(p,d,declination_profile=declination_profile) if bstatus=='available' else None})
    return {'rows':rows,'supplied_declination_profile':declination_profile,
        'selected_strength_profile':None,'selected_luminary_motion':None,'total_strength':None,
        'notice':'Comparison of numerical formulas on explicitly supplied coordinates, not certification that those coordinates match both historical models. Declination is never inferred from longitude. Missing/out-of-domain input stays unavailable; no clipping or other-profile fallback. Different phase/classification/multiplier rules remain separate. No components from these books are pooled into a total, selected historical epoch, chart rank or personal forecast.'}


def main():
    import argparse,json
    a=argparse.ArgumentParser(description=__doc__)
    a.add_argument('--sun-longitude',required=True,type=float);a.add_argument('--moon-longitude',required=True,type=float)
    for p in ('sun','moon','mercury'):a.add_argument('--'+p+'-declination',type=float)
    a.add_argument('--declination-profile');a.add_argument('--mercury-with-malefic',choices=('true','false'))
    a.add_argument('--association-profile')
    args=a.parse_args()
    ds={p:getattr(args,p.lower()+'_declination') for p in ('Sun','Moon','Mercury') if getattr(args,p.lower()+'_declination') is not None}
    try:
        x=luminary_profile_report(args.sun_longitude,args.moon_longitude,declinations=ds,declination_profile=args.declination_profile,
            mercury_with_malefic=None if args.mercury_with_malefic is None else args.mercury_with_malefic=='true',association_profile=args.association_profile)
        print(json.dumps(x,indent=2))
    except ValueError as exc:a.error(str(exc))


if __name__=='__main__':main()
