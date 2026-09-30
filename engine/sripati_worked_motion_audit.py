"""Printed motion angles are supplied evidence, not recovered ephemeris inputs."""
from fractions import Fraction as F
from .motional_strength import cheshtabala
from .sripati_edition_strength_audit import EARLY
from .full_strength_table_audit import PRINTED,NAMES

ANGLES={'Mars':'325.989','Mercury':'217.059','Jupiter':'216.760','Venus':'351.085','Saturn':'11.270'}
LOCAL={'Mars':'.189','Mercury':'.794','Jupiter':'.795','Venus':'.049','Saturn':'.062'}


def worked_motion_audit():
    rows=[]
    for p,text in ANGLES.items():
        angle=F(text);folded=min(angle,360-angle);exact=folded/180
        pipeline=cheshtabala(p,float(angle))
        early=dict(zip(NAMES,EARLY[p][0].split()))['cheshta']
        late=dict(zip(NAMES,PRINTED[p][0].split()))['cheshta']
        rows.append({'planet':p,'printed_angle_both_editions':text,
            'exact_folded_degrees':str(folded),'exact_motion_rupa':str(exact),
            'calculated_motion_rupa':float(exact),'printed_local_both_editions':LOCAL[p],
            'local_matches_floor3_diagnostic':F(int(exact*1000),1000)==F(LOCAL[p]),
            'pipeline_exact_agreement':abs(pipeline['rupa']-float(exact))<1e-12,
            '1919_aggregate_motion':early,'later_aggregate_motion':late,
            '1919_aggregate_equals_local':F(early)==F(LOCAL[p]),
            'later_aggregate_equals_local':F(late)==F(LOCAL[p]),
            'upstream_inputs':{'mean_unwrapped_degrees':None,'true_unwrapped_degrees':None,
                'sighrochcha_degrees':None,'coordinate_branch':None},
            'independent_angle_reconstruction':None})
    return {'rows':rows,'local_floor3_matches':sum(r['local_matches_floor3_diagnostic'] for r in rows),
        'earlier_local_aggregate_matches':sum(r['1919_aggregate_equals_local'] for r in rows),
        'later_local_aggregate_matches':sum(r['later_aggregate_equals_local'] for r in rows),
        'sources':[
            {'url':'https://archive.org/details/dli.ernet.203510','pdf_pages':[71,72,73],'printed_pages':[57,58,59],'verified_against_page_image':True},
            {'url':'https://archive.org/details/ksu.h1304.sripatipaddhati0000vsub','pdf_pages':[112,113],'printed_pages':[96,97],'verified_against_page_image':True}],
        'selected_motion_values':None,'selected_natal_total':None,
        'notice':'Four printed local values match floor3 of supplied decimal angles; Mars exact.18895 prints.189 rather than floor.188. These diagnostics do not establish a universal precision policy. 1919Saturn aggregate.026 disagrees with its local.062; later aggregate matches all five. Sources attribute angles to Ketkar tables but do not supply their worked mean/true/Sighrochcha triples or branch. One equation cannot uniquely recover three inputs. No inferred triple, circular average, fitted ephemeris, luminary component, or full natal total.'}
