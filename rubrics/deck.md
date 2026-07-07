# Deck / Slide Artifact Rubric (PPTX, explainers, visual documents)

Gate rubric for slide decks and designed documents (tvt-create-deck, tvt-create-pptx,
tvt-create-explainer, tvt-create-design outputs). Criteria seeded from the visual-DNA
and content checklists those skills already carried, plus tvt-create-explainer's
hard-gate items.

## Criterion 1: Headlines are conclusions (weight: 5)

**What to look for:** Slide headlines/section headings state the takeaway, not the
topic. The whole argument is readable from headings and captions alone.

**Score 1.0:** Every headline is a conclusion; skimming headings alone conveys the
full thesis.
**Score 0.5:** Mixed — some topic labels ("Our Approach") where conclusions belong.
**Score 0.0:** Table-of-contents-style headings throughout.

## Criterion 2: One idea per unit, data with meaning (weight: 4)

**What to look for:** One idea per slide/section. Stats carry context (what the
number means, not just the number). No orphaned data — every table/chart is paired
with its insight.

**Score 1.0:** Each unit is one idea; every stat interpreted.
**Score 0.5:** Occasional double-stuffed slides or bare numbers.
**Score 0.0:** Dense multi-idea slides; data dumps without narrative.

## Criterion 3: Brand and template integrity (weight: 4)

**What to look for:** Built on the bundled Tavant template — `tavant-template.pptx`,
found in the plugin's `assets/` directory (or bundled inside the skill on a zip
install); the judge checks the *artifact*, it does not need the template file itself.
Logo and confidentiality footer inherited; orange as accent (bars, not floods); dark
red only for high-emphasis; safe content zone respected (no text under the
footer/logo).

**Score 1.0:** Template layouts used; color rules and safe zone respected.
**Score 0.5:** Right template, but color misuse or content in the footer zone.
**Score 0.0:** Off-template build or third-party branding leaking through.

## Criterion 4: Placeholder and artifact hygiene (weight: 4)

**What to look for:** Zero leftover placeholder text ("Click to add text", "XXXX",
lorem ipsum); no HTML entity codes rendered as literals; figure labels short enough
not to collide (2-5 words for seam/overlap labels); no broken diagram syntax.

**Score 1.0:** Rendered output verified clean (screenshot/pdftoppm pass done for
rendered formats).
**Score 0.5:** Source looks clean but rendered verification was skipped.
**Score 0.0:** Placeholder text or rendering artifacts present.

## Criterion 5: Visual hierarchy and readability (weight: 3)

**What to look for:** 5-second test per slide — the point lands at a glance; 3-level
hierarchy (hero, support, detail); ≥15% whitespace; body text left-aligned and ≥8.5pt;
adjacent slides don't repeat the identical layout 3+ times.

**Score 1.0:** Passes the 5-second test throughout.
**Score 0.5:** A few dense or flat slides.
**Score 0.0:** Wall-of-text slides; hierarchy absent.

## Criterion 6: Commercial-model discipline (weight: 3)

**What to look for:** Same hard gate as client-facing docs: platform framed as
bundled-with-services (never sold/licensed standalone), no pricing on any slide
(speaker notes only), CTA is a conversation.

**Score 1.0:** All compatible; pricing absent from visible content.
**Score 0.5:** Ambiguous standalone-product phrasing.
**Score 0.0:** License/buy framing or visible pricing.

## Gate threshold

Weighted score ≥ 0.85 to pass. On FAIL: remediate once, re-gate; still failing →
surface to the user with the eval record. Never ship silently.
