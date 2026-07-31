# mini-GL — Global Leadership content factory

Factory for soft-skills workshop packs: normalize existing assets, validate, render HTML preview, then publish to a thin HTML repo.

Platform (EGREGOR) convert/upload is **out of scope** for the current MVP.

## MVP (locked)

| Field | Value |
| --- | --- |
| Program (internal) | `ATC` |
| Public title (EN) | Habit Systems for Frontline Leaders |
| Public title (ES) | Sistemas de hábitos para líderes de primera línea |
| Unit | `u01` (1% improvements / systems vs goals) |
| Audience | `tier_2_frontline_leader` |
| Locales | `en` first, then `es` |
| Ship | HTML preview → publish repo |

Internal workshop codes (backend): see `Notes/` / `old-gl/notes/workshop-naming-convention`. Client-facing titles must **not** use book names (e.g. “Atomic Habits”).

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
| Internal ID | `ATC` / `atc_u01` |
| Client EN | Habit Systems for Frontline Leaders |
| Client ES | Sistemas de hábitos para líderes de primera línea |
| Audience | Metadata `audience_id`, not a separate workshop code |
