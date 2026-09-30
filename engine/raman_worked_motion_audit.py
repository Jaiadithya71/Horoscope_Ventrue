"""Compare Raman's printed rounded motion triples with opening true coordinates."""
from decimal import Decimal as D
from .raman_motion_source_audit import SOURCE_URL

DATA=[('Mars','266.34','229.50','181.23',(229,30,34),'293.31'),
      ('Mercury','181.23','181.52','174.49',(181,31,34),'353.11'),
      ('Jupiter','66.91','84.01','181.23',(84,0,49),'105.77'),
      ('Venus','181.23','171.16','158.35',(171,9,56),'342.15'),
      ('Saturn','111.23','124.39','181.23',(124,22,41),'63.42')]


def raman_worked_motion_audit():
    rows=[]
    for p,m,rounded,sighra,dms,printed in DATA:
        exact=D(dms[0])+D(dms[1])/60+D(dms[2])/3600
        variants=[]
        for profile,true in [('printed_motion_decimal_true',D(rounded)),('opening_sexagesimal_true',exact)]:
            k=(D(sighra)-(D(m)+true)/2)%360;k=(k+360)%360;fold=min(k,360-k)
            variants.append({'true_input_profile':profile,'true_degrees':str(true),'cheshtakendra_degrees':str(k),
                'folded_degrees':str(fold),'virupa':str(fold/3),'difference_from_printed_kendra_degrees':str(k-D(printed))})
        rows.append({'planet':p,'printed_mean_degrees':m,'printed_sighra_degrees':sighra,
            'opening_true_dms':list(dms),'printed_kendra_degrees':printed,'arithmetic_candidates':variants})
    return {'rows':rows,'coordinate_frame_evidence':{
        'opening_true_label':'Nirayana/ex-precession','mean_sun_label':'ex-precession',
        'pdf_pages':[7,76,82,83],'printed_pages':[2,71,77,78],'url':SOURCE_URL,'verified_against_page_image':True},
        'selected_motion_input':None,'arbitrary_date_ephemeris_verified':False,'universal_wrap_rule_verified':False,
        'notice':'Independent printed input comparison, not reconstruction of true longitudes. Same displayed0..360 branch as this example only. Mean/Sighra values retain source discrepancies. Decimal and sexagesimal true coordinates are separate; neither is altered to force printed angles. Source frame labels do not identify a modern ayanamsa or arbitrary-date model.'}
