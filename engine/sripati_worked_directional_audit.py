"""Worked Digbala source-chain check, no table-driven corrections."""
from fractions import Fraction
from .sripati_worked_navamsa_audit import WORKED_DMS
from .bhava_geometry import bhava_geometry
from .continuous_strength import digbala,WEAKEST_BHAVA

LOCAL={'Sun':'.444','Moon':'.037','Mars':'.554','Mercury':'.260',
    'Jupiter':'.887','Venus':'.535','Saturn':'.074'}
LATE_AGGREGATE=dict(LOCAL)


def worked_directional_audit():
    asc=Fraction(14)+Fraction(31,60)+Fraction(46,3600)
    mc=Fraction(277)+Fraction(42,60)+Fraction(11,3600)
    anchors={1:asc,4:(mc+180)%360,7:(asc+180)%360,10:mc}
    geometry=bhava_geometry(float(asc),float(mc));rows=[]
    for planet,(sign,degree,minute,second) in WORKED_DMS.items():
        lon=sign*30+degree+Fraction(minute,60)+Fraction(second,3600)
        weak=WEAKEST_BHAVA[planet];delta=(lon-anchors[weak])%360
        exact=min(delta,360-delta)/180
        actual=digbala(planet,float(lon),geometry['centres'])
        # Compare floor-to3places as observed in worked rows, not a general
        # engine policy or a selected source rounding convention.
        floor=Fraction(int(exact*1000),1000)
        rows.append({'planet':planet,'exact_folded_degrees':str(exact*180),
            'weakest_bhava':weak,'exact_weakest_centre_degrees':str(anchors[weak]),
            'exact_rupa':str(exact),'calculated_rupa':actual['rupa'],
            'float_pipeline_agrees_with_exact':abs(actual['rupa']-float(exact))<1e-12,
            'observed_three_decimal_floor':str(floor),
            '1919_local_printed':LOCAL[planet],'later_local_printed':LOCAL[planet],
            'later_aggregate_printed':LATE_AGGREGATE[planet],
            'local_equals_observed_floor':Fraction(LOCAL[planet])==floor,
            'later_aggregate_equals_local':LATE_AGGREGATE[planet]==LOCAL[planet]})
    return {'rows':rows,
        'earlier_local_source':{'url':'https://archive.org/details/ksu.h1304.sripatipaddhati0000vsub',
            'pdf_page':100,'printed_page':84,'verified_against_page_image':True},
        'later_local_source':{'url':'https://archive.org/details/dli.ernet.203510',
            'pdf_page':56,'printed_page':42,'verified_against_page_image':True},
        'later_formula_source':{'pdf_page':55,'printed_page':41,'verified_against_page_image':True},
        'later_aggregate_source':{'pdf_page':75,'printed_page':61,'verified_against_page_image':True},
        'local_rows_equal_observed_floor':sum(r['local_equals_observed_floor'] for r in rows),
        'mercury_jupiter_exchange_hypothesis':{'computed_mercury_floor':'.887','computed_jupiter_floor':'.260',
            'printed_mercury':'.260','printed_jupiter':'.887','intent_verified':False},
        'selected_directional_values':None,'selected_natal_total':None,
        'notice':'Both local tables giveMars.554, consistent with exact.554540123... from suppliedlongitude/4thcentre; later aggregate also prints .554, verified by enlarged crop; prior .534 reading was our error. Namedformula on sameinputs givesMercury.887219135... andJupiter.260486111..., whereasbothlocal/aggregate tables exchange.260/.887. Apparent transposition is hypothesis, not editorintent. Fiveofsevenlocalrows match observed3decimalfloor; this does not authorize universal truncation or natalvalue replacement.'}
