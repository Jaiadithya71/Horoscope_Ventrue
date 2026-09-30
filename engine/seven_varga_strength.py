"""Explicit-input direct-owner Sripati III.2-3 profile, not automatic Shadbala."""
from .vargas import seven_varga_owner_evidence
from .friendship import CLASSICAL
from .continuous_strength import source

RELATION_RUPA={'very_friend':3/8,'friend':1/4,'neutral':1/8,'enemy':1/16,'very_enemy':1/32}


def direct_owner_seven_varga(planet,longitude,compound_relations,*,relation_profile,rasi_moolatrikona=None):
    """Unresolved owner relations or Moolatrikona leave total None, never default."""
    if planet not in CLASSICAL:raise ValueError('Classical planet required')
    if not relation_profile:raise ValueError('Named relation profile required')
    if rasi_moolatrikona is not None and type(rasi_moolatrikona) is not bool:raise ValueError('Moolatrikona requires bool or None')
    from .continuous_strength import valid_longitude
    valid_longitude(longitude)
    from .natal_factors import MOOLATRIKONA
    from .forecast import SIGNS
    sign,begin,end=MOOLATRIKONA[planet]
    expected_moola=SIGNS[int(longitude//30)]==sign and begin<=longitude%30<end
    if rasi_moolatrikona is not None and rasi_moolatrikona!=expected_moola:
        raise ValueError('Supplied Moolatrikona condition disagrees with checked Phaladeepika portion profile')
    result=seven_varga_owner_evidence(planet,longitude)
    missing=[]
    for row in result['vargas']:
        owner=row['owner'];rel='self' if owner==planet else compound_relations.get(owner)
        if rel is not None and rel!='self' and rel not in RELATION_RUPA:raise ValueError('Unknown compound relation')
        if rel=='self' and owner!=planet:raise ValueError('Self relation requires own owner')
        score=.5 if owner==planet else RELATION_RUPA.get(rel)
        if row['varga']=='rasi':
            if rasi_moolatrikona is None:score=None
            elif rasi_moolatrikona:score=.75
        if score is None:missing.append(row['varga'])
        row.update(compound_relation=rel,rupa=score)
    result.update(profile='sripati_direct_planet_to_varga_owner',relation_profile=relation_profile,
                  supplied_rasi_moolatrikona=rasi_moolatrikona,
                  moolatrikona_validation_source={'slug':'phaladeepika-1937','chapter':'I','sloka':7,'pdf_page':41,'printed_page':4,'verified_against_page_image':True},
                  rupa=None if missing else sum(x['rupa'] for x in result['vargas']),
                  unresolved_vargas=missing,score_status='partial' if missing else 'explicit_input_component',
                  strength_sources=[source('2-3',38,24),source('3',40,26),source('3 commentary',45,31)],
                  alternative_interpretation={'status':'not_calculated','source':source('3 commentary',46,32),
                      'notice':'Owner-own-placement alternative yields2.75 versus direct2.5 in the Sun example. Its printed integer/fraction values also differ. Not merged.'},
                  notice='Only a caller-selected direct-owner component. Supplied relation profile and Rasi Moolatrikona condition must be grounded externally. Cross-source geometry remains explicit. No positional or full strength sum, selected natal total, or outcomes.')
    return result
