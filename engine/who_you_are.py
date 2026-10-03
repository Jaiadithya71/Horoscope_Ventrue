"""'Who you are' layer 1: rising-sign and Moon-sign temperament, Phaladeepika Adh. IX.

Scan checked at PDF 135-139 (printed pp. 98-102), slokas 1-13. Own-words paraphrase of the
translator's English, rewritten as plain second-person temperament. Held out: body marks and
physical build, and clauses that call the person false, shameless, sinful, a hypocrite,
covetous or similar character verdicts, sexual-habit remarks, and the child-count remarks
(a child count is not stated as a prediction here). Sloka 13 says the same sign results
apply when the Moon is in that sign, so the Moon-sign read reuses the same text and says so.
Not tested forecasts. Alternative readings are not ranked; nothing here overrides a period reading.
"""
PHALA = 'https://archive.org/details/in.ernet.dli.2015.92117'
SRC = {'book': 'phaladeepika-1937', 'chapter': 'IX', 'pdf_pages': [135, 136, 137, 138, 139], 'verified_against_page_image': True, 'url': PHALA}
SRC13 = dict(SRC, sloka='13', pdf_pages=[139])

# sign -> (sloka, traits as 'you' text, strengths/pointers list)
TRAITS = {
 'Aries': (1, 'You are restless and always on the move, with a quick, changeable temper. Your energy is high and you do not like sitting still. Water and sheer exhaustion can unsettle you.', ['energy', 'restlessness']),
 'Taurus': (2, 'You are generous, forgiving and able to put up with hardship. You do best through steady, practical work and tend to settle well in the middle and later parts of life. Warm company matters to you, and you like having your own resources around you.', ['steadiness', 'generosity', 'later-life ease']),
 'Gemini': (3, 'You are quick at reading what other people are thinking, with a feel for music, art and conversation. You like company and play, and you prefer to stay close to home.', ['people-reading', 'the arts']),
 'Cancer': (4, 'You are surrounded by friends and home matters a lot to you. You are shrewd, quick on your feet and drawn to water. You can be stubborn in your views, and your wife or partner may carry a lot of influence over you. Money tends to come.', ['friends', 'home', 'shrewdness']),
 'Leo': (5, 'You are proud, strong-willed and a natural leader, with a quick temper over small things. You like hills, forests and open places, you are firm-minded and you are close to your mother.', ['leadership', 'firmness']),
 'Virgo': (6, 'You are modest, truthful and kind in speech, and you gain respect through other people and their resources. You are good with study and with interpreting texts or situations.', ['kindness', 'study', 'modesty']),
 'Libra': (7, 'You are brave, clever in trade and fair-minded when you argue a point. You are drawn to worship and to rituals, you like to travel and you are not easily pushed around.', ['trade', 'fairness', 'courage']),
 'Scorpio': (8, 'You are intense and strong in spirit. Early life can be hard, with illness or distance from parents and teachers. You tend to be taken seriously by people in authority.', ['intensity', 'authority']),
 'Sagittarius': (9, 'You are focused on getting your work done and eloquent when you speak. You are generous, you stand out to people in power and you do well against opponents. You respond to kindness and tend to resist force.', ['eloquence', 'generosity', 'strength']),
 'Capricorn': (10, 'You are determined, with strong courage, and you finish what you take on. You can be slow to start and may be tough on your legs, joints and nerves. Luck tends to turn your way.', ['determination', 'courage']),
 'Aquarius': (11, 'You are private and calculating in how you handle things. You can cope with long journeys and hard stretches, and your means often start modest. Money may rise and fall.', ['endurance', 'privacy']),
 'Pisces': (12, 'You are gentle, learned and appreciative of what others have done for you. You tend to overcome opponents, you keep a good bearing and luck is on your side. Water and the sea may be significant for you, and close partnership matters a great deal to you.', ['gratitude', 'learning', 'luck']),
}


def who_you_are(report):
    chart = report['natal_chart']
    rise = chart['ascendant']['sign']
    moon = chart['placements']['Moon']['sign']
    if rise not in TRAITS or moon not in TRAITS: return None
    r, m = TRAITS[rise], TRAITS[moon]
    out = {
        'status': 'temperament_not_tested_forecast',
        'outer_you': {'text': r[1], 'pointers': r[2], 'rules': [{'rule_id': f'phaladeepika-ix-{r[0]}-rising', 'source': dict(SRC, sloka=str(r[0])), 'sign': rise, 'effect': r[1]}]},
        'inner_you': {'text': m[1], 'pointers': m[2], 'rules': [{'rule_id': f'phaladeepika-ix-13-moon-{m[0]}', 'source': SRC13, 'sign': moon, 'effect': 'Same sign results apply when the Moon is in that sign (Sloka 13).'},
                                                               {'rule_id': f'phaladeepika-ix-{m[0]}-moon-echo', 'source': dict(SRC, sloka=str(m[0])), 'sign': moon, 'effect': m[1]}]},
        'same_sign': rise == moon,
        'held_out': ['body marks and build', 'character verdicts (false, shameless, hypocrite, covetous)', 'sexual-habit remarks', 'child-count remarks'],
        'notice': 'A short temperament sketch from one classical text (Phaladeepika Adh. IX). It is a starting point, not a verdict, and was not tested against real outcomes.',
    }
    return out
