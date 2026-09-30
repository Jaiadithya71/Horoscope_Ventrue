"""III.3-4 printed seven-varga precision audit, no friendship reconstruction."""
from decimal import Decimal
from fractions import Fraction
from .continuous_strength import source

PRINTED={
 'Sun':('.375 .375 .5 .5 .25 .375 .125','2.5'),
 'Moon':('.25 .5 .25 .25 .25 .375 .25','2.125'),
 'Mars':('.375 .375 .5 .375 .375 .25 .5','2.75'),
 'Mercury':('.25 .375 .062 .25 .25 .25 .25','1.687'),
 'Jupiter':('.75 .125 .5 .5 .375 .5 .375','3.125'),
 'Venus':('.25 .031 .031 .125 .031 .375 .062','.905'),
 'Saturn':('.125 .125 .062 .125 .062 .062 .125','.689')}
FRACTIONS={'.031':Fraction(1,32),'.062':Fraction(1,16)}


def audit_printed_seven_varga_table():
 rows=[]
 for planet,(s,total) in PRINTED.items():
  vals=s.split();decimal_sum=sum(Decimal(v) for v in vals)
  exact=sum((FRACTIONS.get(v,Fraction(v)) for v in vals),Fraction(0))
  rows.append({'planet':planet,'printed_varga_values':vals,'printed_decimal_sum':str(decimal_sum),
     'printed_total':total,'decimal_sum_matches_printed_total':decimal_sum==Decimal(total),
     'exact_fraction_sum_if_fractional_relation_values_used':str(exact),'exact_fraction_sum_rupa':float(exact),
     'fraction_interpretation_notice':'Only .031/.062 are replaced by cited1/32,1/16 relation units for precision comparison, not recomputed relations or chart geometry.',
     'source':source('3-4 seven-varga table',49,35)})
 return {'rows':rows,'decimal_sums_matching':sum(r['decimal_sum_matches_printed_total'] for r in rows),
    'selected_natal_component':None,
    'notice':'Venus printed entries legitimately sum.905, equal to its separate Uchcha by coincidence; exact units give.90625. Saturn entries sum.686, printed total.689, exact units.6875. PDF53 uses.686. None is corrected or used as a chart algorithm oracle.'}
