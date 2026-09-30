"""Worked categorical relations against explicitly named candidate sources."""
from fractions import Fraction
from .sripati_worked_navamsa_audit import WORKED_DMS
from .forecast import SIGNS
from .bhava_geometry import bhava_geometry,house_membership
from .friendship import compound_relationship_candidates
from .vargas import seven_varga_owner_evidence

# Page-image transcription of1919PDF95/79, in seven-varga order.
PRINTED_RELATIONS={
 'Sun':('very_friend','very_friend','self','self','friend','very_friend','neutral'),
 'Moon':('friend','self','friend','friend','friend','very_friend','friend'),
 'Mars':('very_friend','very_friend','self','very_friend','very_friend','friend','self'),
 'Mercury':('friend','very_friend','enemy','friend','friend','friend','friend'),
 'Jupiter':('moolatrikona','neutral','self','self','self','self','very_friend'),
 'Venus':('friend','very_enemy','very_enemy','neutral','very_enemy','very_friend','enemy'),
 'Saturn':('neutral','neutral','enemy','neutral','enemy','enemy','neutral')}


def worked_relation_audit():
    geometry=bhava_geometry(14+31/60+46/3600,270+7+42/60+11/3600)
    placements={}
    for planet,(sign,degree,minute,second) in WORKED_DMS.items():
        lon=float(sign*30+degree+Fraction(minute,60)+Fraction(second,3600))
        placements[planet]={'sign':SIGNS[sign],'longitude':lon,
            'sripati_degree_house':house_membership(lon,geometry)}
    evidence=compound_relationship_candidates(placements)
    mapping={(pair['planet'],pair['other'],c['house_profile']):c['compound_relation']
        for pair in evidence['directed_pairs'] for c in pair['candidates']}
    rows=[]
    for planet,p in placements.items():
        for index,row in enumerate(seven_varga_owner_evidence(planet,p['longitude'])['vargas']):
            printed=PRINTED_RELATIONS[planet][index]
            candidates={}
            for profile in ('rasi_relative','lagna_bhava_relative'):
                relation='self' if row['owner']==planet else mapping[(planet,row['owner'],profile)]
                # Moolatrikona portion not certified here, only owner relations.
                candidates[profile]={'relation':relation,
                    'matches_printed':None if printed=='moolatrikona' else relation==printed}
            rows.append({'planet':planet,'varga':row['varga'],'geometry_owner':row['owner'],
                '1919_printed_relation':printed,'candidates':candidates})
    return {'rows':rows,'directed_relation_evidence':evidence,
        'worked_houses':{p:x['sripati_degree_house']['house'] for p,x in placements.items()},
        'anchor_source':{'url':'https://archive.org/details/ksu.h1304.sripatipaddhati0000vsub',
            'pdf_page':79,'printed_page':63,'verified_against_page_image':True,
            'ascendant_dms':[0,14,31,46],'midheaven_dms':[9,7,42,11]},
        'categorical_source':{'pdf_page':95,'printed_page':79,'verified_against_page_image':True},
        'profile_match_counts':{profile:sum(r['candidates'][profile]['matches_printed'] is True for r in rows)
            for profile in ('rasi_relative','lagna_bhava_relative')},
        'profiles_distinguished_by_example':any(r['candidate_conflict'] for r in evidence['directed_pairs']),
        'selected_relation_profile':None,'selected_strength_total':None,
        'notice':'Phaladeepika1937 natural plus Kapoor compound candidates, not Sripati source-selected relations.48comparable categorical rows exclude JupiterRasi Moolatrikona portion;47match both profiles, JupiterNavamsa own does not. SaturnDwadashamsa printed enemy matches computed Jupiter owner even though1919 owner handle saysSaturn. Rasi and LagnaBhava agree throughout this fixture, so agreement cannot distinguish conventions. Source says planet-recast alternative was not used (laterPDF43/29), but arbitrary charts remain separate profiles.'}
