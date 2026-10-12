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


D4_SOURCE={'slug':'parashara-hora-ch1-10-sanskrit','chapter':'VI','sloka':9,
           'pdf_page':15,'printed_page':14,'verified_against_page_image':True,
           'url':'https://sanskritdocuments.org/doc_z_misc_sociology_astrology/par0110.pdf'}
D10_SOURCE={'slug':'parashara-hora-ch1-10-sanskrit','chapter':'VI','sloka':'13-14',
            'pdf_page':16,'printed_page':15,'verified_against_page_image':True,
            'url':'https://sanskritdocuments.org/doc_z_misc_sociology_astrology/par0110.pdf'}


def selected_divisional_geometry(longitude,division):
    """Named source geometry only. Does not feed predictions or strength totals."""
    if division not in (1,3,4,7,9,10):
        raise ValueError('Division not in the selected display profile')
    if not math.isfinite(longitude) or not 0<=longitude<360:
        raise ValueError('Longitude must be finite and in [0,360)')
    lon=Fraction(str(longitude));index=int(lon//30);degree=lon-index*30
    part=int(degree*division//30)
    if division in (1,3,9):
        name={1:'rasi',3:'drekkana',9:'navamsa'}[division]
        row=dict(next(x for x in six_vargas(longitude)['vargas'] if x['varga']==name))
        convention={1:'D1 natal sign',3:'Same, fifth, ninth signs (Phaladeepika III.4)',9:'Element-based start (Phaladeepika III.4)'}[division]
    elif division==7:
        row=saptamsa(longitude);convention='Odd: same-sign start; even: seventh-sign start (Sarvartha I.19)'
    else:
        target=(index+3*part)%12 if division==4 else (index+(0 if index%2==0 else 8)+part)%12
        row={'varga':'chaturthamsa' if division==4 else 'dasamsa','part_1_based':part+1,
             'sign':SIGNS[target],'owner':LORDS[target],'source':D4_SOURCE if division==4 else D10_SOURCE}
        convention='Same, fourth, seventh, tenth signs (Parashara VI.9)' if division==4 else 'Odd: same-sign start; even: ninth-sign start (Parashara VI.13-14)'
    row.update({'division':division,'natal_sign':SIGNS[index],
                'natal_degree_in_sign':float(degree),'part_1_based':part+1,
                'part_start_degree':float(Fraction(30*part,division)),
                'part_end_degree':float(Fraction(30*(part+1),division)),
                'convention':convention,'notice':'Start-inclusive/end-exclusive partition. Geometry only; no domain outcome or strength score.'})
    return row


def divisional_chart_report(chart):
    """Small public geometry bundle, including ascendant and opposite-point Ketu."""
    points={name:p['longitude'] for name,p in chart['placements'].items()}
    points['Ketu']=(points['Rahu']+180)%360
    points['Lagna']=chart['ascendant']['longitude']
    return {'profile':'source_named_divisional_geometry_v1',
            'charts':{str(d):{name:selected_divisional_geometry(lon,d) for name,lon in points.items()} for d in (1,3,4,7,9,10)},
            'node_mode':chart.get('node_mode','mean'),
            'notice':'Named source conventions, not the only varga conventions. Ketu derives from Rahu plus 180 degrees before division. Divisional Lagna and boundary placements depend on precise birth inputs. D2 sign scheme remains unselected. No new predictive rules.'}
