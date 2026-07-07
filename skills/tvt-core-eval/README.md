# Universal Measurement — System Documentation

A human-readable guide to the eval system that runs across every AI process in
this Claude environment. If you want the machine-readable spec, see
[`SKILL.md`](./SKILL.md).

---

## TL;DR

Every AI output produced in this environment — every skill, agent, loop,
pipeline result — is automatically scored against task-appropriate criteria
before being declared done. High-stakes outputs (client-facing, capital-touching,
production-deploying) are gated and will refuse to proceed if score is
insufficient. The cost is roughly **$1.70/day** for full coverage.

This is not opt-in. It's the default behavior, mandated by Constitution
Principle VI: Universal Measurement.

---

## Why this exists

> "To trust AI is to be able to evaluate it in detail and hold it accountable
> to measures."

Without measurement, every AI output is a hope. Most failures in AI systems
aren't catastrophic — they're silent quality decay that nobody notices until
someone in the field sees a bad output. The fix is to make every AI process
measurable, log every score, detect regression, and gate consequential actions
behind score thresholds.

This system codifies that principle into infrastructure rather than relying on
discipline.

---

## The architecture (2 required layers + 2 optional override layers)

```
┌─────────────────────────────────────────────────────────────┐
│  1. tvt-core-eval skill (this package)                       │
│     The engine — 7 modes, 3 depth tiers, eval records.       │
│     Ships with built-in process-type defaults — works out    │
│     of the box, no config file needed.                       │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  2. Per-skill frontmatter (declared on every shipped skill)  │
│     eval_exempt | eval_mode | eval_depth declared inline     │
└─────────────────────────────────────────────────────────────┘

Optional, only if present in YOUR project (neither ships with this package):
┌─────────────────────────────────────────────────────────────┐
│  3. eval-policy.yml (optional)   ~/.claude/eval-policy.yml   │
│     Overrides the built-in process-type defaults, floors,    │
│     cost caps, for your own project                          │
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│  4. A project constitution (optional)                        │
│     If your own project has adopted a numbered-principle      │
│     constitution, wire this skill's mandate to whichever      │
│     principle covers measurement                              │
└─────────────────────────────────────────────────────────────┘
```

The two required layers work standalone: the skill ships with sane built-in
defaults, and every skill in this package already declares its own
`eval_exempt`/`eval_mode`/`eval_depth`. The two optional layers only apply if
your own project happens to have that infrastructure.

---

## What changed automatically (before / after)

| Scenario | Before | After |
|---|---|---|
| `/g-ops-morning` runs autonomously | Daily intel published unconditionally | Gated at standard depth — won't publish if score < 0.85 |
| Trading system fires a signal via `tvt-core-mcts` | Signal passes through to execution | Mandatory `gate deep` — refuses to proceed on insufficient score |
| `/tvt-sales-pack` produces a presales deck | Hand-checked or shipped on faith | Auto-gated before declaring client-ready |
| `/g-create-pdf` merges PDFs | Same as before | Same as before — exempt (no AI output) |
| `/g-ai-loop` iterates a task | Pass/fail on completion | Per-iteration score + run summary with pass@k, regressions, cost-to-pass |
| Any new skill you build | No eval | Inherits global default `score` at `light` depth automatically |

---

## The mental model

Every skill falls into one of five buckets, declared in its frontmatter:

| Bucket | Count | Frontmatter | Behavior |
|---|---|---|---|
| **Primitive** | 1 | (special) | The eval engine itself — `tvt-core-eval`. Cannot eval itself. |
| **Composes eval** | 1 | `g-ai-loop` | Calls eval inside its own logic (per-iteration scoring) |
| **Gate deep** | 1 | `eval_mode: gate, eval_depth: deep` | Capital floor — `tvt-core-mcts`. Refuses to proceed on fail. |
| **Gate standard** | 11 | `eval_mode: gate, eval_depth: standard` | High-stakes — ops/sales/intel/brand. Refuses to publish on fail. |
| **Exempt** | 12 | `eval_exempt: true` | Deterministic — file ops, infra, guides. No eval needed. |
| **Default inherit** | 9 | (none) | Medium-stakes — light score by default. |

The model is: **everyone evals unless explicitly exempt, and the higher the stakes the deeper the eval**.

---

## How it works in practice (4 concrete scenarios)

### 1. The morning intel run

You run `/g-ops-morning`. It autonomously reads inbox, calendar, Teams, extracts
signals, and prepares to write a daily intel file.

Before publishing, it invokes:
```
/tvt-core-eval gate \
  --output drafts/daily_2026-05-02.md \
  --criteria "Surface high-priority signals, identify portfolio impacts, ..." \
  --gate-threshold 0.85 \
  --depth standard
```

If score ≥ 0.85: file publishes, you see "PASS (score 0.91)" in the report.
If score < 0.85: publishing halts, you see "GATE FAIL (score 0.72) — missing
portfolio impact analysis on 3 of 5 signals". You decide whether to iterate or
ship anyway.

### 2. The trading signal

The trading system's MCTS engine produces a candidate trade. Before passing to
execution:

```
/tvt-core-eval gate \
  --output signal.json \
  --criteria "..." \
  --gate-threshold 0.90 \
  --depth deep   ← mandatory floor for capital-touching paths
```

`deep` runs 3 judge calls and takes consensus. If any disagree below threshold,
gate fails, signal does not pass to Alpaca/Binance execution. Capital protected
by infrastructure, not vigilance.

### 3. A creative skill (medium stakes)

You invoke `/tvt-create-pptx` to generate a deck. The skill produces the file,
then automatically:

```
/tvt-core-eval score \
  --output deck.pptx-spec.md \
  --criteria "..." \
  --depth light
```

Score reported: "PASS (score 0.88)". Deck delivered. Total added cost: $0.02.

### 4. An exempt skill

You run `/g-create-pdf merge a.pdf b.pdf -o out.pdf`. The skill's frontmatter
has `eval_exempt: true`. Eval is skipped silently. No cost, no delay.

---

## Cost & limits

Default depth tiers:

| Depth | Cost | Time | When |
|---|---|---|---|
| `light` | ~$0.02 | ~5s | Default for all skills |
| `standard` | ~$0.05 | ~10s | High-stakes (gates) |
| `deep` | ~$0.20 | ~30s | Capital floor / production deploy |

Expected daily spend at typical usage:

- 30 light evals = $0.60
- 10 standard gates = $0.50
- 1–3 deep gates = $0.60
- **~$1.70/day** for universal measurement coverage

Hard limits in `eval-policy.yml`:
- Warn if a single eval exceeds $0.50
- Abort if a single eval exceeds $2.00

Override on a per-call basis with `--depth light` if you want to drop a
high-stakes call to cheap mode (not recommended; mandatory floors override).

---

## File map

| File | Purpose | Edit when |
|---|---|---|
| `SKILL.md` (this skill's own dir) | The engine spec (machine-readable) | Adding new modes or capabilities |
| `README.md` (this file) | Human docs | When the system changes meaningfully |
| each skill's own `SKILL.md` frontmatter | Per-skill eval contract | Changing a skill's eval contract |
| `~/.claude/eval-policy.yml` (optional, your project) | Process-type default overrides, floors, cost caps | Tuning depth/mode policy for your project |
| your project's own constitution (optional) | Constitutional mandate | Amending the principle itself, if you have one |

Eval records (runtime artifacts) land in:
- `.claude-evals/` (per-project default)
- `.claude-loop-runs/{run-id}/evals/` (loop runs)
- `.claude-evals/quarantine/` (failed gate outputs, when `--on-fail quarantine`)
- `.claude-evals/bench/` (variance benchmarks)

---

## Maintenance

### Weekly

- Run `/tvt-core-eval coverage` to spot any drift (new skills not yet classified)
- Review failed evals in `.claude-evals/quarantine/` if any accumulated

### When adding a new skill

The skill inherits the global default (`score` at `light`) automatically — no
action needed. If the skill is high-stakes or deterministic, add the appropriate
frontmatter:

```yaml
# High-stakes (client-facing, autonomous publishing, etc.)
eval_mode: gate
eval_depth: standard

# OR — deterministic / no AI output
# eval: <one-line reason>
eval_exempt: true
```

### When a skill regresses

Run `/tvt-core-eval bench --process <skill> --input <test-fixture> --n 10` to
measure variance. If `reliability: low`, the skill's prompt or temperature
needs tightening.

For pipeline regressions across time:
```
/tvt-core-eval regress \
  --output current_run.md \
  --baseline last_known_good.json \
  --criteria criteria.md
```

### When the eval cost gets too high

Lower the built-in `light` depth usage share (it already covers most cases), or —
if your project has one — tune `~/.claude/eval-policy.yml`:
- Raise `default_pass_threshold` to fail-fast and avoid retries
- Lower `warn_cost_per_eval_usd` and `abort_cost_per_eval_usd` to cap

### When something feels wrong

- Check the skill's frontmatter declared what you think
- If you rely on a project `CLAUDE.md` for voice/style, check it's loaded (every session reads it)
- If your project has `~/.claude/eval-policy.yml`, check it for an override you forgot
- Run `/tvt-core-eval coverage` to see the current classification

---

## Known gaps & limitations

1. **No hook-based enforcement** — eval is enforced by the per-skill frontmatter
   mandate and each skill's own discipline, not a hook. A determined skill or
   accidental shortcut could skip eval. The visibility tool (`coverage`) is the
   backstop. A hook-based enforcement layer is intentionally not built; it's too
   blunt and adds cost everywhere.

2. **The 9 "default inherit" skills are unverified** — they'll auto-eval on
   invocation, but none have been bench-tested for variance or had baseline
   evals captured. Add baselines as you use them.

3. **`tvt-core-write` has its own quality gate** — it pre-dates `tvt-core-eval`.
   Consolidating onto `tvt-core-eval gate` mode is a TODO; for now there are two
   measurement layers in that skill, which is fine but not ideal.

4. **Cross-skill eval store is project-scoped** — `.claude-evals/` is in the
   working directory. There's no global query store. Add later only if a real
   cross-project query need emerges.

5. **No human-in-the-loop on borderline scores** — currently gates either pass
   or fail. A "needs_work" verdict (0.5–0.85) doesn't pause for human review.
   Add later if false-positive halts become a problem.

---

## Reference

- **Engine spec**: [`SKILL.md`](./SKILL.md)
- **Policy override (optional, your project)**: `~/.claude/eval-policy.yml`
- **Industry sources**:
  - HumanEval / pass@k — Chen et al. 2021
  - LangSmith eval pattern (per-trace scoring + run aggregation)
  - OpenAI evals framework (per-criterion breakdown with evidence)
  - AgentBench (efficiency_rate as agent metric)

---

## Changelog

### v1.2.0 — 2026-05-02 (post second dogfood eval)

v1.1 scored 0.817 / needs_work (up from v1.0's 0.338 / fail). v1.2 closes the
remaining gaps to clear the 0.85 pass bar:

- **Evidence-before-score field ordering** in canonical judge prompt — judge
  must articulate evidence and reasoning BEFORE assigning a score, preventing
  anchor bias.
- **Prompt-cache breakpoints** explicitly documented — preamble marked as
  `cache_control: ephemeral`, ~90% input-token discount on repeated criteria.
- **`--batch` flag** in bench mode — uses Anthropic Message Batches API for
  50% cost discount when N ≥ 10.
- **`--producer-model` flag** + self-preference policy — system warns at
  standard depth, blocks at deep, when judge and producer are from the same
  model family. Cites Panickssery et al. 2024.
- **Statistical rigor propagated** to `regress` mode — paired t-test,
  delta_ci_95, judge_drift_check (catches comparing scores across model
  upgrades).
- **Starter golden-set fixture** shipped at `criteria/templates/golden-set-example.jsonl`
  — 12 hand-labeled items across 6 task types so callers have a working
  example to clone for their own calibration.

### v1.1.0 — 2026-05-02 (post first dogfood eval)

The v1.0 spec was scored against 2024–2025 industry best practice and failed
(weighted 0.34 / fail). v1.1 addresses the gaps:

- **New mode: `calibrate`** — score a hand-labeled golden set, compute Cohen's
  kappa + Pearson r, accept/reject the rubric. A rubric MUST pass calibration
  before it can be used in a `gate` at standard or deep depth.
- **Position-bias defense** — `compare` mode auto-swaps positions and averages.
  New `--swap-positions on|off|auto` flag exposes the behavior.
- **Bias-hardened canonical judge prompt** — explicit defenses for length bias,
  position bias, prompt-injection attempts, eloquence-over-evidence.
- **Failure-mode template library** — 6 starter rubrics at
  `criteria/templates/`: hallucination, instruction-following, refusal-
  appropriateness, schema-compliance, tool-call-correctness, prompt-injection-
  robustness. Compose, don't reinvent.
- **Statistical rigor in `bench`** — output now includes SEM, 95% CI, paired
  t-test with Holm-Bonferroni correction vs baseline, n_effective for clustered
  designs.
- **`--judge-model-pin`** — pin to exact model version for drift detection
  across time.
- **Prompt-cache-friendly judge structure** — stable preamble first, variable
  inputs last. Enables ~90% cost reduction on cache hits.
- **Panel judge mode** — `--judge panel` runs N different model families with
  median aggregation; default at `deep` depth (replaces old "3 same-model
  calls" pattern which was just temperature noise).

### v1.0.0 — 2026-05-02 (initial)

Initial release. Modes: score, summarize, compare, bench, regress, gate,
coverage. Three depth tiers. Workspace-wide constitutional mandate.

---

**Version**: 1.2.0 | **Last updated**: 2026-05-02
