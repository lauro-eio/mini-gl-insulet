# mini-GL — Global Leadership content factory

Factory for soft-skills workshop packs: normalize existing assets, validate, render HTML preview, then publish to a thin HTML repo.

Platform (EGREGOR) convert/upload is **out of scope** for the current MVP.

## Scope boundary

**Global Leadership (this factory)** = catalog programs such as ATC (and future TFS, EIG, …).

**Insulet** = a separate, tailored **client** workshop. It is **not** part of the GL catalog, not a factory program ID, and must not be mixed into GL publish surfaces or the Insulet-named client hosting repo. Keep any Insulet files under `examples/insulet/` (or a future `clients/insulet/`) isolated from `library/`, `content/`, and GL preview publishing.

## MVP (locked)

| Field | Value |
| --- | --- |
| Handle | `ATC-T2-U01` (program complete through U04 — see Notes/atc-program.md) |
| Program title (EN) | Operational Habits & Execution |
| Lens title (EN) | Team Accountability Loops |
| Program title (ES) | Hábitos operativos y ejecución |
| Lens title (ES) | Bucles de responsabilidad del equipo |
| Units | `u01`–`u04` (T2) |
| Audience | `tier_2_frontline_leader` |
| Locales | `en`, `es` |
| Ship | HTML preview → publish repo |

Full codebook, lens matrix, and ingest rules: [Notes/workshops-naming-convention.md](Notes/workshops-naming-convention.md). Client titles must **not** use book names (e.g. “Atomic Habits”).

HTML publish (one repo, unit atoms, editor catalog): [Notes/html-index.md](Notes/html-index.md).  
Publish target (HTML only): [https://github.com/lauro-eio/GL-Preview.git](https://github.com/lauro-eio/GL-Preview.git) — [Notes/gl-preview-repo.md](Notes/gl-preview-repo.md).

ATC T2 status: [Notes/atc-program.md](Notes/atc-program.md).

## Layout

```text
schemas/          # JSON Schema contracts
library/atc/      # Normalized + approved source packs
content/atc/u01/  # Ship-ready structured content
scripts/          # validate.py, render.py
preview/          # Generated HTML (gitignored)
examples/         # Optional published HTML copies for hosting
Notes/            # Design contracts (local / tracked)
```

## Commands

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

python scripts\validate.py --program atc --unit u01 --locale en
python scripts\render.py --program atc --unit u01 --locale en
```

Rendered output: `preview/atc/u01/en/index.html`

## Naming

| Layer | Example |
| --- | --- |
| Handle (internal) | `ATC-T2-U01` |
| `program_title` (client) | Operational Habits & Execution |
| `lens_title` (client H1) | Team Accountability Loops |
| Audience | `audience_id` → T1–T4 in the handle |
| Unit | `unit_id` + `unit_goal` (not a third brand title) |

### Ingest checklist (new packs)

1. Confirm code in the codebook (or add once).
2. Path: `content/{code_lower}/{uNN}/{locale}/`.
3. Manifest: `program_id`, `unit_id`, `audience_id`, `program_title`, `lens_title` from the naming note — no third title.
4. Ban book/source names in `banned_phrases`.
5. Asset titles stay on assets.
6. Talk ID: `{CODE}-T{n}-U{nn}` only.
