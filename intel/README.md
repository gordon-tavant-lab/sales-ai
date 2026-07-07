# Intel inputs — customer, vertical, and competition research

`tvt-sales-prospect` and `tvt-sales-pov` don't do research themselves — they consume it. A
skill-coverage audit (2026-07-02) confirmed all nine `tvt-intel-*` skills are wired into the spec, and
this doc is where a reader sees exactly which one answers which question, before it hits the
scorer or the POV synthesis step.

| Question | Answers with | Depth | Feeds |
|---|---|---|---|
| **Customer** — who is this account, structurally? | `tvt-intel-customer` (top-ranked accounts only, spec §5 tiering) or `tvt-intel-dossier` (everyone else) | 5-step: financial structure, platform mapping, insider knowledge, market impact, case-study grounding | `strategic_fit`, `deal_value` inputs to `score.py`; POV account research |
| **Vertical** — what does the industry itself look like? | `tvt-intel-pipeline`'s `industry` param (`mortgage`\|`fintech`\|`auto`\|`insurance`\|`banking`\|`general`) — not a separate skill, an input to the existing research chain | Targets industry-specific searches inside `deep`/`customer`/`dossier` stages | Sharpens `tvt-intel-flywheel` cross-client pattern matching for the POV |
| **Competition** — who else is in the deal? | `tvt-intel-fanout` — scans research/transcripts for named entities, spawns parallel research per entity | Mini-intel per competitor/vendor named | MEDDPICC **Competition** dimension (0-3, "unknown → 1-2 named → all 3 categories") |
| **Is any of this actually true?** | `tvt-intel-factcheck` — **mandatory gate**, not optional | Extracts every claim, verifies against external sources | Blocks unverified research from reaching `tvt-sales-pov` synthesis (spec §3a, §7) |

## The chain, in order

```
tvt-intel-pipeline (industry=<vertical>)
  ├─ tvt-intel-deep         base research cycle
  ├─ tvt-intel-customer     [only if top-ranked, spec §5]  OR  tvt-intel-dossier [everyone else]
  ├─ tvt-intel-fanout       named competitors/vendors → MEDDPICC Competition
  ├─ tvt-intel-qbr          [expand motion only] account whitespace
  └─ tvt-intel-factcheck    MANDATORY — verifies every extracted claim
        │
        ▼ (only fact-checked research passes)
  tvt-sales-pov synthesis  ← also tvt-intel-flywheel (cross-client patterns) + tvt-pm-jtbd (scored outcomes)
```

## Enriched example

`../skills/tvt-sales-prospect/scripts/opportunities.example.json` has the bare fields the scorer needs.
A record with intel attached looks like:

```json
{
  "id": "acct-radian", "motion": "expand",
  "meddpicc": [3,3,2,2,2,3,2,2],
  "intel": {
    "customer_research": "tvt-intel-customer, run 2026-06-15, factchecked",
    "vertical": "mortgage",
    "competitors_named": ["Incumbent MI Provider A", "Incumbent MI Provider B"],
    "factcheck_status": "cleared"
  }
}
```

`meddpicc[7]` (Competition) should reflect `len(competitors_named)` per the MEDDPICC scoring rubric
— 0-3 based on named-competitor coverage, not asserted by the LLM without the `tvt-intel-fanout` trace
behind it.

## Where the research skills live

The nine `tvt-intel-*` skills are vendored in this repo (2026-07-04, spec 007 FR-001) — they install
with the same `/plugin install` as everything else. This directory documents the contract between
them and the scorer/POV steps; the research logic itself lives in each skill's own directory
(anti-scope-creep contract, spec §9: this doc does not duplicate it).
