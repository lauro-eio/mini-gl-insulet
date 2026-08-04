# global-leadership-preview — HTML publish repo (locked)

**Repo:** [https://github.com/lauro-eio/global-leadership-preview.git](https://github.com/lauro-eio/global-leadership-preview.git)

This repository is **only** for published Global Leadership **HTML content** (unit atoms + optional editor catalog). Vercel (or similar) will pull from here.

Formerly named `GL-Preview` (deleted); use the lowercase name only.

## What belongs here

| Include | Exclude |
| --- | --- |
| Static HTML unit pages (`/{program}/{unit}/{locale}/`) | Factory source (`content/`, `library/`, schemas, scripts) |
| Locale catalogs `/en/` and `/es/` | Markdown drafts, YAML manifests |
| Minimal site assets needed to serve HTML | Insulet / client-tailored workshops |
| | Notes, agent transcripts, Python tooling |

## Relationship to mini-GL

```text
mini-GL (factory)  →  validate / render  →  copy HTML into global-leadership-preview  →  Vercel
```

- **mini-GL** = source of truth and generation.
- **global-leadership-preview** = thin publish surface for the app and revision browsing.
- Do not develop workshop content inside the publish repo.

## Rules (see also html-index.md)

1. One GL publish repo — this one — not one repo per unit.
2. Atoms have no cross-unit / cross-workshop navigation.
3. App deep-links unit URLs only; catalog is editor-facing.
4. Never publish Insulet into this site.

## Status

ATC T2 U01–U04 EN+ES published at `/atc/u0N/{en,es}/`. Locale catalogs at `/en/` and `/es/`. Connect Vercel when ready.
