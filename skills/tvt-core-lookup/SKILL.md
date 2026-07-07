---
name: tvt-core-lookup
description: 'Core skill — the "connect the dots" + "what playbook applies?" engine.
  Given signals, findings, entities, or client context, cross-reference them against
  portfolio, intel files, daily briefs, and playbooks to surface connections, recurring
  patterns, conflicts, and best-fit AI solution patterns. A single multi-mode lookup skill
  covering cross-reference and pattern-match duties in one place.

  '
layer: kernel
modes:
- connections
- patterns
- conflicts
- playbook-match
trigger_phrases:
- cross reference
- cross-reference
- find connections
- what connects
- check against portfolio
- what playbook fits
- match pattern
- pattern match
- which pattern applies
- gap check
- find conflicts
- what overlaps
inputs:
- name: items
  type: list
  required: true
  description: Signals, findings, entities, or pain points to look up
- name: check_against
  type: list (portfolio|intel_files|daily_briefs|playbooks)
  required: false
  description: 'Which data sources to check. Default for connections/patterns/conflicts:
    [portfolio, intel_files, daily_briefs, playbooks]. Default for playbook-match:
    [playbooks] + built-in AI solution patterns.

    '
- name: mode
  type: enum (connections|patterns|conflicts|playbook-match)
  required: true
  description: What kind of lookup to perform
- name: sub_mode
  type: enum (match|apply|gap-check)
  required: false
  description: Sub-mode for playbook-match only (default = match)
- name: library_path
  type: text
  required: false
  description: Path to playbook library (default ${CLAUDE_PLUGIN_ROOT}/playbooks/)
outputs:
- name: connections
  type: structured-data
  description: Which item links to which engagement/signal (mode=connections)
- name: pattern_candidates
  type: list
  description: Themes appearing across 2+ sources (mode=patterns)
- name: conflicts
  type: list
  description: Timeline collisions, resource overlaps, contradictions (mode=conflicts)
- name: matches
  type: structured-data
  description: Ranked playbooks/patterns with fit scores and relevant excerpts (mode=playbook-match)
- name: gaps
  type: list
  description: Pain points with no matching pattern (mode=playbook-match, sub_mode=gap-check)
depends_on: []
consumed_by:
- tvt-core-extract(mode=signals)
- tvt-intel-flywheel
- tvt-sales-pack
expected_impact: medium
default_overhead: light
eval:
  mode: score
  depth: light
---
# Lookup

Multi-mode "connect the dots" and "what playbook applies?" engine. Four modes, one skill.

| Mode | Purpose |
|---|---|
| `connections` | Find how items relate to existing engagements, signals, people |
| `patterns` | Detect themes appearing across 2+ items or sources |
| `conflicts` | Surface contradictions, resource collisions, timeline clashes |
| `playbook-match` | Match context against AI solution patterns and playbook library |

---

## Shared Process

All modes follow this flow:

1. **Receive items** — signals, findings, entities, or pain points
2. **Load sources** — based on `check_against` or mode defaults:
   - `portfolio` → Read `PORTFOLIO.md`
   - `intel_files` → Scan `./sales-intel/*/*.md` (created in your current project directory) filenames + executive summaries
   - `daily_briefs` → Read last 7 days of `./sales-intel/daily/daily_intel_*.md`
   - `playbooks` → Scan `${CLAUDE_PLUGIN_ROOT}/playbooks/*.md` pattern names + built-in AI solution patterns
3. **Search** — for each item, search loaded sources for matches on:
   - Company names
   - People names
   - Technology/product names
   - Pain point themes
   - Timeline overlaps
4. **Classify** — route results through the active mode's logic
5. **Return** — structured results per mode's output format

---

## Shared Rules

- Don't force connections — "no connection found" is a valid result
- Pattern candidates require actual evidence (not just name similarity)
- Conflicts should include suggested resolutions, not just identification
- For efficiency, scan filenames and section headers before reading full files
- If checking against `intel_files`, read the Executive Summary section only (not full files) unless a match is found
- Never invent new AI solution patterns ad-hoc. If a new one is needed, propose it as a playbook first.
- If a pain point matches **Hybrid Rules + LLM**, always flag it — this is a recurring Tavant differentiator

---

## Mode: connections

**Purpose:** Find how items connect to existing engagements, signals, or people.

This is the default mode. For each item, check:

1. **PORTFOLIO.md** — Does this relate to an active engagement? Which tier? What's the current status?
2. **Intel files** (`./sales-intel/*`) — Do we have existing research on this entity or topic?
3. **Recent daily briefs** (`./sales-intel/daily/daily_intel_*.md`, last 7 days) — Was this mentioned before? Is it escalating?
4. **Playbooks** (`${CLAUDE_PLUGIN_ROOT}/playbooks/*`) — Does this match a known pattern?

### Output per item

```
- [Item]: Connects to → [Engagement/File/Signal]
  - Relationship: [how they connect]
  - Implication: [what the connection means for you]
```

### Output Format

```markdown
### Cross-Reference Results (connections)

**Items checked:** {count}
**Sources checked:** {list}
**Connections found:** {count}

#### Connections
| Item | Connects To | Relationship | Implication |
|---|---|---|---|
| [item] | [engagement/file] | [how] | [so what] |
```

---

## Mode: patterns

**Purpose:** Find themes appearing across 2+ items or 2+ data sources.

### Pattern Classification

| Count | Classification |
|---|---|
| 3+ clients/sources | **Confirmed pattern** — strong playbook candidate |
| 2 clients/sources | **Emerging pattern** — monitor, cite as supporting evidence |
| 1 source | **Not a pattern yet** — client-specific |

### Output Format

```markdown
### Cross-Reference Results (patterns)

**Items checked:** {count}
**Sources checked:** {list}

#### Pattern Candidates
| Theme | Seen In | Count | Classification | Playbook Candidate? |
|---|---|---|---|---|
| [theme] | [list of sources] | [N] | Confirmed/Emerging/Not yet | Yes/No |
```

---

## Mode: conflicts

**Purpose:** Find contradictions, resource collisions, or timeline conflicts.

### What to look for

- Same person or team committed to overlapping engagements
- Conflicting timelines (two deadlines in the same week)
- Contradictory signals (one source says expanding, another says cutting)
- Resource competition across engagements

### Output Format

```markdown
### Cross-Reference Results (conflicts)

**Items checked:** {count}
**Sources checked:** {list}

#### Conflicts
| Conflict | Between | Risk | Suggested Resolution |
|---|---|---|---|
| [description] | [entity A vs entity B] | [High/Medium/Low] | [resolution] |
```

---

## Mode: playbook-match

**Purpose:** Match client context against the pattern library (${CLAUDE_PLUGIN_ROOT}/playbooks/ + built-in AI solution patterns). Returns ranked matches with fit scores and relevant excerpts. The "what playbook applies here?" engine.

### Built-In AI Solution Patterns (Canonical)

These are Tavant's core AI solution archetypes. Every client pain point should map to one or more:

| Pattern | Description | Indicators | Tavant Capability |
|---|---|---|---|
| **Data Foundation** | Unify siloed data into a reliable intelligence layer | "our data is everywhere", data quality complaints, no single source of truth | Data & Analytics |
| **Hybrid Rules + LLM** | Combine deterministic business rules with LLM reasoning | Compliance-heavy domains, auditability needed, "AI can't override our policies" | Mortgage Domain AI, Knowledge.AI |
| **Intelligent Automation** | Automate repetitive decisions + exception handling | High-volume manual work, SLA pressure, staffing constraints | Agentic QE, Ops Pilot |
| **Predictive Intelligence** | Forecast risk, demand, or behavior | Underwriting, credit, fraud, capacity planning | Data Science Agent |
| **Agentic Workflow** | Multi-step autonomous task execution with human oversight | Complex end-to-end processes, orchestration needs, "messy middle" | DMA, App Modernizer |
| **AI Governance** | Measure, audit, and control AI in production | Regulatory pressure, risk aversion, "how do we know it's working" | AI Governance frameworks |
| **AI-Powered Product** | Embed AI into customer-facing products | Differentiation goals, competitor pressure, revenue expansion | Dev Studio, Knowledge.AI |

### Sub-mode: match (default)

Find best-fit patterns:

1. Read the context (pain points, challenges, signals)
2. Score each built-in AI pattern against the context (High/Medium/Low fit)
3. Scan `${CLAUDE_PLUGIN_ROOT}/playbooks/*.md` for matching playbooks
4. Return ranked list: pattern name, fit score, evidence from context, relevant playbook (if exists)

### Sub-mode: apply

Same as `match` but also extracts:

- The "How to Apply" section from matching playbooks
- Key messages and objection handling from playbooks
- Specific Tavant accelerator/tool to lead with

### Sub-mode: gap-check

Identify pain points in the context that DON'T match any existing pattern or playbook:

- These are candidates for new playbook creation
- Flag: "Pain point X has no matching playbook — consider creating one if seen at 2+ clients"
- Gap-check results should inform `tvt-core-write(type=playbook)` — if the same gap appears at 3+ clients, it's time to create a playbook

### Fit Scoring

| Score | Criteria |
|---|---|
| **High** | Tavant has delivered this pattern before at a comparable client. Direct evidence of capability. |
| **Medium** | Tavant has adjacent capability. Pattern fits but would require adaptation. |
| **Low** | Pattern matches the pain but Tavant would need to build or partner. |

### Output Format

```markdown
### Pattern Matches for [Company/Context]

| Rank | Pattern | Fit | Evidence | Playbook | Tavant Lead |
|---|---|---|---|---|---|
| 1 | [pattern] | High | [specific pain point that matches] | [playbook name or "none"] | [accelerator/tool] |

### Unmatched Pain Points (gap-check sub-mode)
| Pain Point | Why No Match | Recommendation |
|---|---|---|
| [pain] | [reason] | [create playbook / explore partner / skip] |
```

### playbook-match Rules

- Always return at least the top 3 matching patterns, even if fit is Medium/Low
- If a pain point matches **Hybrid Rules + LLM**, always flag it — this is a recurring Tavant differentiator
- The built-in patterns above are the CANONICAL list — don't invent new patterns ad-hoc. If a new one is needed, propose it as a playbook first.
- Gap-check results feed into `tvt-core-write(type=playbook)` for pattern creation
