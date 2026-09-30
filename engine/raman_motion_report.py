"""Clock/table/motion candidates with explicit Sun revolution branch, no winner."""
from .raman_mean_clock import raman_local_mean_clock
from .raman_motion_inputs import raman_motion_inputs


def raman_motion_report(local_mean_timestamp,longitude,*,clock_kind,clock_profile,sun_revolution_branch,superior_means,true_longitudes,inferior_sighra,input_profile,coordinate_branch):
    if type(sun_revolution_branch) is not int:raise ValueError('Explicit integer Sun revolution branch required')
    clock=raman_local_mean_clock(local_mean_timestamp,longitude,clock_kind=clock_kind,clock_profile=clock_profile)
    rows=[]
    for c in clock['mean_sun_table_candidates']['candidates']:
        mean=float(c['mean_sun_degrees'])+360*sun_revolution_branch
        rows.append({'mean_sun_constant_profile':c['constant_profile'],
            'source_table_candidate':c,'assigned_sun_unwrapped':mean,
            'motion_input_evidence':raman_motion_inputs(mean,superior_means,true_longitudes,inferior_sighra,
                input_profile=input_profile+'; raw Raman mean-Sun table candidate '+c['constant_profile'],coordinate_branch=coordinate_branch)})
    return {'clock_evidence':clock,'sun_revolution_branch':sun_revolution_branch,'candidates':rows,
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
