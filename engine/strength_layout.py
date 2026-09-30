"""Sripati III.20 printed row layout versus inclusive motion class."""
from decimal import Decimal,InvalidOperation
from .continuous_strength import source


def supplied_layout_audit(components,*,layout,complete,component_profile):
 if type(complete) is not bool:raise ValueError('Complete declaration must be bool')
 if not isinstance(component_profile,str) or not component_profile.strip():raise ValueError('Named supplied component profile required')
 required={'sthana','kala','dig','natural','cheshta','ayana'} if layout=='expanded_printed_rows' else {'sthana','kala','dig','natural','cheshta_including_ayana'} if layout=='five_classes_inclusive_motion' else None
 if required is None:raise ValueError('Explicit known layout required')
 if not isinstance(components,dict) or set(components)-required:raise ValueError('Known component keys required; cannot mix inclusive and expanded motion')
 vals={}
 for k,v in components.items():
  if v is None:continue
  if isinstance(v,bool):raise ValueError('Finite nonnegative decimal components required')
  try:d=Decimal(str(v))
  except InvalidOperation as exc:raise ValueError('Decimal component required') from exc
  if not d.is_finite() or d<0:raise ValueError('Finite nonnegative base component required')
  vals[k]=d
 missing=sorted(required-set(vals))
 inclusive=None
 if layout=='expanded_printed_rows' and not {'cheshta','ayana'}-set(vals):inclusive=str(vals['cheshta']+vals['ayana'])
 elif layout=='five_classes_inclusive_motion':inclusive=str(vals['cheshta_including_ayana']) if 'cheshta_including_ayana' in vals else None
 return {'layout':layout,'component_profile':component_profile,'declared_complete':complete,
  'missing_base_components':missing,'inclusive_motion_rupa':inclusive,
  'supplied_base_sum_rupa':str(sum(vals.values())) if not missing and complete else None,
  'source':source('20 quoted Cheshta including Ayana and expanded table',74,60),
  'table_source':source('20 expanded component rows',75,61),
  'engine_computed_full_strength':None,'signed_aspect_adjustment':None,
  'notice':'Layout arithmetic on supplied declared components only. Completeness is not engine certification. Aspect adjustment, war treatment, component input/profile validation remain outside. Inclusive Cheshta must not receive another Ayana term. No selected full strength, rank or prediction.'}


def supplied_layout_with_aspects(components,*,layout,complete,component_profile,
                                  target,target_longitude,aspecting_placements,
                                  classifications,classification_profile,
                                  war_treatment):
 """III.20 assembly on declared supplied base, not a natal total calculator."""
 from .signed_aspect_strength import signed_aspect_adjustment
 if war_treatment not in ('confirmed_no_war','included_in_supplied_components','excluded_candidate'):
  raise ValueError('Explicit supplied war treatment required; no extra war transfer is applied')
 base=supplied_layout_audit(components,layout=layout,complete=complete,component_profile=component_profile)
 aspects=signed_aspect_adjustment(target,target_longitude,aspecting_placements,classifications,
                                  classification_profile=classification_profile)
 adjustment=aspects['signed_adjustment_rupa']
 candidate=None
 if base['supplied_base_sum_rupa'] is not None and adjustment is not None:
  candidate=str(Decimal(base['supplied_base_sum_rupa'])+Decimal(str(adjustment)))
 return {'planet':target,'supplied_layout':base,'aspect_evidence':aspects,
  'war_treatment':war_treatment,'candidate_total_rupa':candidate,
  'negative_candidate_total':None if candidate is None else Decimal(candidate)<0,
  'source':source('20',74,60),'engine_computed_full_strength':None,
  'notice':'III.20 signed quarter-aspect addition on explicitly complete supplied base only. Missing base/aspect inputs block arithmetic, not replaced with zero. Inclusive motion cannot duplicate Ayana. War declaration is supplied context, not validated detection; no additional war transfer or negative clipping. No ranking, threshold certification, selected natal total or prediction.'}
