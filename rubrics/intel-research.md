# Intel / Research Artifact Rubric (dossiers, deep research, fanout, QBR, flywheel)

Gate rubric for research artifacts from the tvt-intel-* family. Criteria seeded from
tvt-intel-dossier's Phase-4 quality gate and tvt-intel-customer's per-step gates.
NOTE: the Output Gate for intel skills has a mandatory step BEFORE this rubric —
run `tvt-intel-factcheck` on the output. This rubric assumes factcheck ran; criterion 2
verifies the artifact carries the evidence of it.

## Criterion 1: Sourced claims (weight: 5)

**What to look for:** Every factual claim is linked to a source (URL, document, CRM
record, named meeting). Claims tagged `[confirmed]` / `[reported]` / `[inferred]`
where the skill's format calls for it.

**Score 1.0:** All major claims traceable; inference clearly separated from fact.
**Score 0.5:** Mostly sourced; a few load-bearing claims float unattributed.
**Score 0.0:** Narrative asserts facts with no trail.

## Criterion 2: Fact-check gate evidence (weight: 5)

**What to look for:** The artifact shows the mandatory tvt-intel-factcheck pass
happened: a factcheck status/verdict section, or per-claim verification marks.
Research that skipped the gate must not read as verified.

**Score 1.0:** Factcheck evidence present; failed/unverifiable claims visibly
downgraded or removed.
**Score 0.5:** Gate claimed but no per-claim evidence visible.
**Score 0.0:** No factcheck trace — unverified research dressed as verified.

## Criterion 3: 10-second insight test (weight: 4)

**What to look for:** Each chapter/section's first paragraph conveys the key insight.
An executive skimming first paragraphs only gets the true story.

**Score 1.0:** Every section front-loads its insight.
**Score 0.5:** Some sections bury the lede.
**Score 0.0:** Chronological data recitation; insights implicit or absent.

## Criterion 4: Actionability (weight: 4)

**What to look for:** The reader knows what to DO after reading — next actions,
talking points, or the decision the research informs. For QBR/whitespace artifacts:
named expansion opportunities, not just account history.

**Score 1.0:** Concrete, prioritized actions tied to findings.
**Score 0.5:** Actions present but generic ("engage stakeholders").
**Score 0.0:** Pure information; no path from insight to action.

## Criterion 5: Freshness honesty (weight: 3)

**What to look for:** Anything older than ~3 months is flagged as potentially stale;
data-as-of dates present; no undated market claims presented as current.

**Score 1.0:** Ages visible; stale items flagged.
**Score 0.5:** Dates on some sources; staleness unexamined.
**Score 0.0:** Old data presented as current state.

## Gate threshold

Weighted score ≥ 0.85 to pass. On FAIL: remediate once, re-gate; still failing →
surface to the user with the eval record. Never ship silently.
