"""Exact supplied-longitude six-part Ayana audit; no multiplier selection."""
from fractions import Fraction as F
from .sripati_worked_temporal_audit import longitude
from .historical_declination import historical_ayana_from_longitude,INCREMENTS_ARCMINUTES

DECL={'Sun':'14.877','Moon':'-18.984','Mars':'7.806','Mercury':'6.420',
      'Jupiter':'-23.607','Venus':'13.657','Saturn':'17.938'}
AYANA={'Sun':'.810','Moon':'.895','Mars':'.662','Mercury':'.633',
       'Jupiter':'.008','Venus':'.784','Saturn':'.126'}


def worked_ayana_audit():
    ayanamsa=21+F(47,60)+F(38,3600);rows=[]
    for p in DECL:
        tropical=(longitude(p)+ayanamsa)%360
        folded=tropical%180;distance=min(folded,180-folded)
        index=min(int(distance//15),6)
        minutes=F(sum(INCREMENTS_ARCMINUTES[:index]))
        if index<6:minutes+=(distance-index*15)/15*INCREMENTS_ARCMINUTES[index]
        decl=minutes/60*(1 if tropical<180 else -1)
        adjusted=abs(decl) if p=='Mercury' else -decl if p in ('Moon','Saturn') else decl
        base=(24+adjusted)/48
        pipeline=historical_ayana_from_longitude(p,float(tropical),longitude_profile='Printed DMS plus printed21d47m38s ayanamsa')
        rows.append({'planet':p,'exact_sayana_longitude_degrees':str(tropical),
            'exact_declination_degrees':str(decl),'calculated_declination_degrees':float(decl),
            'printed_declination_both_editions':DECL[p],
            'declination_abs_floor3_matches':F(int(abs(decl)*1000),1000)==abs(F(DECL[p])),
            'exact_base_ayana_rupa':str(base),'calculated_base_ayana_rupa':float(base),
            'printed_ayana_both_editions':AYANA[p],
            'base_floor3_matches':F(int(base*1000),1000)==F(AYANA[p]),
            'pipeline_exact_agreement':abs(pipeline['historical_declination']['declination_degrees']-float(decl))<1e-12 and abs(pipeline['ayana_candidates']['candidates'][0]['rupa']-float(base))<1e-12,
            'ayana_pipeline_candidates':pipeline['ayana_candidates'],
            'exact_explicit_sun_double_rupa':str(2*base) if p=='Sun' else None})
    return {'supplied_ayanamsa_degrees':str(ayanamsa),'rows':rows,
        'declination_floor3_matches':sum(r['declination_abs_floor3_matches'] for r in rows),
        'ayana_base_floor3_matches':sum(r['base_floor3_matches'] for r in rows),
        'sources':[
            {'url':'https://archive.org/details/dli.ernet.203510','pdf_pages':[17,67,69],'printed_pages':[3,53,55],'verified_against_page_image':True},
            {'url':'https://archive.org/details/ksu.h1304.sripatipaddhati0000vsub','pdf_page':111,'printed_page':95,'verified_against_page_image':True}],
        'selected_ayana_values':None,'selected_natal_total':None,
        'notice':'Exact six-increment table using supplied DMS plus supplied ayanamsa cross-checks actual pipeline. Six declinations and six base strengths match floor3 diagnostic, not a universal rounding policy. Sun exact declination14.879053... differs from both printed14.877; base.809980... is near printed.810 but not floor3. Explicit doubledSun1.619960... remains distinct from printed undoubled.810 and motion allocation. No modern latitude/declination model, fitted correction, multiplier winner or natal total selected.'}
