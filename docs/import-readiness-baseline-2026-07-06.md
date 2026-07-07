# Import-Readiness Gate — baseline run, 2026-07-06

**What landed**: a two-layer judge for the question spec 007 US1 poses — *can someone who
isn't the author install this plugin from gitlab.tavant.com and actually use it?*

| Layer | Artifact | Runs |
|---|---|---|
| Deterministic (12 checks C1–C12) | `tests/test_import_readiness.py` | `scripts/judge-import.sh` (ratchet) / `--strict` (publish gate) |
| LLM judge (4 axes + 4 hard fails) | `rubrics/import-readiness.md` | via `tvt-os-judge`, one judge per skill |
| Known-open debt | `tests/import-gate-baseline.yml` | consumed by the ratchet |

**Ratchet contract**: the default `pytest` run stays green unless a commit introduces a
*new* violation or fixes one without removing it from the baseline (stale entries fail
too — the baseline can only tell the truth). `--strict` ignores the baseline and is the
gate an actual marketplace publish must pass. Regenerating the baseline
(`--rebaseline`) is a deliberate, diff-reviewed act.

Self-test performed: injecting a fake `g-totally-fake-skill` reference correctly failed
the ratchet as a C3 REGRESSION; reverting restored green. Full suite: 70 passed
(58 pre-existing unit tests + 12 gate checks).

## Baseline: 153 open findings (strict gate = BLOCK, as expected pre-Wave-1b)

| Check | What it catches | Open | Burn-down owner |
|---|---|---|---|
| C1 manifests valid/consistent | broken storefront | 0 | — |
| C2 SKILL.md structure/frontmatter | loader + claude.ai picker | 1 (`g-sales-prospect` has no SKILL.md) | Wave 1 |
| C3 dangling skill references | router invokes skills that don't ship | **58** | Wave 1b (worst: tvt-core-extract 7, tvt-core-lookup 6, tvt-core-write 6, tvt-core-eval 5; incl. half-renamed ghosts like `tvt-core-write-intel`) |
| C4 persona leak (author's name) | package unusable by anyone else | **41** files (25 skills, 14 playbooks) | Wave 1b sweep — wider than planned: plan scoped it to SKILL.md; gate scopes it to the full shipped surface |
| C5 workspace coupling | author-machine paths (`~/.claude/...`, `specs/NNN-`, org/, DemoServer/agent-lab.io) | **46** | Waves 1b + 4 |
| C6 `${CLAUDE_PLUGIN_ROOT}` refs resolve | invoke-time file loads | 0 | — |
| C7 relative markdown links resolve | broken references/ | 2 (tvt-create-pptx → `../pptx/*.md`) | Wave 1b |
| C8 unshipped isolation | routing into `unshipped/` | 2 (tvt-core-write, tvt-os-replay → `tvt-os-research`) | Wave 1b |
| C9 scripts compile (Py 3.9 floor) | broken tooling | 0 | — |
| C10 fresh-clone (`git archive`) unit suite | untracked-file crutches | 0 | — |
| C11 zip channel self-contained | claude.ai upload path | 3 (g-sales-engine, tvt-os-judge, tvt-os-loop zips keep unresolved plugin-root refs) | Wave 1b/2 |
| C12 claimed counts honest | storefront trust | 0 (claims "35", catalog has 35) | recheck after every unship |

Notable: C4/C5 confirm the Wave-1 persona sweep has **not** run yet, and the gate widens
its scope beyond the plan's `*/SKILL.md` acceptance grep — playbooks ship too, and 14 of
them carry the author's name plus named-client war stories (also an HF3 confidentiality
risk under the rubric).

## LLM judge — calibration sample

Three skills judged against `rubrics/import-readiness.md` by independent judges under
the fresh-installer persona: **3/3 BLOCK** (g-sales-engine 0.50, tvt-intel-deep 0.10,
tvt-core-eval 0.50). The judges also caught four deterministic-gate blind spots, now
closed (+28 baseline findings). Full record: `docs/import-readiness-judge-2026-07-06.md`.

## Stale sibling artifact (out of scope here, flagging)

`docs/tvt-skills-one-pager.{html,pdf}` still lists the 8 STUB skills that Wave 1a moved
to `unshipped/` and footers "8 of 43 items are unbuilt stubs" — regenerate its body after
Wave 1b (only the header was renamed on 2026-07-06 per request).
