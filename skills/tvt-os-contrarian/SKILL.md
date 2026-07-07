---
name: tvt-os-contrarian
description: 'For a rep just asking "critique this" or "is this good", use tvt-os-metacognition instead — it routes here automatically. The devil''s-advocate / red-team voice that attacks an idea so you see outside your own box. TWO depths: LIGHT (inline, current model, ~5s — the Red-Team-6 lenses, default) and DEEP (multi-model panel, ~20-60s — fans the idea to genuinely DIFFERENT model families wearing different expert hats, then synthesizes where they agree/split/diverge). Ends with an evidence-gated best-option recommendation. Composes model_panel.sh (the keystone fan-out tool). Manual: /tvt-os-contrarian "<idea>" [--deep] [--research]. Invoked by tvt-os-judge in the WARN band and by tvt-os-metacognition as the blind-spot pass.'
version: 1.0.0
author: Tavant
created: '2026-06-21'
tier: A
pack_compat:
- '*'
eval:
  mode: score
  depth: light
layer: self-improvement
expected_impact: high
default_overhead: standard
metadata:
  keystone_script: scripts/model_panel.sh
  providers_registry: scripts/providers.yml
  composes:
  - tvt-core-lookup (research backbone — Exa/WebFetch/Context7)
  - tvt-os-judge (invokes this in WARN band)
  - tvt-os-metacognition (routes here for blind-spot scan)
  changelog:
  - '1.0.0 (2026-06-21): initial ship. Light (Red-Team-6) + Deep (multi-model panel
    via model_panel.sh: Bedrock Nova/Mistral + Gemini + OpenAI + ollama, Claude as
    same-family anchor). Evidence-gated best-option engine. Live-verified Nova+Gemini+Mistral.'
---
# tvt-os-contrarian — Different Minds, Not Just a Louder One

> *"A contrarian on the same model that wrote the answer shares its blind spots.
>  The only real escape from your box is a genuinely different mind.
>  Attack the idea, steelman the opposite, then tell me the best option — with evidence."*

## Why this exists

You generate AI answers all day. The failure mode isn't that they're *wrong* — it's that they're **plausibly right and quietly blinkered**: built on an unexamined assumption, blind to a failure mode, optimized for the obvious option when a better one sat just outside view.

A self-critique pass helps a little, but it's the same model grading its own homework — `tvt-os-judge`'s own docs name **same-family self-preference** as the #1 documented judge bias. The fix isn't a sterner prompt. It's **a different mind**: a model from a different family, trained on different data, wearing a different expert hat, attacking your idea independently.

`tvt-os-contrarian` is that mind — on demand, at two depths:

- **LIGHT** — one fast adversarial pass, current model, inline. The everyday "poke holes in this before I commit." ~5s.
- **DEEP** — a **panel of genuinely different model families** (Amazon Nova, Mistral, Google Gemini, OpenAI, a local model), each in a distinct expert persona, each answering *independently with no cross-contamination*, then a synthesis that separates **consensus risk** (they all flag it → real) from **split opinion** (they disagree → your judgment call) from **lone-wolf objections** (only one saw it → the outside-the-box gold). ~20-60s.

Both depths end with the thing you actually asked for: **the best option, with the evidence behind it** — and an honest tag when the evidence is missing.

---

## When to invoke

### Manual

```
/tvt-os-contrarian "<idea, claim, plan, or path-to-artifact>"        # LIGHT (default)
/tvt-os-contrarian "<idea>" --deep                                   # multi-model panel
/tvt-os-contrarian "<idea>" --deep --research                        # panel + cite sources
/tvt-os-contrarian "<idea>" --best-option "A | B | C"                # decide between options
/tvt-os-contrarian --probe                                           # which models are live?
```

### Automatic (composed by other skills)

- **`tvt-os-judge`** fires this in the **WARN band (composite 0.70–0.85)** only — where adversarial review adds the most value (PASS doesn't need it, BLOCK already has clear remediation). The panel's cross-family models are the judge's same-family-bias fix.
- **`tvt-os-metacognition`** routes here when the task is "pressure-test a new idea" rather than "gate a finished artifact."

### When NOT to use it
- Don't run DEEP on a settled decision you're not reopening — it's a thinking tool, not a ritual.
- Don't make it permanent. (Mason Research, Feb 2026: a *permanently* adversarial role degrades quality — the critic learns to manufacture fault.) The contrarian is invoked, not always-on.

---

## LIGHT mode — the Red-Team-6 (default)

One pass, current model, structured by six lenses. The model adopts a genuine adversary's stance (not a polite reviewer's) and returns **only the sharp parts** — no preamble, no recap of the idea.

The six lenses (run all, surface the ones that bite):

1. **Falsify the core claim.** What single fact, if true, collapses the whole thing? Go look for it.
2. **Steelman the opposite.** Make the *strongest* case for the contrary position — not a strawman. If it's persuasive, say so.
3. **Name the failure mode.** Not "it might not work" — *the specific way it breaks*, who notices first, and when (demo / pilot / scale / 2am).
4. **Hunt disconfirming evidence.** What would a skeptic Google? What base rate argues against this? (How often do projects like this actually succeed?)
5. **Check the base rate / reference class.** Is this idea special, or is it the median member of a class that usually fails? Anchor to the outside view.
6. **Surface the unknown-unknown.** The assumption so baked-in nobody stated it. The question not being asked in the room.
7. **Find the simpler rival.** Is there a materially simpler design/model/framing that meets the *same* requirement? Strip every layer (provenance, independence, governance, extra sources/structure) and ask which ones are load-bearing vs. decorative rigor. If the stripped version still passes the bar, the elaborate version is over-built — name it. (This is the workspace's most frequent correction; `feedback_simplest_framing_wins`.)

**LIGHT output (terse):**

```
⚔️  CONTRARIAN — LIGHT  ·  <one-line restatement of the idea>

Sharpest objections:
  1. <objection> — <why it bites, concrete>
  2. <objection> — ...
  3. <objection> — ...

Strongest opposite case: <the steelman, 1-2 sentences>

Most likely failure mode: <the specific break + when it shows>

What would change my mind: <the evidence that would flip the verdict>

Verdict: PROCEED / PROCEED-WITH-GUARDRAILS / RECONSIDER / KILL
        + the single highest-leverage thing to do about it
```

If a claim hinges on an external fact the model can't verify from training, it tags it `[unverified — run --research]` rather than asserting it.

---

## DEEP mode — the multi-model panel

This is the differentiator. Instead of one model thinking harder, **many different models think independently**, then their outputs are triangulated.

### Step 1 — Fan out (the keystone)

```bash
bash scripts/model_panel.sh --prompt "<the idea>" [--research-context <file>] [--timeout 60]
```

`model_panel.sh` reads `scripts/providers.yml` and calls every reachable provider **in parallel**, each wearing a distinct persona so the objections come from different vantage points, not just different weights:

| Provider | Family | Default hat | Role |
|---|---|---|---|
| Amazon **Nova Pro** (Bedrock) | amazon-nova | Skeptical Operator | "what breaks at 2am" — fast, concrete |
| **Mistral Large 3** (Bedrock) | mistral | First-Principles Contrarian | ignore consensus, reason from base rates |
| **Gemini 2.5 Pro** (API) | google-gemini | Outside-Industry Analogist | the cross-domain analogy, the bubble assumption |
| **GPT-4o** (API) | openai | First-Principles Contrarian | (auto-skips if no `OPENAI_API_KEY`) |
| **Local model** (ollama) | local-llama | Domain Architect | free, private (auto-skips if none pulled) |
| **Claude** | anthropic-claude | Domain Architect | **same-family anchor** — orchestrator fills inline, flagged so synthesis discounts its agreement |

Unreachable providers are **skipped gracefully** with an actionable note (`run: ollama pull …`, `no OPENAI_API_KEY`) — the panel degrades, never breaks. Output is a JSON array: `{id, family, persona, same_family, status, latency_s, text}`.

**The same_family discipline:** Claude is the same family that likely wrote the idea. Its seat is the *domain anchor*, not a diversity vote. In synthesis, agreement *with* the Claude anchor counts for less than agreement *among the cross-family models* — that's the explicit defense against grading your own homework.

### Step 2 — Synthesize (triangulate the panel)

The orchestrator reads the JSON and produces the only output that matters:

```
⚔️  CONTRARIAN — DEEP PANEL  ·  <idea>
    Panel: <N live models across M families>  (skipped: <list>)

🔴 CONSENSUS RISK  (≥2 cross-family models independently flagged — treat as real)
   • <risk> — flagged by: Nova, Mistral, Gemini

🟡 SPLIT  (models disagree — this is YOUR judgment call, here's the spread)
   • <issue>: Nova says X / Gemini says Y — the disagreement is about <root assumption>

🟢 LONE-WOLF  (only one model saw it — the outside-the-box angle, worth a look)
   • <objection> — Gemini only: "<the analogy / unusual frame>"

Strongest steelman of the opposite (best across panel): <...>

Cross-family confidence: <HIGH if cross-family models converge / LOW if they scatter>
   (Claude anchor agreement noted but discounted — same family as the writer.)
```

**Why this structure beats "average the critiques":** the *agreement pattern* is the signal. When three different families independently flag the same risk, that's not noise — it's robust. When they scatter, the idea lives in genuinely uncertain territory and *you* must decide, not the models. When one model alone surfaces a frame the others missed, that's the value of diversity made visible.

**Variance rule (borrowed from tvt-os-judge):** if the cross-family models *disagree on the verdict itself* (some say proceed, some say kill), escalate to "your call" explicitly — high panel variance = genuine uncertainty, not a thing to average away.

---

## Best-option engine (evidence-gated)

Your explicit ask: not just "what's wrong" but **"what's the best option, the best practice."** Both modes can end here; DEEP always does when `--best-option` or multiple candidates are present.

1. **Enumerate candidates** (from the idea, or the `--best-option "A | B | C"` list).
2. **Score each on 5 axes** (0–2 each): evidence strength · reversibility (can we undo it cheaply?) · cost/effort · failure blast-radius · flywheel-fit (does it compound into reusable Tavant IP? — per the director north-star).
3. **Research-gate the evidence axis.** With `--research`, call `tvt-core-lookup` / Exa→WebFetch / Context7 (for technical/library questions) to ground "best practice" claims in a source. **A "best option" assertion without a citation is tagged `[unverified]`** — never stated as fact. (Memory: Exa credits may be exhausted → WebFetch is the reliable fallback.)
4. **Recommend ONE**, name the **runner-up**, and state the **trigger that flips the choice** ("go with B instead if latency budget drops below X").

```
🎯 BEST OPTION: <choice>
   Why: <2-3 evidence-backed reasons, each with [source] or [inferred]>
   Runner-up: <choice> — <when you'd pick it instead>
   Flip trigger: <the condition that changes the answer>
   Confidence: HIGH / MEDIUM / LOW  ·  Evidence: [cited] / [partially cited] / [unverified]
```

---

## Research integration (best-practice grounding)

`--research` turns the contrarian from "reasons from training" to "reasons from current evidence." Order of preference:

1. **Context7** — for any library / framework / SDK / API question ("is X still the best practice"). Current docs beat training memory.
2. **Exa** (`web_search_exa`) — semantic web search for best-practice / comparison / "how do others solve this." *(Note: credits exhausted 2026-06-06 per workspace memory — falls back to #3.)*
3. **WebFetch** — the reliable fallback; fetch named sources and extract.
4. **Tavily** — not currently connected as an MCP in this workspace; if wired later, slots in alongside Exa.

The contrarian cites what it finds inline (`[source: <url/lib>]`) and is explicit when it *couldn't* verify — an honest `[unverified]` is worth more than a confident hallucination. (Memory: source-attribution itself can be hallucinated — only claim a source the tool actually returned.)

---

## Composition

- **`tvt-core-lookup`** — the research backbone for `--research`. The contrarian doesn't reimplement search; it calls lookup.
- **`tvt-os-judge`** — invokes this in the WARN band; the panel result is appended to the judge record as `adversarial_review`. The cross-family models are the judge's same-family-bias countermeasure.
- **`tvt-os-metacognition`** — the orchestrator that decides *whether* you need the judge (artifact quality) or the contrarian (idea blind-spots) or both, and picks LIGHT vs DEEP by stakes.
- **`tvt-grill-me`** — when you want to *argue back* interactively rather than receive a verdict, that's the right tool; the contrarian is one-shot.

---

## Anti-patterns this skill guards against (and its own)

1. **Same-family echo** — Claude critiquing Claude. Defended by the cross-family panel + same_family discounting.
2. **Strawmanning** — the steelman lens is mandatory; a weak opposite case is itself a finding ("I couldn't build a strong opposite → maybe the idea is solid").
3. **Vague doom** ("it might not scale") — every objection must name the *specific* break + when it shows.
4. **Confident unverified "best practice"** — the `[unverified]` tag is mandatory without a cited source.
5. **Permanent adversary** (its own worst failure) — invoked, never always-on; LIGHT is the default so DEEP stays meaningful.
6. **Averaging the panel** — the value is the *agreement pattern* (consensus / split / lone-wolf), not the mean.
7. **Over-built rigor mistaken for thoroughness** — the "simpler rival" lens (#7) exists because elaborate provenance/governance/independence structure often reads as rigor but is decorative; always test whether the stripped version still meets the bar.

---

## Setup notes (to widen the panel)

The panel works *now* with Bedrock (Nova, Mistral) + Gemini. To add more different minds:

```bash
# Local model (free, private, more family diversity):
ollama pull llama3.1:8b        # then it auto-joins the panel

# OpenAI (GPT-4o joins automatically once the key is set):
export OPENAI_API_KEY=sk-...

# Check what's live any time:
bash scripts/model_panel.sh --probe
```

Edit `scripts/providers.yml` to enable/disable providers, swap models, or reassign personas.

---

## Sources / lineage

- `tvt-os-judge` SKILL.md — same-family self-preference as #1 bias; WARN-band composition contract; variance-escalation rule.
- Panickssery (2024) + Mason Research "Same model, same blind spots" (Feb 2026) — same-family bias; don't make the critic permanent.
- DEBATE / multi-agent adversarial patterns (Kim et al., ACL Findings 2024 → 2026) — independent panel beats single critic.
- Workspace memory: Exa credits exhausted (2026-06-06) → WebFetch fallback; source-attribution hallucination guard; eval-first philosophy.

> *"Different minds, not a louder one. Attack it, steelman it, then give me the best option — with the receipts."*
