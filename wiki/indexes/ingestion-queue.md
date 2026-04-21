# Ingestion Queue

This queue defines the recommended order for deeper ingestion. Each pass should read the repository itself, capture the important files into `raw/` as needed, and then create or expand the corresponding wiki pages.

## Recommended Order

1. `SEM-4-IITB-EE` -> [seed page created](../projects/sem-4-iitb-ee.md)
2. `SEM-5-IITB-EE` -> [seed page created](../projects/sem-5-iitb-ee.md)
3. `SEM-6-IITB-EE` -> [seed page created](../projects/sem-6-iitb-ee.md)
4. `SEM-7-IITB-EE` -> [seed page created](../projects/sem-7-iitb-ee.md)
5. `SEM-8-IITB-EE` -> [seed page created](../projects/sem-8-iitb-ee.md)
6. `SOC-2020` -> [seed page created](../projects/soc-2020.md)
7. `UMIC_TEAM4-Final` -> [seed page created](../projects/umic-team4-final.md)
8. `InstiShop` -> target page `wiki/projects/instishop.md`
9. `MA-tuts` -> [seed page created](../projects/ma-tuts.md)
10. `MOOC-content` -> [seed page created](../projects/mooc-content.md)
11. `reports_SOC2020` -> [seed page created](../projects/reports-soc2020.md)
12. `16-bit-ALU` -> [seed page created](../projects/16-bit-alu.md)
13. `Autumn-of-Automation` -> [seed page created](../projects/autumn-of-automation.md)
14. `iamprasann.github.io` -> intentionally skipped because this repository is the host knowledge base

## Why This Order

- Start with the semester repositories because they are likely to expose the broadest undergraduate structure.
- Move next to bounded projects that can become stronger narrative pages.
- Leave forks and support repositories later, once the main academic story is already mapped.
- Do not ingest the site repository itself; it is the host knowledge base for the derived wiki.

## Per-Repository Pass Checklist

- Read `README` and top-level structure.
- Identify courses, projects, reports, notebooks, presentations, and datasets.
- Capture important references, screenshots, and source links into `raw/` only when needed.
- Write or expand the project page in `wiki/projects/`.
- Update `wiki/indexes/repositories.md` with the local page link once it exists.
- Create follow-on concept, course, or timeline pages when the repo supports broader synthesis.

## Related

- [Repositories](./repositories.md)

## Sources

- [raw/github/2026-04-21-iamprasann-repositories.json](../../raw/github/2026-04-21-iamprasann-repositories.json)
