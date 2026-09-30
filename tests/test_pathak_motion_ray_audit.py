import itertools
import unittest
from engine.pathak_motion_ray_audit import pathak_motion_ray_audit


class PathakMotionRayTests(unittest.TestCase):
    def test_three_valued_or_and_separate_obscuration(self):
        for r, f, o in itertools.product((None, False, True), repeat=3):
            x = pathak_motion_ray_audit(r, f, o)
            expected = (True if r is True or f is True else
                        False if r is False and f is False else None)
            self.assertIs(x['hindi_strength_clause_applies'], expected)
            self.assertIs(x['hindi_weakness_clause_applies'], o)
            self.assertEqual(x['simultaneous_strength_and_weakness_evidence'],
                             expected is True and o is True)
            self.assertEqual(x['full_rays_and_obscuration_supplied_together'],
                             f is True and o is True)

    def test_invalid_flags_and_no_automatic_total(self):
        for index in range(3):
            for bad in (0, 1, 'yes', [], {}):
                args = [None, None, None]
                args[index] = bad
                with self.assertRaises(ValueError):
                    pathak_motion_ray_audit(*args)
        x = pathak_motion_ray_audit(False, True, True)
        self.assertEqual(x['source']['pdf_pages'], [65, 66])
        self.assertEqual(x['hindi_positive_connective'], 'OR')
        for key in ('sanskrit_boolean_connective_selected', 'selected_universal_connective',
                    'selected_physical_ray_definition', 'numeric_strength',
                    'global_precedence', 'personal_outcome'):
            self.assertIsNone(x[key])
