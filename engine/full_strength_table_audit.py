"""Printed III.20 table consistency, not independently reconstructed Shadbala."""
from decimal import Decimal
from .continuous_strength import source
from .positional_table_audit import PRINTED as POSITIONAL

PRINTED={
 'Sun':('4.707 .949 .444 .810 .810 1.000','8.720','.295','0','9.015'),
 'Moon':('4.022 2.050 .037 .895 .518 .857','8.379','.109','.291','8.197'),
 'Mars':('3.667 2.013 .534 .662 .189 .285','7.370','.361','0','7.731'),
 'Mercury':('2.238 1.518 .260 .633 .794 .428','5.871','.338','0','6.209'),
 'Jupiter':('4.311 2.236 .887 .008 .795 .571','8.808','.261','.456','8.613'),
 'Venus':('2.811 2.236 .535 .784 .049 .714','7.129','.330','0','7.459'),
 'Saturn':('2.231 1.013 .074 .126 .062 .142','3.648','.196','0','3.844')}
NAMES=('sthana','kala','dig','ayana','cheshta','natural')


def audit_printed_full_strength_table():
 rows=[]
 for planet,(pieces,subtotal,benefic,malefic,final) in PRINTED.items():
  components=dict(zip(NAMES,pieces.split()))
  computed=sum(Decimal(x) for x in components.values())
  adjustment=Decimal(benefic)-Decimal(malefic)
  s,f=Decimal(subtotal),Decimal(final)
  rows.append({'planet':planet,'printed_components':components,
     'sum_of_printed_components':str(computed),'printed_subtotal':subtotal,
     'subtotal_delta':str(computed-s),'subtotal_matches':computed==s,
     'printed_quarter_benefic':benefic,'printed_quarter_malefic':malefic,
     'printed_final':final,'printed_subtotal_adjusted':str(s+adjustment),
     'aspect_equation_matches':s+adjustment==f,
     'component_sum_adjusted':str(computed+adjustment),
     'prior_positional_table':POSITIONAL[planet][-1],
     'cross_table_positional_delta':str(Decimal(components['sthana'])-Decimal(POSITIONAL[planet][-1])),
     'source':source('20-21 printed full-strength table',75,61)})
 return {'rows':rows,'subtotal_matches':sum(r['subtotal_matches'] for r in rows),
    'aspect_equations_match':sum(r['aspect_equation_matches'] for r in rows),
    'computed_natal_total':None,'selected_profile':None,
    'notice':'Exact decimal consistency only. Mars printed components sum7.350 not printed7.370; Venus/Saturn positional values shift by.001 from PDF53. No correction, rounding explanation, full-profile selection or chart-derived total inferred. III20 prose describes five classes but printed table separately includes Ayana; enumeration conflict remains.'}
