# Tiered Assets — Audience & Asset Contract

Frozen decisions for **what** Global Leadership generates, **for whom**, and **where** each asset is deployed.

| Companion doc | Owns |
| --- | --- |
| `07226-1748-audiances.md` | Tier rationale (transition-based segmentation) |
| `072226-1813-workshop-architecture.md` | Module atoms, duration profiles, hero-module selection |
| `072226-1830-deployment-mapping.md` | Slot mapping (pre / live / post) per delivery format |
| `justification.md` | Client-facing pedagogical argument |

Sections 1–3 are locked; do not re-litigate them in prompts. Section 6 is not locked.

---

## 1. Audience enum (locked)

| `audience_id` | Operational scope | Prior terms |
| --- | --- | --- |
| `tier_1_operator` | Task execution, peer communication, personal habits, voicing concerns upward | Bottom-Line Operators, frontline operators |
| `tier_2_frontline_leader` | Direct supervision, 1-on-1 coaching, delegation, peer-to-boss transition | Junior Management, supervisors, coordinators, first-time managers |
| `tier_3_operational_manager` | Cross-functional coordination, managing up, coaching lower-tier leaders | Middle Management, managers of managers, department heads |
| `tier_4_strategic_leader` | Organizational culture, long-term strategy, change and ambiguity | Upper Management, directors, VPs, executives |

**Rule:** one principle, one syllabus spine, different scenario lens. Never fork the curriculum per tier.

Tiers 3 and 4 stay separate: grouping mid-level execution with strategy loses the manager→systems transition.

---

## 2. Asset catalog (locked)

Seven assets per principle. `shared` = one generation per principle. `lens` = one generation per `(principle, audience_id)`.

| # | `asset_id` | Name | Tiering | Default slot | Notes |
| --- | --- | --- | --- | --- | --- |
| 1 | `research_article` | Research / investigation article | shared | pre (series) · post (intensive) | Empirical data, metrics, behavioral science. Optional light per-tier implications footer. |
| 2 | `opinion_article` | Opinion article | lens | pre (series) · post (intensive) | Narrative portrait of a dilemma inside the tier's operational reality. |
| 3 | `key_notes` | Key notes / takeaways | shared | post (take-away) | Definitions and heuristics. One-page, high-visual. |
| 4 | `self_assessment` | Self-assessment (quiz) | lens | pre | Situational judgment questions scoped to the tier's decision authority. |
| 5 | `case_study` | Case study + discussion guide | lens | live | Scenario-heavy, written for subgroup breakouts. No prerequisites on other principles. |
| 6 | `framework_tool` | Framework / tool | lens | live | Operational canvas scaled to tier (habit tracker → steering matrix). |
| 7 | `commitment_plan` | Commitment / action plan | lens | post (session close) | Form skeleton is shared; stems, examples, and pledge target (peers / direct reports / org) take a lens. |

Slots above are defaults. The active delivery format overrides them — see `072226-1830-deployment-mapping.md`.

Why case study and framework are both `live`: the case is practice on someone else's problem, the framework is a tool for your own. They are not substitutes.

---

## 3. Generation policy

1. **Extraction runs once per principle.** Core data is audience-agnostic.
2. **Shared assets generate once per principle** (2 of 7).
3. **Lens assets generate per requested `audience_id`** (5 of 7):
   - *Library fill* — generate all four tiers to stock the catalog.
   - *Client job* — generate only the requested tier(s). Never emit 4 × 5 for a single-tier sale.
4. **Metadata:** every asset carries `audience_id` — a tier ID on lens assets, `shared` on shared assets. Platform filtering depends on this distinction.
5. **Guardrails live in schema, compiled reference, and prompt templates** so CLI and GUI jobs behave identically. `.cursorrules` may mirror them; it is not the source of truth.

---

## 4. Tier guardrails (prompt context)

| `audience_id` | Write about | Never use |
| --- | --- | --- |
| `tier_1_operator` | Individual performance, peer friction, shift handoffs, receiving feedback, raising concerns | Budget ownership, headcount decisions, board dynamics |
| `tier_2_frontline_leader` | Delegation, 1-on-1s, correcting a former peer, enforcing rules without burning bridges | Cross-BU strategy, executive peer alignment |
| `tier_3_operational_manager` | Managing up, lateral negotiation, coaching leaders, safety across teams | Individual task-level chores, C-suite/board framing |
| `tier_4_strategic_leader` | Culture and systems, change under uncertainty, influence without authority | Entry-level tasks, single-team supervision detail |

---

## 5. Prompt lens pattern

Add `{audience_id}` to every lens asset prompt:

> **Task:** Write a narrative-driven corporate portrait illustrating [core principle].
> **Audience:** `{audience_id}`.
> **Constraint:** Show, don't tell. Scenario, conflict, and character roles must sit inside the operational reality of `{audience_id}`. Do not use C-suite dynamics for tiers 1–2, and do not use entry-level tasks for tier 4.

---

## 6. Open locks / MVP resolutions

| Item | Status |
| --- | --- |
| Case cardinality | **Resolved (MVP):** `cases[]` with 1–N. ATC U01 ships two cases. |
| MVP audience | **Resolved (MVP):** ship `tier_2_frontline_leader` only; other tiers later. |
| Live extras | **Resolved (MVP):** `live_roleplay_1v1` and `live_roleplay_strategic` allowed on unit manifest (outside core 7). |
| Segment naming | Open: prefer principle / unit / module atom over book / chapter. |
| Justification sync | Open: `justification.md` still argues 6 assets; update to 7 + case. |
| Naming layers | Open: keep client labels separate from `asset_id`. |
| Case independence check | Open: enforce in `scripts/validate.py`. |
