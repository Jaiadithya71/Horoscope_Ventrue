"""Actual local table11/13 candidates, including residual disagreement."""
from decimal import Decimal, ROUND_HALF_UP


def mercury_upstream_candidate():
    days=Decimal('54.086')  # Nyasa4 rows19/21/23 and III commentary.
    f=days-54
    centre=Decimal('208.038')+f*(Decimal('210.993')-Decimal('208.038'))
    residual=Decimal('63.3')+f*(Decimal('60.3')-Decimal('63.3'))
    solar_days=Decimal('92.597')
    samanantara=(solar_days-90)/10*Decimal('-1.1')
    return {'source':{'url':'https://archive.org/details/jyotir-ganita-venkatesh-ramakrishna-kethkar-dattatreya-ketkar-surakant-jha',
        'pdf_pages':[173,174,180,207,227],'printed_pages':[106,107,113,140,160],
        'verified_against_page_image':True,'tables':'11 Mercury rows54/55;13 Mercury rows90/100'},
        'printed_mercury_centre_days':str(days),'centre_days_prior_wake_typo':'54.069',
        'table11_rows':{'54':{'centre':'208.038','residual':'63.3'},
                        '55':{'centre':'210.993','residual':'60.3'}},
        'computed_manda_centre_degrees':str(centre),
        'rounded_candidate_centre_degrees':str(centre.quantize(Decimal('.001'),rounding=ROUND_HALF_UP)),
        'printed_table_manda_centre_degrees':'208.292',
        'computed_residual_linear_candidate':str(residual),
        'rounded_candidate_residual':str(residual.quantize(Decimal('.1'),rounding=ROUND_HALF_UP)),
        'printed_nyasa4_residual':'63.3','printed_III13_narrative_residual':'63.27',
        'linear_candidate_reproduces_printed_residual':False,
        'table13_rows':{'90':'0.0','100':'-1.1'},'sun_centre_days':str(solar_days),
        'computed_samanantara':str(samanantara),
        'rounded_candidate_samanantara':str(samanantara.quantize(Decimal('.01'),rounding=ROUND_HALF_UP)),
        'printed_narrative_samanantara':'-.28',
        'source_selects_unique_interpolation':False,'residual_selected_for_true_chain':None,
        'notice':'54.086 is page-verified;54.069 was a continuation-prompt typo, not source evidence. Two-row linear candidate reproduces printed manda centre208.292 but yields table13samanantara-.28567 (half-up-.29, narrative-.28) and residual63.042, rounded63.0, not Nyasa4 63.3 or narrative63.27. Do not infer a correction or fitted offset. Residual choice remains unresolved.'}
