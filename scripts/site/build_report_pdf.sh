#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
CHROME="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
SOURCE="$REPO_ROOT/docs/report.md"
HTML="$REPO_ROOT/build/report-pdf/report.html"
OUT="$REPO_ROOT/docs/report.pdf"

if [[ ! -x "$CHROME" ]]; then
  echo "Chrome executable not found: $CHROME" >&2
  exit 1
fi

cd "$REPO_ROOT"

uv run \
  --with markdown==3.6 \
  --with beautifulsoup4==4.12.3 \
  python scripts/site/render_report_pdf.py "$SOURCE" "$HTML"

HTML_URL="$(python3 -c 'from pathlib import Path; import sys; print(Path(sys.argv[1]).resolve().as_uri())' "$HTML")"

"$CHROME" \
  --headless=new \
  --disable-gpu \
  --no-pdf-header-footer \
  --run-all-compositor-stages-before-draw \
  --virtual-time-budget=10000 \
  --print-to-pdf="$OUT" \
  "$HTML_URL"

pdfinfo "$OUT" | grep -E "Title|Creator|Producer|Pages|Page size|File size|PDF version"
