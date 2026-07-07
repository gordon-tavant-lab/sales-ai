---
name: tvt-os-replay
version: 0.1.0
description: Re-runs a prior engine run against the workspace's currently checked-out
  skill versions, using its `traces/<YYYY>/<MM>/<run_id>/trace.jsonl` as the dispatch
  record. Pair with `git checkout <sha>` to bisect a regression that surfaced between
  runs (US9 / SC-018 / FR-046, FR-047). Trigger on "replay run", "rerun run_id", "git-bisect
  this regression", "/tvt-os-replay".
tier: A
pack_compat:
- '*'
eval:
  mode: score
  depth: light
layer: self-improvement
expected_impact: low
default_overhead: light
---
# tvt-os-replay — replay a prior run

Read `scripts/replay.py` for the implementation. The CLI is the canonical
entry point; this SKILL.md exists so Claude can surface replay capability via
the `Skill` tool and so the replay surface participates in the same trace +
provenance pipeline as the rest of the engine.

## When to invoke

- A regression appeared between two runs and the inspector wants to confirm
  whether code or LLM nondeterminism caused it.
- A reviewer is auditing a past run and wants to recompute it against today's
  skill versions to see what would have changed.
- A `git bisect` session is hunting for the commit that broke a fixture-bug
  scenario (SC-018).

## Inputs

- `--run-id` (required): the run id of the prior run. The CLI globs
  `traces/<YYYY>/<MM>/<run_id>/trace.jsonl` to locate it.
- `--brief` (optional): override the brief path. If omitted, the CLI reads
  `gordon_os.brief_path` from the original orchestrator span attributes.

## Outputs

A JSON object on stdout:

```
{
  "original_run_id": "...",
  "original_commit_sha": "<short HEAD at original run>",
  "original_skill_versions": ["tvt-intel-deep@0.1.0#sha256:...", ...],
  "replay_run_id": "...",
  "replay_trace": "traces/.../trace.jsonl",
  "replay_recommendation": "recommendations/..."
}
```

## Determinism contract

The orchestrator stamps every run's orch span with
`gen_ai.eval.commit_sha` and `gen_ai.skills.versions[]`. Replay reads these
from the original trace, so the JSON payload shows the original revision and
the replay revision side by side. Diffing the two trace.jsonl files is the
canonical way to inspect what changed between runs (G-VIII inspectable
state). The span tree **shape** (which skills ran, in what order, with what
ctx keys) is deterministic given the same brief + same `goal-weights.yaml`
+ same skill versions; the span **content** is not (LLM token sampling
remains nondeterministic — that's expected, not a regression).
