"""Historical XV.13-14 geometric effect fraction, not scientific probability."""
from .bhava_geometry import house_membership
from .continuous_strength import valid_longitude

SOURCE={'slug':'phaladeepika-1937','chapter':'XV','sloka':'13-14','pdf_page':194,
        'printed_page':157,'verified_against_page_image':True,
        'url':'https://archive.org/details/in.ernet.dli.2015.92117'}


def bhava_effectiveness(longitude,geometry):
    valid_longitude(longitude)
    member=house_membership(longitude,geometry,tolerance_degrees=0)
    if member['at_sandhi']:
        return {'membership':member,'historical_effect_fraction':0.0,'source':SOURCE,
                'qualifies_despite_strength':True,'notice':'Exact supplied geometric Sandhi, not a near-boundary orb. House assignment remains unresolved. Traditional clause only, not a probability or event forecast.'}
    house=member['house'];centre=geometry['centres'][house]
    before=geometry['boundary_after_house'][house-1 if house>1 else 12]
    after=geometry['boundary_after_house'][house]
    # Unwrap longitude relative to preceding Sandhi in this local house arc.
    width=(after-before)%360;centre_offset=(centre-before)%360;x=(longitude-before)%360
    if not 0<centre_offset<width or not 0<=x<=width:raise ValueError('Invalid supplied geometry')
    fraction=x/centre_offset if x<=centre_offset else (width-x)/(width-centre_offset)
    return {'membership':member,'historical_effect_fraction':fraction,
            'source':SOURCE,'qualifies_despite_strength':False,
            'notice':'Linear rule-of-three between supplied centre/full and Sandhi/zero. This fraction is historical geometric evidence only, not strength, probability, favorability, timing or outcome. No near-Sandhi cutoff inferred.'}
