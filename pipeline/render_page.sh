#!/usr/bin/env bash
# Render one PDF page as PNG for citation verification.
# Usage: pipeline/render_page.sh pdfs/<file>.pdf <page> [out.png] [dpi]
set -euo pipefail
PDF="$1"; PAGE="$2"; OUT="${3:-page.png}"; DPI="${4:-200}"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
pdftoppm -f "$PAGE" -l "$PAGE" -r "$DPI" -gray -png "$PDF" "$TMP/p"
mv "$TMP"/p-*.png "$OUT"
echo "$OUT"
