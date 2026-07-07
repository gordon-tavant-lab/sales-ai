---
name: tvt-sales-engine
layer: orchestrator
description: >
  Entry-point router for the end-to-end AI-assisted sales motion. Classifies a sales intent,
  fires the existing skill that owns that Job-to-be-Done stage, and measures the transition KPI.
  Mirrors g-dev-build's intent→phase→execute pattern for the sales domain. Owns none of the
  underlying work — orchestrator, not implementer.
  Trigger on any sales intent: "find new prospects", "who should I focus on", "expand <account>",
  "build a POV for <target>", "draft outreach to <target>", "prep for <meeting>", "status",
  "pipeline".
argument-hint: "<intent> | status | pipeline [--capacity N --floor hunt=N,expand=N]"
user-invocable: true
eval:
  mode: gate
  depth: standard
  note: only job 4 (outreach drafts) produces this router's own client-facing artifact; job 1 delegates to tvt-sales-prospect's deterministic gate, job 3 to tvt-sales-pov's gate.

---

# tvt-sales-engine — Sales Motion Router

Full design: see docs/ in this repo (this file mirrors the design's routing section as the build
contract). Do not duplicate the reasoning there — this file is the thin routing surface that fires
the skill owning each Job-To-Be-Done (JTBD). It computes nothing itself: `tvt-sales-prospect` does
the scoring math, `tvt-sales-pov` does the synthesis, the `tvt-intel-*` family does the research.

## How to Use This Skill

| You want to... | Say this |
|---|---|
| Find new-logo targets (HUNT) | `tvt-sales-engine "find new credit-union prospects"` |
| Rank this week's focus | `tvt-sales-engine "who should I focus on this week"` |
| Mine whitespace in a won account (EXPAND) | `tvt-sales-engine "expand Acme Corp"` |
| Form a point of view on a target | `tvt-sales-engine "build a POV for <target>"` |
| Draft (never send) outreach | `tvt-sales-engine "draft outreach to <target>"` |
| Prep for a meeting | `tvt-sales-engine "prep for <meeting>"` |
| See the portfolio scorecard | `tvt-sales-engine status` |
| See the ranked opportunity list | `tvt-sales-engine pipeline --capacity 8 --floor hunt=3,expand=2` |

## Step 1: Intent Router

Parse the intent text and classify against the JTBD spine (see docs/ in this repo, jobs 0–8). Motion (HUNT vs
EXPAND) and job are independent axes — detect both.

### Motion detection

| Signal | Motion |
|---|---|
| "new", "prospect(s)", "credit union(s)", a market/vertical name with no existing account context | **HUNT** |
| An existing/won account name ("expand X", "whitespace in X", "X's next opportunity") | **EXPAND** |
| Ambiguous (bare account name, no verb) | Ask one question: "Is this a new target or an existing account?" |

### Job classification

| Signal words | Job | Fires | Output |
|---|---|---|---|
| "find", "prospects", "new targets", "whitespace scan" | 0 · Find where to play | `tvt-intel-dispatch` (HUNT) / `tvt-intel-qbr` (EXPAND) | candidate list |
| "who should I focus on", "shortlist", "capacity", "this week" | 1 · Decide who to focus | `tvt-sales-prospect` (`score.py --rank`) | K-item shortlist + parked list |
| "understand", "research", "dossier on" | 2 · Understand the target | `tvt-intel-pipeline` with `stages=` tiered by job-1 rank (floor items → `deep,customer,fanout,dossier`; parked → `dossier` only) | account dossier |
| "build a POV", "point of view", "business value hypothesis", "BVH" | 3 · Form the POV | `tvt-sales-pov` (Stage 1 curated provocation, or Stage 2 synthesis once unlocked) — input **must** have cleared `tvt-intel-factcheck` first | POV artifact |
| "draft outreach", "reach out to", "make contact" | 4 · Make contact | outreach-draft action (this skill, §"Job 4" below) — **draft only, never sent** | staged draft |
| "prep for <meeting>", "validate", "qualify" | 5 · Validate & qualify | `tvt-sales-pov` validation-tracking (manually-authored `claims.json` → `gate.py` risk-tiered gate → `tvt-gov-attest`) + `tvt-pm-jtbd` | validated/refuted/refined POV claims + MEDDPICC /24 |
| "design", "POC", "proposal", "deck for" | 6 · Design & prove | `tvt-pm-grow` → `tvt-sales-pack`/`tvt-sales-pitch`/`tvt-sales-engagement-proposal`/`tvt-create-deck` | proposal artifact |
| "win", "close", "objection" | 7 · Win | `tvt-sales-pack` → `tvt-intel-flywheel` (capture the case study) | close support |
| "expand" + an already-won account, "mine <account>" | 8 · Expand (loops to job 0, EXPAND) | `tvt-intel-qbr` + `tvt-intel-flywheel` → `tvt-pm-jtbd` | next hypothesis |
| `status` | — | `tvt-sales-prospect` (`kpi.py scorecard`) | portfolio KPI scorecard |
| `pipeline` | — | `tvt-sales-prospect` (`score.py --rank`) | ranked opportunity list, protected floor per motion |

If ambiguous between two jobs, prefer the **earlier** job (more conservative — matches
`g-dev-build`'s routing-logic convention). If genuinely unclear, ask one question rather than
guessing which JTBD is meant.

## Step 2: Fire the Owning Skill

This router never reimplements a fired skill's logic. Concretely:

```
job 1 / `pipeline` / `status`:
  cd ${CLAUDE_PLUGIN_ROOT}/skills/tvt-sales-prospect/scripts
  python3 score.py --rank --opportunities-file <opps.json> --capacity <K> --floor <motion=n,...>
  python3 kpi.py --opportunities-file <kpi_opps.json> --quota-hunt <$> --quota-expand <$>
  # <opps.json> and <kpi_opps.json> are DIFFERENT record shapes (see below) — never reuse one file for both

job 2:
  tvt-intel-pipeline stages=deep,customer,fanout,dossier   (floor/shortlisted accounts)
  tvt-intel-pipeline stages=dossier                        (parked accounts)

job 3 / job 5:
  tvt-sales-pov "<intent>"   (see tvt-sales-pov/SKILL.md — this skill hands off intent + account
  context verbatim; tvt-sales-pov owns Stage 1/2 selection and validation-tracking)

job 6/7/8:
  fire the existing skill named in the table above with the account/opportunity context this
  router already resolved (motion, job-1 rank, job-2 dossier reference).
```

### Opportunity data source

Both `<opps.json>` and `<kpi_opps.json>` are **local JSON files** populated the same way — by hand
or via a CSV export from whatever CRM a rep actually has — but they are **not the same shape**, and
`kpi.py` will fail with a bare `{"error": "'stage'"}` if handed the `score.py`-shaped file. This is
the primary, supported path, not a fallback (design decision: Salesforce MCP wiring is deliberately
deferred, since most sales-team members don't have direct SFDC SSO/MCP access — see docs/ in this
repo).

- `score.py` (`<opps.json>`) fixture:
  `${CLAUDE_PLUGIN_ROOT}/skills/tvt-sales-prospect/scripts/opportunities.example.json`
  (MEDDPICC dimensions, strategic fit, winnability — ranking inputs)
- `kpi.py` (`<kpi_opps.json>`) fixture:
  `${CLAUDE_PLUGIN_ROOT}/skills/tvt-sales-prospect/scripts/kpi_opportunities.example.json`
  (stage, amount, created/close dates — pipeline-health inputs)

If Salesforce MCP is ever wired later, it would only need to produce these same two JSON shapes —
nothing else in this router or in `tvt-sales-prospect` changes. Annotate every KPI/shortlist output
with `"data_source"` naming where the file came from and how stale it is; never fabricate a
live-looking number from an old file.

## Job 4: Outreach-Draft Action (owned here by design)

Fires when intent matches "draft outreach", "reach out to", "make contact". Produces a **draft
only** — this router has no send path and must never acquire one (hard rule: AI drafts,
human sends). The draft:

1. Pulls the POV artifact from `tvt-sales-pov` (job 3) as the anchor — never a blank "checking in".
2. Multi-threads the CEO/CTO/CAIO/CDO/CIO cluster simultaneously (per the buyer-persona note for
   job 4) rather than one contact sequentially — draft one variant per persona, not one generic
   email.
3. Stages the drafts as files/output for your review — does not call any send/email tool.
4. Records nothing to the attest ledger at draft time (only a *sent* outreach is a real-world
   signal worth measuring — the transition KPI is outreach → response, which starts once you
   confirm you sent it, not when the draft was generated).

### Output Gate (mandatory before staging the draft)

Before staging any outreach draft for review: `/tvt-core-eval gate --output <draft>
--criteria ${CLAUDE_PLUGIN_ROOT}/rubrics/outreach.md`. This runs before the human ever sees the
draft — the gate checks quality, not the send decision (there is no send path here).

## Guardrails (recap — full detail in docs/ in this repo)

- **AI drafts, human sends.** Never wire a send/email/message tool into this router.
- **No naked confidence numbers.** Any shortlist/status output must carry the calibration state
  (`uncalibrated` → ordinal band; `calibrated (n=…)` → percent) exactly as `score.py` emits it —
  this router must not reformat or strip that field.
- **CRM PII → `tvt-gov-guard`** before any opportunity data reaches a log, draft, or artifact.
- **No CRM data exfil** — opportunity data stays in-workspace.
- **Staleness, not fabrication**, when the local opportunity/claims file is old (see "Opportunity
  data source" above).

## Build Status

Implemented: intent classification (motion + job), firing table, job-4 outreach-draft action,
data-source annotation. Depends on: `tvt-sales-prospect` (implemented, 60/60 tests passing) and
`tvt-sales-pov` (Stage 1 authoring workflow + job-5 verification gate implemented, 28/28 tests
passing — see its own SKILL.md for what's still open there). Salesforce/Notion MCP integration is
deliberately **not** on the build list (design decision) — this router is designed to run entirely
on local JSON, which is the intended distribution shape for sales-team members who won't have
personal MCP access, not a stopgap. See docs/ in this repo for the full verification checklist
before this router is considered done end-to-end.
