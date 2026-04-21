# Working Principles

This skill adapts the "LLM wiki" pattern into a plain repository workflow.

## Three layers

1. `raw/`: immutable source material such as repos, articles, papers, notes, screenshots, and datasets.
2. `wiki/`: derived markdown pages written and maintained by the LLM.
3. Skill instructions: the operating rules that tell the LLM how to ingest, compile, link, and lint the wiki.

The core idea is simple: keep source material stable, let the LLM maintain the derived layer, and make the outputs accumulate over time.

## What to preserve from the original pattern

- The wiki should be maintained by the LLM, not manually curated page by page.
- New source material should make the existing wiki denser, not just longer.
- Small index files and concise summaries are often enough at this scale; do not reach for RAG by default.
- Durable answers should become files in the repo so future work compounds instead of resetting every session.
- Periodic health checks are part of the system, not an afterthought.

## Repo-native adaptation

- Use normal markdown links and local files. Do not rely on Obsidian-only features.
- Write for two readers at once: the LLM maintaining the corpus and a human browsing it on GitHub or GitHub Pages.
- Prefer a few strong navigation pages over many shallow top-level pages.
- Keep the knowledge base factual and browsable; repositories are evidence, but concept, course, and timeline pages provide the synthesis.

## Recommended entry points

If the corpus is centered on undergraduate work, prioritize:

- a repositories index
- project pages
- concept pages that cut across multiple projects
- course pages that group work by academic context
- timeline pages that show growth over time

That structure lets viewers browse by artifact, idea, or period instead of only by repository name.
