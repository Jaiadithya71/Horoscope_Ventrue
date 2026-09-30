"""Original Ketkar terminology, not reconstructed Sripati motion inputs."""

SOURCE_URL = ('https://archive.org/details/'
              'jyotir-ganita-venkatesh-ramakrishna-kethkar-dattatreya-ketkar-surakant-jha')


def ketkar_motion_input_audit():
    return {
        'source': {'url': SOURCE_URL, 'pdf_pages': [25, 26, 27, 170, 172, 173, 174],
                   'verified_against_page_image': True},
        'author_preface': {
            'pdf_page': 25, 'printed_page': 2,
            'anomaly_argument': 'days rather than arc',
            'table_output': 'true anomaly at equal day intervals',
            'longitude_operation': 'true anomaly plus longitude of perihelion',
            'longitude_output': 'true heliocentric position',
            'mean_motion_table_substitution_verified': False,
            'notice': 'Author explicitly says he gets rid of mean-motion tables; '
                      'this does not prove no mean quantities exist elsewhere in the book.'},
        'coordinate_stages': [
            {'pdf_pages': [170], 'printed_pages': [103],
             'term': 'madhyama computation', 'role': 'upstream day arguments and auxiliaries'},
            {'pdf_pages': [172, 173], 'printed_pages': [105, 106],
             'term': 'ravimadhya', 'role': 'Sun-centred planet position',
             'not_synonymous_with': 'uniform mean geocentric longitude'},
            {'pdf_pages': [173, 174], 'printed_pages': [106, 107],
             'term': 'bhumadhya', 'role': 'Earth-centred conversion and true position'}],
        'existing_mercury_fixture': {
            'ravimadhya_longitude': '261.814',
            'provisional_bhumadhya_longitude': '330.960',
            'narrative_true_bhumadhya_longitude': '327.879',
            'nyasa_true_bhumadhya_longitude': '327.878',
            'source_labelled_sripati_mean': None,
            'source_labelled_sripati_sighrochcha': None},
        'sripati_mapping': {
            'mean_unwrapped_degrees': None, 'true_unwrapped_degrees': None,
            'sighrochcha_degrees': None, 'coordinate_branch': None,
            'independent_full_angle_reconstruction': None},
        'raman_assignment_transfer_verified': False,
        'historical_ephemeris_complete': False,
        'selected_natal_total': None,
        'notice': 'Do not relabel true heliocentric output or provisional Earth-centred '
                  'output as the missing mean input. A shared word madhya does not '
                  'establish a shared coordinate centre or mean-motion model. '
                  'The preface and chapter distinguish these stages but do not '
                  'identify a unique Sripati mean/true/Sighrochcha triple or unwrap. '
                  'Existing edition, interpolation and rounding gates remain open.'}


if __name__ == '__main__':
    import json
    print(json.dumps(ketkar_motion_input_audit(), indent=2))
