"""Run a house-based reading under whole-sign and Sripati degree-Bhava occupancy.

The source audit (house-system research file) found no universal choice:
Sripati builds degree Bhavas, Phaladeepika wants Bhava-degree and Sandhi effects,
Hora Ratnam keeps sign-based steps for some purposes. So each rule is run with
planet occupancy under both models. Where the two disagree the row becomes
'house_model_dependent' and both statuses are kept. Only occupancy changes:
house lordship stays by sign from the Lagna sign in both runs (labeled).
A planet inside a Sandhi gets no house at all in the degree run, so rules that
need it to occupy a house read as not satisfied there and are flagged.
"""
import copy

MODELS=('whole_sign','sripati_degree_bhava')


def degree_chart(chart):
    c=copy.deepcopy(chart)
    for p,v in c['placements'].items():
        d=v.get('sripati_degree_house')
        if not d:raise ValueError('Degree Bhava membership unavailable for '+p)
        v['whole_sign_house_from_ascendant']=d['house']
        v['_at_sandhi']=bool(d.get('at_sandhi'))
    return c


def dual_house_model(fn,chart,**kw):
    whole=fn(chart,**kw)
    try:
        deg=fn(degree_chart(chart),**kw)
    except ValueError as exc:
        whole['house_model_sensitivity']={'status':'degree_model_unavailable','reason':str(exc)}
        return whole
    out=copy.deepcopy(whole)
    changed=0
    for a,b in zip(out['rows'],deg['rows']):
        a['status_by_house_model']={MODELS[0]:a['status'],MODELS[1]:b['status']}
        a['detail_by_house_model']={MODELS[0]:a['detail'],MODELS[1]:b['detail']}
        if a['status']!=b['status']:
            a['status']='house_model_dependent';changed+=1
    out['house_model']='both_whole_sign_and_sripati_degree_bhava_occupancy'
    out['house_model_sensitivity']={'rows_that_differ':changed,'models':list(MODELS),
        'note':'Occupancy differs by model; lordship stays by sign. No model is selected.'}
    return out
