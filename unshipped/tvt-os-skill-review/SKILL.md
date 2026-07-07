---
name: tvt-os-skill-review
description: Review queue manager for Tier-B skill candidates emitted by the engine.
  Lists pending candidates, shows diffs against existing skills, approves (promotes
  to .claude/skills/ + auto-commits) or rejects (removes from queue). Tier-B candidates
  are routed here whenever a skill emission carries requires/mcp_tool_registrations/secret_references
  or eval_mode=gate (per FR-026b). Trigger on "review skill queue", "approve skill",
  "skill review", "/tvt-os-skill-review".
tier: B
pack_compat:
- '*'
eval:
  mode: gate
  depth: standard
layer: self-improvement
expected_impact: medium
default_overhead: standard
---
# tvt-os-skill-review

Human gate for Tier-B skill candidates. Tier-B skills are NEVER auto-committed
- they land in `state/skill_review_queue/<hash>/` and wait here until a human
explicitly approves or rejects them (FR-026a).

## When to invoke

- An engine run emits a skill candidate that the classifier routes to
  Tier-B (i.e. the frontmatter has non-empty `requires`,
  `mcp_tool_registrations`, `secret_references`, or `eval_mode: gate` per
  FR-026b).
- The user asks to "review the skill queue", "approve a skill candidate",
  "see pending skills", or runs `/tvt-os-skill-review`.
- After a US5 run-driven emission cycle, before declaring the run done.

## How to invoke

All operations route through `scripts/review.py`:

```bash
# List every pending Tier-B candidate (short-hash, name, emitted_at).
python scripts/review.py list

# Inspect a candidate (full SKILL.md + unified diff vs any existing skill
# of the same name). Accepts either the full sha256:<hex> or a hex prefix.
python scripts/review.py diff <hash>

# Promote the candidate to .claude/skills/<name>/SKILL.md. Auto-commits when
# inside a git repo (use --no-auto-commit to skip).
python scripts/review.py approve <hash>

# Remove the candidate from the queue without promoting.
python scripts/review.py reject <hash>
```

Always run `diff` before `approve`. The diff is the review.

## Safety contract

- Tier-B candidates are NEVER auto-committed. Only an explicit
  `approve <hash>` call promotes them to `.claude/skills/<name>/`.
- `reject <hash>` is non-destructive to any existing skill of the same
  name - it only removes the queue entry. The existing skill stays put.
- Approval is the only path that mutates `.claude/skills/`. The CLI rejects
  unknown hashes with exit code 1 - it will not silently no-op.
- This skill itself declares `eval_mode: gate` so every invocation runs
  through `tvt-core-eval gate` at `standard` depth before completing.
