# Workshop Naming Convention (locked)

Client pages use **two titles only**: `program_title` + `lens_title`.  
Internal ops use a short handle. There is **no third client page title**.

## Layers

| Layer | Field / form | Client-facing? | Rule |
| --- | --- | --- | --- |
| Handle | `{PROGRAM}-T{n}-U{nn}` | No | Slack / sheets / paths talk (e.g. `ATC-T2-U01`) |
| Program title | `program_title` | Yes — hero program line | Stable per workshop code; locale variant only |
| Lens title | `lens_title` | Yes — hero H1 | Per `(program × tier)` only |
| Unit | `unit_id` + `unit_goal` | Goal is lead copy only | Not a brand title; units share program + lens for that tier |

**Multi-unit:** same `program_title` + same `lens_title` for all units of that program×tier. Differentiate with `unit_id`, `unit_goal`, and asset titles.

**Tier letters A–E are abandoned.** Use T1–T4 only:

| Handle | `audience_id` |
| --- | --- |
| T1 | `tier_1_operator` |
| T2 | `tier_2_frontline_leader` |
| T3 | `tier_3_operational_manager` |
| T4 | `tier_4_strategic_leader` |

Book / methodology names are **internal provenance only**. Never use them as client titles; put them in `banned_phrases` when relevant.

## Codebook (internal)

| Code | Source methodology (internal) |
| --- | --- |
| TFS | Thinking, Fast and Slow |
| EIG | Emotional Intelligence |
| ATC | Atomic Habits |
| HWF | How to Win Friends and Influence Others |
| TCM | The Culture Map |
| GTY | Getting to Yes |
| PRL | Powerful |
| TDC | The Diamond Cutter |
| SWW | Start with Why |

Folder slug = lowercase code (`ATC` → `content/atc/`).

## Public catalog (`program_title`)

| Code | EN | ES |
| --- | --- | --- |
| TFS | Cognitive Anchors & Deliberation | Anclaje cognitivo y deliberación |
| EIG | Emotional Resilience & Resonance | Resiliencia y resonancia emocional |
| ATC | Operational Habits & Execution | Hábitos operativos y ejecución |
| HWF | Interpersonal Synergy & Diplomacy | Sinergia interpersonal y diplomacia |
| TCM | Cross-Cultural Integration | Integración intercultural |
| GTY | Tactical & Enterprise Negotiation | Negociación táctica y empresarial |
| PRL | High-Performance Architecture | Arquitectura de alto rendimiento |
| TDC | Mindful Productivity & Governance | Productividad consciente y gobernanza |
| SWW | Purpose-Driven Vision | Visión orientada al propósito |

## Lens matrix EN (`lens_title`)

| Code | T1 | T2 | T3 | T4 |
| --- | --- | --- | --- | --- |
| TFS | Cognitive Anchors | Analytical Deliberation | Strategic Intuition | Enterprise Risk & Forecasting |
| EIG | Self-Regulation Fundamentals | Empathic Team Leadership | Organizational Resonance | Executive Presence & Stewardship |
| ATC | Micro-Habits for Execution | Team Accountability Loops | Systemic Scaling Architecture | Cultural Habit Transformation |
| HWF | Interpersonal Synergy | Team Engagement Strategies | Strategic Diplomacy | Alliance & Industry Influence |
| TCM | Cross-Cultural Collaboration | Operational Adaptability | Cultural Matrix Synthesis | Global Enterprise Integration |
| GTY | Collaborative Alignment | Tactical Negotiation | Cross-Functional Mediation | High-Stakes Enterprise Negotiation |
| PRL | High-Performance Basics | Accountability Frameworks | Talent Velocity Optimization | Radical Culture Stewardship |
| TDC | Mindful Productivity | Resilient Team Dynamics | Values-Driven Governance | Corporate Karma & Universal Ethics |
| SWW | Purpose-Driven Contribution | Translating Team Purpose | Operational Value Alignment | Strategic & Generational Purpose |

## Lens matrix ES (`lens_title`)

| Code | T1 | T2 | T3 | T4 |
| --- | --- | --- | --- | --- |
| TFS | Anclajes cognitivos | Deliberación analítica | Intuición estratégica | Riesgo corporativo y predicción |
| EIG | Fundamentos de autorregulación | Liderazgo empático de equipos | Resonancia organizacional | Presencia ejecutiva y responsabilidad institucional |
| ATC | Microhábitos para la ejecución | Bucles de responsabilidad del equipo | Arquitectura de escalamiento sistémico | Transformación cultural de hábitos |
| HWF | Sinergia interpersonal | Estrategias de compromiso en el equipo | Diplomacia estratégica | Alianzas e influencia en la industria |
| TCM | Colaboración intercultural | Adaptabilidad operativa | Síntesis de matrices culturales | Integración empresarial global |
| GTY | Alineación colaborativa | Negociación táctica | Mediación interfuncional | Negociación empresarial de alto nivel |
| PRL | Fundamentos de alto rendimiento | Marcos de trabajo para la rendición de cuentas | Optimización de la velocidad del talento | Gestión de la cultura radical |
| TDC | Productividad consciente | Dinámicas de equipo resilientes | Gobernanza basada en valores | Karma corporativo y ética universal |
| SWW | Contribución orientada al propósito | Traducción del propósito del equipo | Alineación operativa de valores | Propósito estratégico y generacional |

### ATC T2 (shipped)

| Field | EN | ES |
| --- | --- | --- |
| `program_title` | Operational Habits & Execution | Hábitos operativos y ejecución |
| `lens_title` | Team Accountability Loops | Bucles de responsabilidad del equipo |

## Ingest checklist (future packs)

1. Confirm code exists in the codebook (or add it once).
2. Path: `content/{code_lower}/{uNN}/{locale}/`.
3. Manifest: `program_id`, `unit_id`, `audience_id`, `program_title`, `lens_title` from this note — **do not invent a third title**.
4. Ban book/source names in `banned_phrases`.
5. Asset titles stay on assets; they are not program/lens brands.
6. Internal talk: `{CODE}-T{n}-U{nn}` only.

## Hero render contract

1. Platform brand: Global Leadership  
2. Program line: `program_title`  
3. H1: `lens_title`  
4. Lead: `unit_goal`  
5. Meta may show program · unit (e.g. `ATC · U01`) — not tier/locale  
6. Footer: `{program_title} · Global Leadership · {E}`
