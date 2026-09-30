import json
import subprocess
import sys
import unittest
from engine.ketkar_motion_input_audit import ketkar_motion_input_audit
from engine.motional_strength import cheshtabala, cheshta_from_supplied_mean_true


class KetkarMotionInputAuditTests(unittest.TestCase):
    def test_true_heliocentric_is_not_missing_mean(self):
        r = ketkar_motion_input_audit()
        self.assertEqual(r['author_preface']['table_output'], 'true anomaly at equal day intervals')
        self.assertFalse(r['author_preface']['mean_motion_table_substitution_verified'])
        self.assertEqual(r['existing_mercury_fixture']['ravimadhya_longitude'], '261.814')
        self.assertIsNone(r['existing_mercury_fixture']['source_labelled_sripati_mean'])
        self.assertTrue(r['source']['verified_against_page_image'])

    def test_mapping_and_forecast_not_filled(self):
        r = ketkar_motion_input_audit()
        self.assertTrue(all(value is None for value in r['sripati_mapping'].values()))
        self.assertFalse(r['raman_assignment_transfer_verified'])
        self.assertFalse(r['historical_ephemeris_complete'])
        self.assertIsNone(r['selected_natal_total'])
        self.assertNotEqual(r['existing_mercury_fixture']['narrative_true_bhumadhya_longitude'],
                            r['existing_mercury_fixture']['nyasa_true_bhumadhya_longitude'])

    def test_source_audit_imports_without_astronomy(self):
        code = "import sys; sys.modules['swisseph']=None; from engine.ketkar_motion_input_audit import ketkar_motion_input_audit; import json; print(json.dumps(ketkar_motion_input_audit()))"
        p = subprocess.run([sys.executable, '-c', code], capture_output=True, text=True, check=True)
        self.assertFalse(json.loads(p.stdout)['historical_ephemeris_complete'])

    def test_source_only_cli(self):
        p = subprocess.run([sys.executable, '-m', 'engine.ketkar_motion_input_audit'],
                           capture_output=True, text=True, check=True)
        self.assertIsNone(json.loads(p.stdout)['sripati_mapping']['mean_unwrapped_degrees'])

    def test_bad_motion_angles_rejected(self):
        for value in (True, False, '12', None, float('inf'), float('nan'), 10**400):
            with self.subTest(value=repr(value)[:30]):
                with self.assertRaises(ValueError):
                    cheshtabala('Mars', value)
                for index in range(3):
                    args = [80, 60, 250]
                    args[index] = value
                    with self.assertRaises(ValueError):
                        cheshta_from_supplied_mean_true('Mars', *args, input_profile='supplied', coordinate_branch='literal')

    def test_bad_provenance_rejected(self):
        for value in ('', '   ', None, True, 1, ['profile']):
            for key in ('input_profile', 'coordinate_branch'):
                kwargs = {'input_profile': 'supplied', 'coordinate_branch': 'literal'}
                kwargs[key] = value
                with self.assertRaises(ValueError):
                    cheshta_from_supplied_mean_true('Mars', 80, 60, 250, **kwargs)

    def test_overflow_rejected_and_normal_fixture_unchanged(self):
        with self.assertRaises(ValueError):
            cheshta_from_supplied_mean_true('Mars', 1e308, -1e308, 250, input_profile='supplied', coordinate_branch='literal')
        r = cheshta_from_supplied_mean_true('Mars', 80, 60, 250, input_profile='supplied', coordinate_branch='literal')
        self.assertEqual(r['cheshtakendra_degrees'], 180)
        self.assertEqual(r['cheshtabala']['rupa'], 1)
