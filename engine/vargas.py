"""Original-page-checked six-varga geometry and owner evidence, not a score."""
import math
from fractions import Fraction
from .forecast import SIGNS
from .synthesis import LORDS
from .friendship import natural_relation, CLASSICAL

SOURCE={'slug':'phaladeepika-1937','pdf_page':62,'printed_page':25,
        'chapter':'III','sloka':4,'verified_against_page_image':True}
DEFINITION_SOURCE={'slug':'phaladeepika-1937','pdf_page':61,'printed_page':24,
                   'chapter':'III','sloka':'1-2','verified_against_page_image':True}


def six_vargas(longitude):
    if not math.isfinite(longitude) or not 0 <= longitude < 360:
        raise ValueError('Longitude must be finite and in [0,360)')
    # Decimal-to-rational partitioning avoids rounding exact 2.5/10/15 degree
    # boundaries backwards; repeating 3d20m inputs must use full precision.
    lon=Fraction(str(longitude));index=int(lon//30);degree=lon-index*30
    odd=index%2==0
    def sign_row(name,part,index):
        return {'varga':name,'part_1_based':part+1,'sign':SIGNS[index%12],
                'owner':LORDS[index%12],'source':SOURCE}
    rows=[sign_row('rasi',0,index)]
    hora=int(degree//15)
    rows.append({'varga':'hora','part_1_based':hora+1,'sign':None,
                 'owner':('Sun','Moon')[hora] if odd else ('Moon','Sun')[hora],
                 'source':SOURCE,'notice':'Verse gives owners of halves, not a selected modern D2 sign scheme'})
    drekkana=int(degree//10)
    rows.append(sign_row('drekkana',drekkana,index+4*drekkana))
    nav=int(degree*3//10)
    rows.append(sign_row('navamsa',nav,(0,9,6,3)[index%4]+nav))
    dwad=int(degree*2//5)
    rows.append(sign_row('dwadasamsa',dwad,index+dwad))
    rulers=('Mars','Saturn','Jupiter','Mercury','Venus') if odd else ('Venus','Mercury','Jupiter','Saturn','Mars')
    spans=(5,5,8,7,5) if odd else (5,7,8,5,5)
    begin=0
    for part,(ruler,span) in enumerate(zip(rulers,spans)):
        if begin<=degree<begin+span:
            rows.append({'varga':'trimsamsa','part_1_based':part+1,'sign':None,
                         'owner':ruler,'start_degree_in_sign':begin,'end_degree_in_sign':begin+span,
                         'source':SOURCE,'notice':'Unequal-degree owner bands; no unverified D30 sign assignment'})
            break
        begin+=span
    return {'sidereal_longitude':longitude,'vargas':rows,'definition_source':DEFINITION_SOURCE,
            'vargottama':rows[0]['sign']==rows[3]['sign'],
            'notice':'Geometry and owners only. No combined positional strength or personal effect.'}


def varga_owner_evidence(planet,longitude):
    result=six_vargas(longitude)
    for row in result['vargas']:
        row['own_owner']=row['owner']==planet
        row['natural_relation_to_owner']=('self' if row['own_owner'] else natural_relation(planet,row['owner'])) if planet in CLASSICAL else None
    result['planet']=planet
    result['score_status']='not_scored'
    result['notice']='Varga owners and natural relationships only; no sum, weighted strength, or unsupported varga sign assignment.'
    return result


SAPTAMSA_SOURCE={'slug':'sarvartha-chintamani-1899-part-1','chapter':'I','stanza':19,
                 'pdf_pages':[44,45],'printed_pages':[26,27],'verified_against_page_image':True,
                 'url':'https://archive.org/details/Astrology_Books_by_B_Suryanarayana_Row'}


def saptamsa(longitude):
    if not math.isfinite(longitude) or not 0<=longitude<360:
        raise ValueError('Longitude must be finite and in [0,360)')
    lon=Fraction(str(longitude));index=int(lon//30);degree=lon-index*30
    part=int(degree*7//30)
    target=(index+(0 if index%2==0 else 6)+part)%12
    return {'varga':'saptamsa','sidereal_longitude':longitude,'part_1_based':part+1,
            'sign':SIGNS[target],'owner':LORDS[target],'source':SAPTAMSA_SOURCE,
            'notice':'Seven equal divisions; own-sign start for odd signs, seventh-sign start for even. Geometry only, no children outcome or strength sum.'}


def seven_varga_owner_evidence(planet,longitude):
    result=varga_owner_evidence(planet,longitude)
    seventh=saptamsa(longitude)
    seventh['own_owner']=seventh['owner']==planet
    seventh['natural_relation_to_owner']=('self' if seventh['own_owner'] else natural_relation(planet,seventh['owner'])) if planet in CLASSICAL else None
    result['vargas'].insert(3,seventh)
    result['membership_source']={'slug':'sripatipaddhati-sastri-archive-203510','chapter':'III','sloka':3,
        'pdf_page':40,'printed_page':26,'verified_against_page_image':True,'url':'https://archive.org/details/dli.ernet.203510'}
    result['notice']='Seven-varga owner geometry from explicitly named sources, not a source-selected strength aggregation. Compound relations and alternative owner-strength interpretation remain unresolved.'
    return result
