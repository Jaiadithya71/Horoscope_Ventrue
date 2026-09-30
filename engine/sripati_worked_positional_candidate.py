"""Worked chart exercise of the four-axis candidate matrix, never selected."""
from fractions import Fraction
from .sripati_worked_navamsa_audit import WORKED_DMS
from .sripati_worked_strength_candidate import worked_direct_owner_candidates
from .bhava_geometry import bhava_geometry,house_membership
from .forecast import SIGNS
from .continuous_strength import NEECHA
from .positional_candidates import positional_candidates
from .positional_table_audit import PRINTED,NAMES

EARLY_TOTAL={'Sun':'4.707','Moon':'4.022','Mars':'3.667','Mercury':'2.238',
    'Jupiter':'4.436','Venus':'2.811','Saturn':'2.231'}


def worked_positional_candidates():
    geometry=bhava_geometry(14+31/60+46/3600,277+42/60+11/3600)
    placements={};exact_longitudes={}
    for planet,(sign,degree,minute,second) in WORKED_DMS.items():
        exact=sign*30+degree+Fraction(minute,60)+Fraction(second,3600)
        exact_longitudes[planet]=exact
        placements[planet]={'sign':SIGNS[sign],'longitude':float(exact),
            'whole_sign_house_from_ascendant':sign+1,
            'sripati_degree_house':house_membership(float(exact),geometry)}
    matrix=positional_candidates(placements)
    varga={r['planet']:r for r in worked_direct_owner_candidates()['rows']}
    rows=[]
    for row in matrix['planets']:
        planet=row['planet'];candidates=[]
        delta=(exact_longitudes[planet]-Fraction(str(NEECHA[planet])))%360
        uchcha=min(delta,360-delta)/180
        for candidate in row['independent_profile_matrix']:
            seven=next(c for c in varga[planet]['candidates'] if c['house_profile']==candidate['relation_profile'])
            p=candidate['pieces_rupa']
            exact_total=uchcha+Fraction(seven['exact_total_rupa'])+sum(Fraction(str(p[k]))
                for k in ('rasi_navamsa_parity','house_category','base_decan'))
            candidates.append({'relation_profile':candidate['relation_profile'],
                'house_category_profile':candidate['house_category_profile'],
                'pieces_rupa':p,'pipeline_total':candidate['base_five_piece_sum_rupa'],
                'exact_total_rupa':str(exact_total),'exact_total_decimal':float(exact_total),
                'float_pipeline_agrees_with_exact':abs(float(exact_total)-candidate['base_five_piece_sum_rupa'])<1e-12,
                'difference_from_1919_printed_total':str(exact_total-Fraction(EARLY_TOTAL[planet])),
                'difference_from_later_printed_total':str(exact_total-Fraction(PRINTED[planet][-1]))})
        rows.append({'planet':planet,'candidates':candidates,
            'later_printed_components':dict(zip(NAMES,PRINTED[planet][:5])),
            '1919_printed_total':EARLY_TOTAL[planet],'later_printed_total':PRINTED[planet][-1],
            'selected_positional_total':None})
    return {'rows':rows,'candidate_count':sum(len(r['candidates']) for r in rows),
        'fixture_distinguishes_axes':any(len({c['exact_total_rupa'] for c in r['candidates']})>1 for r in rows),
        'earlier_source':{'url':'https://archive.org/details/ksu.h1304.sripatipaddhati0000vsub',
            'pdf_page':99,'printed_page':83,'verified_against_page_image':True},
        'later_source':{'url':'https://archive.org/details/dli.ernet.203510',
            'pdf_page':53,'printed_page':39,'verified_against_page_image':True},
        'axis_limit_source':{'pdf_page':52,'printed_page':38,'verified_against_page_image':True,
            'text':'Neither view affects the horoscope in question.'},
        'selected_profile':None,'selected_natal_total':None,
        'notice':'28 explicitly mixed-source five-piece base candidates all agree across axes on this fixture, not arbitrary charts. Exact computation is not rounded to match printed intermediate tables. Jupiter1919 difference follows erroneous Navamsa; Venus/Saturn precision errors stay exposed. Own-Shadvarga decan refinement excluded, not guessed. No selected positional/full-strength total or historical ephemeris/outcome accuracy.'}
