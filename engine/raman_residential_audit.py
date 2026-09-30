"""Independent Raman residential example audit, not a strength total."""
from decimal import Decimal as D
from .raman_motion_source_audit import SOURCE_URL
from .bhava_geometry import bhava_geometry
from .bhava_effectiveness import bhava_effectiveness

ROWS=[('Sun',(180,53,55),9,(13,22,25),(16,21,30),'.80'),
      ('Moon',(311,17,19),1,(3,31,11),(16,21,30),'.24'),
      ('Mars',(229,30,34),10,(0,43,56),(13,38,30),'.11'),
      ('Mercury',(181,31,34),9,(14,0,4),(16,21,30),'.89'),
      ('Jupiter',(84,0,49),6,(6,29,19),(13,38,30),'.48'),
      ('Venus',(171,9,56),9,(3,38,26),(16,21,30),'.22'),
      ('Saturn',(124,22,41),7,(10,25,49),(16,21,30),'.64'),
      ('Rahu',(234,23,47),11,(4,9,17),(13,38,30),'.30'),
      ('Ketu',(54,23,47),5,(4,9,17),(13,38,30),'.30')]


def seconds(x):return x[0]*3600+x[1]*60+x[2]


def raman_residential_audit():
    geometry=bhava_geometry(298+27/60,216+30/60);rows=[]
    for p,long,house,arc,half,printed in ROWS:
        ratio=D(seconds(arc))/seconds(half)
        evidence=bhava_effectiveness(seconds(long)/3600,geometry)
        rows.append({'planet':p,'opening_longitude_dms':list(long),'printed_house':house,
            'printed_arc_dms':list(arc),'printed_half_width_dms':list(half),'printed_fraction':printed,
            'exact_arc_over_half_fraction':str(ratio),'absolute_printed_difference':str(abs(ratio-D(printed))),
            'anchor_route_difference_from_printed_arc_ratio':str(D(str(evidence['historical_effect_fraction']))-ratio),
            'independent_geometry_evidence':evidence})
    return {'rows':rows,'source':{'url':SOURCE_URL,'pdf_pages':[8,11,12,13,14],
        'printed_pages':[3,6,7,8,9],'verified_against_page_image':True},
        'selected_residential_fraction':None,'total_strength':None,
        'notice':'Actual printed anchors/coordinates under independent Sripati geometry reproduce local memberships, but not the later printed boundary/half-width ratios. The two routes remain separate, not reconciled by changed anchors. Residential-effect fraction is not a seventh Shadbala term or probability. Printed Moon.24, Mars.11, Mercury.89 remain discrepancies, not fitted targets. Nodes are included only in this supplied residential fixture, not classical motional strength.'}
