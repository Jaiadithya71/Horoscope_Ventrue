import unittest
from fractions import Fraction as F
from engine.bphs_jha_paksha import bphs_jha_paksha
from engine.bphs_jha_general_aspect import dms


class JhaPakshaTests(unittest.TestCase):
    def result(self, sun, moon, **kwargs):
        return bphs_jha_paksha(sun, moon, coordinate_profile=kwargs.get('profile', 'supplied fixture'))

    def test_printed_waning_fixture_and_fixed_groups(self):
        x = self.result(dms(2, 5, 25, 15), dms(9, 25, 37, 45))
        self.assertEqual(F(x['benefic_paksha_virupa_rational']), dms(0, 43, 15, 50))
        self.assertEqual(F(x['malefic_paksha_virupa_rational']), dms(0, 16, 44, 10))
        for p in ('Moon', 'Mercury', 'Jupiter', 'Venus'):
            self.assertEqual(x['planet_paksha_virupa_rational'][p], x['benefic_paksha_virupa_rational'])
        for p in ('Sun', 'Mars', 'Saturn'):
            self.assertEqual(x['planet_paksha_virupa_rational'][p], x['malefic_paksha_virupa_rational'])
        self.assertEqual(x['moon_multiplier'], 1)
        self.assertNotIn('Ketu', x['planet_paksha_virupa_rational'])

    def test_conjunction_opposition_quarters_and_wrap(self):
        for sun, moon, expected in ((0, 0, 0), (0, 180, 60), (0, 90, 30), (0, 270, 30), (350, 10, F(20, 3))):
            x = self.result(sun, moon)
            self.assertEqual(F(x['benefic_paksha_virupa_rational']), expected)
            self.assertEqual(F(x['benefic_paksha_virupa_rational']) + F(x['malefic_paksha_virupa_rational']), 60)

    def test_exact_rational_reflection(self):
        a = self.result('1/7', '181/7')
        b = self.result('181/7', '1/7')
        self.assertEqual(a['benefic_paksha_virupa_rational'], b['benefic_paksha_virupa_rational'])
        self.assertEqual(F(a['benefic_paksha_virupa_rational']), F(60, 7))

    def test_invalid_coordinates_and_provenance(self):
        for value in (True, False, None, '', 'NaN', 'inf', -1, 360, '1/0'):
            with self.assertRaises(ValueError): self.result(value, 0)
            with self.assertRaises(ValueError): self.result(0, value)
        for profile in (None, '', ' ', False):
            with self.assertRaises(ValueError): self.result(0, 0, profile=profile)

    def test_source_and_abstention(self):
        x = self.result(0, 90)
        self.assertEqual(x['source']['pdf_pages'], [188])
        self.assertEqual(x['source']['slokas'], '10-11')
        self.assertIsNone(x['selected_natal_strength_profile'])
        self.assertIsNone(x['full_strength'])
        self.assertFalse(x['universal_multiplier_policy_verified'])
