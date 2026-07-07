# Rubric — Import Readiness (LLM judge)

**What this judges**: a single shipped skill, against spec 007 User Story 1 — *"Give a
Claude Code instance with only this plugin installed (no Workspace context) to someone
who isn't the author."* The deterministic half of this gate is
`tests/test_import_readiness.py` (C1–C12); do **not** re-litigate what it already measures
(dangling names, broken paths, persona greps). This rubric covers what greps cannot:
whether a stranger gets **first-run value**.

**When to run**: before any marketplace publish or version bump; after any wave that
rewrites SKILL.md bodies. Run via `tvt-os-judge` with this file as the rubric, one judge
per skill (batch of 40 → fan out; do not judge your own edits).

## Judge setup (per skill)

You are a Tavant fintech **salesperson**, not an engineer. You installed the
`tvt-sales-skills` plugin five minutes ago into an empty project directory. You have:
Claude Code, this plugin, your own pipeline notes, and public internet. You have **never
seen** the author's Workspace, PORTFOLIO.md, agent.db, DemoServer, or any `g-*` skill.
Read the skill's full directory (SKILL.md + references/ + scripts/), then score.

## Axes

### A1 — Picker discoverability (weight 0.20)
Would the model's skill picker fire this skill at the right moment from `name` +
`description` alone (claude.ai Desktop reads nothing else)?
- 1.0: description states what it does, when to trigger, and what comes out; trigger
  phrases are things a salesperson actually types.
- 0.5: accurate but vague; triggers assume author vocabulary ("morning brief",
  "the flywheel") without defining it.
- 0.0: description references a person, an unavailable system, or reads as internal notes.

### A2 — First-run executability (weight 0.35, the heart of the gate)
Walk the skill's happy path mentally as the persona. Count every step where you'd stall.
- 1.0: all required inputs are things the persona has or the skill fetches; outputs land
  in a stated, plugin-relative or cwd-relative location; scripts run with documented deps.
- 0.5: runs, but assumes undefined conventions (an output tree that's never created, a
  "tracker" that doesn't exist on a fresh machine) that a resourceful user can improvise.
- 0.0: any hard stall — a required input only the author possesses, a step that reads
  state no fresh install has, a script pointed at a path this package doesn't contain.

### A3 — Semantic self-containment (weight 0.25)
The deterministic gate catches literal dangling names; you catch **conceptual** ones.
- 1.0: every concept the skill leans on is defined in-package (its own SKILL.md,
  references/, or bundled playbooks).
- 0.5: leans on concepts defined elsewhere but guessable from context.
- 0.0: load-bearing concept is undefined in-package ("update the portfolio", "follow the
  demo commandments" with no bundled definition, workflows that only close via an absent
  skill).

### A4 — Output gate present (weight 0.20)
The eval mandate: does the skill verify its own output before handing it to the user?
- 1.0: an explicit closing verification/eval step (or `eval:` frontmatter + gate section)
  appropriate to the output type; factual outputs route through fact-checking.
- 0.5: a checklist exists but is advisory, mid-document, or skippable.
- 0.0: produces client-facing or numeric output with no verification step at all.

## Hard fails (score is irrelevant — verdict is BLOCK)

- **HF1**: the skill instructs invoking a skill, script, or file that does not exist in
  this package (report it — it means the deterministic gate has a blind spot).
- **HF2**: first-run requires author-only infrastructure with no documented fallback
  (DemoServer, agent.db, a specific person's inbox/calendar, private dashboards).
- **HF3**: the skill would emit client-confidential material (named-client war stories,
  internal pricing, personnel commentary) into a deliverable.
- **HF4**: following the instructions verbatim would write outside the user's project
  (absolute paths, `~/.claude` mutations) without asking.

## Scoring and verdict

`composite = 0.20·A1 + 0.35·A2 + 0.25·A3 + 0.20·A4`

Aligned with `tvt-os-judge` bands: **PASS ≥ 0.85**, **WARN 0.70–0.85**, **BLOCK < 0.70**
or any hard fail.

## Output format (per skill)

```
skill: <name>
A1: <score> — <one line of evidence>
A2: <score> — <one line of evidence, name the stall step if any>
A3: <score> — <one line of evidence>
A4: <score> — <one line of evidence>
hard_fails: [] | [HFn: <evidence>]
composite: <0.xx>
verdict: PASS | WARN | BLOCK
one_fix: <the single edit that most raises this skill's score>
```

## Package verdict (aggregation)

- Any skill BLOCK → package **BLOCK** (a marketplace install is judged by its worst
  first-run experience, and the router makes every skill reachable).
- ≥ 25% of skills WARN → package **WARN**.
- Else **PASS**.
Record the run as `docs/import-readiness-judge-<date>.md` with the per-skill table and
the package verdict. A publish needs: deterministic gate strict-clean **and** package
PASS here.
