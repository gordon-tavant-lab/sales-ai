# Design / Product / Eval Review — spec 006 + the `tvt-*` skill set

**Date**: 2026-07-06
**Scope**: everything the 2026-07-05 integrity audit did NOT cover. That audit was mechanical
(cross-skill name resolution, missing deps — all fixed, `1b1ab62`). This one is design-level:
three independent parallel reviewers on (A) spec-vs-reality drift in spec 006, (B) product
cohesion for the actual audience (a non-technical Tavant sales rep), (C) eval/judge coverage of
every skill's output — plus deterministic checks run directly (zip build, YAML parse, test
inventory).
**Method**: each reviewer read the real files and cited path+line for every claim; deterministic
claims (grep counts, test runs, zip contents) were executed, not asserted.

---

## Verdict

The deterministic core is genuinely good — `score.py`'s protected-floor allocator implements the
spec faithfully including cases the spec didn't demand, the guardrail philosophy ("AI drafts,
human sends" with no send path wired) is architectural rather than aspirational, and the
local-JSON-first scope call is right for the audience. But the package fails three systemic tests:

1. **Every loop that needs data to arrive from the world is unbuilt or unowned** — outcomes never
   reach calibration, the abuse-rate KPI has no counter, the heartbeat scripts don't exist, the
   provocations library is empty. The machinery is real; the pipelines into it are fiction.
2. **It was renamed, not productized** — 30 of 44 SKILL.md files still address the author by name, write to
   his Workspace paths, and 7 skills are shipping stubs whose entire body is a task-number
   reference to a repo the rep will never see. "forecast" — the most sales-shaped word in the
   catalog — is one of the dead ones.
3. **0 of 19 output-producing skills invoke any independent eval or judge on their own output** —
   despite the package shipping `tvt-core-eval` (700 lines) and `tvt-os-judge`, and despite
   `tvt-core-eval`'s own text mandating that `tvt-sales-pack` "should gate before declaring a deck
   client-ready." Client-facing artifacts ship on same-context self-checklists.

---

## Priority findings (merged from all three reviewers + direct checks, deduped, ranked)

### P0 — breaks the product for its actual audience

**F1. Zip distribution silently broken for 13 skills** *(direct check)*
`build-zips.sh` zips each skill dir alone; 13 skills reference `../playbooks/`, `../accelerators/`,
or `../assets/` — paths that don't exist inside a zip. `tvt-tavantize.zip` cannot do its one job
(the 1.3MB template isn't in the zip). Neither `build-zips.sh` nor README Option B warns.
Also: `dist/` has no zips at all for `g-sales-engine`/`g-sales-pov`/`g-sales-prospect`/`g-gov-*`
(the glob is `tvt-*/`) — Option B users can't get the engine itself.
*Fix options*: bundle referenced shared content into each dependent zip (path-rewritten), or mark
the 13 as Claude-Code-only in README + make `build-zips.sh` refuse/warn on them.

**F2. Seven dead stubs ship under sales-shaped names** *(reviewer B)*
`tvt-os-forecast/improve/reason/recommend/research/synthesize/verify` are 17-20-line placeholders
("Stub lands in US1 (T054)") whose skill-picker descriptions read "Auto-synthesized at T042;
expand later." A rep invoking "forecast" gets a task-number reference. CAPABILITIES.md discloses
this honestly — but a rep reads the picker, not the capability inventory. Blast radius: trust in
all 47. *Fix*: exclude the 7 from the shipped plugin, or rewrite descriptions to "Not yet
available."

**F3. The persona transplant never happened** *(reviewers A+B, convergent)*
30 SKILL.md files reference the author by name — including trigger phrases ("Use when **the user says**
'research [company]'") that won't match the actual user. Output paths point at his Workspace
layout (`research/intel/{Client}_...`); exemplar citations point at his real projects
(`project/{Client}/...`); `g-sales-engine` stages drafts "for **your** review" and runs
`cd g-sales-prospect/scripts` — a relative path that won't resolve once the plugin lives in
`~/.claude/plugins/` (needs `${CLAUDE_PLUGIN_ROOT}`). *Fix*: one sweep — author's name→"you", Workspace
paths→plugin-relative conventions, `cd`→`${CLAUDE_PLUGIN_ROOT}/...`.

**F4. Zero independent eval on any output; client-facing artifacts are self-graded** *(reviewer C)*
Coverage table result: 0/19 output-producing skills invoke `tvt-core-eval` or `tvt-os-judge`.
`tvt-sales-pack`, `tvt-sales-pitch`, `tvt-sales-engagement-proposal`, `tvt-create-deck` — the
things a client sees — end with same-context self-checklists; two of them delegate to a "g-write"
quality gate that (a) is a wrong skill name in this package and (b) is itself self-review.
`tvt-create-explainer`'s own line 126 documents the failure mode: "A passive pitfall note here
failed to catch the mistake 4 times running." Eval frontmatter exists on 18 of the 21 cognitive/
core skills and on **zero** of the sales/intel/create/pm skills — the exact population producing
client-facing output. *Fix*: the Output-Gate convention (below) — ~24 files, 5 shared rubrics,
zero new infrastructure.

### P1 — spec claims the repo contradicts

**F5. The calibration feedback loop is fiction** *(reviewer A — the sharpest finding)*
Spec §5/§7 promise score→outcome pairs attest to the `g-gov-attest` ledger and the scorer
"converges to backtested confidence." Reality: `eval_backtest.py` reads a hand-authored
`backtest.json` (the exact "bespoke store" §8 forbids); nothing writes shortlist snapshots or
outcomes to the ledger; nothing reads the ledger back; and `score.py` never adjusts
`confidence_value` from backtest results — `calibration_n >= 100` only flips a display label.
Worse (F5a): `calibration_n` is a **hand-typed per-opportunity input field**, so any rep typing
`"calibration_n": 100` flips the display to a trustworthy-looking percentage, silently bypassing
the §5 anchoring guard. *Fix*: one `close-out <opp-id> won|lost` command that appends the outcome
pair to the attest ledger and regenerates the labeled file; derive calibration state from that
artifact, never from input JSON.

**F6. The spine's transition KPIs are uncomputable** *(reviewer A)*
The spec's core claim — "tracks real Gong-class KPIs at every stage" — requires
outreach/response/meeting events, rep fields, and ramp dates that the opportunity schema doesn't
have. `kpi.py` computes 6 portfolio KPIs over a stage snapshot; the per-job transition KPIs in §3's
table (response rate, meeting rate, POC→proposal) and `rep_ramp_time` cannot be computed from any
data a user could supply. *Fix*: add an events array to the schema, or amend §3 to mark those KPIs
"observed manually, not computed" — in writing, pick one.

**F7. The verification gate contradicts its own threat model on the primary path** *(reviewer A)*
The §7 gate exists because *machine extraction* hallucinates >1/3 of the time and hand-typing is
"the adoption killer." The 2026-07-04 scope decision made hand-typed `claims.json` the primary
path — and `gate.py` still requires the author to invent an `extraction_confidence` number for
their own typed claim, then auto-attests anything self-labeled ≥0.85. On the primary path the gate
adds the friction §7 forbids while guarding against a hallucination source that isn't present.
*Fix*: manual authorship = the confirm event (author is the verifier); keep the tiered gate for
the deferred machine-extraction path it was designed for.

**F8. Unbuilt §6 automation, falsely asserted as wired** *(reviewer A)*
`sales-pulse.sh`/`prospect-radar.sh`/`outreach-followup.sh` exist nowhere; `hermes.sh` has zero
references; yet CAPABILITIES.md states they "register here." Deeper: Hermes is the author's personal
launchd — the automation layer has no story at all for the plugin's actual audience. *Fix*: delete
§6 from this spec (or rewrite as manual cadence commands) and correct CAPABILITIES.md.

**F9. `g-sales-prospect` is a ghost** *(reviewers A+C, convergent with a prior open flag)*
No SKILL.md anywhere in its history; `references/` (mandated by §8: scoring model + backtest
harness + cold-start prior docs) is empty; `plugin.json` headlines it as a deliverable. It also
holds the package's best eval asset (`eval_backtest.py` — Brier score, calibration curve, drift
check) that no coverage tooling can see. *Fix*: write the SKILL.md declaring
`eval: mode: gate` with `eval_backtest.py` as its custom evaluator + one references/scoring-model.md;
or amend §8 to declare it a script library owned by the router and fix plugin.json.

### P2 — trust, confusion, and hygiene

**F10. Display-layer guarantees are actually prompt discipline** *(reviewer A)* — `score.py` emits
raw `confidence_value` floats for uncalibrated items; the "never displays a numeric %" rule lives
in a SKILL.md sentence asking the LLM not to reformat — the exact caveat-doesn't-defeat-anchoring
mechanism the cross-family panel rejected. *Fix*: `--display` mode that omits raw floats.

**F11. Queue/abuse-rate KPI has no state** *(reviewer A)* — no queue file, no timestamps, no
accumulator; `--elapsed-seconds` is typed in by the person being policed. *Fix*: persist queue
batches to JSONL with created-at stamps; compute elapsed at confirm time.

**F12. Skill-picker collisions and the critique-cluster maze** *(reviewer B)* —
`tvt-intel-customer` and `tvt-intel-pipeline` trigger on the identical phrase "full research on
[company]" (a genuine model-routing coin flip). Five skills (`tvt-os-metacognition/judge/
contrarian`, `tvt-grill-me`, `tvt-core-eval`) all answer "critique my thing" in engineer-speak;
judge's description advertises hooks and a `/g-dev-build` that aren't in the package. *Fix*:
pipeline owns "full research"; point-tools get "usually invoked via pipeline" descriptions; one
rep-facing critique entry that routes internally.

**F13. README has no first step; the flagship self-labels "build in progress"** *(reviewer B)* —
README never names a single skill to type after install; `g-sales-engine`'s frontmatter carries
maintainer bookkeeping ("status: build in progress...", spec § pointers to unshipped files);
plugin.json's storefront description is changelog-speak ("2026-07-04 decision"). *Fix*: "Your
first 10 minutes" README section (3 commands, all starting `g-sales-engine`); move build-status to
docs/; rewrite the storefront line.

**F14. Factcheck mandate not propagated to producers** *(reviewer C)* — spec and consumers say
"mandatory gate," but `grep -i factcheck` in `tvt-intel-deep/customer/dossier/fanout/qbr/flywheel`
returns zero hits. Invoke any of the 6 directly ("dossier on a client") and nothing tells the model to
verify before finishing. *Fix*: wave-2 of the Output-Gate rollout (below).

**F15. Playbooks ship named-client anecdotes** *(reviewer B)* — e.g. a named client's failed
vendor workshop and an internal scoping-failure narrative, onto every rep laptop; one copy-paste
from a client-facing deck. *Fix*: ship only skill-referenced playbooks; genericize named anecdotes.

**F16. ~14 of 47 skills are developer tools, not sales tools** *(reviewer B)* — the 7 stubs plus
`tvt-os-skill-review` (reviews SKILL.md files), `tvt-os-replay` (git-bisect helper),
`tvt-core-mcts` (raw MCTS engine), `tvt-os-loop`, `tvt-os-prompt`. Core-for-a-rep is ~20 skills.
*Fix*: cut or hide; dependency completeness ≠ catalog visibility.

**F17. Stale/contradictory lines in shipped docs** *(reviewers A+B)* — `g-sales-pov/SKILL.md`
says "this repo does not vendor g-gov-attest" (it does, `src/g-gov-attest/`); `g-sales-engine`'s
job-5 firing row still says "Notion transcript" (deferred); "g-write" naming in two files; Brier
drift-check P1 alarm fires on coin-flip variance below its own significance floor. *(One-line
fixes each.)*

**F18. `tvt-pm-jtbd`/`tvt-pm-grow` have zero tests** *(direct check)* — the "AI-opportunity
engine" is the only scoring machinery in the package with no test file (source never had any).

### Verified healthy (direct checks)

42/42 zips build; all 42 frontmatter blocks parse and match their directory names; `dist/`
correctly untracked; 57/57 tests pass; no cross-skill relative-path imports; no personal
paths/credentials (re-checked).

---

## What's genuinely right (calibration, not politeness)

- **`score.py::rank_shortlist`** distinguishes `below_cutoff` from
  `capacity_consumed_by_motion_floor` in parked reasons — truthful about policy-vs-score losses, a
  case the spec never demanded. Tested.
- **Guardrails are structural**: the router has no send path to misuse; calibration state is a
  field contract, not a hope.
- **The local-JSON scope inversion** was made for the right reason (audience credentials) and
  cascaded through the doc family.
- **README's voice and failure-mode candor** (the allowlist trap, the "Cowork will never work —
  stop" warning, Option B's honest caveats) is rare and right for the audience.
- **`kpi.py` surfaces its own limits in output** (snapshot-vs-transition note, warns on unlabeled
  wins instead of averaging them away).

---

## Remediation roadmap (proposed, not yet executed)

**Wave 0 — one-line truth fixes (hours):** F17's four items; CAPABILITIES.md hermes line (F8);
gate `build-zips.sh` on the 13 shared-content skills with a warning (F1 interim).

**Wave 1 — ship-safety (1-2 days):** exclude/relabel the 7 stubs (F2); persona-transplant sweep
(F3: author's name→you, paths→`${CLAUDE_PLUGIN_ROOT}`); README quickstart + storefront rewrite (F13);
zip strategy decision + implementation (F1); `g-sales-prospect/SKILL.md` (F9).

**Wave 2 — the eval mandate (2-3 days):** Output-Gate convention from reviewer C: `eval:` frontmatter
+ closing mandatory-gate section on ~19 skills, 5 shared rubric files (seeded from the existing
checklists — they're good rubric content in the wrong enforcement position), factcheck step wired
into the 6 producer intel skills (F14/F4). ~24 files, ~400 lines, zero new infrastructure.
`tvt-core-eval coverage` mode becomes the regression check for the mandate itself.

**Wave 3 — close the loops (2-3 days):** `close-out won|lost` command → attest ledger → labeled
backtest file (F5, the single highest-leverage code change in the package); `--display` mode
(F10); queue JSONL state (F11); manual-claims gate redesign (F7); KPI schema decision (F6);
spec §6 rewrite (F8); tests for `tvt-pm-*` (F18).

**Wave 4 — product curation (1 day):** catalog cut to ~20 core + optional tier (F16); trigger
de-collision (F12); playbook trim + anonymization (F15).
