"""Clock/table/motion candidates with explicit Sun revolution branch, no winner."""
from .raman_mean_clock import raman_local_mean_clock
from .raman_motion_inputs import raman_motion_inputs
from .raman_inferior_sighra import raman_inferior_sighra


def raman_motion_report(local_mean_timestamp,longitude,*,clock_kind,clock_profile,sun_revolution_branch,superior_means,true_longitudes,inferior_sighra,input_profile,coordinate_branch,inferior_table_requests=None):
    if type(sun_revolution_branch) is not int:raise ValueError('Explicit integer Sun revolution branch required')
    if inferior_table_requests is not None and (not isinstance(inferior_table_requests,dict) or set(inferior_table_requests)-{'Mercury','Venus'}):raise ValueError('Inferior table requests must name Mercury or Venus')
    inferior_tables={p:raman_inferior_sighra(p,**request) for p,request in (inferior_table_requests or {}).items()}
    clock=raman_local_mean_clock(local_mean_timestamp,longitude,clock_kind=clock_kind,clock_profile=clock_profile)
    rows=[]
    for c in clock['mean_sun_table_candidates']['candidates']:
        mean=float(c['mean_sun_degrees'])+360*sun_revolution_branch
        rows.append({'mean_sun_constant_profile':c['constant_profile'],
            'source_table_candidate':c,'assigned_sun_unwrapped':mean,
            'motion_input_evidence':raman_motion_inputs(mean,superior_means,true_longitudes,inferior_sighra,
                input_profile=input_profile+'; raw Raman mean-Sun table candidate '+c['constant_profile'],coordinate_branch=coordinate_branch)})
    table_motion=[]
    for sun in rows:
        for planet,table in inferior_tables.items():
            for correction in table['candidates']:
                angle=correction['sighrochcha_degrees']
                angles=dict(inferior_sighra);angles[planet]=None if angle is None else float(angle)
                evidence=raman_motion_inputs(sun['assigned_sun_unwrapped'],superior_means,true_longitudes,angles,
                    input_profile=input_profile+'; raw inferior table '+correction['correction_profile'],coordinate_branch=coordinate_branch)
                table_motion.append({'planet':planet,'mean_sun_constant_profile':sun['mean_sun_constant_profile'],
                    'correction_profile':correction['correction_profile'],
                    'motion_input_evidence':next(r for r in evidence['rows'] if r['planet']==planet)})
    return {'inferior_table_evidence':inferior_tables,'inferior_table_motion_candidates':table_motion,
        'inferior_table_notice':'Optional independent supplied elapsed-day and epoch-clock requests. No clock equivalence assumed with mean-Sun chain. Supplied-Sighra candidates remain unchanged. Each planet is propagated separately, not combined into a selected chart.',
        'clock_evidence':clock,'sun_revolution_branch':sun_revolution_branch,'candidates':rows,
        'selected_mean_sun':None,'selected_motion_profile':None,'total_strength':None,
        'notice':'Runnable Raman clock/table/assignment/algebra evidence only. Digit-table columns are already modulo360; their sum does not recover physical revolutions. Sun revolution branch is explicit caller input, not inferred from elapsed days. Other mean/true/Sighra inputs and clock provenance remain caller-grounded. Both raw epoch constants propagate separately; no circular-average choice, source-typo repair, Ketkar equivalence or full strength total.'}


def main():
    import json,sys,argparse
    a=argparse.ArgumentParser(description=__doc__)
    a.add_argument('--input-json',required=True,help='Explicit structured input file; use - to read stdin')
    args=a.parse_args()
    try:
        if args.input_json=='-':data=json.load(sys.stdin)
        else:
            with open(args.input_json) as f:data=json.load(f)
        print(json.dumps(raman_motion_report(**data),indent=2))
    except (ValueError,TypeError) as exc:a.error(str(exc))


if __name__=='__main__':main()
