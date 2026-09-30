"""Sripati I.6-8 geometry from supplied ascendant/meridian anchors."""
import math

SOURCE={'slug':'sripatipaddhati-sastri-archive-203510','chapter':'I','sloka':'6-8',
        'pdf_pages':[25,26],'printed_pages':[11,12],'verified_against_page_image':True,
        'url':'https://archive.org/details/dli.ernet.203510'}


def bhava_geometry(ascendant_longitude,midheaven_longitude):
    for x in (ascendant_longitude,midheaven_longitude):
        if not math.isfinite(x) or not 0<=x<360:raise ValueError('Anchors must be finite in [0,360)')
    anchors={1:ascendant_longitude,4:(midheaven_longitude+180)%360,
             7:(ascendant_longitude+180)%360,10:midheaven_longitude}
    centres={}
    for n in (1,4,7,10):
        start=anchors[n];end=anchors[n+3 if n<10 else 1]
        arc=(end-start)%360
        if not 0<arc<180:raise ValueError('Supplied anchors do not form ordered nondegenerate quadrants')
        for k in range(3):centres[n+k]=(start+k*arc/3)%360
    boundaries={}
    for n in range(1,13):
        next_n=n+1 if n<12 else 1
        boundaries[n]=(centres[n]+((centres[next_n]-centres[n])%360)/2)%360
    return {'centres':centres,'boundary_after_house':boundaries,'source':SOURCE,
            'anchor_inputs':{'ascendant_longitude':ascendant_longitude,'midheaven_longitude':midheaven_longitude},
            'notice':'Quadrant trisection of supplied real anchors, not a whole-sign cusp system. Anchor astronomical calculation is not verified by this helper.'}


def house_membership(longitude,geometry,tolerance_degrees=1e-9):
    if not math.isfinite(longitude) or not 0<=longitude<360:raise ValueError('Longitude must be in [0,360)')
    if not math.isfinite(tolerance_degrees) or not 0<=tolerance_degrees<=.001:raise ValueError('Boundary tolerance must be in [0,.001]')
    boundaries=geometry['boundary_after_house']
    for n,b in boundaries.items():
        delta=abs((longitude-b+180)%360-180)
        if delta<=tolerance_degrees:
            return {'house':None,'at_sandhi':True,'between_houses':[n,n+1 if n<12 else 1],
                    'source':SOURCE,'notice':'Exact boundary held unresolved; no life effect asserted.'}
    for n in range(1,13):
        start=boundaries[n-1 if n>1 else 12];end=boundaries[n]
        if (longitude-start)%360<(end-start)%360:
            return {'house':n,'at_sandhi':False,'source':SOURCE,
                    'notice':'Degree-based membership, separate from whole-sign labels; no life effect asserted.'}
    raise ValueError('Invalid geometry')
