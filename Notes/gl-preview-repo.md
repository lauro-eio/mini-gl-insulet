# GL-Preview — HTML publish repo (locked)

**Repo:** [https://github.com/lauro-eio/GL-Preview.git](https://github.com/lauro-eio/GL-Preview.git)

This repository is **only** for published Global Leadership **HTML content** (unit atoms + optional editor catalog). Vercel (or similar) will pull from here.

## What belongs here

| Include | Exclude |
| --- | --- |
| Static HTML unit pages (`/{program}/{unit}/{locale}/`) | Factory source (`content/`, `library/`, schemas, scripts) |
| Optional `/_review/` editor catalog | Markdown drafts, YAML manifests |
| Minimal site assets needed to serve HTML | Insulet / client-tailored workshops |
| | Notes, agent transcripts, Python tooling |

## Relationship to mini-GL

```text
mini-GL (factory)  →  validate / render  →  copy HTML into GL-Preview  →  Vercel
```

- **mini-GL** = source of truth and generation.
- **GL-Preview** = thin publish surface for the app and revision browsing.
- Do not develop workshop content inside GL-Preview.

## Rules (see also html-index.md)

1. One GL publish repo — this one — not one repo per unit.
2. Atoms have no cross-unit / cross-workshop navigation.
3. App deep-links unit URLs only; catalog is editor-facing.
4. Never publish Insulet into GL-Preview.

## Status

Repo exists and is currently empty. First push should follow the path pattern in [html-index.md](html-index.md) (e.g. `/atc/u01/en/index.html`).
