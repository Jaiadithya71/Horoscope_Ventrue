"""Quoted three-khanda Ayana, distinct from six-increment declination."""
from .continuous_strength import valid_longitude,NEECHA,source
from .historical_declination import historical_ayana_from_longitude
from .sripati_worked_temporal_audit import longitude
from fractions import Fraction as F

RESIDUAL_SOURCE='http://jyotishvidya.com/ch27.htm'
EXAMPLE_SOURCE='https://saravali.github.io/astrology/bala_ayana.html'


def three_segment_ayana_candidates(planet,sayana_longitude):
    if planet not in NEECHA:raise ValueError('Classical planet required')
    valid_longitude(sayana_longitude)
    arc=sayana_longitude%180;distance=min(arc,180-arc)
    index=min(int(distance//30),2)
    prior=(0,45,78)[index];khanda=(45,33,12)[index]
    rows=[]
    for profile,degrees in [('residual_segment_degrees',distance-index*30),
                            ('literal_full_bhuja_degrees',distance)]:
        value=prior+degrees*F(khanda,30)
        positive=planet=='Mercury' or ((sayana_longitude<180) != (planet in ('Moon','Saturn')))
        base=(90+(value if positive else -value))/180
        rows.append({'profile':profile,'khanda_accumulated_value':float(value),
            'exact_khanda_accumulated_value':str(value) if isinstance(value,F) else None,
            'base_rupa':float(base),'exact_base_rupa':str(base) if isinstance(base,F) else None,
            'base_within_zero_one':0<=base<=1,
            'explicit_sun_double_rupa':float(2*base) if planet=='Sun' else None,
            'interpretation_source':RESIDUAL_SOURCE if profile=='residual_segment_degrees' else None})
    return {'planet':planet,'sayana_longitude_degrees':float(sayana_longitude),
        'nearest_equinox_distance_degrees':float(distance),'segment_index_0_based':index,
        'candidates':rows,'selected_profile':None,
        'quoted_book_sources':[source('15-16 quoted Parashara',68,54),source('15-16 quoted Parashara continued',69,55)],
        'clearer_book_source':{'url':'https://archive.org/details/ksu.h1304.sripatipaddhati0000vsub','pdf_pages':[110,111],'printed_pages':[94,95],'verified_against_page_image':True},
        'residual_interpretation_sources':[RESIDUAL_SOURCE,EXAMPLE_SOURCE],
        'notice':'Book translation does not explicitly subtract completed30degree segments. Separately fetched BPHS translation says degrees devoid of Rasi; modern worked examples clarify residual interpretation. Literal full-Bhuja diagnostic retained, never clipped when outside0..1. Residual extension makes30/60/90 boundaries continuous. No conflation with six-increment historical declination, multiplier choice or natal total.'}


def worked_three_segment_ayana_audit():
    ayanamsa=21+F(47,60)+F(38,3600);rows=[]
    for p in NEECHA:
        tropical=(longitude(p)+ayanamsa)%360
        three=three_segment_ayana_candidates(p,tropical)
        six=historical_ayana_from_longitude(p,float(tropical),longitude_profile='PrintedDMS+printedayanamsa')
        rows.append({'planet':p,'three_segment_candidates':three,
            'six_increment_base_rupa':six['ayana_candidates']['candidates'][0]['rupa'],
            'residual_minus_six_increment_base':three['candidates'][0]['base_rupa']-six['ayana_candidates']['candidates'][0]['rupa']})
    return {'rows':rows,'selected_model':None,'selected_natal_total':None,
        'notice':'Three-khanda and six-increment methods are distinct named source profiles, not interchangeable precision approximations or calibration targets. All seven supplied fixture inputs compared without fitting printed rows. External clarifications support residual segment interpretation only, not a universal full-strength school.'}
