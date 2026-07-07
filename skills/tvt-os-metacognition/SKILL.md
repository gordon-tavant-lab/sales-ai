---
name: tvt-os-metacognition
description: 'The rep-facing entry point for "critique my thing" — use this for "review this", "is this any good", "critique my deck/plan/pitch", "sanity check this idea", or "what am I missing". The thinking-about-thinking front door. Two faces. PROSPECTIVE (default): you hand it a new idea/answer/plan and it routes to the right cognitive tool — tvt-os-contrarian for blind-spot/red-team (idea quality) and/or tvt-os-judge for drift/evidence gating (artifact quality) — picking LIGHT vs DEEP by stakes, then returns ONE decision-ready verdict. RETROSPECTIVE: analyzes recent reasoning for patterns, blind spots, drift. Manual: /tvt-os-metacognition "<idea>" [--deep] or /tvt-os-metacognition --retro. The orchestrator over judge + contrarian — invoke this directly rather than judge/contrarian/tvt-core-eval unless you specifically need one of those tools'' own explicit invocation syntax.'
version: 1.0.0
author: Tavant
created: '2026-06-21'
tier: A
pack_compat:
- '*'
eval:
  mode: score
  depth: standard
layer: self-improvement
expected_impact: high
default_overhead: light
metadata:
  routes_to:
  - tvt-os-contrarian (blind-spot / red-team / best-option)
  - tvt-os-judge (drift / evidence gate on artifacts)
  changelog:
  - '1.0.0 (2026-06-21): initial ship. Prospective router (idea→contrarian, artifact→judge,
    stakes→light/deep) + retained retrospective reasoning-quality face.'
---
# tvt-os-metacognition — Think About Your Thinking

> *"Before you commit an answer: is it the right answer (judge), and what am I not seeing (contrarian)?
>  This skill decides which question matters here, picks the depth, and gives you one verdict."*

## Why this exists

You have two cognitive guardrails:
- **`tvt-os-judge`** — gates *finished artifacts* for drift + evidence (is this still faithful to intent? are the claims grounded? block-on-fail).
- **`tvt-os-contrarian`** — red-teams *ideas* for blind spots, then recommends the best option (what am I not seeing? what's the strongest opposite?).

The mistake is reaching for the wrong one — running a quality gate on a half-formed idea, or red-teaming a finished spec that just needs an evidence check. `tvt-os-metacognition` is the **front door**: tell it what you've got, it routes to the right tool at the right depth, and returns a single decision-ready answer instead of two raw tool dumps.

It's the "lightweight + deep" dial you asked for, made into a router.

---

## PROSPECTIVE mode (default) — route a new idea/answer

```
/tvt-os-metacognition "<idea, answer, plan, or path-to-artifact>"     # auto-route, LIGHT
/tvt-os-metacognition "<idea>" --deep                                 # force DEEP (multi-model panel)
/tvt-os-metacognition "<idea>" --research                             # ground best-practice claims
/tvt-os-metacognition <path/to/spec.md>                               # artifact → judge-led route
```

### The routing decision (how it picks)

```
            ┌─ Is the input a FINISHED ARTIFACT on a load-bearing path?
            │   (spec/plan/ADR/intel/code — see tvt-os-judge include globs)
            │
   YES ─────┴──▶  JUDGE-LED:  run tvt-os-judge (drift + evidence + dep-liveness).
                              If verdict lands in WARN band → also run tvt-os-contrarian
                              (judge already composes this). Return judge verdict + any
                              adversarial findings.
            │
   NO  ─────┬──▶  CONTRARIAN-LED:  it's an idea/answer, not a gated artifact.
            │                      Run tvt-os-contrarian (blind-spot + best-option).
            │
            └─ BOTH when: a high-stakes idea is ALSO about to become an artifact
               (e.g. "here's my architecture decision, I'm about to write the ADR")
               → contrarian first (shape the idea), then judge the resulting artifact.
```

### The depth decision (LIGHT vs DEEP)

Pick DEEP automatically when **any** of:
- the user said `--deep`, "really pressure-test", "outside the box", "all angles";
- the decision is **hard to reverse** (architecture, vendor choice, client-facing commitment, anything capital- or constitution-touching);
- a first LIGHT pass came back **genuinely uncertain** (the contrarian's verdict was RECONSIDER, or the steelman was as strong as the original).

Otherwise LIGHT — fast, current model, inline. *Don't burn a 5-model panel on a low-stakes call.* (Stakes-proportionate overhead is the whole point of having two depths.)

### Output — ONE verdict, not two dumps

```
🧠 METACOGNITION  ·  <one-line restatement>
    Routed to: <contrarian-led | judge-led | both>  ·  Depth: <light | deep>

<the routed tool's result, surfaced — contrarian objections / judge verdict>

──────────────────────────────────────────
BOTTOM LINE: <PROCEED / PROCEED-WITH-GUARDRAILS / RECONSIDER / KILL  — or  PASS/WARN/BLOCK for artifacts>
Highest-leverage next move: <the single thing to do>
Confidence: <HIGH/MED/LOW>  ·  Evidence: <[cited]/[unverified]>
```

The point: you get a **decision**, with the routing reasoning visible (so you can override it), not a pile of raw critique to re-synthesize yourself.

---

## RETROSPECTIVE mode — analyze how we reasoned

`/tvt-os-metacognition --retro` — the original face. Looks back over recent workspace activity (whatever activity log or session history your own project keeps) and surfaces reasoning quality, not artifact quality.

### Process
1. **Pattern recognition** — what approaches kept working? (preserve these)
2. **Blind-spot detection** — what was missed? what signals ignored?
3. **Repetition analysis** — what got redone unnecessarily, and why?
4. **Quality variance** — which outputs were sharp vs generic filler?
5. **Drift detection** — did any skill produce output that didn't match its SKILL.md intent?

### Metacognitive questions (the workspace's standing principles)
- Was **deterministic-first** applied, or did we default to LLM for everything?
- Was the **evidence chain** maintained, or were conclusions unsupported?
- Was **distillation discipline** followed, or did docs grow without compression?
- Was **external audit** applied, or did we self-certify?
- Were **drift scores measured**, or was "it works" accepted as sufficient?

### Output
```markdown
## Metacognition (retro): [date]
### Confirmed Good Patterns
- [pattern]: [evidence it worked]
### Blind Spots Identified
- [blind spot]: [what was missed + why]
### Repetitions (Waste)
- [repeated action]: [count] [root cause]
### Quality Variance
- Sharpest: [file] — why · Weakest: [file] — what went wrong
### Drift Detected
- [skill/process]: [how it drifted from intent]
```

### Quality gate (retro)
- Every blind spot must cite specific evidence (not speculation).
- Must identify ≥1 confirmed good pattern worth preserving.
- Must identify ≥1 drift between skill intent and actual output.

---

## Composition

- **`tvt-os-contrarian`** — the blind-spot / best-option engine (LIGHT inline or DEEP multi-model panel). Metacognition routes ideas here.
- **`tvt-os-judge`** — the drift + evidence gate. Metacognition routes finished artifacts here.
- **`tvt-grill-me`** — when the user wants to *argue* with a verdict interactively, hand off here.

## Anti-patterns it guards against
1. **Wrong-tool reaching** — judging an unformed idea, or red-teaming a spec that needs an evidence check. The router fixes this.
2. **Depth waste** — a 5-model panel on a trivial call (over-spend) or a one-line self-check on an irreversible decision (under-spend). Stakes drive depth.
3. **Two raw dumps** — returning tool output without a synthesized decision. Metacognition always lands on ONE bottom line.
4. **Self-certification** — routing high-stakes ideas to a same-family self-check instead of the cross-family panel.

> *"Right answer? Ask the judge. What am I missing? Ask the contrarian. Which one matters now — and how deep? That's this skill."*
