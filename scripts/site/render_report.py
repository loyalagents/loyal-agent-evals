#!/usr/bin/env python3
"""Render docs/report.md into the static website report page."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import markdown
from bs4 import BeautifulSoup


REPO_ROOT = Path(__file__).resolve().parents[2]
HARD_LEAK_RE = re.compile(r"/Users/|Dropbox|file://|/tmp/\w")


def slugify(text: str, used: set[str]) -> str:
    text = text.lower().replace("§", "section ")
    slug = re.sub(r"[^a-z0-9]+", "-", text).strip("-") or "section"
    base = slug
    i = 2
    while slug in used:
        slug = f"{base}-{i}"
        i += 1
    used.add(slug)
    return slug


def guard_text(label: str, text: str) -> None:
    hits = []
    for line_no, line in enumerate(text.splitlines(), 1):
        if HARD_LEAK_RE.search(line):
            hits.append(f"{label}:{line_no}: {line[:180]}")
    if hits:
        raise SystemExit("Hard-leak hits during report rendering:\n  " + "\n  ".join(hits))


def strip_paragraph(html: str) -> str:
    html = html.strip()
    if html.startswith("<p>") and html.endswith("</p>"):
        return html[3:-4]
    return html


def normalize_references(markdown_text: str) -> str:
    references: dict[str, str] = {}
    lines: list[str] = []
    inserted = False
    for line in markdown_text.splitlines():
        match = re.match(r"^\[\^(\d+)\]:\s*(.*)$", line)
        if match:
            references[match.group(1)] = match.group(2)
            continue
        lines.append(line)
        if line.strip() == "## 15. References" and not inserted:
            lines.append("")
            lines.append("@@REFERENCES@@")
            inserted = True

    def marker(match: re.Match[str]) -> str:
        ref = match.group(1)
        return f'<sup class="ref-marker"><a href="#ref-{ref}">[{ref}]</a></sup>'

    text = "\n".join(lines)
    text = re.sub(r"\[\^(\d+)\]", marker, text)

    ref_lines = ['<ol class="bibliography">']
    for ref_id in sorted(references, key=lambda value: int(value)):
        entry = markdown.markdown(references[ref_id], extensions=["tables", "fenced_code"])
        ref_lines.append(f'  <li id="ref-{ref_id}">{strip_paragraph(entry)}</li>')
    ref_lines.append("</ol>")
    return text.replace("@@REFERENCES@@", "\n".join(ref_lines))


def build_toc(soup: BeautifulSoup) -> str:
    used: set[str] = set()
    entries = []
    for heading in soup.find_all(re.compile("^h[2-4]$")):
        title = heading.get_text(" ", strip=True)
        if not heading.get("id"):
            heading["id"] = slugify(title, used)
        else:
            used.add(str(heading["id"]))
        level = int(heading.name[1])
        entries.append((level, heading["id"], title))

    lines = ['<nav class="report-toc" aria-label="Report table of contents">', "<h2>Contents</h2>", "<ol>"]
    for level, target, title in entries:
        class_name = f'report-toc__level-{level}'
        lines.append(f'<li class="{class_name}"><a href="#{target}">{title}</a></li>')
    lines.extend(["</ol>", "</nav>"])
    return "\n".join(lines)


def page_shell(title: str, body: str, toc: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} — Loyal Agent Evals</title>
  <meta name="description" content="Rendered HTML version of the Loyal Agent Evals report, with section anchors and visible references.">
  <link rel="stylesheet" href="../assets/css/style.css">
</head>
<body>
  <a class="skip-link" href="#main">Skip to main content</a>
  <header class="site-header">
    <div class="site-header__inner">
      <a class="site-header__brand" href="../">Loyal Agent Evals</a>
      <button class="site-nav__toggle" type="button" aria-controls="site-nav-list" aria-expanded="false">Menu</button>
      <nav class="site-nav" aria-label="Primary">
        <ul class="site-nav__list" id="site-nav-list" data-open="false">
          <li><a href="../report/">Report</a></li>
          <li><a href="../results/">Results</a></li>
          <li><a href="../walkthroughs/">Walkthroughs</a></li>
          <li><a href="../methodology/">Methodology</a></li>
          <li><a href="../framework/">Framework</a></li>
          <li><a href="../tos/">ToS</a></li>
          <li><a href="../artifacts/">Artifacts</a></li>
          <li><a href="../contract/">Contract</a></li>
        </ul>
      </nav>
    </div>
  </header>
  <main id="main" class="report-layout">
    <header class="page-hero page-hero--compact">
      <p class="eyebrow">Rendered report</p>
      <h1>{title}</h1>
      <p>The canonical Markdown remains available at <a href="../docs/report.md">docs/report.md</a>. This page renders the same report with stable section anchors and a visible §15 bibliography.</p>
    </header>
    <div class="report-shell">
      {toc}
      <article class="report-body">
        {body}
      </article>
    </div>
  </main>
  <footer class="site-footer">
    <div class="site-footer__inner">
      <p>Documentation licensed under <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>. Code licensed under <a href="https://www.apache.org/licenses/LICENSE-2.0">Apache 2.0</a>. Source at <a href="https://github.com/loyalagents/loyal-agent-evals">github.com/loyalagents/loyal-agent-evals</a>.</p>
    </div>
  </footer>
  <script src="../assets/js/nav.js" defer></script>
</body>
</html>
"""


def render(source: Path, target: Path) -> None:
    raw = source.read_text()
    guard_text(str(source.relative_to(REPO_ROOT)), raw)
    prepared = normalize_references(raw)
    html = markdown.markdown(prepared, extensions=["tables", "fenced_code", "sane_lists"])
    soup = BeautifulSoup(html, "html.parser")
    title_tag = soup.find("h1")
    title = title_tag.get_text(" ", strip=True) if title_tag else "Loyal Agent Evals Report"
    toc = build_toc(soup)
    output = page_shell(title, str(soup), toc)
    guard_text(str(target.relative_to(REPO_ROOT)), output)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(output)
    print(f"Rendered {source.relative_to(REPO_ROOT)} -> {target.relative_to(REPO_ROOT)}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("target", type=Path)
    args = parser.parse_args()
    render((REPO_ROOT / args.source).resolve(), (REPO_ROOT / args.target).resolve())


if __name__ == "__main__":
    main()
