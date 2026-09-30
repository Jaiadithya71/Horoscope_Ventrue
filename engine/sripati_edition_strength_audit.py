"""1919 versus archive fifth-edition worked rows; no print-fit correction."""
from decimal import Decimal
from .full_strength_table_audit import PRINTED,NAMES

EARLY={
 'Sun':('4.707 .949 .444 .810 .810 1.000','8.720','.295','0','9.015'),
 'Moon':('4.022 2.050 .037 .895 .518 .857','8.379','.109','.291','8.197'),
 'Mars':('3.667 2.013 .554 .662 .189 .285','7.370','.361','0','7.731'),
 'Mercury':('2.238 1.518 .260 .633 .794 .428','5.871','.338','0','6.209'),
 'Jupiter':('4.436 2.236 .887 .008 .795 .571','8.933','.261','.456','8.738'),
 'Venus':('2.811 2.236 .535 .784 .049 .714','7.129','.330','0','7.459'),
 'Saturn':('2.231 1.013 .074 .126 .026 .142','3.612','.196','0','3.808')}


def edition_strength_audit():
 rows=[]
 for planet,(pieces,subtotal,good,bad,final) in EARLY.items():
  comp=dict(zip(NAMES,pieces.split()));late=dict(zip(NAMES,PRINTED[planet][0].split()))
  total=sum(Decimal(x) for x in comp.values())
  rows.append({'planet':planet,'1919_printed_components':comp,'1919_printed_subtotal':subtotal,
    '1919_printed_final':final,'1919_component_sum':str(total),
    '1919_subtotal_matches':total==Decimal(subtotal),
    '1919_aspect_equation_matches':Decimal(subtotal)+Decimal(good)-Decimal(bad)==Decimal(final),
    'changed_component_rows':[{ 'component':k,'1919':comp[k],'archive_later':late[k]} for k in NAMES if Decimal(comp[k])!=Decimal(late[k])],
    'selected_component_values':None})
 return {'earlier_source':{'url':'https://archive.org/details/ksu.h1304.sripatipaddhati0000vsub',
   'edition_year':1919,'title_pdf_page':5,'table_pdf_page':114,'printed_page':98,'verified_against_page_image':True},
   'later_source':{'url':'https://archive.org/details/dli.ernet.203510','edition_note':'Registry identifies fifth edition1976, not1934',
   'table_pdf_page':75,'printed_page':61,'verified_against_page_image':True},
   'rows':rows,'earlier_subtotals_match':sum(r['1919_subtotal_matches'] for r in rows),
   'upstream_component_trace':{
    'jupiter':{'1919_navamsa_owner':'Jupiter','1919_navamsa_relation':'own',
     '1919_navamsa_rupa':'.5','later_navamsa_rupa':'.375',
     'seven_varga_delta':str(Decimal('3.25')-Decimal('3.125')),
     'positional_delta':str(Decimal('4.436')-Decimal('4.311')),
     'earlier_relation_source':{'pdf_page':95,'printed_page':79,'verified_against_page_image':True},
     'earlier_numeric_source':{'pdf_page':96,'printed_page':80,'verified_against_page_image':True},
     'earlier_positional_source':{'pdf_page':99,'printed_page':83,'verified_against_page_image':True},
     'later_numeric_source':{'pdf_page':49,'printed_page':35,'verified_against_page_image':True},
     'notice':'Own-owner Navamsa score is internally consistent in1919; later relation/score change needs independent chart reconstruction, not automatic import.'},
    'saturn':{'1919_local_motion_table_rupa':'.062','1919_aggregate_motion_rupa':'.026',
     'printed_cheshtakendra_degrees':'11.270','folded_angle_rupa':str(Decimal('11.270')/180),
     'earlier_local_source':{'pdf_page':113,'printed_page':97,'verified_against_page_image':True},
     'earlier_aggregate_source':{'pdf_page':114,'printed_page':98,'verified_against_page_image':True},
     'notice':'Earlier aggregate.026 reverses digits of local.062, but intent is unverified. Earlier exact subtotal closure therefore does not prove component correctness. Later.062 agrees with local table yet angle rounding remains separate.'}},
   'sun_doubling_allocation_resolved':False,'selected_natal_total':None,
   'notice':'Same translator across editions, not independent authority. Earlier MarsDig.554 closes its subtotal; later.534 does not. Jupiterpositional4.436 versus4.311 and Saturnmotion.026 versus.062 change complete rows. Earlier SunAyana.810 andCheshta.810 still appear separately, so edition comparison alone does not resolve universal multiplier allocation. The1919Saturn aggregate conflicts with its own local motion row despite exact aggregate sums. No earlier/later value automatically chosen or input reconstruction certified.'}
