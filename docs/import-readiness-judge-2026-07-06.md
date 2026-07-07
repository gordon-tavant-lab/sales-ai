# LLM Judge Run — import readiness calibration sample, 2026-07-06

Rubric: `rubrics/import-readiness.md`. Three skills judged by independent judges under
the fresh-installer persona (Tavant salesperson, plugin-only install, empty directory).
Purpose: calibrate the rubric and hunt deterministic-gate blind spots (HF1 requires
judges to report them). Full 40-skill run is due before publish.

## Package verdict: BLOCK (3/3 sampled skills BLOCK)

| Skill | A1 | A2 | A3 | A4 | Composite | Verdict | Hard fail |
|---|---|---|---|---|---|---|---|
| g-sales-engine | 0.5 | 0.5 | 0.5 | 0.5 | 0.50 | BLOCK | HF1: cites `specs/006-g-sales-engine/spec.md` 8× — not shipped |
| tvt-intel-deep | 0.0 | 0.0 | 0.0 | 0.5 | 0.10 | BLOCK | HF1: Step 1 delegates to `g-research` — doesn't exist in package |
| tvt-core-eval | 0.0 | 0.5 | 0.5 | 1.0 | 0.50 | BLOCK | HF1: requires `~/.claude/eval-policy.yml` + workspace constitution — neither ships |

## Highest-value evidence (beyond the deterministic gate's reach)

- **g-sales-engine**: the judge *executed* the documented commands — `score.py` works
  first-try, but `kpi.py --opportunities-file` against the package's own
  `opportunities.example.json` returns `{"error": "'stage'"}`; kpi.py needs a different
  record shape (stage/amount/created_date) documented only inside the script. Also:
  g-sales-pov's provocations library ships empty ("until [the author] writes the first
  3-5"), so the router's "build a POV" path yields no content on first run.
- **tvt-intel-deep**: the entire research method (37 queries, dimensions A–I) lives only
  in the absent `g-research` SKILL.md — the skill cannot start. Never routes its factual
  output through `tvt-intel-factcheck` despite it shipping in the same package.
- **tvt-core-eval**: A4 = 1.0 is the calibration proof the rubric can reward — `eval:
  mode: exempt` with rationale is exactly right for the measurement primitive. Its
  failures are the enforcement layer (`~/.claude/eval-policy.yml`, constitution,
  g-ai-loop/g-ops-morning composition examples) — all author-machine concepts.

## Gate blind spots the judges caught → status

| Blind spot | Fix | Status |
|---|---|---|
| `specs/NNN-...` outer-Workspace doc paths | C5 pattern added | closed (7 findings) |
| `~/.claude/` machine state (eval-policy.yml, CLAUDE.md) | C5 pattern added | closed (11 findings) |
| `.specify/` constitution paths | C5 pattern added | closed (4 findings) |
| single-segment names (`g-research`, `g-core`, `g-portfolio`) | token regex relaxed + family-glob/plugin-name exclusions | closed (+6 C3 findings) |
| `kpi.py` fixture-shape mismatch | not grep-detectable; belongs to Wave 3's script tests | open — tracked here |
| `.claude-evals/` fixtures still say `"skill": "g-core-eval"` | data files out of C3's md-only scan | open — accept or extend C3 |

## Rubric calibration notes

- Score spread behaved (0.10–0.50 across genuinely different quality levels; A4 spread
  0.5–1.0), and every hard fail cited quotable evidence — keep the rubric as-is.
- Judges converge with the deterministic gate on the same root causes (persona leak,
  dangling names) without being told about the baseline — good independence signal.
- Expect verdicts to flip to WARN/PASS only after Waves 1b–2; re-run the full catalog
  then, and after that at every version bump.
