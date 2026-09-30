"""Worked longitudes versus categorical Navamsa tables, explicit geometry source."""
from fractions import Fraction
from .vargas import seven_varga_owner_evidence

# Zero-based sign counts as printed; no modern ephemeris reconstruction.
WORKED_DMS = {
    'Sun': (0, 17, 43, 30), 'Moon': (9, 14, 29, 39),
    'Mars': (11, 27, 53, 9), 'Mercury': (11, 24, 13, 44),
    'Jupiter': (8, 1, 25, 1), 'Venus': (0, 14, 2, 56),
    'Saturn': (0, 27, 55, 41),
}
EARLY_SIGNS = {'Sun':'Virgo', 'Moon':'Taurus', 'Mars':'Pisces',
    'Mercury':'Aquarius', 'Jupiter':'Sagittarius', 'Venus':'Leo', 'Saturn':'Sagittarius'}
LATER_SIGNS = dict(EARLY_SIGNS, Jupiter='Aries')


def worked_navamsa_audit():
    rows = []
    for planet, (sign, degree, minute, second) in WORKED_DMS.items():
        exact = sign*30 + degree + Fraction(minute, 60) + Fraction(second, 3600)
        geometry = seven_varga_owner_evidence(planet, float(exact))
        nav = next(row for row in geometry['vargas'] if row['varga']=='navamsa')
        rows.append({'planet':planet, 'printed_longitude_dms':list(WORKED_DMS[planet]),
            'exact_longitude_degrees':str(exact), 'calculated_navamsa':nav,
            '1919_printed_navamsa_sign':EARLY_SIGNS[planet],
            'later_printed_navamsa_sign':LATER_SIGNS[planet],
            '1919_matches_named_geometry':nav['sign']==EARLY_SIGNS[planet],
            'later_matches_named_geometry':nav['sign']==LATER_SIGNS[planet]})
    return {'rows':rows,
        'longitude_source':{'url':'https://archive.org/details/ksu.h1304.sripatipaddhati0000vsub',
            'edition_year':1919, 'pdf_page':80, 'printed_page':64,
            'verified_against_page_image':True},
        '1919_relation_source':{'pdf_page':95,'printed_page':79,'verified_against_page_image':True},
        'later_relation_source':{'url':'https://archive.org/details/dli.ernet.203510',
            'pdf_page':48,'printed_page':34,'verified_against_page_image':True},
        'geometry_profile':'Phaladeepika1937 III.4 first Navamsas Aries/Capricorn/Libra/Cancer repeating',
        '1919_geometry_matches':sum(r['1919_matches_named_geometry'] for r in rows),
        'later_geometry_matches_for_1919_longitudes':sum(r['later_matches_named_geometry'] for r in rows),
        'selected_seven_varga_total':None,
        'notice':'Jupiter at Sagittarius1d25m1s is in the first Navamsa, Aries/Mars under the named geometry. This contradicts1919 Sagittarius/Jupiter/own but agrees with the later categorical row. Earlier score.5 follows its own categorical error; later.375 is compatible with its printed very-friend relation. Later original longitude table agrees (PDF17/3, checked separately); relation reconstruction and source-selected full strength remain unverified. No natal correction or historical ephemeris accuracy claimed.'}

# Owner handles transcribed independently from each page, not computed by sign.
# The later Saturn Dwadashamsa cell shows12 without a legible owner handle.
VARGA_ORDER = ('rasi','hora','drekkana','saptamsa','navamsa','dwadasamsa','trimsamsa')
EARLY_OWNERS = {
    'Sun':('Mars','Moon','Sun','Sun','Mercury','Mars','Jupiter'),
    'Moon':('Saturn','Moon','Venus','Venus','Venus','Mercury','Jupiter'),
    'Mars':('Jupiter','Sun','Mars','Jupiter','Jupiter','Saturn','Mars'),
    'Mercury':('Jupiter','Sun','Mars','Saturn','Saturn','Jupiter','Saturn'),
    'Jupiter':('Jupiter','Sun','Jupiter','Jupiter','Jupiter','Jupiter','Mars'),
    'Venus':('Mars','Sun','Sun','Moon','Sun','Mercury','Jupiter'),
    'Saturn':('Mars','Moon','Jupiter','Venus','Jupiter','Saturn','Venus'),
}
LATER_OWNERS = dict(EARLY_OWNERS,
    Jupiter=('Jupiter','Sun','Jupiter','Jupiter','Mars','Jupiter','Mars'),
    Saturn=('Mars','Moon','Jupiter','Venus','Jupiter',None,'Venus'))


def worked_seven_varga_owner_audit():
    rows=[]
    for planet,(sign,degree,minute,second) in WORKED_DMS.items():
        exact=sign*30+degree+Fraction(minute,60)+Fraction(second,3600)
        calculated=seven_varga_owner_evidence(planet,float(exact))
        for index,row in enumerate(calculated['vargas']):
            assert row['varga']==VARGA_ORDER[index]
            early=EARLY_OWNERS[planet][index];later=LATER_OWNERS[planet][index]
            rows.append({'planet':planet,'varga':row['varga'],
                'calculated_owner':row['owner'],'geometry_source':row['source'],
                '1919_printed_owner':early,'later_printed_owner':later,
                '1919_matches_named_geometry':early==row['owner'],
                'later_matches_named_geometry':None if later is None else later==row['owner']})
    return {'rows':rows,'sources':worked_navamsa_audit(),
        'later_longitude_source':{'url':'https://archive.org/details/dli.ernet.203510',
            'pdf_page':17,'printed_page':3,'verified_against_page_image':True,
            'all_seven_longitudes_match_1919':True},
        '1919_owner_matches':sum(r['1919_matches_named_geometry'] for r in rows),
        'later_comparable_owners':sum(r['later_printed_owner'] is not None for r in rows),
        'later_owner_matches':sum(r['later_matches_named_geometry'] is True for r in rows),
        'selected_strength_total':None,
        'notice':'Owner geometry only across49 cells, not categorical relationship or score certification.1919Jupiter Navamsa and Saturn Dwadashamsa owner handles disagree with named geometry. Later Saturn Dwadashamsa owner absent/unreadable is None, not inferred from printed sign12. Same worked longitudes verified in laterPDF17/3. Cross-source Phaladeepika and Sarvartha geometry remains explicit; no independent historical ephemeris reconstruction.'}
