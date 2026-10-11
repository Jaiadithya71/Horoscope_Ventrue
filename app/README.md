# Horoscope chart research app

Live: https://horoscope-ventrue.vercel.app/

Phone-first UI over the source-led rule engine. Modern Moshier/Lahiri chart
math is explicitly labelled; historical astronomical frame, calendar and
strength choices remain separate research lanes. Passing tests verify code
and arithmetic, not predictive accuracy. No book scans or copied competitor
interpretation content are added by the client-notebook work.

## Local preview and tests

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
npm ci
npx playwright install chromium
.venv/bin/python app/server.py
# http://127.0.0.1:8000
.venv/bin/python -m unittest discover -s tests -q
npx playwright test
```

Place lookup uses OpenStreetMap Nominatim, with one throttled request per
lookup. Birth details go only to this app's calculator endpoints when Calculate
is chosen. Request bodies are not logged by the local/API handler. Hosting
providers can retain operational metadata. No analytics or accounts are added.

## Client notebook

Opt-in local-browser client records keep the exact/uncertain/known-lagna input
mode, birth coordinates/timezone, dated astrologer readings, client-reported
follow-up and private notes. Nothing is automatically saved, uploaded, synced
or submitted for benchmarking. Names and notes are rendered as text, not markup.
The user must obtain client permission.

Storage is not encrypted. Anyone with access to the browser can read it.
Clearing browser data deletes the records; explicit JSON download/import is
available as a private backup. Import validates the format and adds records
without overwriting existing clients. Notes never enter calculation requests.
No new database, paid service or default astrology convention was introduced.

Tests cover notebook persistence, editing, deletion, unsafe text, uncertain time,
corrupt storage and private backup handling, alongside the existing chart tests.
See docs/srirangam-spot-checks.md for the limited external arithmetic comparison.
