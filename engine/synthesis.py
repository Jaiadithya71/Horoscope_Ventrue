"""Source-traced structural synthesis, not an automatic outcome predictor."""
from .forecast import SIGNS, sign_index

LORDS=('Mars','Venus','Mercury','Moon','Sun','Mercury','Venus','Mars',
       'Jupiter','Saturn','Saturn','Jupiter')
LORD_SOURCE={'slug':'phaladeepika-1937','pdf_page':40,'printed_page':3,
             'chapter':'I','sloka':6,'verified_against_page_image':True}
ASPECT_SOURCE={'slug':'phaladeepika-1937','pdf_page':55,'printed_page':18,
               'chapter':'II','sloka':23,'verified_against_page_image':True}
DERIVED_SOURCE={'slug':'phaladeepika-1937','pdf_page':197,'printed_page':160,
                'chapter':'XV','sloka':20,'verified_against_page_image':True}
TOPICS={2:'wealth',5:'children',7:'partnership',10:'work',11:'gain'}
# A topic label is metadata only, not a promise the aspect produces that outcome.
TOPIC_SOURCES={2:{'slug':'phaladeepika-1937','pdf_page':197,'printed_page':160,'chapter':'XV','sloka':20,'verified_against_page_image':True},
               5:{'slug':'phaladeepika-1937','pdf_page':196,'printed_page':159,'chapter':'XV','sloka':17,'verified_against_page_image':True},
               7:{'slug':'phaladeepika-1937','pdf_page':196,'printed_page':159,'chapter':'XV','sloka':17,'verified_against_page_image':True},
               10:{'slug':'phaladeepika-1937','pdf_page':196,'printed_page':159,'chapter':'XV','sloka':17,'verified_against_page_image':True},
               11:{'slug':'phaladeepika-1937','pdf_page':196,'printed_page':159,'chapter':'XV','sloka':17,'verified_against_page_image':True}}


def lordship(reference_sign):
    i=sign_index(reference_sign)
    return {'reference_sign':SIGNS[i], 'houses':[
        {'house':h,'sign':SIGNS[(i+h-1)%12], 'lord':LORDS[(i+h-1)%12]}
        for h in range(1,13)],'source':LORD_SOURCE,
        'notice':'Sign ownership only; strength and effect are not inferred.'}


def aspects(planet, from_sign, reference_sign):
    """Whole-sign aspect targets from the planet, measured against a reference sign.

    For the prototype only full aspects are emitted. Nodes have no rule here.
    Phaladeepika IV.9 describes a competing emphasis on seventh vs special
    aspects; record both references rather than claiming universal precedence.
    """
    if planet in ('Rahu','Ketu'):
        return {'planet':planet,'targets':[],'notice':'Node aspects not enabled by this checked verse.'}
    if planet not in ('Sun','Moon','Mars','Mercury','Jupiter','Venus','Saturn'):
        raise ValueError('Unknown planet')
    from_i,ref_i=sign_index(from_sign),sign_index(reference_sign)
    full={7}
    full|={'Mars':{4,8},'Jupiter':{5,9},'Saturn':{3,10}}.get(planet,set())
    targets=[]
    for relative in sorted(full):
        target=(from_i+relative-1)%12
        house=(target-ref_i)%12+1
        targets.append({'relative_house_from_planet':relative,'target_sign':SIGNS[target],
                        'target_house_from_reference':house,'topic_label':TOPICS.get(house), 'topic_source':TOPIC_SOURCES.get(house),
                        'special':relative!=7})
    return {'planet':planet,'from_sign':SIGNS[from_i],'reference_sign':SIGNS[ref_i],
            'targets':targets,'source':ASPECT_SOURCE,
            'notice':'Geometric whole-sign aspects and topic tags only, not asserted outcomes or strength. IV.9 (PDF p. 74) notes differing views on special-aspect efficacy.'}


def structural_factors(reference_sign, placements):
    """Traceable positional evidence to feed rules; do not invent a reading."""
    owners=lordship(reference_sign)
    links=[]
    for planet, position in placements.items():
        sign=position['sign']
        own=[row['house'] for row in owners['houses'] if row['lord']==planet]
        link={'planet':planet,'sign':sign,'house_from_reference':(sign_index(sign)-sign_index(reference_sign))%12+1,
              'rules_owned':own,'aspects':aspects(planet,sign,reference_sign)['targets'],
              'sources':{'lordship':LORD_SOURCE,'aspects':ASPECT_SOURCE,'derived_house':DERIVED_SOURCE}}
        links.append(link)
    return {'reference_sign':reference_sign,'lordships':owners,'planet_factors':links,
            'notice':'Structural chart factors only. A topic label or aspect is not a forecast; an outcome requires a verified conditional rule, natal context, timing, and conflict handling.'}
