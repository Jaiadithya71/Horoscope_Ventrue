"""IG content studio: page-cited reference cards for the user's own short-video
content creation. Internal tooling; the page is not linked from the public site.

Every bullet carries its book citation. Where the library has no direct rule,
the card says so plainly and any assembled chain (weekday to day-lord to planet
nature; nakshatra to dasha lord to that planet's presiding deity) is labelled
'derived', never presented as a direct classical rule. Historical astrological
interpretations, not validated prediction.
"""

PHALA = 'Phaladeepika (1937)'
BJ = 'Brihat Jataka (1905)'
ASI = 'Astrological Self-Instructor (1893)'

# ---- Planets -------------------------------------------------------------

PLANETS = ('Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu')
PLANET_TA = {'Sun': 'சூரியன்', 'Moon': 'சந்திரன்', 'Mars': 'செவ்வாய்', 'Mercury': 'புதன்',
             'Jupiter': 'குரு', 'Venus': 'சுக்கிரன்', 'Saturn': 'சனி', 'Rahu': 'ராகு', 'Ketu': 'கேது'}

# Phaladeepika ch. II, sloka 27 (PDF p. 57): presiding deities of the planets
# "from the Sun in their order".
DEITY_PHALA = {
    'Sun': 'Rudra (Siva)', 'Moon': 'Amba (Parvati)', 'Mars': 'Guha (Kumara)',
    'Mercury': 'Vishnu', 'Jupiter': 'Brahman', 'Venus': 'Lakshmi',
    'Saturn': 'Kala (Yama)', 'Rahu': 'the serpent Adisesha', 'Ketu': 'Brahman',
}
DEITY_PHALA_TA = {
    'Sun': 'ருத்திரன் (சிவன்)', 'Moon': 'அம்பா (பார்வதி)', 'Mars': 'குகன் (முருகன்)',
    'Mercury': 'விஷ்ணு', 'Jupiter': 'பிரம்மா', 'Venus': 'லட்சுமி',
    'Saturn': 'காலன் (யமன்)', 'Rahu': 'ஆதிசேஷன் (நாகம்)', 'Ketu': 'பிரம்மா',
}
# Brihat Jataka ch. II, sloka 5 (PDF p. 61): alternate deva list.
DEITY_BJ = {'Sun': 'Agni', 'Moon': 'Varuna', 'Mars': 'Subrahmanya', 'Mercury': 'Vishnu',
            'Jupiter': 'Indra', 'Venus': 'Indrani', 'Saturn': 'Brahma', 'Rahu': None, 'Ketu': None}
DEITY_BJ_TA = {'Sun': 'அக்னி', 'Moon': 'வருணன்', 'Mars': 'சுப்பிரமணியன்', 'Mercury': 'விஷ்ணு',
               'Jupiter': 'இந்திரன்', 'Venus': 'இந்திராணி', 'Saturn': 'பிரம்மா', 'Rahu': None, 'Ketu': None}
# Brihat Jataka ch. II, sloka 5 (PDF p. 61): colours and directions.
COLOR_BJ = {'Sun': 'copper colour', 'Moon': 'white', 'Mars': 'red', 'Mercury': 'green',
            'Jupiter': 'yellow', 'Venus': 'a mixture of various colours', 'Saturn': 'black',
            'Rahu': None, 'Ketu': None}
COLOR_BJ_TA = {'Sun': 'செம்மை நிறம்', 'Moon': 'வெள்ளை', 'Mars': 'சிவப்பு', 'Mercury': 'பச்சை',
               'Jupiter': 'மஞ்சள்', 'Venus': 'பல நிறங்கள் கலந்தவை', 'Saturn': 'கறுப்பு',
               'Rahu': None, 'Ketu': None}
DIRECTION_BJ = {'Sun': 'east', 'Moon': 'north-west', 'Mars': 'south', 'Mercury': 'north',
                'Jupiter': 'north-east', 'Venus': 'south-east', 'Saturn': 'west',
                'Rahu': 'south-west', 'Ketu': None}
DIRECTION_TA = {'east': 'கிழக்கு', 'south-east': 'தென்கிழக்கு', 'south': 'தெற்கு',
                'south-west': 'தென்மேற்கு', 'west': 'மேற்கு', 'north-west': 'வடமேற்கு',
                'north': 'வடக்கு', 'north-east': 'வடகிழக்கு'}
# Phaladeepika ch. II, sloka 28 (PDF p. 57): grains.
GRAIN_PHALA = {'Sun': 'wheat', 'Moon': 'rice', 'Mars': 'dhal', 'Mercury': 'green gram',
               'Jupiter': 'Bengal gram', 'Venus': 'dolichos lablab (cowgram)', 'Saturn': 'sesamum',
               'Rahu': 'black gram', 'Ketu': 'horsegram'}
GRAIN_PHALA_TA = {'Sun': 'கோதுமை', 'Moon': 'அரிசி', 'Mars': 'துவரம் பருப்பு', 'Mercury': 'பச்சை பயறு',
                  'Jupiter': 'கடலை', 'Venus': 'தட்டைப் பயறு', 'Saturn': 'எள்',
                  'Rahu': 'உளுத்தம் பருப்பு', 'Ketu': 'கொள்ளு'}
# Phaladeepika ch. II, sloka 29 (PDF pp. 57-58): precious stones.
GEM_PHALA = {'Sun': 'ruby', 'Moon': 'pure spotless pearl', 'Mars': 'coral', 'Mercury': 'emerald',
             'Jupiter': 'topaz', 'Venus': 'diamond', 'Saturn': 'stainless sapphire',
             'Rahu': 'agate', 'Ketu': 'lapis lazuli or turkois'}
GEM_PHALA_TA = {'Sun': 'மாணிக்கம்', 'Moon': 'மாசற்ற முத்து', 'Mars': 'பவளம்', 'Mercury': 'மரகதம்',
                'Jupiter': 'புஷ்பராகம்', 'Venus': 'வைரம்', 'Saturn': 'மாசற்ற நீலம்',
                'Rahu': 'அகேட்', 'Ketu': 'லாபிஸ் லசூலி / டர்க்கோயிஸ்'}
# Phaladeepika ch. II, sloka 30 (PDF p. 58): substances "from the Sun onwards"
# (seven listed for the seven planets); garments continue the same sloka.
SUBSTANCE_PHALA = {'Sun': 'copper', 'Moon': 'bell-metal', 'Mars': 'copper ore', 'Mercury': 'lead',
                   'Jupiter': 'gold', 'Venus': 'silver', 'Saturn': 'iron', 'Rahu': None, 'Ketu': None}
SUBSTANCE_PHALA_TA = {'Sun': 'செம்பு', 'Moon': 'வெங்கலம்', 'Mars': 'செம்புத் தாது', 'Mercury': 'ஈயம்',
                      'Jupiter': 'தங்கம்', 'Venus': 'வெள்ளி', 'Saturn': 'இரும்பு', 'Rahu': None, 'Ketu': None}
GARMENT_PHALA = {p: 'cloth bearing the planet\u2019s colour' for p in
                 ('Sun', 'Moon', 'Mercury', 'Jupiter', 'Venus', 'Rahu', 'Ketu')}
GARMENT_PHALA['Mars'] = 'a cloth singed by fire'
GARMENT_PHALA['Saturn'] = 'a rag'
# Phaladeepika ch. II, sloka 31 (PDF p. 58): flavours.
FLAVOUR_PHALA = {'Sun': 'pungent', 'Moon': 'saltish', 'Mars': 'bitter', 'Mercury': 'mixed',
                 'Jupiter': 'sweet', 'Venus': 'sour (acid)', 'Saturn': 'astringent',
                 'Rahu': None, 'Ketu': None}
FLAVOUR_PHALA_TA = {'Sun': 'காரம்', 'Moon': 'உப்புச் சுவை', 'Mars': 'கசப்பு', 'Mercury': 'கலந்த சுவை',
                    'Jupiter': 'இனிப்பு', 'Venus': 'புளிப்பு', 'Saturn': 'துவர்ப்பு', 'Rahu': None, 'Ketu': None}
# Phaladeepika ch. II, after sloka 32 (PDF p. 59): ages typified.
AGE_PHALA = {'Sun': '50 years', 'Moon': '70 years', 'Mars': '16 years', 'Mercury': '20 years (a lad)',
             'Jupiter': '30 years', 'Venus': '7 years (a child)', 'Saturn': '100 years',
             'Rahu': '100 years', 'Ketu': None}
# Brihat Jataka ch. II, sloka 12 (PDF p. 63): places, garments, metals.
PLACE_BJ = {'Sun': 'the place of worship', 'Moon': 'wells', 'Mars': 'the fire place',
            'Mercury': 'play grounds', 'Jupiter': 'the store room', 'Venus': 'bed room',
            'Saturn': 'places where sweepings are gathered', 'Rahu': None, 'Ketu': None}
PLACE_BJ_TA = {'Sun': 'வழிபாட்டிடம்', 'Moon': 'கிணறு', 'Mars': 'அடுப்பு இடம்',
               'Mercury': 'விளையாட்டு மைதானம்', 'Jupiter': 'பண்டகச் சாலை', 'Venus': 'படுக்கையறை',
               'Saturn': 'குப்பை கொட்டும் இடம்', 'Rahu': None, 'Ketu': None}
METAL_BJ = {'Sun': 'copper', 'Moon': 'gems', 'Mars': 'gold', 'Mercury': 'brass',
            'Jupiter': 'silver', 'Venus': 'pearls', 'Saturn': 'iron', 'Rahu': None, 'Ketu': None}
METAL_BJ_TA = {'Sun': 'செம்பு', 'Moon': 'ரத்தினங்கள்', 'Mars': 'தங்கம்', 'Mercury': 'பித்தளை',
               'Jupiter': 'வெள்ளி', 'Venus': 'முத்து', 'Saturn': 'இரும்பு', 'Rahu': None, 'Ketu': None}
GARMENT_BJ = {'Sun': 'of thick thread', 'Moon': 'new', 'Mars': 'partly burnt', 'Mercury': 'wet',
              'Jupiter': 'somewhat used', 'Venus': 'strong', 'Saturn': 'torn', 'Rahu': None, 'Ketu': None}

# Phaladeepika ch. II, slokas 8-14 (PDF pp. 49-51): temperament and appearance.
NATURE_PHALA = {
    'Sun': 'bilious temperament, strong in bones; limited hair, dark-red form, reddish-brown eyes; '
           'clad in red, square-built body; valiant and wrathful, with massive arms',
    'Moon': 'huge yet lean white body; fine lovely eyes, black thin hair; governs blood; soft in speech, '
            'wears white; beautiful; wind and phlegm in composition, mild in temperament',
    'Mars': 'slender waist, curled shining hair, fierce eyes; bilious and cruel in nature yet '
            'exceedingly generous; wears red, of reddish hue, youthful; governs marrow',
    'Mercury': 'green as the durva blade; a mixture of the three humours; pleasant in speech, red long '
               'eyes, clad in green; governs the skin; fond of fun, even limbs',
    'Jupiter': 'yellowish body, brown eyes and hair; fat elevated chest, big body; phlegmatic; '
               'exceedingly intelligent; voice like a lion or a conch; always after wealth',
    'Venus': 'variegated garment, black curled hair, huge limbs; much wind and phlegm; durva-sprout '
             'colour, very lovely, broad eyes',
    'Saturn': 'dark in form, lame, wind in composition; deep eyes, lean tall body; idle, exceedingly '
              'calumniating; governs muscle; cruel, without pity, dull-headed; large nails and teeth, '
              'stiff hair; fierce, ripe with old age, wears black',
    'Rahu': None, 'Ketu': None,
}
NATURE_PHALA_PAGE = {'Sun': 49, 'Moon': 49, 'Mars': 50, 'Mercury': 50, 'Jupiter': 50, 'Venus': 51, 'Saturn': 51}
NATURE_PHALA_SLOKA = {'Sun': 'II.8', 'Moon': 'II.9', 'Mars': 'II.10', 'Mercury': 'II.11',
                      'Jupiter': 'II.12', 'Venus': 'II.13', 'Saturn': 'II.14'}

SHANTI_RULE = {
    'text_en': 'If planets are badly situated during their Dasa, Bhukti, Ashtakavarga or transit, one ought '
               'to propitiate them by prayers and incantations agreeable to the concerned planets, and perform '
               'Shantis (propitiatory rites) by doing virtuous actions, observing religious vows, making gifts '
               'and doing proper adorations. Planets are always favourable to one who is harmless, self-controlled, '
               'earns wealth by virtuous means and observes religious discipline.',
    'text_ta': 'ஒரு கிரகம் திசை, புத்தி, அஷ்டகவர்க்கம் அல்லது கோச்சாரத்தில் கெட்ட நிலையில் இருந்தால், '
               'அந்தக் கிரகத்திற்கு உரிய ஜபம், பிரார்த்தனை, தானம், விரதம், சாந்தி பூஜை ஆகியவற்றால் '
               'சாந்திப்படுத்த வேண்டும் என்கிறது பலதீபிகை. தீங்கு செய்யாத, பொருளை நேர்மையாகச் சம்பாதிக்கும், '
               'ஒழுக்கமுடையவர்களுக்குக் கிரகங்கள் எப்போதும் அனுகூலம் என்றும் அடுத்த ஸ்லோகம் சொல்கிறது.',
    'source': f'{PHALA}, ch. XXVI, slokas 49-50, PDF p. 356',
}

# ---- Weekdays ------------------------------------------------------------
# The classics give no weekday-of-birth character rules. What they do give is
# the weekday's ruling planet (ASI pp. 99-100 derives the weekday names from
# the succession of planetary horas) and each planet's nature (Phaladeepika
# II.8-14). The chain is assembled and labelled derived.

WEEKDAYS = ('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday')
WEEKDAY_TA = {'Sunday': 'ஞாயிறு', 'Monday': 'திங்கள்', 'Tuesday': 'செவ்வாய்', 'Wednesday': 'புதன்',
              'Thursday': 'வியாழன்', 'Friday': 'வெள்ளி', 'Saturday': 'சனி'}
WEEKDAY_LORD = {'Sunday': 'Sun', 'Monday': 'Moon', 'Tuesday': 'Mars', 'Wednesday': 'Mercury',
                'Thursday': 'Jupiter', 'Friday': 'Venus', 'Saturday': 'Saturn'}
WEEKDAY_LORD_SOURCE = f'{ASI}, week-day origin from planetary horas, PDF pp. 99-100'

# Short Tamil renderings of the day-lord's Phaladeepika nature, for caption drafts.
WEEKDAY_POINTS_TA = {
    'Sunday': ['துணிச்சல் மிக்கவர்; எளிதில் கோபம் வரும் குணம்',
               'உடல் உறுதி; சதுரமான தோற்றம்; சிவப்பு நிற விருப்பம்',
               'கிழமையின் அதிபதி சூரியன் - இது அவரது இயல்பு'],
    'Monday': ['மென்மையான குணம்; இனிமையான பேச்சு',
               'அழகான தோற்றம்; அழகிய கண்கள்; வெள்ளை விருப்பம்',
               'கிழமையின் அதிபதி சந்திரன் - இது அவரது இயல்பு'],
    'Tuesday': ['இளமையான தோற்றம்; கடும் பார்வை',
                'கோபம் இருந்தாலும் மிகவும் தாராள மனது',
                'கிழமையின் அதிபதி செவ்வாய் - இது அவரது இயல்பு'],
    'Wednesday': ['இனிமையான பேச்சு; நகைச்சுவை விருப்பம்',
                  'சீரான உடலமைப்பு; பச்சை நிற விருப்பம்',
                  'கிழமையின் அதிபதி புதன் - இது அவரது இயல்பு'],
    'Thursday': ['மிகுந்த புத்திசாலித்தனம்; சிங்கம் போன்ற குரல்',
                 'பருமனான உடல்; செல்வம் தேடும் இயல்பு',
                 'கிழமையின் அதிபதி குரு - இது அவரது இயல்பு'],
    'Friday': ['மிக அழகியவர்; அகன்ற கண்கள்; கறுப்புச் சுருள் முடி',
               'இசை, கவிதை, திருமணம், விழா ஆகியவற்றின் காரகன்',
               'கிழமையின் அதிபதி சுக்கிரன் - இது அவரது இயல்பு'],
    'Saturday': ['உயரமான ஒல்லி உடல்; ஆழ்ந்த கண்கள்',
                 'சற்று சோம்பல்; பிடிவாதமான தன்மை; கறுப்பு ஆடை',
                 'கிழமையின் அதிபதி சனி - இது அவரது இயல்பு'],
}

WEEKDAY_NOTICE = {
    'en': 'No book in our eight-book library gives character traits by weekday of birth - not for girls, '
          'not for anyone. Stri Jataka, the female-horoscopy book, has no weekday rules either. What the books '
          'do give: the planet that rules each weekday, and that planet\u2019s nature. This card follows that '
          'chain and labels it derived; a reel that presents weekday-birth traits as a direct classical rule '
          'would be claiming more than our sources say.',
    'ta': 'நம் எட்டு நூல்களில் எந்த நூலும் பிறந்த கிழமைக்கான குணக் குறிப்பை நேரடியாகச் சொல்லவில்லை. '
          'பெண் ஜாதக நூலான Stri Jataka-விலும் இல்லை. நூல்கள் சொல்வது: ஒவ்வொரு கிழமையின் அதிபதி கிரகம், '
          'அந்தக் கிரகத்தின் இயல்பு. அந்தச் சங்கிலியிலிருந்து உருவாக்கப்பட்டது இந்த அட்டை - "derived" என்றே குறிப்பிட்டுள்ளோம்.',
}

# ---- Nakshatras ----------------------------------------------------------
# Birth traits: Brihat Jataka ch. XVI, "On the Nakshatras or The Moon in the
# Asterisms" (PDF pp. 208-212). Chapter note: the effects fully come to pass
# only if the Moon is powerful. A second rendering of the same tradition is in
# ASI ch. IX (PDF pp. 185-187); kept as corroboration in the docs note.
# Dasha-lord grouping: Brihat Jataka ch. VIII (PDF p. 139).

NAKSHATRAS = (
    'Ashwini', 'Bharani', 'Krittika', 'Rohini', 'Mrigashira', 'Ardra', 'Punarvasu', 'Pushya',
    'Ashlesha', 'Magha', 'Purva Phalguni', 'Uttara Phalguni', 'Hasta', 'Chitra', 'Swati',
    'Vishakha', 'Anuradha', 'Jyeshtha', 'Mula', 'Purva Ashadha', 'Uttara Ashadha', 'Shravana',
    'Dhanishta', 'Shatabhisha', 'Purva Bhadrapada', 'Uttara Bhadrapada', 'Revati',
)
NAKSHATRA_TA = {
    'Ashwini': 'அசுவினி', 'Bharani': 'பரணி', 'Krittika': 'கார்த்திகை', 'Rohini': 'ரோகிணி',
    'Mrigashira': 'மிருகசீரிடம்', 'Ardra': 'திருவாதிரை', 'Punarvasu': 'புனர்பூசம்', 'Pushya': 'பூசம்',
    'Ashlesha': 'ஆயில்யம்', 'Magha': 'மகம்', 'Purva Phalguni': 'பூரம்', 'Uttara Phalguni': 'உத்திரம்',
    'Hasta': 'அஸ்தம்', 'Chitra': 'சித்திரை', 'Swati': 'சுவாதி', 'Vishakha': 'விசாகம்',
    'Anuradha': 'அனுஷம்', 'Jyeshtha': 'கேட்டை', 'Mula': 'மூலம்', 'Purva Ashadha': 'பூராடம்',
    'Uttara Ashadha': 'உத்திராடம்', 'Shravana': 'திருவோணம்', 'Dhanishta': 'அவிட்டம்',
    'Shatabhisha': 'சதயம்', 'Purva Bhadrapada': 'பூரட்டாதி', 'Uttara Bhadrapada': 'உத்திரட்டாதி',
    'Revati': 'ரேவதி',
}
# name: (dasha lord, BJ XVI page, English traits, Tamil points)
NAKSHATRA_DATA = {
    'Ashwini': ('Ketu', 209, 'fond of ornaments, fine appearance, popular, skilled in work, intelligent',
                ['ஆபரண விருப்பம்; அழகிய தோற்றம்', 'மக்களிடம் பிரபலம்; வேலையில் திறமை; புத்திசாலி']),
    'Bharani': ('Venus', 209, 'successful at work, truthful, free from diseases, able, free from grief',
                ['வேலையில் வெற்றி; உண்மையாளர்', 'நோயற்றவர்; திறமையாளர்; கவலையற்றவர்']),
    'Krittika': ('Sun', 209, 'a glutton, fond of the wives of other men, of bright appearance, of wide-spread fame',
                 ['பிரகாசமான தோற்றம்; பரவலான புகழ்', 'பசி அதிகம்; மற்றவர் உறவில் ஆர்வம் (நூல் குறிப்பு)']),
    'Rohini': ('Moon', 209, 'truthful, does not covet the property of others, cleanly habits, sweet speech, firm views, fine appearance',
               ['உண்மை; பிறர் சொத்தில் ஆசையற்றவர்', 'இனிய பேச்சு; உறுதியான கருத்து; அழகிய தோற்றம்']),
    'Mrigashira': ('Mars', 210, 'of no firm principles, able, timid, of good speech, active habits, rich, indulgent',
                   ['திறமை; நல்ல பேச்சு; சுறுசுறுப்பு; செல்வம்', 'கொள்கையில் உறுதி குறைவு; பயமுள்ள குணம்']),
    'Ardra': ('Rahu', 210, 'insincere, of irascible temper, ungrateful, indulges in torture, addicted to wicked deeds',
              ['கோபக் குணம்; நன்றி மறக்கும் தன்மை (நூல் குறிப்பு)', 'நேர்மை குறைவு என்றும் நூல் சொல்கிறது']),
    'Punarvasu': ('Jupiter', 210, 'devout, of patient habits, lives in comfort, good-natured, quiet, of wrong views, sickly, thirsty, pleased with trifles',
                  ['பக்தி; பொறுமை; வசதியான வாழ்க்கை; நல்ல குணம்', 'சிறியதில் மகிழ்ச்சி; உடல்நலம் குறைவு']),
    'Pushya': ('Saturn', 210, 'control over desires, generally liked, learned in the Sastras, rich, fond of acts of charity',
               ['பேராசை கட்டுப்பாடு; எல்லோருக்கும் பிடித்தவர்', 'சாஸ்திர கல்வி; செல்வம்; தர்ம செயல்களில் ஆர்வம்']),
    'Ashlesha': ('Mercury', 210, 'inattentive to the work of others, a promiscuous eater, sinful, ungrateful, skilled in cheating',
                 ['மற்றவர் வேலையில் கவனமற்றவர்; நன்றி மறப்பு (நூல் குறிப்பு)', 'ஏமாற்றுதலில் திறமை என்றும் நூல் குறிப்பிடுகிறது']),
    'Magha': ('Ketu', 210, 'numerous servants, very rich, lives in comfort, worships the Devas and Pitris, engaged in important works',
              ['பெரும் செல்வம்; வசதியான வாழ்க்கை; பணியாட்கள்', 'தேவதைகளையும் பித்ருக்களையும் வழிபடுபவர்; பெரிய செயல்கள்']),
    'Purva Phalguni': ('Venus', 210, 'sweet speech, liberal in gifts, fine appearance, wandering habits, serves under kings',
                       ['இனிய பேச்சு; தாராளமாக கொடுப்பவர்', 'அழகிய தோற்றம்; சுற்றி திரியும் இயல்பு']),
    'Uttara Phalguni': ('Sun', 210, 'generally liked, earns money by his learning, lives in comfort',
                        ['எல்லோருக்கும் பிடித்தவர்', 'கல்வியால் சம்பாதிப்பவர்; வசதியான வாழ்க்கை']),
    'Hasta': ('Moon', 210, 'active habits, full of resources, shameless, merciless, a thief and a drunkard',
              ['சுறுசுறுப்பு; வசதி மிகுந்தவர்', 'கொடூரம், திருட்டுப் போக்கு என கடுமையாக நூல் குறிப்பிடுகிறது']),
    'Chitra': ('Mars', 210, 'wears clothes and flowers of various colours, beautiful eyes and limbs',
               ['வண்ண வண்ண ஆடைகள், பூக்கள் விருப்பம்', 'அழகிய கண்கள், அழகிய உடலமைப்பு']),
    'Swati': ('Rahu', 210, 'mild and quiet nature, controls passion, skilled in trade, merciful, of sweet speech, disposed to charity',
              ['மென்மையான அமைதியான குணம்; வியாபாரத் திறமை', 'இரக்கம்; இனிய பேச்சு; தர்ம மனம்']),
    'Vishakha': ('Jupiter', 211, 'jealous of another\u2019s prosperity, a niggard, of bright appearance, of distinct speech, skilled in earning money, disposed to quarrels',
                 ['பிரகாசமான தோற்றம்; தெளிவான பேச்சு; சம்பாதிப்பதில் திறமை', 'பிறர் வளர்ச்சியில் பொறாமை; சண்டை மனம் (நூல் குறிப்பு)']),
    'Anuradha': ('Saturn', 211, 'rich, lives in foreign lands, unable to bear hunger, disposed to wander from place to place',
                 ['செல்வம்; வெளிநாட்டு வாழ்க்கை', 'பசி தாங்காதவர்; இடம் மாறித் திரியும் இயல்பு']),
    'Jyeshtha': ('Mercury', 211, 'few friends, very cheerful, virtuous, of irascible temper',
                 ['மிகுந்த மகிழ்ச்சி; நல்லொழுக்கம்', 'நண்பர்கள் குறைவு; கோபக் குணம்']),
    'Mula': ('Ketu', 211, 'haughty, rich, happy, not disposed to injure others, of firm views, lives in luxury',
             ['செல்வம்; மகிழ்ச்சி; உறுதியான கருத்து; சொகுசு வாழ்க்கை', 'மற்றவரைத் துன்புறுத்தாத இயல்பு; சற்று பெருமிதம்']),
    'Purva Ashadha': ('Venus', 211, 'an agreeable wife, proud, attached to friends',
                      ['நல்ல குடும்ப வாழ்க்கை; நண்பர்களிடம் பற்று', 'சற்று பெருமை குணம்']),
    'Uttara Ashadha': ('Sun', 211, 'obedient, learned in the rules of virtue, many friends, grateful, returns favours, generally liked',
                       ['ஒழுக்க விதிகளில் கற்றவர்; நன்றி உணர்வு; நல்லுறவு திருப்பிச் செய்வவர்', 'நண்பர்கள் பலர்; எல்லோருக்கும் பிடித்தவர்']),
    'Shravana': ('Moon', 211, 'prosperous, learned, a liberal-minded wife, rich, of wide-spread fame',
                 ['செழிப்பு; கல்வி; செல்வம்; பரவலான புகழ்', 'தாராள மனப்பான்மையான வாழ்க்கைத் துணை']),
    'Dhanishta': ('Mars', 211, 'liberal in gifts, rich, valiant, fond of music, a niggard',
                  ['தாராளமாக கொடுப்பவர்; செல்வம்; வீரம்', 'இசை விருப்பம்; சில நேரம் இழிபிடி (நூல் குறிப்பு)']),
    'Shatabhisha': ('Rahu', 211, 'harsh in speech, truthful, suffers grief, conquers enemies, thoughtlessly engages in work, of independent ways',
                    ['உண்மை; எதிரிகளை வெல்பவர்; சுதந்திர வழி', 'கடினமான பேச்சு; துன்பம் அனுபவிப்பவர்']),
    'Purva Bhadrapada': ('Jupiter', 211, 'suffers from grief, places his wealth at the disposal of his wife, of distinct speech, a niggard',
                         ['தெளிவான பேச்சு; செல்வத்தை மனைவியிடம் ஒப்படைப்பவர்', 'துன்ப அனுபவம்; இழிபிடித்தனம் (நூல் குறிப்பு)']),
    'Uttara Bhadrapada': ('Saturn', 211, 'an able speaker, happy, possesses children and grand-children, conquers enemies, virtuous',
                          ['திறமையான பேச்சாளர்; மகிழ்ச்சி; நல்லொழுக்கம்', 'பிள்ளைகள், பேரப்பிள்ளைகள்; எதிரிகளை வெல்பவர்']),
    'Revati': ('Mercury', 212, 'perfect limbs, liked by all people, valiant in fight, never covets the property of others, rich',
               ['அழகிய உடலமைப்பு; எல்லோருக்கும் பிடித்தவர்', 'போரில் வீரம்; பிறர் சொத்தில் ஆசையற்றவர்; செல்வம்']),
}
NAKSHATRA_BJ_NOTE = ('Brihat Jataka ch. XVI chapter note: the effects described fully come to pass '
                     'only if the Moon is powerful.')

NAKSHATRA_NOTICE = {
    'en': 'Our eight-book library has no direct "presiding deity of the nakshatra" table. What it does give: '
          'each nakshatra\u2019s birth traits (Brihat Jataka ch. XVI), each nakshatra\u2019s Vimshottari dasha lord '
          '(Brihat Jataka ch. VIII), and each planet\u2019s presiding deity (Phaladeepika ch. II; a second list in '
          'Brihat Jataka ch. II). The deity below is assembled from that chain and labelled derived - it is the '
          'dasha-lord planet\u2019s deity, not a quoted nakshatra devata.',
    'ta': 'நம் நூல் தொகுப்பில் நட்சத்திர அதிதேவதை அட்டவணை நேரடியாக இல்லை. இருப்பது: நட்சத்திரப் பிறப்பு இயல்புகள், '
          'நட்சத்திரத்தின் திசா அதிபதி, கிரகத்தின் அதிதேவதை. கீழே உள்ள தெய்வம் இந்தச் சங்கிலியிலிருந்து உருவாக்கப்பட்டது '
          '(derived) - திசா அதிபதி கிரகத்தின் தெய்வம், நேரடி நட்சத்திர தேவதை அல்ல.',
}

# ---- Signs ---------------------------------------------------------------
# Person traits: Brihat Jataka ch. XVII, "On the Moon in the Several Signs of
# the Zodiac" (PDF pp. 213-216); ASI ch. IX (PDF pp. 187-189) gives the same
# tradition in shorter form (corroboration in the docs note). Sign body-parts:
# Brihat Jataka ch. I, sloka 4 (PDF pp. 46-47). Chapter caveat: sloka 13 -
# effects are full only when the Moon, its sign and the sign's lord are all
# powerful.

SIGNS12 = ('Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio',
           'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces')
SIGN_TA = {'Aries': 'மேஷம்', 'Taurus': 'ரிஷபம்', 'Gemini': 'மிதுனம்', 'Cancer': 'கடகம்',
           'Leo': 'சிம்மம்', 'Virgo': 'கன்னி', 'Libra': 'துலாம்', 'Scorpio': 'விருச்சிகம்',
           'Sagittarius': 'தனுசு', 'Capricorn': 'மகரம்', 'Aquarius': 'கும்பம்', 'Pisces': 'மீனம்'}
SIGN_BODY = {'Aries': 'head', 'Taurus': 'face', 'Gemini': 'breast', 'Cancer': 'heart', 'Leo': 'belly',
             'Virgo': 'navel', 'Libra': 'abdomen', 'Scorpio': 'genital organ', 'Sagittarius': 'two thighs',
             'Capricorn': 'two knees', 'Aquarius': 'two ankles', 'Pisces': 'two feet'}
SIGN_BODY_TA = {'Aries': 'தலை', 'Taurus': 'முகம்', 'Gemini': 'மார்பு', 'Cancer': 'இதயம்', 'Leo': 'வயிறு',
                'Virgo': 'நாபி', 'Libra': 'குலாவ்', 'Scorpio': 'உறுப்பு', 'Sagittarius': 'தொடைகள்',
                'Capricorn': 'முழங்கால்கள்', 'Aquarius': 'கணுக்கால்கள்', 'Pisces': 'பாதங்கள்'}
# sign: (BJ XVII page, English traits, Tamil points)
SIGN_DATA = {
    'Aries': (213, 'round red eyes; fond of vegetable food and hot meals in moderation; quickly relenting; '
                   'fond of travels; weak knees; no permanent wealth; fond of fight; skilled in serving others; '
                   'haughty; eldest of his brothers; fickle-minded; afraid of water',
              ['செவ்விழி; விரைவில் மனம் மாறும் குணம்', 'பயண விருப்பம்; சண்டை மனம்; திடமான செல்வம் குறைவு', 'மூத்தோர்; தன்னிடை நிலை தடுமாறும் மனம்']),
    'Taurus': (213, 'fine appearance and beautiful gait; large thighs and face; liberal in gifts; bears misfortunes; '
                    'great influence and authority; daughters; liked by all; patient; a great eater; attached to friends; '
                    'happy in middle and old age',
               ['அழகிய தோற்றம், அழகிய நடை; தாராளமாக கொடுப்பவர்', 'துன்பம் தாங்கும் மனம்; செல்வாக்கு; எல்லோருக்கும் பிடித்தவர்', 'நண்பர்களிடம் பற்று; நடு, மூப்பு வயதில் மகிழ்ச்சி']),
    'Gemini': (213, 'fond of women; red eyes; learned in the Sastras; carries messages; curling hair, sharp intellect; '
                    'skilled in wit and in discovering the thoughts of others; beautiful features; sweet speech; a great '
                    'eater; fond of music and dance; elevated nose',
               ['கூர்மையான புத்தி; மற்றவர் நினைவை அறியும் திறம்', 'சாஸ்திர கல்வி; இனிய பேச்சு; அழகிய தோற்றம்', 'இசை, நடன ஆர்வம்; சுருண்டை முடி']),
    'Cancer': (213, 'walks fast with bent body; subject to the influence of women; an excellent friend; learned in '
                    'astrology; numerous houses; wealth increasing and decreasing like the Moon; short; won over by kind '
                    'words; attached to friends; fond of water and forests',
               ['ஜோதிட கல்வி; சிறந்த நண்பர்; வீடுகள் பல', 'சந்திரனைப் போல ஏற்ற இறக்கச் செல்வம்', 'அன்பான வார்த்தையில் அடங்குபவர்; நீர், காடு விருப்பம்']),
    'Leo': (213, 'irascible temper; large cheeks, broad face, brown eyes; few sons; fond of animal food, forests and '
                 'hills; anger at trifles lasts long; liberal in gifts; bold in fight; fixed principles; haughty; '
                 'attached to his mother',
            ['உறுதியான கொள்கை; போரில் துணிவு; தாராளம்', 'சிறு விஷயத்தில் நீளும் கோபம்', 'காடு, மலை விருப்பம்; தாயிடம் பற்று']),
    'Virgo': (213, 'lovely eyes and slow gait through modesty; lives in comfort; soft body and speech; truthful; skilled '
                   'in dance, music, painting and book-making; learned in the Sastras; virtuous and intelligent; lives in '
                   'foreign lands; sweet speech; daughters and few sons',
              ['அழகிய கண்கள்; நாணம்; மென்மையான பேச்சு; உண்மை', 'நடனம், இசை, ஓவியம், எழுத்துத் திறமை', 'சாஸ்திர கல்வி; வெளிநாட்டு வாழ்க்கை']),
    'Libra': (214, 'respects Devas, Brahmins and holy men; intelligent; never covets the property of others; learned in '
                   'the Vedas; tall; fond of travels; rich; a trader; protects his family; rejected by kinsmen',
              ['தெய்வீக மரியாதை; பிறர் சொத்தில் ஆசையற்றவர்; வேத கல்வி', 'உயரம்; பயண விருப்பம்; வியாபாரி; செல்வம்', 'குடும்பத்தைக் காப்பவர்; உறவினர்களால் விலக்கப்படுபவர் (நூல் குறிப்பு)']),
    'Scorpio': (214, 'broad eyes, broad breast, round shanks, thighs and knees; separated from parents and preceptors; '
                     'afflicted with diseases when young; respected by the king\u2019s family; not of a straightforward '
                     'nature; conceals sins',
                ['அகன்ற கண்கள், அகன்ற மார்பு', 'இளம் வயதில் உடல்நலக் குறைவு; பெரியோர் மரியாதை', 'நேரடியாகாத குணம் என நூல் குறிப்பிடுகிறது']),
    'Sagittarius': (214, 'long face and neck; inherits his father\u2019s property; liberal in gifts; a literary author; '
                         'powerful and skilled in speech; engages in numerous works; skilled in fine arts; deep inventive '
                         'intellect; yields to kind treatment, never to compulsion',
                    ['தந்தை சொத்து வாரிசு; தாராளம்; இலக்கிய ஆசிரியர்', 'பேச்சுத் திறமை; பல செயல்கள்; கலை நுணுக்கம்', 'அன்பில் அடங்குபவர்; கட்டாயத்தில் அடங்காதவர்']),
    'Capricorn': (215, 'ever attached to wife and children; weak lower limbs, good eyes, thin waist; readily understands '
                       'what is spoken; liked by all; slow at work; cannot bear cold; wandering nature; liberal or powerful; '
                       'a literary author; shameless and merciless',
                  ['மனைவி, பிள்ளைகளிடம் பற்று; எல்லோருக்கும் பிடித்தவர்', 'சொன்னதை உடனே புரிந்துகொள்பவர்; இலக்கிய ஆசிரியர்', 'வேலையில் மெதுவானவர்; குளிர் தாங்காதவர்; திரியும் இயல்பு']),
    'Aquarius': (215, 'camel-like neck; muscular rough hairy body; tall; rises and falls by turns; fond of flowers and '
                      'perfumes; attached to friends; walks without feeling tired',
                 ['உயரமான உருண்ட உடல்', 'ஏற்ற இறக்கமான வாழ்க்கை; பூ, நறுமணம் விருப்பம்', 'நண்பர்களிடம் பற்று; சோர்வற்ற நடை']),
    'Pisces': (215, 'a dealer in the produce of the sea; fond of his wife and clothes; perfect limbs, bright body, long '
                    'nose, large head; puts his enemies to disgrace; beautiful eyes; fair; enjoys hidden treasure; rich; learned',
               ['கடல் பொருட்கள் வியாபாரம்; மனைவி, ஆடை மீது பற்று', 'அழகிய கண்கள்; எதிரிகளை அவமதிப்பவர்', 'மறைந்த புதையல் அனுபவிப்பவர்; செல்வம்; கல்வி']),
}
SIGN_BJ_NOTE = ('Brihat Jataka ch. XVII, sloka 13: the effects fully come to pass only when the Moon, the sign '
                'occupied by the Moon, and the lord of that sign are all powerful.')
SIGN_NOTICE = {
    'en': 'These are the classical Moon-in-sign character lists (the rasi the Moon occupied at birth), quoted from '
          'Brihat Jataka ch. XVII with the Astrological Self-Instructor\u2019s parallel list as corroboration. The '
          'books mix flattering and harsh traits in every sign; choose reel lines deliberately and keep the source '
          'frame visible.',
    'ta': 'இவை பிறப்பில் சந்திரன் இருந்த ராசிக்கான பாரம்பரியக் குணக் குறிப்புகள் (Brihat Jataka ch. XVII). '
          'ஒவ்வொரு ராசியிலும் நல்லவை கெட்டவை கலந்தே உள்ளன; வாசகங்களை தேர்வு செய்யும்போது ஆதாரத்தை மனதில் வையுங்கள்.',
}

# ---- Card assembly --------------------------------------------------------

TOOLS = ('weekday', 'nakshatra', 'graha', 'sign')
HASHTAGS = {
    'weekday': '#astrotamil #tamiljothidam #tamilreels #tamilastrology',
    'nakshatra': '#astrotamil #tamiljothidam #nakshatra #tamilastrology',
    'graha': '#astrotamil #tamiljothidam #remedies #trendingtamil',
    'sign': '#astrotamil #tamiljothidam #rasi #tamilastrology',
}
GENERAL_NOTICE = ('Historical astrological interpretations for content drafting, not validated prediction. '
                  'Books mix flattering and harsh traits; pick reel lines deliberately.')


def _bullet(ta, en, source, kind):
    return {'ta': ta, 'en': en, 'source': source, 'kind': kind}


def _finish(tool, choice, title_en, title_ta, hook_ta, bullets, notices, cta_ta):
    caption_lines = [hook_ta, '']
    caption_lines += [f'\u2022 {b["ta"]}' for b in bullets if b.get('ta')]
    caption_lines += ['', cta_ta, '', HASHTAGS[tool]]
    return {
        'tool': tool, 'choice': choice, 'title_en': title_en, 'title_ta': title_ta,
        'hook_ta': hook_ta, 'bullets': bullets, 'notices': notices, 'cta_ta': cta_ta,
        'hashtags': HASHTAGS[tool], 'caption_text': '\n'.join(caption_lines),
        'general_notice': GENERAL_NOTICE,
    }


def weekday_card(day):
    if day not in WEEKDAYS:
        raise ValueError(f'Unknown weekday: {day!r}. Choose one of {", ".join(WEEKDAYS)}.')
    lord = WEEKDAY_LORD[day]
    lord_src = WEEKDAY_LORD_SOURCE
    nature_src = f'{PHALA}, ch. II, sloka {NATURE_PHALA_SLOKA[lord]}, PDF p. {NATURE_PHALA_PAGE[lord]}'
    bullets = [
        _bullet(f'{WEEKDAY_TA[day]} கிழமையின் அதிபதி: {PLANET_TA[lord]}',
                f'{day} is ruled by {lord} (weekday names derive from the succession of planetary horas).',
                lord_src, 'cited'),
        _bullet(WEEKDAY_POINTS_TA[day][0], NATURE_PHALA[lord], nature_src, 'derived'),
        _bullet(WEEKDAY_POINTS_TA[day][1], f'Colour: {COLOR_BJ[lord]}; direction: {DIRECTION_BJ[lord]}; '
                f'deva: {DEITY_BJ[lord]}.', f'{BJ}, ch. II, sloka 5, PDF p. 61', 'derived'),
        _bullet(WEEKDAY_POINTS_TA[day][2], 'The Tamil points above render the day-lord\u2019s cited nature; '
                'they are not a quoted weekday-birth rule.', None, 'derived'),
    ]
    return _finish(
        'weekday', day, f'{day} child (weekday lord)', f'{WEEKDAY_TA[day]} கிழமை குழந்தை',
        'உங்கள் குழந்தை எந்தக் கிழமையில் பிறந்தது?', bullets,
        [WEEKDAY_NOTICE],
        'உங்கள் குழந்தை பிறந்த கிழமையை கமென்டில் சொல்லுங்கள்')


def nakshatra_card(name):
    if name not in NAKSHATRA_DATA:
        raise ValueError(f'Unknown nakshatra: {name!r}.')
    lord, page, traits_en, points_ta = NAKSHATRA_DATA[name]
    traits_src = f'{BJ}, ch. XVI, PDF p. {page}'
    dasha_src = f'{BJ}, ch. VIII, PDF p. 139'
    deity_src = f'{PHALA}, ch. II, sloka 27, PDF p. 57'
    bullets = [
        _bullet(points_ta[0], f'Moon in {name}: {traits_en}', traits_src, 'cited'),
        _bullet(points_ta[1], f'Chapter note: {NAKSHATRA_BJ_NOTE}', traits_src, 'cited'),
        _bullet(f'{NAKSHATRA_TA[name]} நட்சத்திரத்தின் திசா அதிபதி: {PLANET_TA[lord]}',
                f'Vimshottari dasha lord of {name}: {lord}.', dasha_src, 'cited'),
        _bullet(f'அதிபதி கிரகத்தின் அதிதேவதை: {DEITY_PHALA_TA[lord]}',
                f'Presiding deity of {lord}: {DEITY_PHALA[lord]}'
                + (f' (Brihat Jataka ch. II lists {DEITY_BJ[lord]} instead).' if DEITY_BJ[lord] else '.'),
                deity_src + (f'; {BJ}, ch. II, sloka 5, PDF p. 61' if DEITY_BJ[lord] else ''), 'derived'),
    ]
    return _finish(
        'nakshatra', name, f'{name} nakshatra', f'{NAKSHATRA_TA[name]} நட்சத்திரம்',
        'உங்கள் நட்சத்திரத்தின் அதிதேவதை தெரியுமா?', bullets,
        [NAKSHATRA_NOTICE],
        'உங்கள் நட்சத்திரத்தை கமென்டில் சொல்லுங்கள்')


def graha_card(planet):
    if planet not in PLANETS:
        raise ValueError(f'Unknown graha: {planet!r}.')
    b = []
    b.append(_bullet(f'அதிதேவதை: {DEITY_PHALA_TA[planet]}',
                     f'Presiding deity: {DEITY_PHALA[planet]}'
                     + (f'. Brihat Jataka ch. II lists {DEITY_BJ[planet]}.' if DEITY_BJ[planet] else ''),
                     f'{PHALA}, ch. II, sloka 27, PDF p. 57'
                     + (f'; {BJ}, ch. II, sloka 5, PDF p. 61' if DEITY_BJ[planet] else ''), 'cited'))
    b.append(_bullet(f'ரத்தினம்: {GEM_PHALA_TA[planet]}', f'Gem: {GEM_PHALA[planet]}',
                     f'{PHALA}, ch. II, sloka 29, PDF pp. 57-58', 'cited'))
    if SUBSTANCE_PHALA[planet]:
        b.append(_bullet(f'உலோகம்: {SUBSTANCE_PHALA_TA[planet]}',
                         f'Substance: {SUBSTANCE_PHALA[planet]} (Phaladeepika); {METAL_BJ[planet]} (Brihat Jataka).',
                         f'{PHALA}, ch. II, sloka 30, PDF p. 58; {BJ}, ch. II, sloka 12, PDF p. 63', 'cited'))
    b.append(_bullet(f'தானியம்: {GRAIN_PHALA_TA[planet]}', f'Grain: {GRAIN_PHALA[planet]}',
                     f'{PHALA}, ch. II, sloka 28, PDF p. 57', 'cited'))
    row = []
    if COLOR_BJ[planet]:
        row.append(f'colour {COLOR_BJ[planet]}')
    if DIRECTION_BJ[planet]:
        row.append(f'direction {DIRECTION_BJ[planet]}')
    if row:
        ta_row = []
        if COLOR_BJ_TA[planet]:
            ta_row.append(f'நிறம்: {COLOR_BJ_TA[planet]}')
        if DIRECTION_BJ[planet]:
            ta_row.append(f'திசை: {DIRECTION_TA[DIRECTION_BJ[planet]]}')
        b.append(_bullet('; '.join(ta_row), '; '.join(row).capitalize() + '.',
                         f'{BJ}, ch. II, sloka 5, PDF p. 61', 'cited'))
    if FLAVOUR_PHALA[planet]:
        b.append(_bullet(f'சுவை: {FLAVOUR_PHALA_TA[planet]}', f'Flavour: {FLAVOUR_PHALA[planet]}',
                         f'{PHALA}, ch. II, sloka 31, PDF p. 58', 'cited'))
    if PLACE_BJ[planet]:
        b.append(_bullet(f'இடம்: {PLACE_BJ_TA[planet]}',
                         f'Place: {PLACE_BJ[planet]}; garment: {GARMENT_BJ[planet]}.',
                         f'{BJ}, ch. II, sloka 12, PDF p. 63', 'cited'))
    b.append(_bullet(SHANTI_RULE['text_ta'], SHANTI_RULE['text_en'], SHANTI_RULE['source'], 'cited'))
    notice = {
        'en': 'The modern "one remedy per graha" list is not in our books. What is: the cited deity, gem, grain, '
              'colour, direction and substance of each graha above, and Phaladeepika ch. XXVI\u2019s general shanti '
              'rule (prayers, gifts, vows, adorations) for a badly placed planet. The two books disagree on some '
              'associations (e.g. metals, deities); both are shown.',
        'ta': 'ஒரு கிரகத்திற்கு ஒரு பரிகாரம் என்ற நவீன பட்டியல் நம் நூல்களில் இல்லை. மேலே உள்ளவை நூலில் உள்ள '
              'கிரகத் தொடர்புகள்; பரிகாரம் பற்றி பலதீபிகை அதியாயம் 26 சொல்லும் பொது விதி கடைசி குறிப்பு. '
              'சில தொடர்புகளில் இரு நூல்களும் வேறுபடுகின்றன; இரண்டும் காட்டப்பட்டுள்ளன.',
    }
    return _finish(
        'graha', planet, f'{planet} graha card', f'{PLANET_TA[planet]} கிரகம்',
        '9 கிரகங்களுக்கும் நூல்கள் சொல்லும் தொடர்புகள் தெரியுமா?', b, [notice],
        'உங்களுக்குப் புதிதாகத் தெரிந்தது எது? கமென்டில் சொல்லுங்கள்')


def sign_card(sign):
    if sign not in SIGN_DATA:
        raise ValueError(f'Unknown sign: {sign!r}.')
    page, traits_en, points_ta = SIGN_DATA[sign]
    traits_src = f'{BJ}, ch. XVII, PDF p. {page}'
    bullets = [
        _bullet(points_ta[0], f'Moon in {sign}: {traits_en}', traits_src, 'cited'),
        _bullet(points_ta[1], f'Parallel list in {ASI}, ch. IX, PDF pp. 187-189 (same tradition).',
                f'{ASI}, ch. IX, PDF pp. 187-189', 'cited'),
        _bullet(points_ta[2], f'Caveat: {SIGN_BJ_NOTE}', traits_src, 'cited'),
        _bullet(f'காலபுருஷனின் உடலில் {SIGN_TA[sign]}: {SIGN_BODY_TA[sign]}',
                f'In the frame of Kalapurusha, {sign} is the {SIGN_BODY[sign]}.',
                f'{BJ}, ch. I, sloka 4, PDF pp. 46-47', 'cited'),
    ]
    return _finish(
        'sign', sign, f'{sign} moon-sign traits', f'{SIGN_TA[sign]} ராசி இயல்புகள்',
        f'{SIGN_TA[sign]} ராசியில் பிறந்தவர்களின் இயல்பு என்ன?', bullets,
        [SIGN_NOTICE],
        'உங்கள் ராசியை கமென்டில் சொல்லுங்கள்')


def studio_report(tool, choice):
    if tool not in TOOLS:
        raise ValueError(f'Unknown tool: {tool!r}. Choose one of {", ".join(TOOLS)}.')
    if not isinstance(choice, str):
        raise ValueError('choice must be a string.')
    return {'weekday': weekday_card, 'nakshatra': nakshatra_card,
            'graha': graha_card, 'sign': sign_card}[tool](choice)


def studio_index():
    """Choices per tool, for the picker UI."""
    return {
        'tools': [
            {'id': 'weekday', 'title_en': 'Weekday child', 'title_ta': 'கிழமை குழந்தை',
             'choices': [{'id': d, 'en': d, 'ta': WEEKDAY_TA[d]} for d in WEEKDAYS]},
            {'id': 'nakshatra', 'title_en': 'Nakshatra deity + traits', 'title_ta': 'நட்சத்திரம்',
             'choices': [{'id': n, 'en': n, 'ta': NAKSHATRA_TA[n]} for n in NAKSHATRAS]},
            {'id': 'graha', 'title_en': 'Graha card', 'title_ta': 'கிரகம்',
             'choices': [{'id': p, 'en': p, 'ta': PLANET_TA[p]} for p in PLANETS]},
            {'id': 'sign', 'title_en': 'Moon-sign traits', 'title_ta': 'ராசி இயல்பு',
             'choices': [{'id': s, 'en': s, 'ta': SIGN_TA[s]} for s in SIGNS12]},
        ],
        'general_notice': GENERAL_NOTICE,
  }
