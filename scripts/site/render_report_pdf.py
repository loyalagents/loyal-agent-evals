#!/usr/bin/env python3
"""Render docs/report.md into a print-focused HTML source for docs/report.pdf."""

from __future__ import annotations

import argparse
import html
import re
from pathlib import Path

import markdown
from bs4 import BeautifulSoup, Tag

from render_report import guard_text, normalize_references, slugify


REPO_ROOT = Path(__file__).resolve().parents[2]


PDF_CSS = """
:root {
  --text: #20272b;
  --muted: #667076;
  --maroon: #7d2638;
  --gold: #bb8b2d;
  --rule: #d7dbd1;
  --panel: #f3f1ec;
  --link: #285c7a;
  --sans: "Avenir Next", Avenir, "Helvetica Neue", Arial, sans-serif;
  --serif: Charter, "Bitstream Charter", "Iowan Old Style", Georgia, serif;
  --mono: Menlo, Monaco, Consolas, "Courier New", monospace;
}

@page {
  size: Letter;
  margin: 0.70in 0.72in 0.62in;
}

* { box-sizing: border-box; }

html,
body {
  margin: 0;
  color: var(--text);
  background: #fff;
}

body {
  font-family: var(--serif);
  font-size: 10.8pt;
  line-height: 1.43;
}

a {
  color: var(--link);
  text-decoration: none;
}

.title-page,
.contents-page {
  break-after: page;
}

.top-rule {
  height: 5px;
  width: 100%;
  background: var(--maroon);
}

.bottom-rule {
  height: 1px;
  width: 100%;
  background: var(--gold);
}

.title-page {
  min-height: 9.6in;
  display: flex;
  flex-direction: column;
}

.title-block {
  margin-top: 1.85in;
  max-width: 6.9in;
}

.title-block h1 {
  margin: 0 0 0.30in;
  font-family: var(--sans);
  font-size: 36pt;
  font-weight: 800;
  line-height: 1.08;
  letter-spacing: 0;
}

.subtitle {
  max-width: 7.0in;
  margin: 0 0 0.50in;
  color: var(--maroon);
  font-family: var(--sans);
  font-size: 16.4pt;
  font-weight: 650;
  line-height: 1.3;
}

.byline {
  margin: 0 0 0.14in;
  color: var(--muted);
  font-family: var(--sans);
  font-size: 12pt;
}

.version {
  margin: 0 0 0.34in;
  color: var(--muted);
  font-family: var(--sans);
  font-size: 12pt;
}

.metadata-card {
  margin-top: 0.08in;
  padding: 0.15in 0.23in;
  border-left: 4px solid var(--gold);
  background: var(--panel);
  font-family: var(--sans);
  font-size: 10.6pt;
  line-height: 1.45;
}

.metadata-row {
  margin: 0.02in 0;
}

.metadata-label {
  font-weight: 700;
}

.title-spacer {
  flex: 1;
}

.contents-page {
  min-height: 9.6in;
}

.contents-page h2 {
  margin: 0.25in 0 0.25in;
  font-family: var(--sans);
  font-size: 22pt;
  line-height: 1.15;
}

.contents-list {
  list-style: none;
  margin: 0;
  padding: 0;
  font-family: var(--sans);
  font-size: 11.2pt;
  line-height: 1.55;
}

.contents-list li {
  margin: 0;
  padding: 0;
}

.contents-list a {
  color: var(--text);
}

.report-body {
  overflow-wrap: anywhere;
}

.report-body h1 {
  display: none;
}

.report-body h2 {
  margin: 0.42in 0 0.18in;
  padding-top: 0.22in;
  border-top: 5px solid var(--maroon);
  font-family: var(--sans);
  font-size: 22pt;
  line-height: 1.15;
  break-after: avoid;
}

.report-body h2:first-child {
  margin-top: 0;
}

.report-body h3 {
  margin: 0.26in 0 0.10in;
  font-family: var(--sans);
  font-size: 14.2pt;
  line-height: 1.22;
  break-after: avoid;
}

.report-body h4 {
  margin: 0.20in 0 0.08in;
  color: var(--maroon);
  font-family: var(--sans);
  font-size: 11.4pt;
  line-height: 1.25;
  break-after: avoid;
}

.report-body p {
  margin: 0 0 0.12in;
}

.report-body ul,
.report-body ol {
  margin: 0 0 0.14in 0.22in;
  padding-left: 0.18in;
}

.report-body li {
  margin: 0.03in 0;
}

.report-body hr {
  height: 1px;
  margin: 0.24in 0;
  border: 0;
  background: var(--rule);
}

.report-body blockquote {
  margin: 0.14in 0 0.16in;
  padding: 0.12in 0.18in;
  border-left: 4px solid var(--gold);
  background: var(--panel);
  color: var(--text);
  font-family: var(--sans);
  font-size: 9.8pt;
}

.report-body blockquote p:last-child {
  margin-bottom: 0;
}

strong {
  font-weight: 700;
}

em {
  font-style: italic;
}

code {
  padding: 0.05em 0.28em;
  border: 1px solid #cbd3d8;
  border-radius: 4px;
  background: #eef2f3;
  font-family: var(--mono);
  font-size: 0.86em;
}

pre {
  margin: 0.14in 0;
  padding: 0.12in 0.15in;
  border: 1px solid #d8dedf;
  border-radius: 5px;
  background: #f5f7f7;
  white-space: pre-wrap;
  break-inside: avoid;
}

pre code {
  padding: 0;
  border: 0;
  background: transparent;
  font-size: 8.2pt;
}

table {
  width: 100%;
  margin: 0.15in 0 0.18in;
  border-collapse: collapse;
  table-layout: fixed;
  font-family: var(--sans);
  font-size: 7.2pt;
  line-height: 1.25;
}

th,
td {
  padding: 0.055in 0.06in;
  border: 1px solid #d2d8d2;
  vertical-align: top;
  overflow-wrap: anywhere;
}

th {
  background: #edf1ed;
  font-weight: 700;
}

tr {
  break-inside: avoid;
}

.bibliography {
  font-size: 9.2pt;
}

.bibliography li {
  margin-bottom: 0.10in;
}

.ref-marker {
  font-size: 0.72em;
  vertical-align: super;
}

.appendix-end,
.report-end {
  font-family: var(--sans);
  color: var(--muted);
}
"""


def inline_markdown(value: str) -> str:
    rendered = markdown.markdown(value, extensions=["sane_lists"]).strip()
    if rendered.startswith("<p>") and rendered.endswith("</p>"):
        rendered = rendered[3:-4]
    return rendered


def extract_front_matter(raw: str) -> tuple[str, str, dict[str, str]]:
    lines = raw.splitlines()
    title = ""
    subtitle = ""
    metadata: dict[str, str] = {}

    for line in lines:
        if line.startswith("# "):
            title = line[2:].strip()
            break

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("**") and stripped.endswith("**") and ":" not in stripped[:12]:
            subtitle = stripped.strip("*").strip()
            break

    in_metadata = False
    for line in lines:
        stripped = line.strip()
        if stripped == "---":
            if not in_metadata:
                in_metadata = True
                continue
            break
        if not in_metadata or not stripped:
            continue
        match = re.match(r"^\*\*([^*]+):\*\*\s*(.*?)\s*$", stripped)
        if not match:
            continue
        label, value = match.groups()
        metadata[label.strip()] = value.strip()

    return title, subtitle, metadata


def remove_markdown_cover_nodes(soup: BeautifulSoup) -> None:
    seen_hr = 0
    for node in list(soup.contents):
        if isinstance(node, Tag) and node.name == "hr":
            seen_hr += 1
            node.extract()
            if seen_hr >= 2:
                break
            continue
        node.extract()


def add_heading_ids(soup: BeautifulSoup) -> None:
    used: set[str] = set()
    for heading in soup.find_all(re.compile("^h[2-4]$")):
        title = heading.get_text(" ", strip=True)
        if not heading.get("id"):
            heading["id"] = slugify(title, used)
        else:
            used.add(str(heading["id"]))


def mark_end_paragraphs(soup: BeautifulSoup) -> None:
    for paragraph in soup.find_all("p"):
        text = paragraph.get_text(" ", strip=True)
        if text.startswith("End of Appendix"):
            paragraph["class"] = paragraph.get("class", []) + ["appendix-end"]
        elif text.startswith("End of report"):
            paragraph["class"] = paragraph.get("class", []) + ["report-end"]


def build_contents(soup: BeautifulSoup) -> str:
    lines = ['<ol class="contents-list">']
    for heading in soup.find_all("h2"):
        title = heading.get_text(" ", strip=True)
        target = html.escape(str(heading.get("id", "")), quote=True)
        lines.append(f'  <li><a href="#{target}">{html.escape(title)}</a></li>')
    lines.append("</ol>")
    return "\n".join(lines)


def metadata_card(metadata: dict[str, str]) -> str:
    rows = []
    for label in ("Commissioned by", "License", "Repository", "Citation"):
        value = metadata.get(label)
        if not value:
            continue
        rows.append(
            '<p class="metadata-row">'
            f'<span class="metadata-label">{html.escape(label)}:</span> '
            f"{inline_markdown(value)}</p>"
        )
    return "\n".join(rows)


def page_shell(title: str, subtitle: str, metadata: dict[str, str], contents: str, body: str) -> str:
    author = inline_markdown(metadata.get("Author", ""))
    version_value = inline_markdown(metadata.get("Version", ""))
    version = f"Version {version_value}" if version_value else ""
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{html.escape(title)}</title>
  <style>{PDF_CSS}</style>
</head>
<body>
  <section class="title-page" aria-label="Title page">
    <div class="top-rule"></div>
    <div class="title-block">
      <h1>{html.escape(title)}</h1>
      <p class="subtitle">{inline_markdown(subtitle)}</p>
      <p class="byline">{author}</p>
      <p class="version">{version}</p>
      <div class="metadata-card">
        {metadata_card(metadata)}
      </div>
    </div>
    <div class="title-spacer"></div>
    <div class="bottom-rule"></div>
  </section>
  <section class="contents-page" aria-label="Contents">
    <div class="top-rule"></div>
    <h2>Contents</h2>
    {contents}
  </section>
  <article class="report-body">
    {body}
  </article>
</body>
</html>
"""


def render(source: Path, target: Path) -> None:
    raw = source.read_text()
    guard_text(str(source.relative_to(REPO_ROOT)), raw)
    title, subtitle, metadata = extract_front_matter(raw)
    prepared = normalize_references(raw)
    body_html = markdown.markdown(prepared, extensions=["tables", "fenced_code", "sane_lists"])
    soup = BeautifulSoup(body_html, "html.parser")
    remove_markdown_cover_nodes(soup)
    add_heading_ids(soup)
    mark_end_paragraphs(soup)
    contents = build_contents(soup)
    output = page_shell(title, subtitle, metadata, contents, str(soup))
    guard_text(str(target.relative_to(REPO_ROOT)), output)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(output)
    print(f"Rendered PDF HTML {source.relative_to(REPO_ROOT)} -> {target.relative_to(REPO_ROOT)}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("target", type=Path)
    args = parser.parse_args()
    render((REPO_ROOT / args.source).resolve(), (REPO_ROOT / args.target).resolve())


if __name__ == "__main__":
    main()
