# Remediation Plan — executing the 4-wave roadmap

**Date**: 2026-07-06
**Source**: `docs/review-2026-07-05-design-product-eval.md` (18 findings, F1-F18).
**Approval**: The author approved documenting + planning + implementing all four waves (2026-07-06).
This doc records the task decomposition, the decisions made where the roadmap offered options, and
the acceptance criterion per wave. One commit per wave, tests re-run after every wave.

## Decisions made (where the review offered options)

| Finding | Options in review | Decision | Why |
|---|---|---|---|
| F2 (7 stubs) | exclude vs. relabel | **Move to `unshipped/`** (out of the installable catalog, kept in repo) | Reversible; honest at the picker; spec 007 FR-013 gets a note that stub vendoring is deferred until upstream implements them. Relabeling would ship dead skills with nicer labels — still dead. |
| F1 (zip break) | bundle vs. mark Claude-Code-only | **Bundle at build time**: `build-zips.sh` stages each shared-content skill to a temp dir, copies the referenced `playbooks/`/`accelerators/`/`assets/` files in, rewrites `../playbooks/` → `playbooks/` in the staged copy only | Repo layout unchanged; zips become genuinely self-contained; matches the self-contained-skill convention. Also add zips for `g-sales-engine`/`g-sales-pov`/`g-gov-*` (`g-sales-prospect` has no SKILL.md until Wave 1 delivers it). |
| F6 (uncomputable KPIs) | events array vs. document-as-manual | **Document as manually-observed** in spec §3 | An events schema with no consumer is speculative machinery — the exact over-engineering pattern F12 flagged. Revisit when a real event source exists. |
| F7 (gate threat-model) | — | `gate.py --source manual\|extracted`; manual = author-is-verifier (attested `author_attested`, no invented confidence number); tiered gate reserved for `extracted` | Restores the gate to the threat it was designed for. |
| F16 (catalog cut) | cut ~14 vs. hide | **Unship 9** (7 stubs + `tvt-os-skill-review` + `tvt-os-replay`); **keep** `tvt-core-mcts`/`tvt-os-loop`/`tvt-os-prompt`/`tvt-core-eval`/`tvt-os-judge` | The kept five are real, and eval/judge are the Wave-2 machinery; skill-review + replay are purely maintainer-workflow (review SKILL.md queues; git-bisect helper) with zero rep value. |
| F15 (playbooks) | trim + genericize | Keep only playbooks actually referenced by shipped skills; genericize named-client anecdote lines in those | Methodology ships; client-named vendor-failure stories don't. |

## Open verification item (may add a task)

**Plugin skill-discovery structure**: this repo keeps skill dirs at the repo root; the gordon-os
marketplace convention is `plugins/<name>/skills/<skill>/`. If Claude Code's loader only discovers
`<plugin-root>/skills/`, the plugin currently installs **zero skills** — being verified against
current official docs before Wave 1 completes. If confirmed, a restructure task (move skill dirs
under `skills/`, update manifests/scripts/docs) is inserted into Wave 1 as its first item.

## Waves, tasks, acceptance criteria

### Wave 0 — one-line truth fixes
Fix F17 (4 items), F8's false CAPABILITIES.md line, interim `build-zips.sh` warning for the 13
shared-content skills, Brier-P1 suppression below the calibration floor (+ test).
**Accept when**: each fixed line greps correct; 57/57 + new test pass.

### Wave 1 — ship-safety
Stubs → `unshipped/` + count/manifest/spec-007 sync; persona-transplant sweep (~30 files:
the author's name→"you", Workspace paths→plugin-relative output conventions, `cd` → `${CLAUDE_PLUGIN_ROOT}`);
README "first 10 minutes" + storefront description rewrite; `g-sales-prospect/SKILL.md` (declares
`eval_backtest.py` as its evaluator, documents the scoring model); `build-zips.sh` bundling fix.
**Accept when**: a grep for the author's name across `*/SKILL.md` returns zero shipped files; zip of `tvt-tavantize`
contains the template; README names ≥3 concrete first commands; installable-skill count is honest
everywhere it appears.

### Wave 2 — the eval mandate
`rubrics/` ×5 (seeded from the existing checklists — content moves, enforcement position changes);
`eval:` frontmatter + closing mandatory Output-Gate section on ~19 output-producing skills;
factcheck wired as step 1 in the 6 producer intel skills; `eval_exempt` rationale on factcheck.
**Accept when**: every output-producing shipped skill either declares `eval: mode: gate` + gate
section, or declares `eval_exempt` with rationale; zero "g-write" refs; deterministic-vs-LLM split
follows the review's table.

### Wave 3 — close the data loops
`close_out.py` (outcome → attest ledger → regenerated backtest artifact); `score.py` derives
calibration from the backtest artifact and grows a `--display` mode with no raw floats while
uncalibrated; `gate.py` queue-state JSONL (timestamps, computed elapsed, accumulated abuse rate) +
`--source manual|extracted`; tests for all of the above + `tvt-pm-jtbd/scripts/score.py`; spec.md
(outer repo) §3 KPI decision + §6 automation rewrite.
**Accept when**: a full simulated cycle runs — rank → close-out → backtest regenerates from ledger
→ calibration state changes only via that artifact; all tests green.

### Wave 4 — product curation
Unship skill-review/replay; trigger de-collision (pipeline owns "full research"; critique cluster
routes through metacognition); playbook trim + anonymization; final manifest/count sync; full
re-verify (pytest, 33+ zips, persona grep, stale-name grep).
**Accept when**: all Wave-4 greps clean; final verification block recorded at the bottom of this doc.

---

## Final verification block (all 4 waves, 2026-07-06)

Verified against the actual repo state, not assumed from the plan text above:

- **Import-readiness gate** (`tests/test_import_readiness.py`, 12 checks): `python3 -m pytest -q`
  → 12/12 passing. Baseline (`tests/import-gate-baseline.yml`) went **153 → 39 open findings**
  across the 4 waves (C1/C2/C4/C6/C7/C8/C9/C10/C12 all fully clean; C3=25 and C5=12 remaining are
  documented optional-external-toolkit references, not installer-blocking; C11=2 is the tvt-os-judge/
  tvt-os-loop sibling-plugin-discovery code, which degrades gracefully — no crash).
- **Skill test suites** (`scripts/run_all_tests.sh`, one subprocess per suite — see pytest.ini for
  why): **6/6 suites passing, 105/105 tests** (28 gate.py, 12 close_out.py, 13 eval_backtest.py,
  16 kpi.py, 19 score.py, 17 tvt-pm-jtbd score.py).
- **Zip channel** (`scripts/build-zips.sh`, no args = full catalog): **38/38 zips built**, only
  2 carry the accepted WARN (tvt-os-judge, tvt-os-loop).
- **Persona-leak grep** (author's name across the shipped surface): **zero matches** — confirmed
  via the gate's own C4 check, which scans skills/playbooks/accelerators/rubrics/references/
  agents/CAPABILITIES.md/README.md/manifests and returned 0 findings.
- **Stale-name grep** (`g-write`, pre-rename `g-*` names as live dependencies, `g-research`/
  `g-core-research` phantom-skill references): **zero matches** — the last 4 (in tvt-intel-customer/
  deep/fanout/dossier/factcheck + tvt-pm-grow's grow-engine.md) were closed this wave by authoring
  the real research procedure (`references/research-query-library.md`, 37 queries / 9 dimensions)
  instead of continuing to point at a skill (`g-research`) that never existed anywhere upstream.
- **Catalog count**: 38 shipped items (33 `tvt-*` skills + `g-sales-engine`/`g-sales-pov`/
  `g-sales-prospect` + `g-gov-guard`/`g-gov-attest`), honest everywhere it's claimed
  (plugin.json, marketplace.json, one-pager). 9 items live in `unshipped/` (7 upstream stubs +
  `tvt-os-skill-review`/`tvt-os-replay`, both purely maintainer-workflow tools with zero rep value).
- **Trigger de-collision** (F12): `tvt-intel-pipeline` now exclusively owns "full research on
  [company]" (`tvt-intel-customer` defers to it); the 5-way "critique my thing" collision
  (metacognition/judge/contrarian/grill-me/core-eval) resolved by making `tvt-os-metacognition`
  the one rep-facing front door with plain-language trigger phrasing, and adding one-line
  disambiguation notes to judge/contrarian pointing back to it.
- **Playbooks**: cut from 30 files to 6 content playbooks (only ones actually referenced by a
  shipped skill) + a rewritten `README.md` index; the 6 kept were anonymized (named colleagues →
  consistent role labels, real client names → generic descriptors, one broken path artifact from
  the anonymization pass caught and fixed, one real DemoServer URL removed).

**Not fully closed, tracked as open debt** (documented, not silently dropped):
- `accelerators/tvt-sdlc-skills-platform.md` — an unrelated Tavant accelerator's pitch/reference
  doc (cited by `tvt-sales-engagement-proposal` for engineering-platform opportunities), carries
  a handful of C5 findings describing *that other project's own* structure. Scoped with a
  one-line disclaimer rather than rewritten; a candidate for removal from this package entirely
  if a future pass decides it's out of scope for a sales-skills plugin.
- `tvt-core-eval`'s `~/.claude/eval-policy.yml` / `~/.claude/skills/` mentions and `tvt-os-judge`'s
  `.specify/` integration points are correctly reframed as optional overrides (substance fixed in
  Wave 1b), but the gate's pattern-matching still flags the literal path strings — a known
  precision gap in the check itself, not a real installer-blocking dependency.
