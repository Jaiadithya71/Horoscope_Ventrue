# Horoscope_Ventrue

Deterministic vedic-astrology computation on top of page-cited classical texts.
No AI at runtime: the engine computes chart math and cites rules extracted from
the source books by (book, page).

## What's here

- `books.json` - registry of the source texts: edition, translator, coverage,
  completeness, and per-book caveats. READ THIS before trusting any text:
  some books are partial scans and one carries a dated-stereotypes warning.
- `pipeline/extract.py` - page-faithful text extraction (OCR for image scans,
  pdftotext for digital text). Every page of output is anchored to its PDF
  page number.
- `pipeline/render_page.sh` - renders any cited page back to a PNG so a rule
  citation can be verified against the actual page image. Raw OCR is never
  citable alone.
- `extracted/` - per-book outputs:
  - `<slug>.txt` - human-readable, `===== [slug | PDF page N] =====` per page
  - `<slug>.pages.jsonl` - `{"book", "pdf_page", "text"}` per page, for ingestion

## Source PDFs

The scans live in the SASTRA Drive folder (not committed here):
https://drive.google.com/drive/folders/10kr6uYhD-AiF_Qfm4boJicdD3bU1KWvo
Put them in a local `pdfs/` directory with their original filenames to re-run
the pipeline. Sources and rights notes per book are in `books.json` and in the
Drive folder's "READ FIRST - sources and limits.txt".

## Re-running extraction

```bash
sudo apt install poppler-utils tesseract-ocr   # Debian/Ubuntu
python3 pipeline/extract.py --pdf-dir pdfs --out-dir extracted
# one book only:
python3 pipeline/extract.py --pdf-dir pdfs --out-dir extracted --only phaladeepika-1937
# verify a citation:
pipeline/render_page.sh pdfs/Phaladeepika-1937-English-small.pdf 120 page120.png
```

## Citation contract for the app

- Rules cite `(slug, pdf_page)`; the app renders that page image for
  verification before a rule is shown as authoritative.
- Printed page/chapter/sloka numbers appear inline in the extracted text and
  should be parsed into the rule record when a rule is curated.
- Books marked `partial` in `books.json` must never back a claim that needs
  the missing chapters.
- Sarvartha Chintamani coverage ends around ch.1 stanza 146 (2nd house).
- Brihat Samhita here is mundane astrology (omens/climate/collective), not
  natal; parts 1-6 only.
- Stri Jataka is a 1931 historical text with dated gender stereotypes; flag,
  don't sanitize silently.

Astrology is a tradition, not scientifically validated prediction. Classical
texts carry the assumptions of their era; the app should present them as
historical source material.
