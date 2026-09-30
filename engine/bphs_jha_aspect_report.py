"""Runnable supplied-coordinate JhaSudha aspect candidates and source audits."""
import argparse,json,sys
from .bphs_jha_general_aspect import jha_printed_aspect_audit
from .bphs_jha_special_aspect import bphs_jha_aspect_candidates,CLASSICAL
from .bphs_jha_drigbala import bphs_jha_drigbala


def bphs_jha_source_validation():
 return {'printed_arithmetic':jha_printed_aspect_audit(),
  'boundary_diagnostics':[bphs_jha_aspect_candidates(p,0,270,coordinate_profile='synthetic270degree boundary diagnostic, not a natal chart') for p in ('Saturn','Jupiter')],
  'synthetic_drigbala_bridge_check':bphs_jha_drigbala('Sun',{p:100 if p=='Sun' else 0 for p in CLASSICAL},
   dict.fromkeys(set(CLASSICAL)-{'Sun'},'benefic'),coordinate_profile='synthetic common frame, not historical chart',classification_profile='synthetic supplied classes, not natal classifications'),
  'unique_bphs_geometry_verified':False,'selected_natal_strength_total':None,
  'notice':'Page-verified independent edition formulas and exact arithmetic diagnostics, not repaired Santhanam tables, empirical accuracy or a source-selected natal model.'}


DRIG_INPUT_KEYS={'target','longitudes','classifications','coordinate_profile','classification_profile'}


def jha_drigbala_input_report(payload):
 if not isinstance(payload,dict) or set(payload)!=DRIG_INPUT_KEYS:raise ValueError('Exact target,longitudes,classifications,coordinate_profile,classification_profile fields required')
 return {'source_validation':bphs_jha_source_validation(),'supplied_drigbala_evidence':bphs_jha_drigbala(**payload),
  'chart_identity_match_verified':False,'total_strength':None,'personal_forecast':None,
  'notice':'Caller-supplied coordinates and classes remain a separate evidence lane. No modern birth chart is automatically relabeled historical, no source layout is inferred and no component is added to an existing Drik-inclusive strength.'}


def main():
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--input-json',help='Exact Drigbala JSON file or - for stdin; cannot combine coordinate flags')
 parser.add_argument('--aspecting-planet',choices=CLASSICAL)
 parser.add_argument('--aspector-longitude');parser.add_argument('--aspected-longitude');parser.add_argument('--coordinate-profile')
 args=parser.parse_args();values=(args.aspecting_planet,args.aspector_longitude,args.aspected_longitude,args.coordinate_profile)
 if args.input_json is not None:
  if any(v is not None for v in values):parser.error('JSON mode cannot combine coordinate flags')
  try:
   if args.input_json=='-':payload=json.load(sys.stdin)
   else:
    with open(args.input_json) as file:payload=json.load(file)
   print(json.dumps(jha_drigbala_input_report(payload),indent=2))
  except (ValueError,TypeError,OSError) as exc:parser.error(str(exc))
  return
 if any(v is not None for v in values) and not all(v is not None for v in values):parser.error('All four supplied-coordinate arguments required together')
 x={'source_validation':bphs_jha_source_validation(),'supplied_coordinate_candidates':None,'total_strength':None}
 if all(v is not None for v in values):
  try:x['supplied_coordinate_candidates']=bphs_jha_aspect_candidates(args.aspecting_planet,args.aspector_longitude,args.aspected_longitude,coordinate_profile=args.coordinate_profile)
  except ValueError as exc:parser.error(str(exc))
 print(json.dumps(x,indent=2))


if __name__=='__main__':main()
