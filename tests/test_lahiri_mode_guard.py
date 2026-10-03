import unittest
import swisseph as swe
from engine.research_input_report import research_input_report

BIRTH = {'date': '1990-05-15', 'time': '10:30:00', 'timezone': 'Asia/Calcutta', 'latitude': 13.08, 'longitude': 80.27, 'place': 'Chennai'}


class LahiriGuardTest(unittest.TestCase):
    def test_report_uses_lahiri_even_if_process_mode_was_reset(self):
        swe.set_sid_mode(swe.SIDM_FAGAN_BRADLEY)  # what a fresh swisseph state defaults to
        sun = research_input_report(BIRTH)['natal_chart']['placements']['Sun']['longitude']
        self.assertAlmostEqual(sun, 30.389, places=2)  # tropical 54.115 minus Lahiri 23.72


if __name__ == '__main__':
    unittest.main()
