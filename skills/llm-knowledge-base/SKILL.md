---
name: llm-knowledge-base
description: Build and maintain a repo-native markdown knowledge base from GitHub repositories, articles, papers, and notes; use when ingesting new sources, compiling wiki pages, refreshing indexes and backlinks, answering questions by writing markdown outputs, or linting the wiki for gaps and inconsistencies.
metadata:
  short-description: Compile sources into a browsable markdown wiki
---

# LLM Knowledge Base

Turn a folder of source material into a small-scale wiki that the LLM maintains. This skill is for repo-native markdown knowledge bases, not Obsidian. Optimize for GitHub and GitHub Pages browsing.

## Core model

- Keep raw inputs immutable.
- Let the LLM maintain the derived wiki.
- Favor small index files and cross-links over RAG at this scale.
- Prefer writing durable files in the repo over answering only in chat.

Read `references/working-principles.md` when setting up the workflow or adapting it to a new corpus.
Read `references/page-standards.md` when writing or updating wiki pages.

## Default layout

If the repo does not already define a different structure, use:

- `raw/` for immutable captures and imported source material.
- `wiki/` for derived knowledge pages.
- `wiki/indexes/` for small entry-point pages and inventories.
- `outputs/` for one-off analyses, reports, slides, and Q&A results that may later be filed back into `wiki/`.
- `assets/images/` for screenshots and local figures referenced by markdown pages.

## When to use this skill

- Ingest new repositories, articles, papers, or notes into the knowledge base.
- Compile or refresh project, concept, course, person, or timeline pages.
- Build a browsable index of the user's public GitHub repositories.
- Answer a research question by writing a markdown file inside the repo.
- Run a wiki health check to find missing backlinks, broken links, duplicate concepts, stale summaries, or thin pages.

## Workflow

### 1) Inventory the sources

- Prefer local files first. If the corpus lives across GitHub repos or web pages, gather URLs and dates before writing.
- Do not edit raw sources in place. If external material needs preserving, save a capture under `raw/`.
- Keep a compact inventory page in `wiki/indexes/` so future runs can discover the corpus quickly.

### 2) Compile the wiki

- Start with source summaries and project pages before writing broader concept pages.
- Write concept pages only when two or more sources support synthesis.
- Update backlinks and "See also" sections as part of the same pass.
- Keep index files current so the wiki stays easy to navigate without full-text search.
- If a repository already has good docs, summarize and link to them instead of copying them.

### 3) Write outputs as files

- For questions, reports, or comparisons, prefer a file in `outputs/` over a chat-only answer.
- When an output contains durable knowledge, fold the stable parts back into `wiki/` and update indexes.

### 4) Run health checks

- Look for orphan pages, dead links, missing source citations, duplicated concepts, contradictory facts, stale project metadata, and empty sections.
- Suggest the next highest-value pages to create based on gaps in the graph.

## Writing rules

- Use standard Markdown links, not Obsidian wikilinks.
- Optimize for public browsing: clear titles, short intros, stable slugs, and scannable sections.
- Prefer relative links for local pages and absolute URLs for source links.
- Preserve exact dates, repo URLs, and names for facts that may change.
- Every durable claim should trace back to a source, repo, paper, or prior page.
- Synthesize across sources; do not just restate one document.
- Avoid sales language. This is a knowledge base, not a portfolio landing page.

## Undergraduate portfolio guidance

When the knowledge base represents undergraduate work:

- Treat repositories as evidence of projects, not the whole story.
- Add course, theme, and timeline pages so viewers can browse by idea instead of only by repo name.
- For each project page, capture what it is, why it mattered, how it worked, what you learned, and what it connects to.
- Surface growth over time with timeline pages and cross-links between early and later work.

## Deliverables to prefer

- `wiki/projects/<slug>.md`
- `wiki/concepts/<slug>.md`
- `wiki/courses/<slug>.md`
- `wiki/timeline/<slug>.md`
- `wiki/indexes/*.md`
- `outputs/YYYY-MM-DD-<slug>.md`
