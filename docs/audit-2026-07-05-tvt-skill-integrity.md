# Audit — does the vendored `tvt-*` package actually work standalone?

**Date**: 2026-07-05
**Scope**: spec 006 (`g-sales-engine`/`g-sales-pov`/`g-sales-prospect`) + all 40 vendored `tvt-*`
skills (spec 007), against the exact question spec 007 User Story 1 poses: *"Give a Claude Code
instance with only this plugin installed (no Workspace context) to someone who isn't the author."*
**Method**: deterministic greps + an actual pytest run — not an LLM read-and-vibe pass. Every claim
below is reproducible with the command shown.

## Verdict: BLOCK at first pass → remediated same day (see "Remediation applied" below)

Original verdict (per `g-os-judge`'s own rubric — decision axis fails its 0.60 hard floor):

Not because the work is low-quality — the Python core (`score.py`/`kpi.py`/`gate.py`) is genuinely
solid and the path/credential scrub was done correctly. It fails because a load-bearing claim
("vendored, real," "zero-match grep," "installable by someone who isn't the author") was verified
against the wrong risk. The scrub checked for `org/`-paths and personal identifiers (correct, but
not the failure mode that actually breaks the package) and never checked whether one skill can
still *find* another by name at invoke time. Same shape as `g-os-judge`'s own documented v1.0 miss
(archived `Kuzu` dependency, 5 load-bearing references, never checked because no one ran the
deterministic check) — a scriptable verification that was simply never run.

---

## Finding 1 (CRITICAL) — the entry-point router calls skills that don't exist in this package

`g-sales-engine/SKILL.md` and `g-sales-pov/SKILL.md` — spec 006's own new code, written *before*
the tvt- vendoring existed — invoke their dependencies by the **pre-rename `g-` names**:

```
g-sales-engine/SKILL.md:  g-intel-dispatch, g-intel-qbr, g-intel-pipeline, g-intel-factcheck,
                          g-intel-flywheel, g-pm-jtbd, g-pm-grow, g-create-deck, g-sales-pack,
                          g-sales-pitch, g-sales-engagement-proposal
g-sales-pov/SKILL.md:     g-intel-customer, g-intel-dossier, g-intel-flywheel, g-intel-fanout,
                          g-intel-factcheck, g-pm-jtbd
```

None of these exist under those names in this repo — only `tvt-intel-*`/`tvt-sales-*`/`tvt-create-*`
do. On a genuinely fresh install (exactly spec 007 US1's own test), the router that's supposed to
orchestrate the whole system can't find any of the skills it orchestrates. This is invisible on
the author's own machine only because his original `g-*` skills still sit in `.claude/skills/` there —
the bug is silent for the one person who doesn't need this package and load-bearing for everyone
spec 007 exists to serve.

**Reproduce**:
```bash
grep -no "g-intel-[a-z]*\|g-sales-pack\|g-sales-pitch\|g-pm-jtbd\|g-pm-grow\|g-create-[a-z]*" g-sales-engine/SKILL.md
```

## Finding 2 (CRITICAL) — 90% of the vendored skills have the same self-inflicted wound

The rename that produced `tvt-*` only touched each skill's own frontmatter `name:` field. The
**prose inside every SKILL.md** — where a skill tells Claude which sibling skill to invoke next —
was never touched. Result: **36 of 40 vendored skills** still instruct Claude to invoke a sibling
by its pre-rename name.

```bash
for d in tvt-*/; do d="${d%/}"; grep -rlo \
  "g-intel-[a-z]*\|g-sales-[a-z]*\|g-create-[a-z]*\|g-pm-[a-z]*\|g-os-[a-z]*\|g-core-[a-z]*\|\btavantize\b\|\bgrill-me\b" \
  "$d" >/dev/null 2>&1 && echo "$d"; done | wc -l
# → 36
```

Worst offenders (stale-reference count in that one file):

| Skill | Stale refs | Skill | Stale refs |
|---|---|---|---|
| `tvt-os-judge` | 60 | `tvt-create-deck` | 37 |
| `tvt-intel-pipeline` | 43 | `tvt-core-write` | 31 |
| `tvt-core-eval` | 47 | `tvt-os-contrarian` / `tvt-os-metacognition` | 29 each |

This is the actual answer to "are they cohesive": **no** — cohesion breaks exactly where it's
tested, at invocation time. It reads as one renamed family; it behaves as 40 shells still wired
into an ecosystem this package doesn't ship.

## Finding 3 (HIGH) — a load-bearing dependency isn't vendored, and isn't flagged either

`g-pm-jtbd` → `g-pm-grow` is core to `g-sales-engine`'s own job-0/3a spine (spec 006 §1/§3a) — not
optional, not a nice-to-have. It is **not vendored anywhere in this repo** (confirmed: `find . -iname
"*pm-jtbd*" -o -iname "*pm-grow*"` returns nothing), and unlike every other dependency in
`CAPABILITIES.md`, its table has **no Status column at all** — every other section explicitly marks
`Vendored` / `Vendored, real` / `Vendored, stub in source`. This is a silent gap, directly against
spec 007's own **SC-005**: *"every transitive dependency... is present... or named as an explicit
external prerequisite... no silent gaps."*

## Finding 4 (LOW) — cosmetic/dead-code items, not functional breaks

- `tvt-os-judge/scripts/check_dep_liveness.sh` line 74 hardcodes `SKIP_PATH =
  "skills/g-os-judge/scripts"` — the old folder name, now stale (folder is `tvt-os-judge/scripts`).
  Harmless today (script isn't wired to run — no `hooks.json` shipped, correctly, per FR-014), but
  wrong if it's ever activated.
- `tvt-os-judge/scripts/judge_hook.sh` (a hook *trigger* script) ships despite the FR-014
  skills-only decision. `hooks.json` itself was correctly excluded (verified: zero matches
  repo-wide), so this is inert, not a functional violation — just a bit of confusing dead weight
  for a future maintainer wondering why a hook script exists with nothing wiring it up.
- `g-sales-prospect` still has **zero `SKILL.md`** — flagged as an open gap in an earlier session's
  audit note (2026-07-05 status block, spec 007), still unresolved. It works mechanically today only
  because `g-sales-engine/SKILL.md` shells out to `score.py`/`kpi.py` directly by file path rather
  than invoking it as a Claude Code skill — that may be an intentional "backend-only" design, but it
  hasn't been confirmed as a decision vs. an oversight.

## What actually does work (verified, not assumed)

- **57/57 pytest tests pass** — ran live, not read from a prior claim:
  `python3 -m pytest g-sales-prospect/ g-sales-pov/ -q` → `57 passed in 0.06s`.
- **Zero relative-filesystem-path violations** between sibling skill directories — the
  self-contained-skill convention (duplicate small shared code rather than `../sibling/scripts/`
  imports) held everywhere checked.
- **Zero author-personal path/credential leaks** — the `org/`-path and AWS-profile scrub from the
  original vendoring pass is still clean on re-check.
- **No stray `hooks.json`** anywhere in the vendored tree — the FR-014 skills-only decision's letter
  was followed correctly, even where a leftover script (Finding 4) suggests it wasn't followed in
  spirit everywhere.

## Recommended remediation (priority order)

1. **P0 — Global rewrite of every vendored skill's internal cross-references.** Not a targeted
   frontmatter patch this time: `g-intel-* → tvt-intel-*`, `g-sales-pack/pitch/distill/
   engagement-proposal → tvt-sales-*`, `g-create-* → tvt-create-*`, `g-os-* → tvt-os-*` (careful
   with substring collisions), `g-core-* → tvt-core-*`, bare `tavantize → tvt-tavantize`, bare
   `grill-me → tvt-grill-me`. Re-run Finding 2's grep after — it must return zero.
2. **P0 — Fix `g-sales-engine/SKILL.md` and `g-sales-pov/SKILL.md` the same way.** These keep their
   own `g-` prefix (correct, per FR-002 — they're 006's own code), but every *reference* to a
   vendored dependency inside them must point at the `tvt-` name, since that's the only name that
   will exist in an installer's package.
3. **P0 — Resolve `g-pm-jtbd`/`g-pm-grow`.** Either vendor as `tvt-pm-jtbd`/`tvt-pm-grow` (matches
   the established pattern; probably correct since the spine depends on them) or explicitly mark
   them "NOT VENDORED — external prerequisite" in `CAPABILITIES.md` with install instructions. Silent
   is the one option FR-013/SC-005 rule out.
4. **P1 — Actually run spec 007 User Story 1's own acceptance test.** A clean environment, install
   *only* this plugin, invoke one skill per category end-to-end. This exact test would have caught
   every finding above on day one; it should become a real repeatable script
   (`scripts/smoke-test-fresh-install.sh` or similar), not a one-time manual claim in a status block.
5. **P2 — Fix the stale `SKIP_PATH` constant** in `check_dep_liveness.sh`.
6. **P2 — Close out `g-sales-prospect`'s missing-`SKILL.md` question** — decide intentional vs. gap,
   stop re-flagging it as "not yet resolved" across sessions.
7. **P3 — Decide whether to keep the inert `judge_hook.sh`/`judge_runner.sh` files** bundled without
   their `hooks.json`, or drop them for clarity, since FR-014 already decided hooks aren't in scope.

## Remediation applied (2026-07-05, same day)

All P0/P1 items fixed and re-verified — not just claimed:

1. **Global cross-reference rewrite.** A script-driven, word-boundary-safe rename across all 40
   `tvt-*` skills + `g-sales-engine`/`g-sales-pov`: 436 substitutions in 61 files (first pass), plus
   41 more once `tvt-pm-jtbd`/`tvt-pm-grow` were added (below) — 477 total. Re-ran Finding 1 and
   Finding 2's exact grep commands afterward: **zero remaining stale references** in either router
   skill, and every one of the 10 remaining matches across the `tvt-*` tree was individually
   inspected and confirmed to be a legitimate non-bug (see item 4).
2. **`g-pm-jtbd`/`g-pm-grow` vendored** as `tvt-pm-jtbd`/`tvt-pm-grow` (Finding 3) — same pattern as
   the original 18: copied from `.claude/skills/`, scrubbed for `org/`-paths and personal
   identifiers (clean), stripped Gordon-OS-template bootstrap junk this copy carried (`PORTFOLIO.md`,
   `goal-weights.yaml`, `.claude/session-log.txt`), frontmatter renamed, internal cross-references
   fixed (41 substitutions). `CAPABILITIES.md`'s "Product / AI-opportunity loop" section now has a
   Status column like every other section — the silent gap is closed, not just documented as closed.
3. **Two generic collective mentions** (`` `g-intel-*` family ``, prose not caught by the exact-name
   rename map) fixed in `g-sales-engine/SKILL.md` and `tvt-create-explainer/SKILL.md`. Two
   self-referencing header comments in `tvt-create-explainer/assets/{render.js,explainer.css}`
   fixed for the same reason (a skill's own bundled asset still named itself `g-create-explainer`).
4. **Re-inspected every remaining match individually — none were bugs:**
   - `g-create-pdf`/`g-create-doc`/`g-create-xlsx` mentions in `tvt-core-write`/`tvt-create-explainer`/
     `tvt-sales-engagement-proposal` describe those skills' historical absorption of/relationship to
     skills already **explicitly out of scope** for this repo (spec 006 §"Explicitly out of scope") —
     not broken references to something this package needs.
   - `.claude-evals/*.json` inside `tvt-core-eval` are immutable historical eval records (a run
     snapshot), left untouched per the established convention of not editing point-in-time records.
   - `g-core-research` (in 5 `tvt-intel-*` frontmatter `depends_on:` lines + `tvt-pm-grow/references/
     grow-engine.md`) is a **pre-existing anomaly in the source gordon-os-marketplace content itself**
     — no `g-core-research`/`tvt-core-research` skill exists anywhere in either the source or this
     vendored copy (the actual core family is clarify/eval/extract/lookup/mcts/portfolio/write; the
     research skill lives in `g-os-cognitive`, not `g-core`). Predates this vendoring pass and this
     rename; flagged here rather than silently guess-fixed, since the correct target (`tvt-os-research`?
     something else?) isn't this session's call to make.
   - `tvt-os-loop/scripts/orchestrator.py`'s stale `g-os-cognitive`/`g-core` sibling-directory
     path-resolution comment: confirmed **already inert** — `source_freshness.py`, the module this
     fallback tries to import, was never vendored anywhere in this package (it lived in the source
     marketplace's `g-core/lib/`, which this repo never bundled). The function already returns `None`
     gracefully every time; fixing the path computation wouldn't change behavior since the target
     file doesn't exist regardless. Flagged, not fixed, for the same reason as the item above.
5. **Re-verified, not re-claimed:** `python3 -m pytest g-sales-prospect/ g-sales-pov/ -q` → still
   **57/57 passing** after every change above.

## Contrarian note on why this happened

The steelman for how this slipped through twice (once at vendoring, once at the "implementation
status" audit that found only the `g-sales-prospect` gap): every prior check optimized for the
*portability* risk (author-personal paths, credentials) because that was the explicitly named FR-003/
FR-004 concern. Nobody wrote a check for *cross-skill name resolution* because it wasn't named as a
risk anywhere — it's the same class of miss as "renamed a function, forgot the call sites," and it's
a predictable failure mode of a targeted rename script rather than a full-text find-replace. The fix
isn't just applying the P0 rewrite — it's adding Finding 2's grep as a permanent, cheap, deterministic
pre-publish check (line 1 of remediation item 1's re-verification) so this class of bug can't
reoccur silently on the next vendoring pass.
