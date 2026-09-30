"""Explicit mixed-source direct-owner component benchmark, not full strength."""
from fractions import Fraction
from .sripati_worked_navamsa_audit import WORKED_DMS
from .sripati_worked_relation_audit import worked_relation_audit
from .seven_varga_strength import direct_owner_seven_varga
from .natal_factors import dignity
from .forecast import SIGNS
from .seven_varga_table_audit import PRINTED

EXACT_UNITS={'self':Fraction(1,2),'very_friend':Fraction(3,8),
    'friend':Fraction(1,4),'neutral':Fraction(1,8),
    'enemy':Fraction(1,16),'very_enemy':Fraction(1,32)}
EARLY_TOTALS={'Sun':'2.5','Moon':'2.125','Mars':'2.75','Mercury':'1.687',
    'Jupiter':'3.25','Venus':'.906','Saturn':'.687'}


def worked_direct_owner_candidates():
    relation_audit=worked_relation_audit()
    rows=[]
    for planet,(sign,degree,minute,second) in WORKED_DMS.items():
        longitude=float(sign*30+degree+Fraction(minute,60)+Fraction(second,3600))
        moola=dignity(planet,SIGNS[sign],longitude)['flags']['moolatrikona_portion']
        candidates=[]
        for profile in ('rasi_relative','lagna_bhava_relative'):
            mapping={pair['other']:next(c['compound_relation'] for c in pair['candidates']
                if c['house_profile']==profile) for pair in relation_audit['directed_relation_evidence']['directed_pairs']
                if pair['planet']==planet}
            component=direct_owner_seven_varga(planet,longitude,mapping,
                relation_profile=profile+'; Phaladeepika1937 natural + KapoorII23 compound',
                rasi_moolatrikona=moola)
            exact_rows=[]
            for row in component['vargas']:
                exact=Fraction(3,4) if row['varga']=='rasi' and moola else EXACT_UNITS[row['compound_relation']]
                exact_rows.append({'varga':row['varga'],'owner':row['owner'],
                    'relation':row['compound_relation'],'exact_rupa':str(exact)})
            total=sum(Fraction(r['exact_rupa']) for r in exact_rows)
            candidates.append({'house_profile':profile,'component':component,
                'exact_fraction_rows':exact_rows,'exact_total_rupa':str(total),
                'exact_total_decimal':float(total),'float_component_equals_exact':component['rupa']==float(total),
                'difference_from_1919_printed_total':str(total-Fraction(EARLY_TOTALS[planet])),
                'difference_from_later_printed_total':str(total-Fraction(PRINTED[planet][1]))})
        rows.append({'planet':planet,'candidates':candidates,'selected_component':None})
    return {'rows':rows,'relation_audit':relation_audit,
        'moolatrikona_source':{'slug':'phaladeepika-1937','chapter':'I','sloka':7,
            'pdf_page':41,'printed_page':4,'verified_against_page_image':True},
        'earlier_score_source':{'url':'https://archive.org/details/ksu.h1304.sripatipaddhati0000vsub',
            'pdf_page':96,'printed_page':80,'verified_against_page_image':True},
        'later_score_source':{'url':'https://archive.org/details/dli.ernet.203510',
            'pdf_page':49,'printed_page':35,'verified_against_page_image':True},
        'selected_profile':None,'selected_natal_total':None,
        'notice':'Supplied worked chart and explicitly mixed-source geometry/natural/compound/portion conventions only. Both house candidates coincide here, not universally. Exact seven-varga components are Sun2.5 Moon2.125 Mars2.75 Mercury1.6875 Jupiter3.125 Venus.90625 Saturn.6875.1919Jupiter differs by1/8 due to Navamsa row; Mercury/Venus/Saturn decimal discrepancies remain provenance, not rounding corrections. Owner-own-placement alternative is not evaluated. No source-selected positional/full-strength total or predictive validity.'}
