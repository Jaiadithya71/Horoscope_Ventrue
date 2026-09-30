"""Runnable supplied-coordinate JhaSudha aspect candidates and source audits."""
import argparse,json
from .bphs_jha_general_aspect import jha_printed_aspect_audit
from .bphs_jha_special_aspect import bphs_jha_aspect_candidates,CLASSICAL


def bphs_jha_source_validation():
 return {'printed_arithmetic':jha_printed_aspect_audit(),
  'boundary_diagnostics':[bphs_jha_aspect_candidates(p,0,270,coordinate_profile='synthetic270degree boundary diagnostic, not a natal chart') for p in ('Saturn','Jupiter')],
  'unique_bphs_geometry_verified':False,'selected_natal_strength_total':None,
  'notice':'Page-verified independent edition formulas and exact arithmetic diagnostics, not repaired Santhanam tables, empirical accuracy or a source-selected natal model.'}


def main():
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--aspecting-planet',choices=CLASSICAL)
 parser.add_argument('--aspector-longitude');parser.add_argument('--aspected-longitude');parser.add_argument('--coordinate-profile')
 args=parser.parse_args();values=(args.aspecting_planet,args.aspector_longitude,args.aspected_longitude,args.coordinate_profile)
 if any(v is not None for v in values) and not all(v is not None for v in values):parser.error('All four supplied-coordinate arguments required together')
 x={'source_validation':bphs_jha_source_validation(),'supplied_coordinate_candidates':None,'total_strength':None}
 if all(v is not None for v in values):
  try:x['supplied_coordinate_candidates']=bphs_jha_aspect_candidates(args.aspecting_planet,args.aspector_longitude,args.aspected_longitude,coordinate_profile=args.coordinate_profile)
  except ValueError as exc:parser.error(str(exc))
 print(json.dumps(x,indent=2))


if __name__=='__main__':main()
