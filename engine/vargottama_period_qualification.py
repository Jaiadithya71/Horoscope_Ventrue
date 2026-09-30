"""XX.22 favorable-to-mixed qualifier, never universal outcome precedence."""


def vargottama_period_qualification(vargottama,fall_sign,overpowered_sun_rays):
 for flag in (vargottama,fall_sign,overpowered_sun_rays):
  if flag is not None and type(flag) is not bool:raise ValueError('Grounded bool or unresolved None required')
 if vargottama is False:result='not_applicable'
 elif vargottama is None:result='unresolved_vargottama'
 elif fall_sign is True or overpowered_sun_rays is True:result='mixed_in_this_scoped_verse'
 elif fall_sign is None or overpowered_sun_rays is None:result='unresolved_qualifier'
 else:result='favorable_in_this_scoped_verse'
 return {'vargottama':vargottama,'fall_sign':fall_sign,'overpowered_sun_rays':overpowered_sun_rays,
    'scoped_textual_result':result,
    'source':{'slug':'phaladeepika-1937','chapter':'XX','sloka':22,'pdf_page':245,'printed_page':208,
       'url':'https://archive.org/details/in.ernet.dli.2015.92117','verified_against_page_image':True},
    'cross_checked_translation':{'url':'https://jyotishvidya.com/HTMLobj-9415/Mantreswara_s__Phaladeeplka_.pdf','pdf_page':186,'verified_against_page_image':True},
    'personal_outcome':None,'global_precedence':None,
    'notice':'Only qualifies this verse\'s Vargottama-period reading. Missing Sun-ray condition cannot mean uneclipsed. Does not override competing schools, dual lordship, simultaneous unfavorable main/subperiod conditions or calibrate a prediction.'}


def chart_vargottama_period_qualifications(placements):
 from .vargas import six_vargas
 from .natal_factors import dignity
 rows={}
 for planet,p in placements.items():
  d=dignity(planet,p['sign'],p.get('longitude'))
  if d.get('status')=='not_scored':continue
  v=None if p.get('longitude') is None else six_vargas(p['longitude'])['vargottama']
  rows[planet]=vargottama_period_qualification(v,d['flags']['fall_sign'],p.get('overpowered_sun_rays'))
 return {'planets':rows,'active_period':None,'personal_outcome':None,
    'notice':'Natal geometric candidate qualifications only. No active date, default eclipse flag, school choice or personal period forecast inferred.'}
