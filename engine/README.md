# Transit research prototype (not a released app)

This is a small, deterministic Moon-sign forecast engine. It computes Lahiri sidereal positions with Swiss Ephemeris's built-in Moshier model, then emits **only** enabled rules whose original PDF pages were checked visually. It cannot reproduce Balaji Haasan's full consultations. It does not generate interpretation with a language model. Read the [public benchmark](../docs/balaji-haasan-public-technique-benchmark.md) before using it.

## License gate

Swiss Ephemeris is dual-licensed: AGPL or a paid professional license. Its owner says the choice must be made before distributing software using it or activating a public service: https://www.astro.com/swisseph/sweph_e.htm . `pyswisseph` binds this library. This code is research-only until the product's compatible license or professional license is decided. No ephemeris binary is committed. Review the edition/scan rights in `books.json` too. Historical astrology is not scientifically validated; outputs are not health, finance or life advice.

## Try locally (Python 3.10+)

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r engine/requirements-research.txt
python3 -m engine.forecast --date 2026-01-01 --moon-sign Aquarius
python3 -m engine.forecast --date 2026-01-01 --birth-date 2000-01-01 --birth-time 14:30 --birth-tz Asia/Kolkata
python3 -m engine.benchmark
python3 -m unittest discover -s tests -v
```

`--date` samples midnight UTC, not local sunrise. A known Moon sign allows like-for-like comparison with public rashi videos. With a person's birth data, date, **real** clock time and IANA timezone are mandatory; never invent a birth time. Birth place is not needed for this Moon-sign-only slice, but it will be mandatory for any future ascendant/house chart. A production system must add geocoding and chart uncertainty, exact transit change timestamps, a licensed ephemeris route, rule conflict handling and much broader verified source coverage.

Rule records cite `(slug, pdf_page, chapter, sloka)`. The enabled Phaladeepika XXVI excerpts were checked against the original scan's PDF pages 330, 331 and 332, not OCR alone. Four narrow examples are enabled. Rule text is a paraphrase and does not claim that Balaji himself applies that verse. No arbitrary interpretations are filled in. Jupiter fifth-from-Moon produces the children-related *traditional reading* from XXVI.19; it does **not** infer a child's marriage. No unsupported detail is promoted to a rule.

The benchmark's seven atomic rows are a tiny transcript-agreement smoke test. It checks four chart positions and three outcome claims. `chart_match` is agreement on calculated positions, not correct prediction; `unsupported` is a missing book-grounded outcome, not a disproved historical event. Both matches and gaps are printed. Evaluation against actual outcomes requires prospective, complete, timestamped forecasts with recorded misses and independently checked events.

## Natal geometry and period research slice

The optional `--birth-place 'Chennai, India' --birth-lat 13.0827 --birth-lon 80.2707` inputs add a Lahiri sidereal ascendant and whole-sign houses to the normal forecast JSON. **The supplied coordinates must be checked against the actual birth place; the name is a label, not a geocoder.** True birth clock time and IANA timezone remain mandatory. A nonexistent or ambiguous DST clock time is rejected rather than silently assigned an instant. Latitude is strictly between -90 and 90 degrees. The astronomical ascendant comes from Swiss Ephemeris `houses_ex` (sidereal, Lahiri); the returned house numbers are whole-sign from the rising sign, not Placidus or house cusps. Moshier's ephemeris is a research approximation; errors in time or coordinates may change the rising sign, especially near a sign boundary.

The natal JSON also contains a Moon-star period sequence. [Phaladeepika XIX.2-3](https://archive.org/details/in.ernet.dli.2015.92117), original scan PDF p. 229 (printed p. 192), lists the nine star lords and their periods and specifies a fractional balance at birth. p. 230 (printed p. 193), XIX.4, defines a solar year by a return of the Sun to its natal longitude. Our 27 equal sidereal sectors and linear fractional balance are labeled computational approximations; the output is **solar-year offsets**, not fabricated calendar dates. The nine complete subperiods use the 120-year proportions described in B. Suryanarain Row's *Astrological Self-Instructor*, scan [source](https://archive.org/details/Astrology_Books_by_B_Suryanarayana_Row), PDF pp. 111-112 (printed pp. 97-98). These source pages were inspected as images. No personal outcome is implied by the period lord alone, and approximate offsets must not be presented as exact dates. Birth input/output should be handled as sensitive personal data in any product.

```bash
python3 -m engine.forecast --date 2026-01-01 --birth-date 2000-01-01 --birth-time 14:30 --birth-tz Asia/Kolkata --birth-place 'Chennai, India' --birth-lat 13.0827 --birth-lon 80.2707
```

## Verified natal rule registry (no unsupported prediction)

[`natal_rules.json`](natal_rules.json) stores the original-scan-checked [Phaladeepika XV.20-21](https://archive.org/details/in.ernet.dli.2015.92117), PDF p. 197 (printed 160): count topical houses from the relevant natal house, or count from a relative's signifying planet. Only the explicit father/Sun and mother/Moon references are calculated at present; the JSON emits reference signs, not life-event conclusions. XV.25 on p. 198 (printed 161) requires the house, lord and karaka all to be strong before a favorable judgment, so it is recorded as **disabled** until strength calculation is implemented. XIX.11 on p. 232 (printed 195) lists traditional Jupiter-dasha outcomes, but likewise remains disabled because precise date and whole-chart judgment are absent. Each of these pages was visually checked; OCR alone was not used as authority. The source material contains unsupported historical claims, including health/lifespan statements: do not turn these into advice or asserted outcomes.
