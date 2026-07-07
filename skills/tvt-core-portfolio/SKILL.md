---
name: tvt-core-portfolio
description: Core skill — unified portfolio state manager. Reads, scores,
  and patches PORTFOLIO.md through a single interface. Use standalone (/tvt-core-portfolio
  score) or as a pipeline step in compounds. Four operations — read, score, patch,
  read-and-score.
layer: kernel
trigger_phrases:
- portfolio status
- score the portfolio
- update portfolio
- how are my accounts
- portfolio health
inputs:
- name: op
  type: enum (read|score|patch|read-and-score)
  required: true
  description: What to do with the portfolio
- name: patch_changes
  type: list
  required: false
  description: Specific changes to apply (when op=patch)
- name: scoring_context
  type: text
  required: false
  description: Recent signals and daily intel for scoring context
outputs:
- name: state
  type: markdown
  description: Current portfolio state (for read operations)
- name: health
  type: markdown
  description: Scorecards, attention queue, nudges (for score operations)
- name: confirmation
  type: text
  description: What changed (for patch operations)
depends_on: []
consumed_by:
- g-ops-morning
- g-ops-weekly
expected_impact: medium
default_overhead: light
eval:
  mode: score
  depth: light
---
# Portfolio

The single interface for all PORTFOLIO.md operations. Combines reading, health scoring, and surgical patching into one skill.

## Operations

### `read` — Parse Portfolio State

Read `PORTFOLIO.md` and return structured data. ALSO load the workspace people directory and active follow-ups state (Path C shim wire-in, 2026-05-17):

```
- engagements: list of {name, tier, stage, revenue, owner, next_action, due, status_emoji}
- waiting_on: list of {item, who, since, follow_up_date, context}
- priorities: ordered list of this week's priorities
- key_dates: list of {date, event, prep_needed}
- signals: {active: list, fading: list}
- health_summary: {total_active, research_ready, blocked, overdue, revenue, q2_targets, touchpoints_7day}

# Path C shim wire-in:
- people: list of {id, name, role, org, last_touched, sensitivity} from intel/people/INDEX.md
  (empty list if INDEX.md is missing or only contains the empty-state placeholder row)
- follow_ups:
    active: list of {id, title, owner, priority, status, due, source} from state/follow_ups/active.yaml
    counts_by_priority: {urgent, today, tomorrow, week, month, quarter}
    counts_by_status: {open, in_progress, blocked}
  (empty if state/follow_ups/active.yaml is missing or [])
```

Path C contracts: `intel/people/SCHEMA.md` and `state/follow_ups/SCHEMA.md`. The `read` operation is read-only — it does not regenerate INDEX.md (that's `/g-ops-close`'s job) or auto-roll priorities (that's `/g-ops-morning` and `/g-ops-close`).

### `score` — Health Assessment

Score each active engagement across 5 dimensions. Requires `scoring_context` (recent daily intel or signals).

#### Health Dimensions

| Dimension | Green | Yellow | Red |
|---|---|---|---|
| **Momentum** | Activity in last 7 days | Activity in last 14 days | Stale 15+ days |
| **Next action** | Clear, owned, dated | Defined but undated | Missing or blocked |
| **Waiting on** | Not blocked | Waiting ≤7 days | Waiting 8+ days or overdue |
| **Revenue signal** | Committed or close | TBD but engaged | No signal, fading |
| **Relationship** | Active two-way comms | One-way, you pushing | Silent |

#### Score Output

```markdown
## Portfolio Health — {Date}

### Engagement Scorecards

**{Engagement}** ({Tier})
- Momentum: {emoji} {reason}
- Next action: {emoji} {what + who}
- Blocked/waiting: {emoji} {what, since when}
- Revenue: {emoji} {signal}
- Relationship: {emoji} {last interaction}
- **Overall: {emoji}**

---

### Attention Queue (ranked by urgency)
1. {Engagement} — {why now}

### Waiting-On Nudges
- {Item} — waiting on {who} since {date} — {follow-up action}

### Portfolio-Level Signals
- {Cross-engagement pattern or risk}

### Suggested Priority Order
1. {Engagement + specific action}
```

#### Scoring Rules
- Tier 1 engagements rank above Tier 2+ unless Tier 2 has an imminent deadline
- Research-only (Tier 3) don't get health scores — just flag if stale 30+ days
- Any "Waiting On" item overdue 7+ days = automatic Yellow
- Any engagement with no activity 15+ days = automatic Red on momentum

### `patch` — Surgical Update

Apply specific changes to `PORTFOLIO.md`. Never rewrites the whole file.

#### What Can Be Patched

| Section | When to Update |
|---|---|
| Engagement status row | Stage, next action, due date, or status emoji changed |
| Waiting On table | New item added, existing resolved, follow-up date updated |
| This Week's Priorities | Reordered or new item surfaced |
| Key Dates | New event or existing updated |
| Active Signals | New signal, promotion from Fading, or removal |
| Fading Signals | Added or removed |
| Portfolio Health Summary | Count or revenue figure changed |

#### Patch Process
1. Read current `PORTFOLIO.md`
2. Identify exactly which rows/cells/bullets need to change
3. State changes explicitly before applying
4. Apply only those changes via targeted edits
5. Update the `> Last updated:` timestamp
6. Confirm exactly which sections were updated

#### Status Emoji Key
| Emoji | Meaning |
|---|---|
| 🔴 | Urgent / at risk / due imminently |
| 🟡 | Needs attention / waiting / behind |
| 🟢 | On track / active / healthy |
| ⚪ | Dormant / research-only / not started |

### `read-and-score` — Combined Operation

Most common usage (especially for weekly reviews). Equivalent to `read` followed by `score`, but more efficient — reads once, scores in the same pass.

## Rules

- **Never** rewrite the whole PORTFOLIO.md — always patch surgically
- Always update the `Last updated` timestamp on any write operation
- Resolved "Waiting On" items: remove from table, don't leave as resolved
- New engagements go to the correct tier — don't misplace for convenience
- If in doubt about a change, ask before patching — incorrect patches corrupt the source of truth
- After any patch, confirm to the user exactly what changed
