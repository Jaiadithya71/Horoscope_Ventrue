"""Original III.6 printed positional table audit, never a natal total."""
from decimal import Decimal
from .continuous_strength import source

# PDF53/printed39 directly image-checked. Preserve printed inputs separately
# from any computed chart components, even when a value looks suspicious.
PRINTED={
    'Sun':('0.957','2.5','0.25','1.0','0','4.707'),
    'Moon':('0.397','2.125','0.5','1.0','0','4.022'),
    'Mars':('0.667','2.75','0','0.25','0','3.667'),
    'Mercury':('0.051','1.687','0.25','0.25','0','2.238'),
    'Jupiter':('0.186','3.125','0.5','0.25','0.25','4.311'),
    'Venus':('0.905','0.905','0','1.0','0','2.810'),
    'Saturn':('0.044','0.686','0.5','1.0','0','2.230')}
NAMES=('uchcha','seven_varga','parity','house_category','decan')


def audit_printed_positional_table():
    rows=[]
    for planet,values in PRINTED.items():
        components=dict(zip(NAMES,values[:5]))
        computed=sum(Decimal(x) for x in components.values())
        printed=Decimal(values[5])
        rows.append({'planet':planet,'printed_components':components,
                     'sum_of_printed_components':str(computed),'printed_total':str(printed),
                     'sum_minus_printed':str(computed-printed),'internal_sum_matches':computed==printed,
                     'computed_from_chart':False,'source':source('6 preceding positional table',53,39)})
    return {'rows':rows,'internal_arithmetic_matches':sum(x['internal_sum_matches'] for x in rows),
            'full_strength':None,'selected_natal_positional_total':None,
            'unresolved_alternatives':[{'kind':'own-Shadvarga decan refinement','source':source('5 commentary',52,38),
                'notice':'Quoted refinement would change printed Jupiter decan. Condition definition is not silently inferred.'},
                {'kind':'seven-varga direct-owner versus owner-placement','source':source('3 commentary',46,32),
                 'notice':'Printed table is not proof that one profile or every input value is correct.'}],
            'notice':'Seven printed positional sums are an internal arithmetic audit only, not independent chart reconstruction, source-selected natal positional total, total Shadbala, calibrated weights or personal effects. Suspicious duplicate Venus Uchcha/seven-varga values are preserved rather than guessed corrections.'}


if __name__=='__main__':
    import json
    print(json.dumps(audit_printed_positional_table(),indent=2))
