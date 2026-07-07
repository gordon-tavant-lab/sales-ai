# Client-Facing Document Rubric (proposals, presales packs, pitch briefs)

Gate rubric for any prose artifact a client will read: engagement proposals, presales
packs, pitch content briefs. Used by the mandatory Output Gate
(`/tvt-core-eval gate --criteria ${CLAUDE_PLUGIN_ROOT}/rubrics/client-facing-doc.md`).
Criteria seeded from the quality checklists these skills already carried — same content,
moved from same-context self-review to an independent judged gate.

## Criterion 1: Client-specific, not generic (weight: 5)

**What to look for:** The opening uses the client's own language, framing, or named
pain points. Their numbers appear where impact is claimed. An industry-matched case
study or proof point, not a generic one.

**Score 1.0:** A reader at the client would recognize themselves in the first
paragraph; impact math uses their actuals or clearly-labeled estimates.
**Score 0.5:** Client name is present but the substance is template-generic; numbers
are ours, not theirs.
**Score 0.0:** Find-and-replace personalization; no client-specific pain, number, or
case study anywhere.

## Criterion 2: Every claim carries proof (weight: 5)

**What to look for:** Opportunity/benefit assertions are backed by concrete proof
points with stats; no unverifiable superlatives. Nothing contradicts the fact-checked
research the doc was built from.

**Score 1.0:** Each major claim has a specific proof point (stat, named engagement
pattern, verifiable capability); zero unsupported superlatives.
**Score 0.5:** Most claims backed; one or two decorative assertions slipped in.
**Score 0.0:** Confidence without evidence — "market-leading", "proven at scale" with
nothing behind it.

## Criterion 3: Commercial-model discipline (weight: 4)

**What to look for:** If the Tavant Platform is the subject: it is never sold/licensed
standalone — always bundled with services. Grep-check `buy|bought|sold|sell|licens`
hits must all be compatible with "the accelerator that comes with the engagement". No
pricing visible in body content. CTA references a session/workshop, never an SOW.

**Score 1.0:** All hits compatible; no pricing on the page; CTA is a conversation.
**Score 0.5:** Ambiguous phrasing that could be read as a standalone product sale.
**Score 0.0:** Explicit "license/buy the platform" framing, visible pricing, or an
SOW-shaped close.

## Criterion 4: Structure serves the reader (weight: 3)

**What to look for:** Product/accelerator names appear in section bodies, not headers
or the opening (lead with their problem, not our product). Prose sections are prose —
no bullet-list dumps where narrative was asked for. Requested format respected
(e.g. 1hr vs 1-day vs multi-day agenda shapes).

**Score 1.0:** Problem-first structure throughout; format matches the request.
**Score 0.5:** One or two product-first sections or format drift.
**Score 0.0:** Product-catalog structure; the client's problem is decoration.

## Criterion 5: Honest edges (weight: 3)

**What to look for:** Trade-offs, assumptions, and prerequisites are stated, not
hidden. Anything the team must confirm before the client sees it is flagged for the
human reviewer.

**Score 1.0:** Assumptions and open items are explicit; the human knows exactly what
to verify before sending.
**Score 0.5:** Clean-looking doc with silently embedded assumptions.
**Score 0.0:** Known unknowns presented as settled facts.

## Gate threshold

Weighted score ≥ 0.85 to pass. On FAIL: remediate once against the per-criterion
feedback, re-gate; still failing → surface to the user with the eval record. Never
ship silently.
