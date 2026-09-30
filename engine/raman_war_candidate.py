"""Raman art76-77 supplied partial-base war candidate, not Sripati reconciliation."""
from decimal import Decimal as D,InvalidOperation
from .raman_motion_source_audit import SOURCE_URL

DIAMETERS={'Mars':'9.4','Mercury':'6.6','Jupiter':'190.4','Venus':'16.6','Saturn':'158.0'}
KEYS={'sthana','dig','kala_up_to_hora'}


def raman_supplied_war_candidate(a,b,partial_a,partial_b,*,winner,war_condition_confirmed,
    partial_bases_complete,coordinate_profile,diameter_difference_profile):
    if a not in DIAMETERS or b not in DIAMETERS or a==b:raise ValueError('Distinct classical nonluminaries required')
    if winner not in (a,b) or war_condition_confirmed is not True or partial_bases_complete is not True:
        raise ValueError('Confirmed war, explicit winner and complete partial bases required')
    if not isinstance(coordinate_profile,str) or not coordinate_profile.strip():raise ValueError('Named coordinate/winner provenance required')
    if diameter_difference_profile!='absolute_printed_arcseconds_candidate':raise ValueError('Explicit diameter magnitude candidate required')
    supplied={}
    for planet,parts in ((a,partial_a),(b,partial_b)):
        if not isinstance(parts,dict) or set(parts)!=KEYS:raise ValueError('Only Sthana, Dig and Kala up toHora in virupa required')
        values={}
        for key,x in parts.items():
            if isinstance(x,bool):raise ValueError('Finite nonnegative virupa required')
            try:v=D(str(x))
            except InvalidOperation as exc:raise ValueError('Numeric virupa required') from exc
            if not v.is_finite() or v<0:raise ValueError('Finite nonnegative virupa required')
            values[key]=v
        supplied[planet]=values
    aggregates={p:sum(v.values()) for p,v in supplied.items()}
    difference=abs(aggregates[a]-aggregates[b]);denominator=abs(D(DIAMETERS[a])-D(DIAMETERS[b]))
    transfer=difference/denominator
    adjusted={p:v['kala_up_to_hora']+(transfer if p==winner else -transfer) for p,v in supplied.items()}
    return {'profile':'raman_art76_partial_base_disc_difference_candidate','coordinate_profile':coordinate_profile,
        'supplied_winner':winner,'supplied_partial_components_virupa':{p:{k:str(x) for k,x in v.items()} for p,v in supplied.items()},
        'partial_aggregates_virupa':{p:str(v) for p,v in aggregates.items()},'absolute_aggregate_difference_virupa':str(difference),
        'printed_disc_diameters_arcseconds':{a:DIAMETERS[a],b:DIAMETERS[b]},
        'diameter_difference_profile':diameter_difference_profile,'divisor_arcseconds_magnitude':str(denominator),
        'candidate_yuddhabala_virupa':str(transfer),'candidate_kala_up_to_hora_after_war_virupa':{p:str(v) for p,v in adjusted.items()},
        'negative_kala_candidates':[p for p,v in adjusted.items() if v<0],
        'source':{'url':SOURCE_URL,'pdf_pages':[65,66,67],'printed_pages':[60,61,62],
            'articles':[76,77],'verified_against_page_image':True},
        'selected_winner':None,'complete_kalabala':None,'engine_computed_total_strength':None,
        'notice':'Arithmetic on supplied partial bases only, in virupa. Source explicitly subtracts smaller aggregate from larger; absolute disc difference is a named candidate, not source unit proof. Printed fixed diameters are not modern physical sizes. Caller confirms war and lower-longitude winner interpretation; equality and0degree branch are not resolved here. Ayana, later temporal terms and full strength are not in this numerator; do not apply transfer twice or import into Sripati latitude profile. Negative candidates retained, not clipped.'}
