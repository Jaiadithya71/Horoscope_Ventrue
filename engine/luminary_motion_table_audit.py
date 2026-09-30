"""Cross-table luminary identity, not a universal selected motion model."""
from decimal import Decimal
from .full_strength_table_audit import PRINTED,NAMES
from .continuous_strength import source
from .luminary_motion_identity import supplied_luminary_motion_identity


def luminary_motion_table_audit():
 sun=dict(zip(NAMES,PRINTED['Sun'][0].split()))
 moon=dict(zip(NAMES,PRINTED['Moon'][0].split()))
 rows=[{'planet':'Sun','printed_cheshta':sun['cheshta'],'comparison_component':'printed_ayana',
        'comparison_value':sun['ayana'],'comparison_source':source('15-16 Ayana worked table',69,55)},
       {'planet':'Moon','printed_cheshta':moon['cheshta'],'comparison_component':'printed_paksha',
        'comparison_value':'.518','comparison_source':source('11-12 Paksha worked table',59,45)}]
 for row in rows:
  row['exact_printed_equality']=Decimal(row['printed_cheshta'])==Decimal(row['comparison_value'])
  row['explicit_later_multiplier']=2
  row['doubled_comparison_not_substituted']=str(2*Decimal(row['comparison_value']))
  row['named_bphs_identity_corroboration']=supplied_luminary_motion_identity(row['planet'],float(row['comparison_value']),component_profile='Sripati printed undoubled worked-table component, not selected natal model')
  row['motion_source']=source('20 total table separate motion row',75,61)
  row['later_multiplier_source']=source('15-16 Sun Ayana/Moon Paksha doubling',66,52)
 return {'rows':rows,'universal_luminary_motion_rule_verified':False,
  'selected_III_motion_components':None,'IV_ray_components_substituted':False,
  'total_strength':None,
  'notice':'Equality of printed values is worked-example evidence only. Doubling passage and undoubled table remain distinct. The III expanded Sun motion+Ayana1.620 does not justify dropping one row or doubling every row. IVSun/Moon ray angles are separate transformations; no historical ephemeris reconstruction, universal rule or selected natal total follows.'}
