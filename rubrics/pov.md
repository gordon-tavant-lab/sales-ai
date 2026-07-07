# POV / Business Value Hypothesis Rubric (tvt-sales-pov synthesis output)

Gate rubric for the POV document itself — the input side is already gated (research
must clear tvt-intel-factcheck before synthesis; claims flow through gate.py). This
rubric closes the gap the 2026-07-05 review found: the inputs were gated, the
artifact never was. The crispness criterion is spec 006 §3's own KPI, moved into an
enforced gate.

## Criterion 1: POV crispness (weight: 5)

**What to look for:** The spec's own three-part definition, all present and specific:
(1) a NAMED problem we see at this client, (2) QUANTIFIED impact, (3) a PROPOSED
change. "Problem we see → impact → change we propose" readable as one tight arc.

**Score 1.0:** All three parts present, specific, and quantified where quantifiable.
**Score 0.5:** Three parts present but one is vague (unnamed problem owner,
unquantified impact, or change described only as "leverage AI").
**Score 0.0:** Generic thought-leadership; no client-specific problem or no
proposed change.

## Criterion 2: Grounded in gated inputs (weight: 5)

**What to look for:** Every factual claim traces to fact-checked research or an
attested/confirmed claim from the validation ledger. Nothing appears that bypassed
those gates.

**Score 1.0:** All claims trace to gated inputs; provenance visible.
**Score 0.5:** Mostly traceable; a few assertions of unclear origin.
**Score 0.0:** New unverified facts introduced at synthesis time.

## Criterion 3: Sensemaking, not another insight (weight: 4)

**What to look for:** Per the Challenger-saturation caveat (spec §3): the POV
synthesizes and adjudicates what the buyer already knows/has researched — it
organizes their world, it doesn't perform "provocative insight" theater.

**Score 1.0:** Anchored in the buyer's existing context; adjudicates named
alternatives they're weighing.
**Score 0.5:** Solid content but framed as revelation rather than sensemaking.
**Score 0.0:** Generic provocation disconnected from this buyer's situation.

## Criterion 4: Testable, board-level framing (weight: 3)

**What to look for:** The hypothesis is falsifiable — it names what evidence would
validate or refute it (feeds job-5 validation tracking). Framed at business-outcome
level, not feature level.

**Score 1.0:** Explicit validate/refute conditions; outcome-level language.
**Score 0.5:** Directionally testable but conditions implicit.
**Score 0.0:** Unfalsifiable vision statement.

## Criterion 5: Honest confidence (weight: 3)

**What to look for:** Confidence presented per the anchoring rules — ordinal bands
while uncalibrated, never a naked precision number; inferences flagged; what we don't
yet know stated.

**Score 1.0:** Calibration state visible; unknowns named.
**Score 0.5:** Hedged prose but precision-implying numbers slipped in.
**Score 0.0:** False-precision confidence anywhere.

## Gate threshold

Weighted score ≥ 0.85 to pass. On FAIL: remediate once, re-gate; still failing →
surface to the user with the eval record. Never ship silently.
