# Page Standards

These are the default page shapes for a repo-native knowledge base. Keep them simple and readable in plain markdown.

## General rules

- Start each page with a short summary paragraph instead of metadata-heavy frontmatter.
- Use relative links for local pages and absolute URLs for external sources.
- End each durable page with `## Related` and `## Sources` unless there is a strong reason not to.
- Link every non-index page from at least one index page.
- Prefer a few meaningful links over a long dump of loosely related links.

## Repositories index

Recommended file: `wiki/indexes/repositories.md`

For each repository, capture:

- name
- one-line summary
- primary topic or course
- primary stack
- repository URL
- link to the local project page

Keep this file compact. It is an entry point, not the full write-up.

## Project pages

Recommended file pattern: `wiki/projects/<slug>.md`

Suggested sections:

- `## Overview`
- `## Why It Mattered`
- `## How It Worked`
- `## Key Artifacts`
- `## Lessons Learned`
- `## Related`
- `## Sources`

Project pages should explain the work clearly enough that someone can understand the project without opening the repo first.

## Concept pages

Recommended file pattern: `wiki/concepts/<slug>.md`

Suggested sections:

- `## Definition`
- `## Why It Matters Here`
- `## Evidence Across Projects`
- `## Related`
- `## Sources`

Write a concept page only when at least two sources or projects support the synthesis.

## Course pages

Recommended file pattern: `wiki/courses/<slug>.md`

Suggested sections:

- `## Scope`
- `## Projects And Assignments`
- `## Key Ideas`
- `## Related`
- `## Sources`

These pages help viewers understand the academic context behind the work.

## Timeline pages

Recommended file pattern: `wiki/timeline/<slug>.md`

Suggested sections:

- `## Period`
- `## What Changed`
- `## Projects`
- `## Concepts`
- `## Sources`

Use timeline pages to show progression, not just chronology.

## Outputs

Recommended file pattern: `outputs/YYYY-MM-DD-<slug>.md`

Use outputs for:

- research answers
- comparisons
- reading notes
- drafts for future wiki pages
- slide-ready markdown

If an output becomes durable reference material, move or merge the stable parts into `wiki/`.
