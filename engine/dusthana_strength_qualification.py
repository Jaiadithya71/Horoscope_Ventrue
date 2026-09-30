"""Phaladeepika XV.9 local severity qualifier, not global strength precedence."""

SOURCE={'slug':'phaladeepika-1937','chapter':'XV','sloka':'9 continuation','pdf_page':193,
 'printed_page':156,'verified_against_page_image':True,
 'url':'https://archive.org/details/in.ernet.dli.2015.92117'}


def dusthana_strength_qualification(lord_occupied_house,*,supplied_strength_status,
                                    strength_profile,house_frame):
 if lord_occupied_house is not None and (type(lord_occupied_house) is not int or not 1<=lord_occupied_house<=12):
  raise ValueError('Occupied house1..12 or unresolved None required')
 if supplied_strength_status not in ('strong','weak',None):
  raise ValueError('Supplied strong/weak status or unresolved None required')
 if any(not isinstance(x,str) or not x.strip() for x in (strength_profile,house_frame)):
  raise ValueError('Explicit strength profile and house frame required')
 present=None if lord_occupied_house is None else lord_occupied_house in (6,8,12)
 result='unresolved_house' if present is None else 'not_applicable' if not present else (
  'unresolved_strength' if supplied_strength_status is None else
  'slight_injury_in_this_verse' if supplied_strength_status=='strong' else 'immensely_harmful_in_this_verse')
 return {'lord_occupied_house':lord_occupied_house,'house_frame':house_frame,
  'dusthana_condition':present,'supplied_strength_status':supplied_strength_status,
  'strength_profile':strength_profile,'scoped_textual_qualification':result,
  'source':SOURCE,'cross_checked_translation':{'url':'https://jyotishvidya.com/HTMLobj-9415/Mantreswara_s__Phaladeeplka_.pdf',
   'pdf_page':149,'chapter':'XV','sloka':9,'verified_against_page_image':True},
  'personal_outcome':None,'global_precedence':None,
  'notice':'Local severity qualification of the occupied lord in a dusthana only. Strong does not turn this verse favorable. Status is externally supplied, not inferred from dignity, retrograde motion, partial strength or an unselected total threshold. No numeric probability, event, time or universal override of XV.5 recovery/XV.10 Lagna ownership.'}


def chart_dusthana_strength_qualifications(ascendant_sign,placements,strength_statuses,*,strength_profile):
 from .forecast import sign_index
 from .synthesis import LORDS
 asc=sign_index(ascendant_sign);rows=[]
 for house in range(1,13):
  lord=LORDS[(asc+house-1)%12];p=placements.get(lord,{})
  occupied=None if p.get('sign') is None else (sign_index(p['sign'])-asc)%12+1
  rows.append({'target_house':house,'lord':lord,'qualification':dusthana_strength_qualification(
   occupied,supplied_strength_status=strength_statuses.get(lord),strength_profile=strength_profile,
   house_frame='whole_sign_from_supplied_ascendant_candidate')})
 return {'houses':rows,'personal_outcome':None,'selected_bhava_geometry':None,
  'notice':'Whole-sign candidate occupancy only, not Sripati degree-centre house certification. Each supplied strength status retains its profile; absent placement or status remains unknown.'}
