#!/usr/bin/env python3
"""Page-faithful text extraction for the Horoscope_Ventrue book scans.

Every output line of text is anchored to a PDF page number so the app can
cite rules as (book, page) and render that exact page image for human
verification before treating a citation as trustworthy. Raw OCR output is
never authoritative on its own - always verify against the page image
(render_page.sh) before shipping a rule.

Modes per book (see books.json):
  ocr  - image scan: render each page with pdftoppm, OCR with tesseract
  text - digital text layer: pdftotext per page (keeps page mapping)

Outputs per book in extracted/:
  <slug>.txt         human-readable, one "===== [book | PDF page N] ====="
                     header per page
  <slug>.pages.jsonl one JSON object per page: {"book", "pdf_page", "text"}

Usage:
  python3 pipeline/extract.py --pdf-dir pdfs --out-dir extracted [--only slug ...]
Dependencies: poppler-utils (pdftoppm, pdftotext, pdfinfo), tesseract-ocr.
"""
import argparse, json, os, re, subprocess, sys, tempfile

DPI = 200          # 300dpi OOMs on 2GB machines and is no more accurate on these scans
TESS_LANG = "eng"
PSM = "3"


def pdf_pages(pdf):
    out = subprocess.run(["pdfinfo", pdf], capture_output=True, text=True, check=True).stdout
    return int(re.search(r"^Pages:\s+(\d+)", out, re.M).group(1))


def ocr_page(pdf, page, workdir):
    """Render one page and OCR it. Returns the page text."""
    base = os.path.join(workdir, f"p{page}")
    subprocess.run(["pdftoppm", "-f", str(page), "-l", str(page), "-r", str(DPI),
                    "-gray", "-png", pdf, base], check=True, capture_output=True)
    pngs = [f for f in os.listdir(workdir) if f.startswith(f"p{page}-") and f.endswith(".png")]
    if not pngs:
        raise RuntimeError(f"no render for page {page}")
    png = os.path.join(workdir, pngs[0])
    out_base = os.path.join(workdir, f"o{page}")
    env = dict(os.environ, OMP_THREAD_LIMIT="2")
    subprocess.run(["tesseract", png, out_base, "--psm", PSM, "-l", TESS_LANG],
                   check=True, capture_output=True, env=env)
    with open(out_base + ".txt", encoding="utf-8") as fh:
        text = fh.read()
    os.remove(png); os.remove(out_base + ".txt")
    return text


def text_page(pdf, page):
    out = subprocess.run(["pdftotext", "-f", str(page), "-l", str(page), pdf, "-"],
                         capture_output=True, text=True, check=True)
    return out.stdout


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf-dir", default="pdfs")
    ap.add_argument("--out-dir", default="extracted")
    ap.add_argument("--only", nargs="*", default=None)
    ap.add_argument("--status-file", default=None, help="append one status line per finished page")
    args = ap.parse_args()

    with open("books.json", encoding="utf-8") as fh:
        registry = json.load(fh)["books"]
    os.makedirs(args.out_dir, exist_ok=True)

    for book in registry:
        slug = book["slug"]
        if args.only and slug not in args.only:
            continue
        pdf = os.path.join(args.pdf_dir, book["file"])
        if not os.path.exists(pdf):
            print(f"[{slug}] MISSING {pdf}", flush=True); continue
        pages = pdf_pages(pdf)
        page_texts, failed = [], []
        with tempfile.TemporaryDirectory() as workdir:
            for p in range(1, pages + 1):
                try:
                    t = ocr_page(pdf, p, workdir) if book["mode"] == "ocr" else text_page(pdf, p)
                except Exception as e:  # keep going; a failed page is marked, never silently dropped
                    t, failed = f"[EXTRACTION FAILED on this page: {e}]", failed + [p]
                page_texts.append(t)
                if args.status_file:
                    with open(args.status_file, "a") as sf:
                        sf.write(f"{slug} {p}/{pages}\n")
        txt_path = os.path.join(args.out_dir, f"{slug}.txt")
        jsonl_path = os.path.join(args.out_dir, f"{slug}.pages.jsonl")
        with open(txt_path, "w", encoding="utf-8") as fh:
            fh.write(f"{book['title']} ({book.get('year') or 'n.d.'}) - {book.get('author') or ''}\n")
            fh.write(f"Translator: {book.get('translator') or 'n/a'} | Coverage: {book['coverage']}\n")
            fh.write("Cite as (slug, PDF page). Verify against the page image before trusting a rule.\n\n")
            for i, t in enumerate(page_texts, 1):
                fh.write(f"===== [{slug} | PDF page {i}] =====\n{t.strip()}\n\n")
        with open(jsonl_path, "w", encoding="utf-8") as fh:
            for i, t in enumerate(page_texts, 1):
                fh.write(json.dumps({"book": slug, "pdf_page": i, "text": t.strip()},
                                    ensure_ascii=False) + "\n")
        print(f"[{slug}] done: {pages} pages, {len(failed)} failed {failed[:10]}", flush=True)


if __name__ == "__main__":
    sys.exit(main())
