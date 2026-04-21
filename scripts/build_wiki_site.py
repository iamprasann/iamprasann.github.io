from __future__ import annotations

import html
import json
import re
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable
from urllib.parse import quote


ROOT = Path(__file__).resolve().parent.parent
WIKI_ROOT = ROOT / "wiki"
RAW_ROOT = ROOT / "raw"
ASSETS_DIR = ROOT / "assets"

NAV_ORDER = [
    "Indexes",
    "Semester Archives",
    "Standalone Projects",
    "Coursework & Practice",
    "Forked Contributions",
]

PROJECT_GROUPS = {
    "Semester Archives": {
        "sem-4-iitb-ee",
        "sem-5-iitb-ee",
        "sem-6-iitb-ee",
        "sem-7-iitb-ee",
        "sem-8-iitb-ee",
    },
    "Standalone Projects": {
        "soc-2020",
        "umic-team4-final",
        "instishop",
    },
    "Coursework & Practice": {
        "ma-tuts",
        "mooc-content",
        "reports-soc2020",
    },
    "Forked Contributions": {
        "16-bit-alu",
        "autumn-of-automation",
    },
}


@dataclass
class TocItem:
    level: int
    text: str
    anchor: str


@dataclass
class Page:
    source_rel: Path
    output_rel: Path
    url: str
    kind: str
    section: str
    title: str
    summary: str
    source_text: str
    body_html: str = ""
    toc: list[TocItem] = field(default_factory=list)

    @property
    def source_url(self) -> str:
        return "/" + quote(self.source_rel.as_posix(), safe="/")


def main() -> None:
    pages = discover_pages()
    page_map = {page.source_rel: page for page in pages}

    for page in pages:
        page.body_html, page.toc = render_markdown(page.source_text, page, page_map)

    home_page = build_home_page(pages)
    all_pages = [home_page, *pages]
    nav_sections = build_nav_sections(pages)
    search_index = build_search_index(all_pages)

    write_assets(search_index)
    write_page(home_page, nav_sections)
    for page in pages:
        write_page(page, nav_sections)
    write_not_found(nav_sections)
    (ROOT / ".nojekyll").write_text("", encoding="utf-8")


def discover_pages() -> list[Page]:
    pages: list[Page] = []

    for source in sorted(WIKI_ROOT.rglob("*.md")):
        source_rel = source.relative_to(ROOT)
        content = source.read_text(encoding="utf-8")
        title = extract_title(content, source.stem)
        summary = extract_summary(content)
        section = "Indexes" if source_rel.parts[1] == "indexes" else classify_project(source.stem)
        kind = "index" if source_rel.parts[1] == "indexes" else "project"
        output_rel = source_rel.relative_to("wiki").with_suffix(".html")
        pages.append(
            Page(
                source_rel=source_rel,
                output_rel=output_rel,
                url="/" + quote(output_rel.as_posix(), safe="/"),
                kind=kind,
                section=section,
                title=title,
                summary=summary,
                source_text=content,
            )
        )

    for source in sorted(RAW_ROOT.rglob("*.md")):
        source_rel = source.relative_to(ROOT)
        content = source.read_text(encoding="utf-8")
        pages.append(
            Page(
                source_rel=source_rel,
                output_rel=source_rel.with_suffix(".html"),
                url="/" + quote(source_rel.with_suffix(".html").as_posix(), safe="/"),
                kind="capture",
                section="Source Captures",
                title=extract_title(content, source.stem),
                summary=extract_summary(content),
                source_text=content,
            )
        )

    return pages


def classify_project(slug: str) -> str:
    for section, slugs in PROJECT_GROUPS.items():
        if slug in slugs:
            return section
    return "Projects"


def extract_title(markdown_text: str, fallback: str) -> str:
    for line in markdown_text.splitlines():
        match = re.match(r"^#\s+(.+?)\s*$", line.strip())
        if match:
            return strip_markdown(match.group(1))
    return fallback.replace("-", " ").title()


def extract_summary(markdown_text: str) -> str:
    lines = markdown_text.splitlines()
    seen_title = False
    current: list[str] = []

    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            if current:
                break
            continue
        if line.startswith("# "):
            seen_title = True
            continue
        if not seen_title:
            continue
        if line.startswith("## ") or line.startswith("|") or line.startswith("- ") or re.match(r"^\d+\.\s", line):
            if current:
                break
            continue
        current.append(line)

    if current:
        return strip_markdown(" ".join(current))

    return ""


def strip_markdown(text: str) -> str:
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"\*([^*]+)\*", r"\1", text)
    return " ".join(text.split())


def render_markdown(markdown_text: str, page: Page, page_map: dict[Path, Page]) -> tuple[str, list[TocItem]]:
    lines = markdown_text.splitlines()
    blocks: list[str] = []
    toc: list[TocItem] = []
    first_h1_skipped = False
    first_paragraph_processed = False
    anchor_counts: dict[str, int] = {}
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        heading_match = re.match(r"^(#{1,6})\s+(.+?)\s*$", stripped)
        if heading_match:
            level = len(heading_match.group(1))
            heading_text = heading_match.group(2)
            if level == 1 and not first_h1_skipped:
                first_h1_skipped = True
                i += 1
                continue
            anchor = unique_anchor(slugify(strip_markdown(heading_text)), anchor_counts)
            toc.append(TocItem(level=level, text=strip_markdown(heading_text), anchor=anchor))
            blocks.append(
                f'<h{level} id="{anchor}">{render_inline(heading_text, page, page_map)}</h{level}>'
            )
            i += 1
            continue

        if stripped.startswith("```"):
            language = stripped[3:].strip()
            i += 1
            code_lines: list[str] = []
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            if i < len(lines):
                i += 1
            code_html = html.escape("\n".join(code_lines))
            lang_attr = f' data-language="{html.escape(language)}"' if language else ""
            blocks.append(f"<pre><code{lang_attr}>{code_html}</code></pre>")
            continue

        if is_table_start(lines, i):
            table_html, i = render_table(lines, i, page, page_map)
            blocks.append(table_html)
            continue

        unordered = re.match(r"^[-*]\s+(.+)$", stripped)
        if unordered:
            items: list[str] = []
            while i < len(lines):
                candidate = lines[i].strip()
                match = re.match(r"^[-*]\s+(.+)$", candidate)
                if not match:
                    break
                items.append(f"<li>{render_inline(match.group(1), page, page_map)}</li>")
                i += 1
            blocks.append("<ul>" + "".join(items) + "</ul>")
            continue

        ordered = re.match(r"^\d+\.\s+(.+)$", stripped)
        if ordered:
            items = []
            while i < len(lines):
                candidate = lines[i].strip()
                match = re.match(r"^\d+\.\s+(.+)$", candidate)
                if not match:
                    break
                items.append(f"<li>{render_inline(match.group(1), page, page_map)}</li>")
                i += 1
            blocks.append("<ol>" + "".join(items) + "</ol>")
            continue

        paragraph_lines = [stripped]
        i += 1
        while i < len(lines):
            candidate = lines[i].strip()
            if not candidate or re.match(r"^(#{1,6})\s+", candidate) or candidate.startswith("```"):
                break
            if is_table_start(lines, i):
                break
            if re.match(r"^[-*]\s+.+$", candidate) or re.match(r"^\d+\.\s+.+$", candidate):
                break
            paragraph_lines.append(candidate)
            i += 1
        paragraph_text = " ".join(paragraph_lines)
        plain_paragraph = strip_markdown(paragraph_text)
        if not first_paragraph_processed and page.summary and plain_paragraph == page.summary:
            first_paragraph_processed = True
            continue
        first_paragraph_processed = True
        blocks.append(f"<p>{render_inline(paragraph_text, page, page_map)}</p>")

    filtered_toc = [item for item in toc if item.level >= 2]
    return "\n".join(blocks), filtered_toc


def is_table_start(lines: list[str], index: int) -> bool:
    if index + 1 >= len(lines):
        return False
    head = lines[index].strip()
    divider = lines[index + 1].strip()
    if "|" not in head:
        return False
    return bool(re.match(r"^\|?(?:\s*:?-{3,}:?\s*\|)+\s*:?-{3,}:?\s*\|?$", divider))


def render_table(
    lines: list[str],
    index: int,
    page: Page,
    page_map: dict[Path, Page],
) -> tuple[str, int]:
    header_cells = split_table_row(lines[index])
    index += 2
    body_rows: list[list[str]] = []
    while index < len(lines):
        line = lines[index].strip()
        if not line or "|" not in line:
            break
        body_rows.append(split_table_row(line))
        index += 1

    thead = "".join(f"<th>{render_inline(cell, page, page_map)}</th>" for cell in header_cells)
    rows = []
    for row in body_rows:
        cells = "".join(f"<td>{render_inline(cell, page, page_map)}</td>" for cell in row)
        rows.append(f"<tr>{cells}</tr>")
    table_html = f"<div class=\"table-wrap\"><table><thead><tr>{thead}</tr></thead><tbody>{''.join(rows)}</tbody></table></div>"
    return table_html, index


def split_table_row(line: str) -> list[str]:
    text = line.strip().strip("|")
    return [cell.strip() for cell in text.split("|")]


def render_inline(text: str, page: Page, page_map: dict[Path, Page]) -> str:
    placeholders: dict[str, str] = {}
    token_counter = 0

    def store_token(content: str) -> str:
        nonlocal token_counter
        token = f"@@TOKEN{token_counter}@@"
        placeholders[token] = content
        token_counter += 1
        return token

    def replace_code(match: re.Match[str]) -> str:
        return store_token(f"<code>{html.escape(match.group(1))}</code>")

    text = re.sub(r"`([^`]+)`", replace_code, text)

    def replace_link(match: re.Match[str]) -> str:
        label = render_inline_basic(match.group(1))
        href = resolve_url(match.group(2).strip(), page, page_map)
        external = " target=\"_blank\" rel=\"noreferrer\"" if href.startswith("http") else ""
        return store_token(f'<a href="{href}"{external}>{label}</a>')

    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", replace_link, text)
    text = html.escape(text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", text)

    for token, rendered in placeholders.items():
        text = text.replace(token, rendered)
    return text


def render_inline_basic(text: str) -> str:
    text = re.sub(r"`([^`]+)`", lambda match: f"<code>{html.escape(match.group(1))}</code>", text)
    text = html.escape(text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", text)
    return text


def resolve_url(target: str, page: Page, page_map: dict[Path, Page]) -> str:
    if target.startswith(("http://", "https://", "mailto:", "#", "tel:")):
        return html.escape(target, quote=True)

    absolute_target = (ROOT / page.source_rel).parent / target
    resolved = absolute_target.resolve()
    try:
        repo_relative = resolved.relative_to(ROOT.resolve())
    except ValueError:
        return html.escape(target, quote=True)

    if repo_relative in page_map:
        return page_map[repo_relative].url

    if repo_relative.suffix == ".md":
        html_target = repo_relative.with_suffix(".html")
        if html_target in page_map:
            return page_map[html_target].url

    if repo_relative.exists():
        return "/" + quote(repo_relative.as_posix(), safe="/")

    return html.escape(target, quote=True)


def slugify(text: str) -> str:
    text = re.sub(r"[^a-zA-Z0-9\s-]", "", text.lower()).strip()
    return re.sub(r"[\s-]+", "-", text) or "section"


def unique_anchor(base: str, seen: dict[str, int]) -> str:
    count = seen.get(base, 0)
    seen[base] = count + 1
    return base if count == 0 else f"{base}-{count + 1}"


def build_nav_sections(pages: list[Page]) -> list[tuple[str, list[Page]]]:
    grouped: dict[str, list[Page]] = {name: [] for name in NAV_ORDER}
    for page in pages:
        if page.kind == "capture":
            continue
        grouped.setdefault(page.section, []).append(page)

    for section, section_pages in grouped.items():
        section_pages.sort(key=lambda item: item.title.lower())
        if section == "Indexes":
            section_pages.sort(key=lambda item: (0 if item.title == "Repositories" else 1, item.title.lower()))

    return [(section, grouped.get(section, [])) for section in NAV_ORDER if grouped.get(section)]


def build_home_page(pages: list[Page]) -> Page:
    project_pages = [page for page in pages if page.kind == "project"]
    capture_pages = [page for page in pages if page.kind == "capture"]
    index_pages = [page for page in pages if page.kind == "index"]

    section_descriptions = {
        "Semester Archives": "Semester-level repositories that organize coursework, reports, notebooks, and project artifacts by academic period.",
        "Standalone Projects": "Bounded engineering or research projects with clearer individual narratives and stronger artifact cohesion.",
        "Coursework & Practice": "Support repositories for tutorials, self-study, MOOC work, and report archives.",
        "Forked Contributions": "Forked repositories that still matter because they preserve real contributed work or formal submission artifacts.",
    }

    grouped: dict[str, list[Page]] = {}
    for page in project_pages:
        grouped.setdefault(page.section, []).append(page)
    for pages_in_section in grouped.values():
        pages_in_section.sort(key=lambda item: item.title.lower())

    cards = []
    for section in [item for item in NAV_ORDER if item != "Indexes"]:
        items = grouped.get(section, [])
        if not items:
            continue
        links = "".join(
            f'<li><a href="{page.url}">{html.escape(page.title)}</a><span>{html.escape(page.summary)}</span></li>'
            for page in items
        )
        cards.append(
            f"""
            <section class="section-card">
              <div class="section-card-header">
                <h2>{html.escape(section)}</h2>
                <span>{len(items)} pages</span>
              </div>
              <p>{html.escape(section_descriptions.get(section, ""))}</p>
              <ul class="section-link-list">{links}</ul>
            </section>
            """
        )

    home_body = f"""
    <section class="hero-card">
      <p class="eyebrow">Prasann Iyer Knowledge Base</p>
      <p class="hero-copy">
        A browsable grayscale wiki built from repository archives, course material, project notes, and source captures from undergraduate work.
        The site is designed as a small personal encyclopedia: concise article pages, explicit source links, and cross-linked indexes instead of portfolio-style summaries.
      </p>
      <div class="hero-grid">
        <div class="hero-stat">
          <strong>{len(project_pages)}</strong>
          <span>Source articles</span>
        </div>
        <div class="hero-stat">
          <strong>{len(index_pages)}</strong>
          <span>Index pages</span>
        </div>
        <div class="hero-stat">
          <strong>{len(capture_pages)}</strong>
          <span>Source captures</span>
        </div>
      </div>
    </section>

    <section class="quick-links">
      <a class="quick-link-card" href="/indexes/repositories.html">
        <strong>Repository Atlas</strong>
        <span>Browse the full corpus and how it is grouped.</span>
      </a>
      <a class="quick-link-card" href="/indexes/ingestion-queue.html">
        <strong>Ingestion Queue</strong>
        <span>See which repositories have been seeded and which are deferred.</span>
      </a>
    </section>

    <section class="section-grid">
      {''.join(cards)}
    </section>
    """

    return Page(
        source_rel=Path("index.html"),
        output_rel=Path("index.html"),
        url="/",
        kind="home",
        section="Home",
        title="Prasann Iyer Knowledge Base",
        summary="A grayscale wiki of undergraduate work, projects, coursework archives, and source notes.",
        source_text="",
        body_html=home_body,
        toc=[],
    )


def build_search_index(pages: Iterable[Page]) -> list[dict[str, str]]:
    entries = []
    for page in pages:
        if page.kind == "capture":
            continue
        haystack = " ".join(
            filter(
                None,
                [
                    page.title,
                    page.summary,
                    strip_markdown(page.source_text) if page.source_text else "",
                    page.section,
                ],
            )
        )
        entries.append(
            {
                "title": page.title,
                "summary": page.summary,
                "section": page.section,
                "kind": page.kind,
                "url": page.url,
                "text": haystack.lower(),
            }
        )
    return entries


def write_assets(search_index: list[dict[str, str]]) -> None:
    ASSETS_DIR.mkdir(exist_ok=True)
    (ASSETS_DIR / "wiki-search.json").write_text(
        json.dumps(search_index, indent=2),
        encoding="utf-8",
    )


def write_page(page: Page, nav_sections: list[tuple[str, list[Page]]]) -> None:
    output_path = ROOT / page.output_rel
    output_path.parent.mkdir(parents=True, exist_ok=True)
    rendered = render_shell(page, nav_sections)
    output_path.write_text(rendered, encoding="utf-8")


def write_not_found(nav_sections: list[tuple[str, list[Page]]]) -> None:
    page = Page(
        source_rel=Path("404.html"),
        output_rel=Path("404.html"),
        url="/404.html",
        kind="index",
        section="Indexes",
        title="Page Not Found",
        summary="The requested page does not exist in the generated wiki.",
        source_text="",
        body_html="""
        <section class="hero-card">
          <p class="eyebrow">404</p>
          <p class="hero-copy">
            The page you requested does not exist in this knowledge base. Use the repository atlas or the search bar to navigate back into the corpus.
          </p>
        </section>
        <section class="quick-links">
          <a class="quick-link-card" href="/">
            <strong>Go Home</strong>
            <span>Return to the main wiki entry point.</span>
          </a>
          <a class="quick-link-card" href="/indexes/repositories.html">
            <strong>Browse Repositories</strong>
            <span>Open the main repository atlas.</span>
          </a>
        </section>
        """,
    )
    write_page(page, nav_sections)


def render_shell(page: Page, nav_sections: list[tuple[str, list[Page]]]) -> str:
    toc_html = build_toc_html(page.toc)
    nav_html = build_nav_html(page, nav_sections)
    breadcrumbs = build_breadcrumbs(page)
    title_text = build_page_title(page)
    kind_label = {
        "home": "Home",
        "index": "Index",
        "project": page.section.rstrip("s") if page.section != "Coursework & Practice" else "Coursework",
        "capture": "Source Capture",
    }.get(page.kind, page.kind.title())
    summary = f"<p class=\"article-summary\">{html.escape(page.summary)}</p>" if page.summary else ""
    source_link = ""
    if page.kind in {"index", "project", "capture"} and page.source_rel.suffix == ".md":
        source_link = f'<a class="source-link" href="{page.source_url}">View Markdown Source</a>'

    body = page.body_html
    if page.kind in {"index", "project", "capture"}:
        body = f"""
        <header class="article-header">
          <div class="article-kicker-row">
            <span class="article-badge">{html.escape(kind_label)}</span>
            {source_link}
          </div>
          <h1>{html.escape(page.title)}</h1>
          {summary}
        </header>
        {body}
        """
    elif page.kind == "home":
        body = f"""
        <header class="article-header home-header">
          <div class="article-kicker-row">
            <span class="article-badge">Home</span>
          </div>
          <h1>{html.escape(page.title)}</h1>
          {summary}
        </header>
        {body}
        """

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title_text)}</title>
  <meta name="description" content="{html.escape(page.summary or page.title)}">
  <link rel="stylesheet" href="/assets/wiki.css">
  <script>
    window.WIKI_CURRENT_URL = {json.dumps(page.url)};
  </script>
  <script defer src="/assets/wiki.js"></script>
</head>
<body data-page-kind="{html.escape(page.kind)}">
  <button class="mobile-nav-toggle" type="button" data-nav-toggle aria-expanded="false" aria-controls="wiki-sidebar">Browse</button>
  <aside class="sidebar" id="wiki-sidebar">
    <a class="brand" href="/">
      <span class="brand-mark">PI</span>
      <span class="brand-copy">
        <strong>Prasann Iyer</strong>
        <span>Knowledge Base</span>
      </span>
    </a>
    {nav_html}
  </aside>
  <div class="page-column">
    <header class="topbar">
      <nav class="breadcrumbs">{breadcrumbs}</nav>
      <div class="search-shell">
        <input class="search-input" type="search" placeholder="Search articles" data-search-input aria-label="Search articles">
        <div class="search-results" data-search-results hidden></div>
      </div>
    </header>
    <main class="article">
      {body}
    </main>
  </div>
  <aside class="toc-shell">
    {toc_html}
  </aside>
</body>
</html>
"""


def build_page_title(page: Page) -> str:
    if page.kind == "home":
        return page.title
    return f"{page.title} | Prasann Iyer Knowledge Base"


def build_nav_html(page: Page, nav_sections: list[tuple[str, list[Page]]]) -> str:
    sections = [
        '<section class="nav-group"><h2>Home</h2><a class="nav-link{}" href="/">Front Page</a></section>'.format(
            " active" if page.url == "/" else ""
        )
    ]
    for section, pages in nav_sections:
        items = []
        for item in pages:
            active = " active" if item.url == page.url else ""
            items.append(f'<a class="nav-link{active}" href="{item.url}">{html.escape(item.title)}</a>')
        sections.append(f'<section class="nav-group"><h2>{html.escape(section)}</h2>{"".join(items)}</section>')
    return "".join(sections)


def build_breadcrumbs(page: Page) -> str:
    crumbs = [('<a href="/">Home</a>')]
    if page.kind == "home":
        return crumbs[0]
    if page.section and page.section != "Home":
        crumbs.append(f"<span>{html.escape(page.section)}</span>")
    crumbs.append(f"<span>{html.escape(page.title)}</span>")
    return "".join(
        f'{crumb}<span class="crumb-sep">/</span>' if index < len(crumbs) - 1 else crumb
        for index, crumb in enumerate(crumbs)
    )


def build_toc_html(toc: list[TocItem]) -> str:
    if not toc:
        return '<div class="toc-card empty"><h2>On This Page</h2><p>No subsection headings on this page.</p></div>'

    items = []
    for item in toc:
        if item.level > 3:
            continue
        cls = "toc-item toc-item-sub" if item.level == 3 else "toc-item"
        items.append(f'<a class="{cls}" href="#{html.escape(item.anchor)}">{html.escape(item.text)}</a>')
    return f'<div class="toc-card"><h2>On This Page</h2>{"".join(items)}</div>'


if __name__ == "__main__":
    main()
