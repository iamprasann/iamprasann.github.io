# Prasann Iyer Knowledge Base

This repository is the source and the published site for `iamprasann.github.io`.

It is structured as a small static wiki:

- `wiki/` holds the curated article layer.
- `raw/` holds source captures and ingestion artifacts.
- `assets/` holds the grayscale site shell, search, and generated search index.
- `scripts/build_wiki_site.py` compiles the markdown corpus into the published HTML site.

## Rebuild the site

Run:

```bash
python3 scripts/build_wiki_site.py
```

That regenerates:

- `index.html`
- `404.html`
- `indexes/*.html`
- `projects/*.html`
- `raw/**/*.html`
- `assets/wiki-search.json`
- `.nojekyll`

The repository is intended to be served directly by GitHub Pages.
