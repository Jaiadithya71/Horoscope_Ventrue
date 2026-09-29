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
