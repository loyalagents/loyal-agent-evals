#!/usr/bin/env python3
"""Static verification for the Loyal Agent Evals website."""

from __future__ import annotations

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit


REPO = Path(__file__).resolve().parents[2]
ROUTES = [
    "index.html",
    "report/index.html",
    "results/index.html",
    "walkthroughs/index.html",
    "methodology/index.html",
    "framework/index.html",
    "tos/index.html",
    "artifacts/index.html",
    "contract/index.html",
]
HARD_LEAK_RE = re.compile(r"/Users/|Dropbox|file://|/tmp/\w")


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[tuple[str, str]] = []
        self.walkthrough_ids: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = dict(attrs)
        for key in ("href", "src"):
            if key in attr and attr[key]:
                self.links.append((key, attr[key] or ""))
        if tag == "article" and attr.get("data-scenario-id"):
            self.walkthrough_ids.append(attr["data-scenario-id"] or "")


def fail(message: str) -> None:
    raise SystemExit(message)


def route_paths() -> list[Path]:
    paths = [REPO / route for route in ROUTES]
    missing = [str(path.relative_to(REPO)) for path in paths if not path.exists()]
    if missing:
        fail("Missing route HTML: " + ", ".join(missing))
    return paths


def url_strategy_check(files: list[Path]) -> None:
    site_files = files + list((REPO / "assets").glob("**/*.css")) + list((REPO / "assets").glob("**/*.js"))
    attr_re = re.compile(r'\b(?:href|src|action|data-[\w-]+)\s*=\s*"(/[^"]*)"')
    fetch_re = re.compile(r'\bfetch\s*\(\s*"(/[^"]*)"')
    hits: list[str] = []
    for file in site_files:
        text = file.read_text(errors="replace")
        for match in attr_re.finditer(text):
            url = match.group(1)
            if url.startswith("//") or url.startswith("/loyal-agent-evals/"):
                continue
            hits.append(f"{file.relative_to(REPO)}: {url}")
        for match in fetch_re.finditer(text):
            url = match.group(1)
            if url.startswith("//") or url.startswith("/loyal-agent-evals/"):
                continue
            hits.append(f"{file.relative_to(REPO)}: fetch({url})")
    if hits:
        fail("Root-relative internal URLs detected:\n  " + "\n  ".join(hits))


def linked_artifact_sweep(files: list[Path]) -> None:
    targets: set[Path] = set()
    missing: list[str] = []
    for html in files:
        parser = LinkParser()
        parser.feed(html.read_text(errors="replace"))
        for _, target in parser.links:
            clean = target.split("#", 1)[0].split("?", 1)[0]
            if not clean or clean.startswith("#") or clean.startswith("mailto:"):
                continue
            if clean.startswith("//") or clean.startswith("http://") or clean.startswith("https://"):
                continue
            resolved = (html.parent / clean).resolve()
            try:
                rel = resolved.relative_to(REPO)
            except ValueError:
                fail(f"Link escapes repo: {html.relative_to(REPO)} -> {target}")
            if not resolved.exists():
                missing.append(f"{html.relative_to(REPO)} -> {target} (expected {rel})")
                continue
            if resolved.is_file():
                targets.add(resolved)
    if missing:
        fail("Linked targets missing from disk:\n  " + "\n  ".join(missing))

    scan_files = files + sorted(targets)
    hits: list[str] = []
    for file in scan_files:
        text = file.read_text(errors="replace")
        for line_no, line in enumerate(text.splitlines(), 1):
            if HARD_LEAK_RE.search(line):
                hits.append(f"{file.relative_to(REPO)}:{line_no}: {line.strip()[:180]}")
    if hits:
        fail("Hard-leak hits:\n  " + "\n  ".join(hits))
    print(f"OK linked-artifact sweep: scanned {len(scan_files)} files.")


def report_reference_check() -> None:
    text = (REPO / "report" / "index.html").read_text(errors="replace")
    for ref_id in range(1, 12):
        if f'id="ref-{ref_id}"' not in text:
            fail(f"Missing bibliography anchor ref-{ref_id}")
    for ref_id in sorted(set(re.findall(r'href="#ref-(\d+)"', text)), key=int):
        if f'id="ref-{ref_id}"' not in text:
            fail(f"In-text reference link lacks bibliography anchor: ref-{ref_id}")
    if '<ol class="bibliography">' not in text:
        fail("Missing visible bibliography list")


def data_checks() -> None:
    site = json.loads((REPO / "assets/data/site_data.v1.json").read_text())
    a = site["headline_results"]["frame_a"]
    b = site["headline_results"]["frame_b"]
    if (a["passed"], a["substantive_denominator"], round(a["pass_rate"], 3)) != (33, 40, 0.825):
        fail("Frame A headline mismatch")
    if (b["passed"], b["substantive_denominator"], round(b["pass_rate"], 3)) != (7, 7, 1.0):
        fail("Frame B headline mismatch")

    for name in ("frame_a", "frame_b"):
        frame = json.loads((REPO / "assets/data" / f"{name}.v1.json").read_text())
        for item in frame["items"]:
            for score in item["scores"]:
                if score["applicable"] and score["status"] != "N/A" and score["score"] is None:
                    fail(f"Null score on applicable row: {name} {item['id']} {score['stage_id']}")


def walkthrough_check() -> None:
    parser = LinkParser()
    parser.feed((REPO / "walkthroughs/index.html").read_text(errors="replace"))
    ids = parser.walkthrough_ids
    if len(ids) != 8 or len(set(ids)) != 8:
        fail(f"Expected 8 unique walkthrough cards, found {len(ids)} / {len(set(ids))}")
    result_ids: list[str] = []
    for name in ("frame_a", "frame_b"):
        frame = json.loads((REPO / "assets/data" / f"{name}.v1.json").read_text())
        result_ids.extend(item["id"] for item in frame["items"])
    duplicates = {value for value in result_ids if result_ids.count(value) != 1}
    if duplicates:
        fail("Duplicate result scenario IDs: " + ", ".join(sorted(duplicates)))
    missing = [value for value in ids if value not in result_ids]
    if missing:
        fail("Walkthrough IDs missing from result data: " + ", ".join(missing))


def site_chrome_overclaim_check(files: list[Path]) -> None:
    chrome_files = [path for path in files if path.relative_to(REPO).as_posix() != "report/index.html"]
    chrome_files += list((REPO / "assets").glob("**/*.css")) + list((REPO / "assets").glob("**/*.js"))
    pat = re.compile(r"Zenodo DOI|CITATION\.cff|v1\.0\.0|PI approval", re.IGNORECASE)
    hits: list[str] = []
    for file in chrome_files:
        text = file.read_text(errors="replace")
        for line_no, line in enumerate(text.splitlines(), 1):
            if pat.search(line):
                hits.append(f"{file.relative_to(REPO)}:{line_no}: {line.strip()[:180]}")
    if hits:
        fail("Site-chrome overclaim hits:\n  " + "\n  ".join(hits))


def main() -> None:
    files = route_paths()
    url_strategy_check(files)
    linked_artifact_sweep(files)
    report_reference_check()
    data_checks()
    walkthrough_check()
    site_chrome_overclaim_check(files)
    print("OK static site verification complete.")


if __name__ == "__main__":
    main()
