# Content ingest (locked)

How new workshop source enters the factory with **minimum operator work**.

## Do / don’t

| Do | Don’t |
| --- | --- |
| Leave Drive/zip source where it is and pass its path | Drop raw files into `content/` |
| Match ingest path to **source shape** (A, B, or C below) | Force Habit-Hacking mapper on foundation-only dumps |
| Rewrite tier packs in `content/` after archive/import | Skip provenance |
| Tell the agent: handle + source path | Hand-build manifests without titles from naming note |

## Source shapes

### Path A — Habit-Hacking unit folders (e.g. ATC)

Per-unit folders with delivery `.txt` (`InvestigativeReport_…`, etc.) already flat in one directory.

```text
Unit folder
  → scripts/ingest_unit.py --program … --unit … --src …
  → library/{program}/u0N/en/_raw/ + *.SOURCE.txt
  → content/{program}/u0N/{en,es}/  (tier rewrite)
```

### Path B — Foundation workshop (e.g. TFS)

Workshop root with `master_foundation.json`, blueprints, chapter JSON/quizzes — **no** unit delivery folders. Syllabus units live inside the foundation JSON.

```text
Workshop ENG root (+ Generated_Quizzes/)
  → library/{program}/_source/en/  (+ _source/Generated_Quizzes/)
  → synthesize each unit into content/{program}/u0N/{en,es}/
```

Do **not** run `ingest_unit.py` on a Path B root (everything will be `WARN unmapped`). Archive to `_source` instead.

### Path C — Asset-type Habit-Hacking dump + foundation (e.g. EIG)

Delivery files use Habit-Hacking prefixes and `*_Unit0N_*` names, but live in **asset-type folders** (InvestigativeReport/, PersonalityQuiz/, …), often with `master_foundation.json` alongside. `ingest_unit.py` does not recurse.

```text
Workshop root
  → library/{program}/_source/   (full archive)
  → stage flat Unit0N delivery .txt → library/{program}/_stage/u0N/
  → scripts/ingest_unit.py --program … --unit u0N --src library/{program}/_stage/u0N
  → library/{program}/u0N/en/ + content rewrite
```

Do **not** browse-ingest the workshop root. See [eig-program.md](eig-program.md).

## Layers (all paths)

```text
library/     = provenance (unit SOURCE and/or program _source)
content/     = ship-ready rewritten packs only
validate / render → examples/ + global-leadership-preview
```

## Operator workflow (least work)

1. Confirm codebook + titles in [workshops-naming-convention.md](workshops-naming-convention.md).
2. Identify Path A, B, or C.
3. Import/archive (script Path A; copy/`_source` Path B; archive + stage + script Path C).
4. Agent rewrites EN → validate/render → skim → ES → catalogs → publish HTML.

You decide once per pack: **program code, unit id, tier** (usually T2).

## Ingest script (Path A and Path C after staging)

```powershell
py -3 scripts/ingest_unit.py --program atc --unit u01 --src "D:\path\to\Unit 01"
py -3 scripts/ingest_unit.py --program eig --unit u01 --src "library/eig/_stage/u01"
py -3 scripts/ingest_unit.py --program atc --unit u01 --browse
.\scripts\ingest_unit.browse.ps1 -Program atc -Unit u01
```

**Implemented:** [scripts/ingest_unit.py](../scripts/ingest_unit.py) — copy + SOURCE map only (`--force` to overwrite). Fixture: `scripts/fixtures/ingest_sample/`.

**Out of scope for the script:** markdown rewrite, validate/render, catalog/publish, Path B foundation archive automation, Path C staging automation.

## Filename map (Path A / Path C)

| Source prefix | `*.SOURCE.txt` |
| --- | --- |
| InvestigativeReport | research_article |
| FeatureStory | opinion_article |
| ParticipantKeyPoints | key_notes |
| PersonalityQuiz | self_assessment |
| CaseStudy | case_study_01 |
| TraditionalBusinessCaseStudy | case_study_02 |
| UnitReflectionQuestions | commitment_plan |
| RolePlayScenario1v1 | live_roleplay_1v1 |
| StrategicRolePlay | live_roleplay_strategic |

## After import/archive

Follow naming checklist + [html-index.md](html-index.md). Titles from the naming note only — no third client page title. For TFS see [tfs-program.md](tfs-program.md); for EIG see [eig-program.md](eig-program.md).
