"""Worked epoch/lords and Kala candidates; not a selected natal model."""
from fractions import Fraction as F
from .historical_day_count import historical_day_count
from .temporal_lords import positional_hora_candidates,lord_components
from .sripati_worked_temporal_audit import worked_temporal_audit,longitude,NAT,PAKSHA,THIRD
from .full_strength_table_audit import PRINTED

LOCAL_TOTAL={'Sun':'.949','Moon':'2.05','Mars':'2.013','Mercury':'1.518',
             'Jupiter':'2.236','Venus':'2.236','Saturn':'1.013'}


def worked_lord_subtotal_audit():
    epoch=historical_day_count(1955884954,0,21,epoch_profile='Sripati printed creation-count fixture only')
    asc=14+F(31,60)+F(46,3600)
    doubled=((asc-longitude('Sun'))%360)*2
    hora=positional_hora_candidates('Venus',float(asc),float(longitude('Sun')))
    temporal=worked_temporal_audit();byplanet={r['planet']:r for r in temporal['rows']}
    printed_rows=[];variants=[]
    for p in NAT:
        lord=F(1,4) if p=='Jupiter' else F(5,4) if p=='Venus' else F(1) if p=='Moon' else F(0)
        sum_printed=F(NAT[p])+F(PAKSHA[p])+THIRD[p]+lord
        printed_rows.append({'planet':p,'sum_printed_subcomponents':str(sum_printed),
            'printed_local_total':LOCAL_TOTAL[p],
            'local_total_closes':sum_printed==F(LOCAL_TOTAL[p]),
            'printed_full_table_kala':PRINTED[p][0].split()[1],
            'full_table_kala_equals_local':F(PRINTED[p][0].split()[1])==F(LOCAL_TOTAL[p])})
    for hora_profile,hora_lord in hora['candidates'].items():
        supplied=lord_components(year='Jupiter',month='Venus',weekday='Venus',hora=hora_lord)
        for phase_profile in ('folded_arc_commentary','literal_translated_dark_half_complement'):
            for moon_multiplier in (1,2):
                rows=[]
                for p,r in byplanet.items():
                    phase=F(r['exact_folded_phase_rupa'])
                    if phase_profile=='literal_translated_dark_half_complement':phase=1-phase
                    if p=='Moon':phase*=moon_multiplier
                    lords=sum(F(str(v)) for v in supplied['rupa_components_by_planet'][p].values())
                    total=F(r['exact_natonnata_rupa'])+THIRD[p]+lords+phase
                    rows.append({'planet':p,'exact_candidate_kala_rupa':str(total),
                        'calculated_candidate_kala_rupa':float(total),
                        'delta_from_printed_local':str(total-F(LOCAL_TOTAL[p]))})
                variants.append({'hora_profile':hora_profile,'hora_lord':hora_lord,
                    'phase_profile':phase_profile,'moon_paksha_multiplier':moon_multiplier,
                    'rows':rows,'selected':False})
    return {'supplied_epoch_reconstruction':epoch,'exact_doubled_arc_degrees':str(doubled),
        'completed_sign_index':int(doubled//30),'worked_ordinal_1_based':int(doubled//30)+1,
        'positional_hora_candidates':hora,'printed_rows':printed_rows,'candidate_matrix':variants,
        'local_subtotals_close':sum(r['local_total_closes'] for r in printed_rows),
        'local_vs_full_table_matches':sum(r['full_table_kala_equals_local'] for r in printed_rows),
        'sources':[
            {'url':'https://archive.org/details/dli.ernet.203510','pdf_pages':[62,63,64,65],'printed_pages':[48,49,50,51],'verified_against_page_image':True},
            {'url':'https://archive.org/details/ksu.h1304.sripatipaddhati0000vsub','pdf_pages':[106,107],'printed_pages':[90,91],'verified_against_page_image':True}],
        'selected_temporal_profile':None,'selected_natal_total':None,
        'notice':'Supplied creation counts reproduce714404106135days and Jupiter/Venus/Venus year/month/day lords. Completed-sign index23 means24th hora, Moon, matching both editions, not a fourth-ordinal conflict. Seven printed Kala sums close and match full table. Eight exact-input candidates retain phase/Moon multiplier/hora indexing axes; no forced print-fit or universal epoch/day-origin/hora selection. Ayana remains separately expanded outside this printed Kala subtotal; do not silently add it here.'}
