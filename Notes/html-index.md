# HTML publish index (locked)

One GL publish repo → one Vercel site. Many unit pages. Two audiences.

**Publish repo (HTML only):** [https://github.com/lauro-eio/GL-Preview.git](https://github.com/lauro-eio/GL-Preview.git) — see [gl-preview-repo.md](gl-preview-repo.md).

Learners must not navigate across units or workshops **inside the HTML**.  
Editors still need a browsable map of everything.

Related: [workshops-naming-convention.md](workshops-naming-convention.md) (handles, titles).

---

## Locked rules

1. **One GL publish repo** (`lauro-eio/GL-Preview`) → one Vercel project. Not one repo per unit. HTML content only — no factory source.
2. **Publish atom** = one HTML document per `(program × unit × locale)`.
3. **No cross-nav in atoms:** unit pages must not link to other units or workshops. In-page section TOC only.
4. **App** deep-links the enrolled unit URL only — never the catalog.
5. **Catalog** = editor revision surface only; protect it and/or keep it out of the app.
6. **Insulet** never ships on the GL publish site.

---

## Surfaces

| Surface | Who | Role |
| --- | --- | --- |
| Unit atom | Learners (via app) | Sealed unit document |
| Catalog (`/_review/` or similar) | Editors | Navigate all packs for revision |
| App | Product | Curriculum router + enrollment gate |

```text
Factory (mini-GL)  →  render HTML
       ↓
Publish repo (GitHub: lauro-eio/GL-Preview)  →  Vercel
       ↓
  ┌────┴────┐
  atom URL   catalog (editor)
  (app only) (you only)
```

---

## URL pattern (stable)

Path-style, derived from ids — **not** from marketing titles:

```text
/{program}/{unit}/{locale}/
```

Examples:

| Pack | URL |
| --- | --- |
| ATC U01 EN | `/atc/u01/en/` |
| ATC U01 ES | `/atc/u01/es/` |

Tier stays in handle/metadata (`ATC-T2-U01`); it does **not** need to appear in the public path. Locale is implied by the path and page language — no locale switcher required on the atom.

Factory preview already mirrors this shape: `preview/atc/u01/en/index.html`.

---

## App contract

Each enrollable unit stores:

| Field | Example |
| --- | --- |
| Handle | `ATC-T2-U01` |
| `content_url_en` | `https://{host}/atc/u01/en/` |
| `content_url_es` | `https://{host}/atc/u01/es/` |

Open unit in-app → load that URL (iframe / WebView / browser). Cross-unit and cross-workshop navigation lives in the **app**, not in the HTML.

---

## Catalog (editor only)

- Location: e.g. `/_review/index.html` (or root `/` only if Deployment Protection / password / private preview).
- May list every program × unit × locale with links to atoms.
- Atoms must **not** link back to the catalog.
- Prefer `noindex` on the catalog when the site is otherwise public.

Root `index.html` in this factory today is a **local/editor convenience**, not a learner entry for production.

---

## Security note

Path isolation stops casual browsing and in-page leakage. Anyone who knows another atom URL can still open it until the app or CDN adds auth. That is acceptable for MVP; do not “fix” it with one-repo-per-unit.

---

## Checklist (new unit to Vercel)

1. Validate + render in factory.
2. Copy atom to publish repo at `/{program}/{unit}/{locale}/index.html`.
3. Update editor catalog entry (handle + program/lens titles + locale links).
4. Set app `content_url_*` for that unit.
5. Confirm atom has no outbound links to other units/workshops.
