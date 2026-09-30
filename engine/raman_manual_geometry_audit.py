"""Compare Manual construction with its printed example and later book inputs."""
from .bhava_geometry import bhava_geometry

SOURCE_URL='https://archive.org/details/AManualOfHinduAstrologyBVRaman1935Edition'


def raman_manual_geometry_audit():
    manual=bhava_geometry(294+57/60,214+55/60)
    later=bhava_geometry(298+27/60,216+30/60)
    # ActualPDF114/printed74, six listed Arambha-sandhis.
    begins=[(281,36,40),(311,36,40),(344,56,0),(18,15,20),(48,15,20),(74,56,0)]
    rows=[]
    for house,dms in enumerate(begins,1):
        printed=dms[0]+dms[1]/60+dms[2]/3600
        before=house-1 if house>1 else 12
        calculated=manual['boundary_after_house'][before]
        rows.append({'house':house,'printed_beginning_dms':list(dms),'calculated_beginning_degrees':calculated,
            'signed_degree_difference':(calculated-printed+180)%360-180})
    return {'manual_1935_geometry':manual,'later_graha_balas_opening_geometry':later,
        'manual_printed_beginning_comparisons':rows,
        'seventh_centre_audit':{'printed_table_degrees':144+57/60,
            'rule_example_degrees':114+57/60,'computed_from_opposite_ascendant':manual['centres'][7]},
        'source':{'url':SOURCE_URL,'pdf_pages':[109,110,111,113,114],'printed_pages':[69,70,71,73,74],
            'verified_against_page_image':True},
        'selected_anchor_set':None,'residential_disagreement_resolved':False,
        'notice':'Art88 ecliptic-quadrant trisection and art90 adjacent-centre midpoints corroborate the named geometry, not the astronomical anchors. Manual1935 worked anchors differ from later Graha Balas opening anchors. Manual tableVII144deg57min disagrees with its opposite-Ascendant rule/example114deg57min. No inferred edition correction, replacement anchors or residential fit.'}
