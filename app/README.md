# Local chart research preview

Run from the repository root:

```sh
python3 -m venv .venv
.venv/bin/pip install -r engine/requirements-research.txt
.venv/bin/python app/server.py
# Open http://127.0.0.1:8000
```

This is a phone-first UI over `engine.research_input_report`, not a new astrology
engine. It shows explicit modern chart placements, Moon nakshatra, source
reference metadata and period arithmetic in solar-year units. Complete strength,
selected historical calendar, personal outcomes and predictive accuracy stay
unavailable. Source text interpretations are not displayed without scanned-page
verification in the app. There are no accounts, analytics, stored charts or
third-party geocoding. Request bodies are not logged by the local/API handler.
Hosting providers may retain operational metadata; review their policy before
public launch.

Public deployment is intentionally NOT configured yet. Swiss Ephemeris license
choice and source-rights review remain launch gates. This code does not choose
an AGPL license or buy a professional license for the owner. Place lookup uses OpenStreetMap Nominatim (one request per lookup, throttled to its usage policy, no query logging by the local handler). The API adapter is
ready for later Python hosting but must not be described as publicly deployed.

Verification:

```sh
.venv/bin/python -m unittest discover -s tests -q
npm ci
npx playwright install chromium
npx playwright test
```

Playwright starts the local server and tests phone/desktop widths, real engine
results, errors, input escaping, research gates and accessible disclosure.
