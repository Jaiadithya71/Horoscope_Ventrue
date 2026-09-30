"""Local table14 lookup candidate for supplied Mercury centre, not global lookup."""
from decimal import Decimal, ROUND_HALF_UP


def mercury_lookup_candidate(centre='269.647'):
    c=Decimal(str(centre))
    if not Decimal(269) <= c <= Decimal(270):
        raise ValueError('Only visually verified table14 rows269 and270 supported')
    f=Decimal(270)-c
    # Right-hand 270/269 columns select the negative inantara and first coefficient.
    rows={270:{'inantara':'-21.162','radius':'1072','first':'-.0499','second':'.36','third':'.13'},
          269:{'inantara':'-21.290','radius':'1066','first':'-.0506','second':'.35','third':'.13'}}
    values={k:Decimal(rows[270][k])+f*(Decimal(rows[269][k])-Decimal(rows[270][k]))
            for k in rows[270]}
    precisions={'inantara':'.001','radius':'.1','first':'.001','second':'.01','third':'.01'}
    rounded={k:str(v.quantize(Decimal(precisions[k]),rounding=ROUND_HALF_UP)) for k,v in values.items()}
    return {'source':{'url':'https://archive.org/details/jyotir-ganita-venkatesh-ramakrishna-kethkar-dattatreya-ketkar-surakant-jha',
          'pdf_pages':[174,231],'printed_pages':[107,164],'table':'14 Mercury rows90/91, mirrored269/270',
          'verified_against_page_image':True},
        'input_sighra_centre_degrees':str(c),'rows':rows,'fraction_from270_to269':str(f),
        'candidate_interpolation':'linear_between_printed_adjacent_rows',
        'computed':{k:str(v) for k,v in values.items()},'rounded_candidate':rounded,
        'printed_narrative':{'inantara':'-21.207','radius':'1069.9','first':'-.050','second':'.36','third':'.13'},
        'matches_narrative_at_candidate_precision':all(Decimal(rounded[k])==Decimal(v) for k,v in
             {'inantara':'-21.207','radius':'1069.9','first':'-.050','second':'.36','third':'.13'}.items()),
        'source_selects_unique_rounding':False,'arbitrary_date_lookup_complete':False,
        'notice':'Actual row lookup reproduces five supplied Mercury narrative inputs at stated candidate precision. Mirrored columns carry different signs, not a blanket positive lookup. Half-up/linear remains a local candidate, not inferred as the entire book rule. Centre itself and upstream manda residual/samanantara still supplied.'}
