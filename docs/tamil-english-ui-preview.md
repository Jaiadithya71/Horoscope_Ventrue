# Tamil-first interface with full English option

Local UI preview, not published. Calculation model, defaults and server endpoints are unchanged.

- First visit opens in Tamil. Header Tamil / English switch stays visible while scrolling and remembers the choice in this browser. Story cards have their own language control.
- Form, uncertain-time choices, result cards, period and phase readings, chart labels, dated periods, notebook controls, errors and calculation caveats follow the selected language.
- English uses transliterated names for Tamil solar years, months, stars, tithi, yoga and karana. Technical source IDs, URLs, IANA time zones and raw JSON remain unchanged.
- No online translation service. Interface strings and paraphrases are kept in a local dictionary. Original report objects remain unchanged.
- Language switching does not make a new calculation request. It preserves form fields, uncertainty warnings, the current story card, opened result disclosures and unsaved notebook fields.
- User-entered client names, birthplace labels and consultation notes are not translated. The device-local private notebook format is unchanged.
- Phone layouts checked at 320px and 390px, desktop at 1280px. Tamil font is embedded and licensed. Controls retain readable spacing and text wrapping.

Verification: 610 Python calculation tests; 44 UI tests including 24 synthetic hourly charts covering all 12 rising signs in both languages, no Tamil leaking into English result prose, no untranslated prose in Tamil except technical identifiers, notebook state/privacy, uncertainty warnings and language persistence.

Astrology readings remain untested against real outcomes. Translation does not increase their accuracy or choose between historical conventions.
