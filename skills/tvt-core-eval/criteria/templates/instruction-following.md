# Instruction-Following Rubric

Use when the prompt contains specific instructions the output must comply with:
format requirements, length limits, content constraints, mandatory inclusions.

## Criterion 1: All hard requirements met (weight: 5)

**What to look for:** Every instruction prefixed with MUST, REQUIRED, "always",
"never", or that is structurally unambiguous, is followed.

**Score 1.0:** All hard requirements satisfied.
**Score 0.5:** One non-critical hard requirement missed (e.g., minor formatting).
**Score 0.0:** Any major hard requirement missed (wrong format, missing required
content, exceeds explicit limit).

**Source:** IFEval (Zhou et al. 2023); LMSYS instruction-following eval.

## Criterion 2: Constraints respected (weight: 4)

**What to look for:** Length limits, language constraints, tone constraints,
exclusion lists ("don't include X") are all honored.

**Score 1.0:** All constraints respected.
**Score 0.5:** One constraint slightly exceeded (e.g., 105 words when limit was 100).
**Score 0.0:** Constraint violated meaningfully (50% over length, used excluded term).

**Source:** IFEval constraint categories.

## Criterion 3: Soft preferences honored (weight: 2)

**What to look for:** Suggested style, "prefer X", "if possible Y" are followed
when reasonable.

**Score 1.0:** Soft preferences clearly addressed.
**Score 0.5:** Some soft preferences ignored without justification.
**Score 0.0:** Most/all soft preferences ignored.

**Source:** common practice in instruction-tuned model evals.

## Criterion 4: No invented requirements (weight: 3)

**What to look for:** The output doesn't add fabricated constraints to itself
("I'll also avoid X" when X wasn't mentioned, padding the response with unrequested
caveats).

**Score 1.0:** Output addresses what was asked, no more.
**Score 0.5:** Minor unrequested additions (acceptable hedges).
**Score 0.0:** Output is dominated by unrequested caveats / digressions.

**Source:** common eval anti-pattern catalog.
