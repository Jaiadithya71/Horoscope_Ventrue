"""Independent rational-second audit of Manual1935 illustrated1932 example."""
from fractions import Fraction as F
from decimal import Decimal as D
from .raman_manual_geometry_audit import SOURCE_URL
from .raman_daily_interpolation import raman_daily_interpolation


def seconds(dms):
    d,m,s=dms
    return d*3600+m*60+s

# Planet, preceding-noon as used by worked table, daily magnitude, printed
# traversal, Sayana at birth, row ayanamsa, readable Nirayana.
DATA=[
 ('Sun',(41,51,32),(0,58,11),(0,30,55),(42,22,27),(21,27,41),(20,54,46)),
 ('Moon',(6,31,20),(11,47,57),(6,16,0),(12,47,20),(20,27,41),(350,19,39)),
 ('Mars',(52,29,0),(0,46,0),(0,24,26),(52,53,26),(21,27,41),(31,25,45)),
 ('Mercury',(16,33,0),(0,40,0),(0,21,15),(16,54,15),(21,27,41),(355,26,34)),
 ('Jupiter',(133,29,0),(0,4,0),(0,2,8),(133,31,8),(21,27,41),(112,3,27)),
 ('Venus',(86,46,0),(0,51,0),(0,27,9),(87,13,9),(21,27,41),(65,45,28)),
 ('Saturn',(304,38,0),(0,1,0),(0,0,32),(304,38,32),(21,27,41),None),
 ('Rahu',(353,51,0),(0,3,0),(0,1,17),(353,49,43),(21,27,41),(332,22,2)),
]
TURN=360*3600


def raman_manual_frame_audit():
    rows=[]
    for planet,noon,daily,arc,sayana,aya,nirayana in DATA:
        sign=-1 if planet=='Rahu' else 1
        exact=F(seconds(daily)*17,32)
        exact_sayana=seconds(noon)+sign*exact
        printed_subtraction=(seconds(sayana)-seconds(aya))%TURN
        common_subtraction=(seconds(sayana)-seconds((21,27,41)))%TURN
        helper=raman_daily_interpolation(D(seconds(noon))/3600,D(seconds(daily))/3600,
            '12.75',D(seconds(aya))/3600,motion_direction='retrograde' if sign<0 else 'direct',
            ephemeris_profile='Manual1935 worked table inputs, not independently verified Raphael',
            clock_profile='printed12.75h from worked preceding Greenwich noon',frame_profile='printed row ayanamsa')
        rows.append({'planet':planet,'worked_noon_dms':list(noon),'daily_magnitude_dms':list(daily),
            'printed_traversal_dms':list(arc),'exact_traversal_arcseconds_rational':str(exact),
            'exact_minus_printed_traversal_arcseconds_rational':str(exact-seconds(arc)),
            'exact_minus_printed_sayana_arcseconds_rational':str(exact_sayana-seconds(sayana)),
            'printed_sayana_dms':list(sayana),'printed_ayanamsa_dms':list(aya),
            'readable_printed_nirayana_dms':list(nirayana) if nirayana is not None else None,
            'printed_row_subtraction_arcseconds':printed_subtraction,
            'common_ayanamsa_subtraction_arcseconds':common_subtraction,
            'row_subtraction_minus_printed_nirayana_arcseconds':printed_subtraction-seconds(nirayana) if nirayana else None,
            'common_subtraction_minus_printed_nirayana_arcseconds':common_subtraction-seconds(nirayana) if nirayana else None,
            'interpolation_helper_candidate':helper})
    # May1-noon353d51m with3m/day retrograde gives May2-noon353d48m.
    node_previous_day_correction=-180
    return {'rows':rows,'rahu_anchor_audit':{'ephemeris_excerpt_anchor_label':'1st May noon',
        'worked_table_anchor_label':'2nd May noon','difference_between_anchor_candidates_arcseconds':node_previous_day_correction,
        'may1_label_propagated_birth_sayana_arcseconds_rational':str(F(seconds((353,51,0)))+node_previous_day_correction-F(180*17,32)),
        'worked_anchor_birth_sayana_arcseconds_rational':str(F(seconds((353,51,0)))-F(180*17,32)),
        'selected_anchor':None},
        'ketu_printed_frame_check':{'printed_sayana_dms':[173,49,43],'printed_nirayana_dms':[132,22,2],
            'nirayana_subtraction_arcseconds':(seconds((173,49,43))-seconds((21,27,41)))%TURN,
            'opposition_to_printed_rahu_arcseconds':648000},
        'source':{'url':SOURCE_URL,'pdf_pages':[120,121,122],'printed_pages':[80,81,82],
            'article':'100, Example31','verified_against_page_image':True},
        'selected_ayanamsa':None,'selected_true_positions':None,'historical_ephemeris_verified':False,
        'notice':'Exact rational arithmetic independently audits displayed inputs, not Raphael ephemeris truth. Moon log-table minute rounding is explicit; its printed20degree ayanamsa disagrees with its output. Rahu May1/May2 anchor labels disagree. Saturn final Nirayana seconds obscured, not reconstructed as printed. Other tiny second differences are retained, not forced to a common rounding rule. Ketu is a printed opposition/frame check, not separately interpolated.'}
