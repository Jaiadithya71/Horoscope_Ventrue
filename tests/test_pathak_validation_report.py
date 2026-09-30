import json
import os
import subprocess
import sys
import unittest
from engine.pathak_validation_report import pathak_validation_report


class PathakValidationTests(unittest.TestCase):
    def test_source_checks_keep_decisions_unknown(self):
        x = pathak_validation_report()
        self.assertEqual(len(x['checks']), 7)
        self.assertEqual(len(x['local_precedence_scope']), 1)
        self.assertIsNone(x['checks']['explicit_lagna_house_or_lord_connective']['condition'])
        for key in ('selected_natal_total', 'selected_calendar_profile', 'selected_translation',
                    'global_precedence', 'empirical_outcome_accuracy'):
            self.assertIsNone(x[key])
        self.assertFalse(x['public_release_rights_cleared'])
        self.assertNotIn('accuracy_percentage', x)

    def test_actual_cli_and_no_ephemeris_dependency(self):
        env = os.environ.copy()
        env.pop('PYTHONPATH', None)
        for command in ([sys.executable, '-m', 'engine.pathak_validation_report'],
                        [sys.executable, '-c', "import sys; sys.modules['swisseph']=None; from engine.pathak_validation_report import pathak_validation_report; import json; print(json.dumps(pathak_validation_report()))"]):
            r = subprocess.run(command, capture_output=True, text=True, env=env, timeout=30)
            self.assertEqual(r.returncode, 0, r.stderr)
            x = json.loads(r.stdout)
            self.assertEqual(x['status'], 'source_validation_not_forecast')
            self.assertEqual(x['checks']['normalized_balance_and_angular_target']['printed_endpoint_samvat'], 2056)
