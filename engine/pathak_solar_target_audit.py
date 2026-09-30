"""Independent Pathak XIX.3-4 angular-target commentary, not a civil oracle."""
from fractions import Fraction as F
from .bphs_jha_general_aspect import dms

SOURCE_URL = 'https://archive.org/details/phala-dipika-of-shri-mantreshwar-hindi-commentary-by-dr.-hari-shankar-patak-chau'


def pathak_solar_target_audit():
    elapsed = F(41) + F(49, 60) + F(30, 3600)
    traversal = F(58) + F(27, 60)
    exact_remaining = (traversal - elapsed) * 20 / traversal
    printed_remaining = F(5) + F(8, 12) + F(7, 360) + F(54, 21600) + F(15, 1296000)
    birth = dms(5, 1, 2, 31)
    printed_target = dms(10, 8, 56, 46)
    computed = (birth + printed_remaining * 360) % 360
    return {'profile': 'pathak_phaladeepika19_angular_target_commentary_audit',
            'printed_birth_date': '1994-06-16', 'printed_birth_clock': '10:10',
            'birth_place_timezone_unverified': True,
            'exact_normalized_remaining_years_rational': str(exact_remaining),
            'printed_remaining_years_rational': str(printed_remaining),
            'printed_minus_exact_balance_palas_rational': str((printed_remaining - exact_remaining) * 1296000),
            'printed_birth_sun_degrees_rational': str(birth),
            'printed_endpoint_samvat': 2056,
            'printed_endpoint_sun_degrees_rational': str(printed_target),
            'printed_balance_added_target_degrees_rational': str(computed),
            'computed_minus_printed_target_arcseconds_rational': str((computed - printed_target) * 3600),
            'explicit_commentary_mapping': 'Add remaining year units to birth Samvat and Sun coordinates; end when Sun reaches the resulting sign and degrees',
            'supported_named_calendar_interpretation': 'solar_angular_target',
            'elapsed_utc_interpolation_explicitly_supported': False,
            'worked_endpoint_arithmetic_matches': computed == printed_target,
            'source': {'url': SOURCE_URL, 'pdf_pages': [222, 223], 'printed_pages': [204, 205],
                       'chapter': 19, 'slokas': '3-4 commentary', 'verified_against_page_image': True},
            'edition': {'commentator': 'Dr. Hari Shankar Pathak',
                        'publisher': 'Chaukhamba Surabharati Prakashan',
                        'series_number': 349, 'reprint_year': 2007,
                        'title_pdf_page': 7, 'copyright_pdf_page': 8,
                        'publisher_all_rights_reserved': True},
            'source_sign_numbering': 'Endpoint sign10 explicitly identified as Aquarius in commentary',
            'input_sign_explanation_found_in_worked_passage': False,
            'public_release_rights_cleared': False,
            'selected_calendar_profile': None, 'exact_civil_endpoint': None,
            'app_contract_changed': False,
            'notice': 'Independent commentary supports angular-target mapping rather than merely '
                      'annual returns. Printed normalized balance differs by subpala truncation; '
                      'printed birth Sun sign5 and endpoint sign10 have a270degree addition mismatch. '
                      'No guessed sign repair, timezone, Samvat conversion or ephemeris is supplied. '
                      'This is not a reliable exact civil benchmark, universal text interpretation '
                      'or verified Balaji setting; existing default remains unchanged.'}
