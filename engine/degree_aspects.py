"""Sripati II degree-aspect table profile, separate from whole-sign aspects."""
import math

CLASSICAL=('Sun','Moon','Mars','Mercury','Jupiter','Venus','Saturn')
BASE_QUARTERS=(0,0,1,3,2,0,4,3,2,1,0,0,0)
# Indices are longitude excesses in signs, NOT inclusive house numbers.
SPECIAL_KNOTS={'Jupiter':{4:4,8:4},'Saturn':{2:4,9:4},'Mars':{3:4,7:4}}
SOURCE={'slug':'sripatipaddhati-sastri-archive-203510','chapter':'II','sloka':'2-6',
        'pdf_pages':[31,32,33,34],'printed_pages':[17,18,19,20],
        'verified_against_page_image':True,'url':'https://archive.org/details/dli.ernet.203510'}


def degree_aspect(aspecting_planet,aspecting_longitude,aspected_longitude):
    if aspecting_planet not in CLASSICAL:raise ValueError('Classical aspecting planet required')
    for lon in (aspecting_longitude,aspected_longitude):
        if not math.isfinite(lon) or not 0<=lon<360:raise ValueError('Longitudes must be finite in [0,360)')
    excess=(aspected_longitude-aspecting_longitude)%360
    index=int(excess//30);fraction=(excess-index*30)/30
    knots=list(BASE_QUARTERS)
    for k,v in SPECIAL_KNOTS.get(aspecting_planet,{}).items():knots[k]=v
    base=(BASE_QUARTERS[index]+fraction*(BASE_QUARTERS[index+1]-BASE_QUARTERS[index]))/4
    total=(knots[index]+fraction*(knots[index+1]-knots[index]))/4
    return {'aspecting_planet':aspecting_planet,'aspecting_longitude':aspecting_longitude,
            'aspected_longitude':aspected_longitude,'directed_excess_degrees':excess,
            'profile':'sripati_degree_table_interpolation','base_rupa':base,
            'special_addition_rupa':total-base,'rupa':total,'virupa':total*60,
            'source':SOURCE,
            'translation_conflict_notice':('PDF34 prose says Jupiter excess3/4 but its explicit worked table, II.5 fifth/ninth places, and worked4sign16degree example support excess4/8. This profile follows those table knots, not the inconsistent prose.' if aspecting_planet=='Jupiter' else None),
            'notice':'Directed geometric aspect amount only. Not whole-sign aspects, benefic/malefic signed Drigbala, total strength, or an outcome. Quoted Parashara formula on PDF35-36 is not blended into this profile.'}


def degree_aspect_evidence(placements):
    rows=[]
    for a in CLASSICAL:
        if placements.get(a,{}).get('longitude') is None:continue
        for b in CLASSICAL:
            if b==a or placements.get(b,{}).get('longitude') is None:continue
            rows.append({'aspected_planet':b,**degree_aspect(a,placements[a]['longitude'],placements[b]['longitude'])})
    return {'directed_pairs':rows,'signed_total':None,'source':SOURCE,
            'notice':'Unsigned degree-aspect evidence only. Benefic/malefic classification, net Drigbala, war and full strength are not inferred.'}
