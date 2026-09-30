"""Independent Garga threshold witness, not a selected Sripati refinement."""
from .own_shadvarga_refinement_audit import own_shadvarga_refinement_audit

SOURCE_URL = 'https://archive.org/stream/Book11.HoraRatnam10NoOCR/Book11.+Hora+ratnam-10+no+OCR_djvu.txt'
PDF_URL = 'https://archive.org/download/Book11.HoraRatnam10NoOCR/Book11.%20Hora%20ratnam-10%20no%20OCR.pdf'


def horaratna_own_varga_scope_audit():
    existing = own_shadvarga_refinement_audit()
    rows = []
    for r in existing['rows']:
        count = len(r['own_varga_names'])
        rows.append({'planet': r['planet'], 'own_varga_names': r['own_varga_names'],
                     'own_varga_count': count,
                     'any_one_owned_hypothesis': count >= 1,
                     'garga_minimum_three_owned_candidate': count >= 3,
                     'all_six_owned_hypothesis': count == 6,
                     'base_decan_rupa': r['base_decan_rupa'],
                     'sripati_explicit_refinement_rupa': r['quoted_refinement_rupa'],
                     'selected_refined_component': None})
    jupiter = next(r for r in rows if r['planet'] == 'Jupiter')
    return {
        'source': {'url': SOURCE_URL, 'pdf_url': PDF_URL,
                   'pdf_pages': [1, 63, 64, 127], 'printed_pages': [66, 67, 130],
                   'verified_against_page_image': True,
                   'title_page': 'Bala Bhadra Hora Ratnam; R. Santhanam translation and notes',
                   'passages': 'I42-44 six-varga definition/Garga threshold; I174 decan rule'},
        'independent_translator_from_sripati_sastri': True,
        'garga_quoted_definition': {'six_divisions': ['rasi', 'hora', 'drekkana',
                                                    'navamsa', 'dwadasamsa', 'trimsamsa'],
                                    'minimum_owned_divisions': 3,
                                    'printed_maximum_owned_divisions': 5,
                                    'printed_all_six_possible': False},
        'horaratna_decan_class_order': {'masculine': 1, 'feminine': 2, 'neuter': 3},
        'sripati_decan_class_order': {'masculine': 1, 'neuter': 2, 'feminine': 3},
        'decan_class_orders_agree': False,
        'worked_rows_using_existing_named_geometry': rows,
        'minimum_three_candidate_fits_explicit_jupiter_example':
            jupiter['garga_minimum_three_owned_candidate'],
        'all_six_candidate_fits_explicit_jupiter_example':
            jupiter['all_six_owned_hypothesis'],
        'horaratna_explicitly_maps_garga_threshold_to_sripati_refinement': False,
        'sripati_any_or_all_quantifier_settled': False,
        'selected_refinement_definition': None,
        'selected_positional_total': None,
        'notice': 'An independent translation of Balabhadra quotes Garga defining '
                  'own divisions by a minimum of three of six. Existing named worked '
                  'owner geometry gives Jupiter exactly three, so this is a supported '
                  'comparison candidate, not proof of Sripati commentary intent. '
                  'Hora Ratnam decan sex-class order differs from Sripati. Do not '
                  'merge the methods, assign new refined values to other rows, or '
                  'enable a positional/natal total. Printed maximum-five assertion '
                  'is recorded as source text, not a universal geometry theorem.'}


if __name__ == '__main__':
    import json
    print(json.dumps(horaratna_own_varga_scope_audit(), indent=2))
