# Capability inventory

Every skill, agent, hook, and data connection this system fires or depends on — one place to see
the whole stack, not just the 3 new components this repo adds. Confirmed against spec 006's
skill-coverage-gap audit (2026-07-02): full coverage across `g-intel-*`, `g-pm-*`, `g-sales-*`;
`g-gov-fairness` and `g-create-doc`/`g-create-pdf` deliberately excluded (see "Explicitly out of
scope" below).

## Intel (research) — all 9 `g-intel-*` skills — vendored as `tvt-intel-*`

| Skill | Fires for | Status |
|---|---|---|
| `tvt-intel-pipeline` | The orchestrator — chains the 6 below, `stages=` selectable, resumable | Vendored |
| `tvt-intel-deep` | Base single-account research cycle | Vendored |
| `tvt-intel-customer` | 5-step deep cycle (financial/platform/insider/market/case-study) — top-ranked accounts only (§5 tiering) | Vendored |
| `tvt-intel-dossier` | Standard per-account research artifact — everyone else | Vendored |
| `tvt-intel-fanout` | Named competitor/vendor entities → MEDDPICC Competition | Vendored |
| `tvt-intel-qbr` | Account review — the EXPAND-motion whitespace input | Vendored |
| `tvt-intel-factcheck` | **Mandatory gate** before research reaches POV synthesis | Vendored |
| `tvt-intel-dispatch` | Parallel fan-out across *many* prospects — the HUNT top-of-funnel scan | Vendored |
| `tvt-intel-flywheel` | Cross-client pattern extraction — feeds POV synthesis | Vendored |

## Product / AI-opportunity loop — vendored as `tvt-pm-*` (added 2026-07-05, closes a silent gap
found in the 2026-07-05 integrity audit — see `docs/audit-2026-07-05-tvt-skill-integrity.md`)

Load-bearing to `tvt-sales-engine`'s own job-0/3a spine (spec 006 §1/§3a) — not optional. Previously
listed here with no Status column at all, the one dependency this table failed to vendor or flag,
against spec 007's own SC-005 ("no silent gaps"). Fixed by vendoring, matching the pattern already
used for every other dependency in this file.

| Skill | Fires for | Status |
|---|---|---|
| `tvt-pm-jtbd` | Score a client's under-served AI opportunities (Ulwick ODI) | Vendored |
| `tvt-pm-grow` | Grow scored opportunities into roadmap + narrative (RICE×Kano + Thompson + MDI) | Vendored |

## Governance — vendored as `tvt-*` (rebranded from `g-` prefix 2026-07-06, transitive deps of `tvt-sales-pov`, FR-009)

| Skill | Fires for | Status |
|---|---|---|
| `tvt-gov-guard` | CRM PII redaction/masking — 006 does not roll its own | Vendored (`tvt-gov-guard/`) |
| `tvt-gov-attest` | Append-only, hash-chained decision ledger — the confidence/outcome backtest substrate | Vendored (`tvt-gov-attest/`) |

## Sales point-tools — vendored as `tvt-sales-*`

| Skill | Fires for | Status |
|---|---|---|
| `tvt-sales-pack` | Presales assembly, close support | Vendored |
| `tvt-sales-pitch` | Deck content strategy | Vendored |
| `tvt-sales-engagement-proposal` | Client-facing engagement proposal (.docx) | Vendored |
| `tvt-sales-distill` | Sales pattern refinement | Vendored |

## Presentation — vendored as `tvt-create-*`

| Skill | Fires for | Status |
|---|---|---|
| `tvt-create-deck` | Client-facing decks | Vendored |
| `tvt-create-explainer` | Persuasive multi-section PDF (used for the spec 006 sales-team overview) | Vendored |
| `tvt-create-pptx` | PPTX build/edit | Vendored |
| `tvt-create-design` | Visual design pass | Vendored |
| `tvt-tavantize` | Apply Tavant branding to a deck; bundles its own copy of `assets/tavant-template.pptx` | Vendored |

## General cognitive skills — vendored as `tvt-os-*` / `tvt-core-*` (added 2026-07-04, spec 007 FR-013)

Sourced from the `gordon-os` marketplace (`github.com/90rdon/gordon-os-marketplace.git`), skills
only — no hooks (FR-014). 2 personal-life packs excluded (`g-os-pack-personal-finance-checkin`,
`g-os-pack-time-attention-mine/review`).

**Source-state caveat (verified 2026-07-04, line-count + content check on every file, not
assumed):** 7 of the 15 originally-vendored cognitive skills are stubs in their
gordon-os-marketplace *source*. As of 2026-07-06 those 7 are **unshipped** (see the note below the
table) rather than listed as installable — an honest maintainer doc was not a remedy for a dead
skill in a rep's picker.

| Skill | Fires for | Status |
|---|---|---|
| `tvt-os-contrarian` | Devil's-advocate / red-team review of an idea or plan | Vendored, real |
| `tvt-os-judge` | Senior-engineer-style drift/quality gate on an artifact | Vendored, real (Stop-hook wiring excluded, FR-014) |
| `tvt-os-loop` | Iterative run-until-criteria-met loop | Vendored, real |
| `tvt-os-metacognition` | Routes an idea to judge and/or contrarian, returns one verdict | Vendored, real |
| `tvt-os-prompt` | — | Vendored, real (176 lines) |
| `tvt-grill-me` | Interviews the user until a plan/design reaches shared understanding | Vendored, real |

**Unshipped (moved out of the installable catalog):** 9 skills total. 7 whose upstream source is
a placeholder stub (17-20 lines of "Stub lands in US1 (T054)" task bookkeeping, 2026-07-06 —
review finding F2): `tvt-os-forecast`, `tvt-os-improve`, `tvt-os-reason`, `tvt-os-recommend`,
`tvt-os-research`, `tvt-os-synthesize`, `tvt-os-verify` — they re-enter `skills/` if/when their
upstream (`gordon-os-marketplace`) actually implements them. Plus 2 purely maintainer-workflow
tools with zero rep value (2026-07-06 — review finding F16, Wave 4 curation): `tvt-os-skill-review`
(a review queue for promoting Tier-B skill *candidates*, not something an installed plugin's user
ever runs) and `tvt-os-replay` (a git-bisect-style regression helper for the maintainer's own
build process). A rep invoking "critique this" or "is this good" routes to `tvt-os-metacognition`
— the one rep-facing front door for that whole cluster (review finding F12).
| `tvt-grill-me` | Interview-style stress-test of a plan/design | Vendored, real |
| `tvt-core-clarify` | Guided intent clarification | Vendored, real (mandatory dep of `tvt-os-*`) |
| `tvt-core-eval` | — | Vendored, real (701 lines) |
| `tvt-core-extract` | — | Vendored, real (410 lines) |
| `tvt-core-lookup` | Pattern-library / playbook matching | Vendored, real (291 lines) |
| `tvt-core-mcts` | — | Vendored, real (334 lines) |
| `tvt-core-portfolio` | — | Vendored, real (170 lines) |
| `tvt-core-write` | — | Vendored, real (1032 lines) |

## Agents

| Agent | Fires for | Status |
|---|---|---|
| `ai-solution-thinker` | `tvt-sales-pov`'s synthesis reasoning — pain-point → solution-hypothesis → accelerator-pattern methodology, reused rather than re-derived | Vendored (`agents/ai-solution-thinker.md`) |

## Bundled reference content (added 2026-07-04)

Several vendored skills reference this shared content by relative path (`../playbooks/...`,
`../accelerators/...`, `../assets/...`) rather than the author's Workspace-only `org/` paths:

| Directory | Contents |
|---|---|
| `playbooks/` | All 30 Tavant methodology playbooks (sales patterns, discovery frameworks, deck design systems, etc.) |
| `accelerators/` | `tvt-sdlc-skills-platform.md` |
| `assets/` | `tavant-template.pptx` — the branded PPTX template `tvt-tavantize`/`tvt-sales-pack` apply |

## Automation (existing substrate, not a new scheduler)

| Component | Role |
|---|---|
| `agents/heartbeat/hermes.sh` | The author's personal 30-min launchd heartbeat (their machine only, not shipped in this plugin). The spec §6 scripts (`sales-pulse.sh`/`prospect-radar.sh`/`outreach-followup.sh`) are **not built** and nothing registers in hermes today — for plugin users the equivalent is a manual cadence: run `tvt-sales-engine status` Monday AM. |

Note: Claude Code **hooks** (PreToolUse/PostToolUse/Stop) are a development-tooling concern for
whoever edits *this repo* with Claude Code — they configure in `.claude/settings.json` on the
editing machine, not in this repo's runtime. This system's own "hooks" are the Hermes heartbeat
scripts above.

## Data connections

| Source | Role |
|---|---|
| Local JSON (`opportunities.json`, `claims.json`) | **Primary data path** — manually authored or CSV-exported. Not a fallback; the intended shape for sales-team members without the author's personal MCP access. |
| Salesforce MCP | Deliberately deferred, not scheduled — a possible future optional adapter onto the same `opportunities.json` shape. |
| Notion MCP | Deliberately deferred, not scheduled — a possible future optional adapter onto the same `claims.json` shape. |

## Router template

`g-dev-build` — not fired at runtime, but `tvt-sales-engine`'s intent→job routing pattern (§4)
mirrors its `intent → phase → execute` structure.

## Explicitly out of scope (skill-coverage audit, 2026-07-02)

- **`g-gov-fairness`** — tests protected-class disparate impact for decisions *about people*
  (ECOA/HMDA/EEOC). This system scores *B2B accounts*, not individuals in protected classes.
  Different job.
- **`g-create-doc`** — already subsumed by `g-sales-engagement-proposal`'s .docx output.
- **`g-create-pdf`** — generic PDF ops (merge/split/OCR); no unmet job here.
- A bespoke DSL/orchestration framework for "stacking" skills — considered and rejected
  (2026-07-02 contrarian pass): the 3-layer skill taxonomy + router-skill pattern already in the
  workspace, plus Anthropic's own "skills should be passive, not agentic" guidance, cover this
  without a new abstraction layer.
