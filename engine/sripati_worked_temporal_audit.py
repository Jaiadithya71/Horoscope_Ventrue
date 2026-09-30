"""Supplied historical birth clock and phase checks, not a temporal total."""
from fractions import Fraction as F
from .sripati_worked_navamsa_audit import WORKED_DMS
from .continuous_strength import natonnatabala,pakshabala_candidates
from .temporal_lords import tribhaga

NAT={'Sun':'.468','Moon':'.532','Mars':'.532','Mercury':'1.00',
     'Jupiter':'.468','Venus':'.468','Saturn':'.532'}
PAKSHA={p:('.518' if p in ('Moon','Mercury','Jupiter','Venus') else '.481') for p in NAT}
THIRD={p:int(p in ('Mars','Jupiter')) for p in NAT}


def longitude(p):
    s,d,m,v=WORKED_DMS[p]
    return 30*s+d+F(m,60)+F(v,3600)


def nearest_three(x):
    # Comparison diagnostic only; not a selected engine precision policy.
    return F((x*1000+F(1,2)).numerator//(x*1000+F(1,2)).denominator,1000)


def worked_temporal_audit():
    day=30+F(55,60);night=60-day;before_sunrise=F(30,60)
    elapsed_after_midnight=night/2-before_sunrise
    hours=elapsed_after_midnight*F(2,5)
    day_rupa=elapsed_after_midnight/30
    elongation=(longitude('Moon')-longitude('Sun'))%360
    folded=min(elongation,360-elongation)/180
    third=tribhaga('night',float((night-before_sunrise)/night))
    rows=[]
    for p in NAT:
        exact_nat=F(1) if p=='Mercury' else day_rupa if p in ('Sun','Venus','Jupiter') else 1-day_rupa
        benefic=p in ('Moon','Mercury','Jupiter','Venus')
        exact_phase=folded if benefic else 1-folded
        pipeline_nat=natonnatabala(p,float(hours))
        pipeline_phase=pakshabala_candidates(p,float(longitude('Sun')),float(longitude('Moon')))
        rows.append({'planet':p,'exact_natonnata_rupa':str(exact_nat),
            'printed_natonnata_both_editions':NAT[p],
            'natonnata_matches_nearest_three_diagnostic':nearest_three(exact_nat)==F(NAT[p]),
            'natonnata_pipeline_agrees':abs(pipeline_nat['rupa']-float(exact_nat))<1e-12,
            'exact_folded_phase_rupa':str(exact_phase),
            'printed_paksha_both_editions':PAKSHA[p],
            'paksha_matches_nearest_three_diagnostic':nearest_three(exact_phase)==F(PAKSHA[p]),
            'paksha_pipeline_candidates':pipeline_phase,
            'printed_tribhaga_both_editions':THIRD[p],
            'calculated_tribhaga':third['rupa_by_planet'][p]})
    return {'rows':rows,'clock_inputs':{'day_ghatika':str(day),'night_ghatika':str(night),
            'before_sunrise_ghatika':str(before_sunrise),
            'elapsed_from_midnight_ghatika':str(elapsed_after_midnight),
            'hours_after_midnight':str(hours),
            'assumption':'Midnight is midpoint of the supplied night; no modern ephemeris, civil timezone, or UTC inferred.'},
        'exact_elongation_degrees':str(elongation),'phase':'dark_half',
        'natonnata_nearest_diagnostic_matches':sum(r['natonnata_matches_nearest_three_diagnostic'] for r in rows),
        'paksha_nearest_diagnostic_matches':sum(r['paksha_matches_nearest_three_diagnostic'] for r in rows),
        'tribhaga_matches':sum(r['printed_tribhaga_both_editions']==r['calculated_tribhaga'] for r in rows),
        'sources':[
            {'url':'https://archive.org/details/dli.ernet.203510','pdf_page':17,'printed_page':3,'use':'clock inputs and DMS','verified_against_page_image':True},
            {'url':'https://archive.org/details/dli.ernet.203510','pdf_pages':[57,58,59,60,61],'printed_pages':[43,44,45,46,47],'use':'formulas and local tables','verified_against_page_image':True},
            {'url':'https://archive.org/details/ksu.h1304.sripatipaddhati0000vsub','pdf_pages':[101,102,103],'printed_pages':[85,86,87],'use':'earlier local tables/commentary','verified_against_page_image':True}],
        'selected_temporal_values':None,'selected_natal_total':None,
        'notice':'Clock reconstruction matches all seven Natonnata rows under nearest-three diagnostic and all seven night-third rows (Mars/Jupiter=1). Folded phase from exact DMS is benefic.517949074.../malefic.482050925...; tables print.518/.481 in both editions. The three malefic values do not match nearest-three and printed complements sum.999. Literal dark-half candidate reverses values and also fails to reproduce table. Moon doubling remains separate evidence. No universal precision policy, phase winner, or full temporal total selected.'}
