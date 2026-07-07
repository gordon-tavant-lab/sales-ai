---
name: tvt-core-extract
description: 'Universal extraction engine — extracts signals, entities,
  patterns, or pain-point mappings from any text. One skill, four modes. Feed it raw
  information (emails, meeting notes, intel files, research outputs) and get back
  decision-ready structured intelligence. This is the core sense-making layer of the
  sales engine — raw information in, actionable intelligence out.

  '
layer: kernel
modes:
- signals
- entities
- patterns
- pain-points
trigger_phrases:
- /extract
- /extract-signals
- /extract-entities
- /find-patterns
- /map-pain-points
inputs:
- name: text
  type: text
  required: true
  description: "Raw text to extract from. Can be email, Teams, meeting notes, news,\
    \ intel files, research outputs, or any prose. Mode-specific notes:\n  signals\
    \    — inbox, Teams, meeting notes, client comms, news\n  entities   — intel files,\
    \ meeting transcripts, daily briefs, research\n  patterns   — 2+ client contexts\
    \ (intel files, summaries, notes)\n  pain-points — client challenges, discovery\
    \ notes, research findings\n"
- name: mode
  type: enum
  required: true
  values:
  - signals
  - entities
  - patterns
  - pain-points
  description: Which extraction mode to run
- name: active_engagements
  type: list
  required: false
  description: (signals) List of engagement names to watch for. Defaults to PORTFOLIO.md
    actives.
- name: company_name
  type: text
  required: false
  description: (pain-points) Company name for output labeling. Required when mode=pain-points.
outputs:
- name: signals
  type: structured-data
  description: (signals) Classified signals — New, Escalating, Recurring, Fading —
    with full treatment
- name: entities
  type: structured-data
  description: (entities) Prioritized entity list with type, context, and priority
    P0-P3
- name: patterns
  type: structured-data
  description: (patterns) Cross-client pattern analysis — confirmed, emerging, client-specific
- name: mapping
  type: structured-data
  description: (pain-points) Pain point → AI pattern → Tavant capability mapping
- name: entry_point
  type: text
  description: (pain-points) Recommended lead use case
- name: flywheel
  type: text
  description: (pain-points) Flywheel sequence if 3+ use cases identified
delegates_to:
- /tvt-core-lookup(mode=connections)
- /tvt-core-lookup(mode=playbook-match)
consumed_by:
- tvt-core-write(type=daily)
- tvt-core-write(type=intel)
- tvt-intel-deep
- tvt-intel-fanout
- tvt-sales-engagement-proposal
expected_impact: medium
default_overhead: light
eval:
  mode: score
  depth: light
---
# Extract — Universal Extraction Engine

One skill, four modes. Feed it raw text; get back structured, decision-ready intelligence.

| Mode | What it does | When to use |
|---|---|---|
| `signals` | Classify signals as New / Escalating / Recurring / Fading | Before daily intel, portfolio updates, inbox scans |
| `entities` | Extract researchable companies, people, platforms | After research, meeting notes, or intel outputs |
| `patterns` | Find recurring themes across 2+ client contexts | After batching research or completing multiple engagements |
| `pain-points` | Map client pains → AI solutions → Tavant capabilities | During presales, proposal writing, meeting prep |

---

## Mode: signals

Analyze text and classify every meaningful signal into four types. This is the core sense-making operation — raw information in, **decision-ready intelligence** out.

**Quality bar:** Every signal must chain: Signal → Implication → What Happens If We Act → What Happens If We Don't. No surface-level signal descriptions.

### Signal Taxonomy

| Type | Meaning | Examples |
|---|---|---|
| **New** | First appearance — no prior context | New client contact surfaces, new budget cycle announced, RFP opened, new exec hire |
| **Escalating** | Was present before, now stronger or more urgent | Exec escalated to CTO, deadline moved up, response overdue, budget approved |
| **Recurring** | Same theme appearing across 2+ clients or 2+ weeks | Governance demand at Anchor AND ICE, hybrid rules+LLM pattern re-emerging |
| **Fading** | Was active, now going silent | No comms from a key contact in 2+ weeks, initiative deprioritized, budget frozen |

### Output Format — Signals

Group signals by type. Omit any type with no signals.

```
### New Signals
**[Client / Context]:** [Specific description — names, dates, numbers, not vague summaries]
- Source: [email / Teams / news / meeting notes / job posting / LinkedIn]
- Strength: [Low / Medium / High] — [reasoning for rating]
- Implication: [What this means for your work — be SPECIFIC to the engagement, not generic]
- Potential: [If this plays out favorably, what's the upside? Revenue, relationship, strategic positioning?]
- If we act: [What happens if you move on this signal now]
- If we don't: [What happens if this is ignored — lost window, competitor advantage, relationship cooling]
- Action: [Specific action with owner and timing. "None — monitor until [trigger]" is valid.]
- **Deep-dive trigger:** [Yes/No] — [If yes, why this signal warrants a separate deep-dive doc]

### Escalating Signals
**[Client / Context]:** [What was the prior state → what changed → why it's escalating]
- Source: [source]
- Prior signal: [reference to when this first appeared, if known]
- Strength: [Low / Medium / High] — [reasoning]
- Implication: [What the escalation changes about our approach or timeline]
- Potential: [upside assessment]
- If we act: [specific outcome of action]
- If we don't: [specific consequence of inaction — deadline, competitor, relationship damage]
- Action: [Specific next step]
- **Deep-dive trigger:** [Yes/No — Escalating + money/timeline = usually Yes]

### Recurring Signals
**[Theme name]:** [Description of the pattern — what's the common thread?]
- Seen in: [Client A, Client B, ...]
- Recurrence count: [how many times / how many clients]
- Playbook candidate: [Yes / No] — [reason. 3+ clients = strong candidate]
- Pattern insight: [What does the recurrence tell us? Industry-wide pain? Tavant positioning opportunity?]
- Action: [Recommended next step — often "extract to playbook" or "use in next client pitch"]

### Fading Signals
**[Client / Context]:** [What was active → what went quiet → when was last contact]
- Source: [absence of expected communication / deprioritization signal / budget freeze]
- Strength: [Low / Medium / High] — [how concerned should you be?]
- Implication: [What silence means — cooling interest, internal blocker, competing priority, or just busy?]
- If we act: [re-engagement approach — specific, not "follow up"]
- If we don't: [risk of losing the account / opportunity window closing]
- Action: [Specific re-engagement step or "Accept fade — deprioritize"]
```

### Reading Between the Lines

Beyond explicit signals, flag these **implicit signals:**

- **Tone shifts:** Email went from casual to formal (or vice versa) — what changed?
- **Response time changes:** Was same-day, now 3+ days — cooling signal
- **CC changes:** Someone new was CC'd (escalation?) or dropped (sidelining?)
- **Language patterns:** "Exploring options" vs. "need to move forward" vs. "let me check internally" — read the buying temperature
- **Silence:** Missing an expected response is a signal. Flag it as Escalating with reason.
- **Budget language:** "What would this cost?" = interested. "Send me some ranges" = shopping. "Can you present to my VP?" = serious. "Let me socialize internally" = 50/50.

### Cross-Referencing

Delegates to: `/tvt-core-lookup(mode=connections)` — cross-references extracted signals against PORTFOLIO.md, existing intel files, and recent daily briefs.

1. Run `/tvt-core-lookup(mode=connections)` with `items=extracted_signals, check_against=[portfolio, intel_files, daily_briefs]` to find how each signal connects to existing engagements and prior intelligence.
2. Run `/tvt-core-lookup(mode=connections)` with `check_against=[portfolio, daily_briefs]` to detect recurring themes across 2+ clients.
3. Merge the cross-reference results into each signal's Implication and Action fields.

---

## Mode: entities

Extract every researchable entity from a piece of text — companies, competitors, partners, vendors, technology platforms, and key external people. Return a structured list ranked by research priority.

### Entity Types

| Type | What to Look For | Examples |
|---|---|---|
| **competitor** | Companies competing with the subject for the same customer or market | Tidalwave AI, Gateless, ICE Mortgage Technology |
| **partner** | Companies the subject integrates with or depends on | LendingPad, Freddie Mac, Fannie Mae |
| **vendor** | Technology/service providers to the subject | GoHighLevel, AWS, Salesforce |
| **prospect** | Companies that could be Tavant clients (mentioned in industry context) | Any lender, servicer, or fintech not already in PORTFOLIO.md |
| **platform** | Named technology platforms worth understanding | Encompass, Black Knight, Clara Rules |
| **person** | Key external individuals (not Tavant staff) with decision-making power | Dr. Ramesh Sarukkai, Adam Boyd |

### Extraction Process

1. **Read the full text** — identify every named entity that is NOT:
   - Tavant or Tavant employees (we already know them)
   - Generic terms (AI, machine learning, cloud computing)
   - Government agencies unless they're a prospect (CFPB, HUD = skip; Texas HHS = keep if prospect)

2. **Classify each entity** by type using the table above

3. **Check existing intel** — for each entity, check if `./sales-intel/{Entity}/` (in your current project directory) already exists
   - If yes → mark as `has_intel` and skip unless the text reveals NEW information worth updating
   - If no → mark as `needs_research`

4. **Assess research priority** based on:

| Priority | Criteria |
|---|---|
| **P0 — Research NOW** | Direct competitor to a Tavant client. Could displace us or block a deal. |
| **P1 — Research this week** | Potential Tavant client ($1M+ potential). Or vendor/partner whose capabilities matter for an active engagement. |
| **P2 — Research when convenient** | Interesting market player, worth understanding for competitive landscape. Not urgent. |
| **P3 — Note and move on** | Small player, niche, or tangential. Just record the name and what we know. |

5. **Capture context** — for each entity, note WHY it was mentioned and what we already know from the source text.

### Priority Decision Tree

```
Is this entity a direct competitor to a Tavant client in an active deal?
  → YES → P0

Could this entity become a Tavant client ($1M+ potential)?
  → YES → P1

Is this entity a vendor/partner we need to understand for an active engagement?
  → YES → P1

Is this entity shaping the market or competitive landscape?
  → YES → P2

None of the above?
  → P3
```

### Output Format — Entities

```markdown
## Entity Scan Results

**Source:** [name/path of the text scanned]
**Entities found:** [total count]
**New (needs research):** [count]
**Already tracked:** [count]

### P0 — Research NOW
| Entity | Type | Context from Source | Why P0 | Existing Intel? |
|---|---|---|---|---|
| [Name] | competitor | [1-2 sentence context] | [reason] | No |

### P1 — Research This Week
| Entity | Type | Context from Source | Why P1 | Existing Intel? |
|---|---|---|---|---|

### P2 — Research When Convenient
| Entity | Type | Context from Source | Why P2 | Existing Intel? |
|---|---|---|---|---|

### P3 — Note Only
| Entity | Type | Context from Source | Notes |
|---|---|---|---|
```

### Entity-Specific Rules

- **Platforms (Encompass, Black Knight, etc.)**: Don't research as companies unless they're potential Tavant clients. Note their capabilities as context for the subject company's tech stack.
- **People**: Only flag individuals who are (a) potential Tavant contacts at prospect companies, or (b) industry thought leaders whose positions matter for Tavant's narrative.
- **GSEs (Fannie, Freddie, Ginnie)**: Never flag as research targets. They're industry infrastructure. Note their relevance to the subject only.
- **Already-researched entities**: If intel exists and the source text adds nothing new, skip entirely. If the source text reveals something new (new product, leadership change, pivot), flag as "update needed" with the specific new information.

---

## Mode: patterns

Analyze multiple client contexts to surface recurring themes. The goal is to identify what appears across engagements — because a pain point at one major lender is an industry pain point, and an industry pain point is a Tavant accelerator opportunity.

### What to Look For

| Category | Examples |
|---|---|
| **Shared pain points** | Same problem at 2+ clients (e.g., AI governance, data silos) |
| **Shared objections** | Same pushback (e.g., "AI can't override compliance rules") |
| **Shared solution patterns** | Same architecture working across clients (e.g., hybrid rules+LLM) |
| **Shared buyer profiles** | Same title, same concern (e.g., CDO worried about data quality) |
| **Shared industry dynamics** | Regulatory driver, market shift affecting multiple clients |

### Process

1. Read each client context provided (intel files, meeting notes, or summaries)
2. Extract key themes from each client
3. Cross-reference — identify themes appearing in 2+ clients
4. Score recurrence: 2 clients = emerging, 3+ clients = confirmed pattern
5. For confirmed patterns, assess playbook readiness
6. Always check `${CLAUDE_PLUGIN_ROOT}/playbooks/` before declaring a new pattern — it may already exist

### Output Format — Patterns

```
## Cross-Client Pattern Analysis
Clients analyzed: [list]
Date: [date]

### Confirmed Patterns (3+ clients)

**[Pattern Name]**
- Seen in: [Client A, B, C]
- Description: [What the pattern is — specific and concrete]
- Tavant's current approach: [How we're solving it now — consistent? ad hoc?]
- Playbook readiness: [Ready to extract / Needs more evidence / Already exists at ${CLAUDE_PLUGIN_ROOT}/playbooks/]
- Recommended action: [Write playbook / Update existing / Document case study]

### Emerging Patterns (2 clients)

**[Pattern Name]**
- Seen in: [Client A, B]
- Description: [...]
- Watch for: [What would confirm this pattern at a 3rd client]

### Client-Specific (not yet a pattern)
- [Client]: [unique theme] — not yet seen elsewhere
```

---

## Mode: pain-points

Transform raw client context (pain points, business challenges, operational problems) into a structured mapping of AI opportunities and Tavant fit. This is the core translation layer between "what the client suffers" and "what you pitch."

**Requires:** `company_name` input.

### AI Solution Pattern Library

Delegates to: `/tvt-core-lookup(mode=playbook-match)` — matches pain points against the canonical pattern library and returns ranked fits with scores.

1. Run `/tvt-core-lookup(mode=playbook-match)` with `context=pain_points, mode=match` to get ranked pattern matches with fit scores.
2. Use the returned matches to populate the mapping table below.
3. For presales use, run `/tvt-core-lookup(mode=playbook-match)` with `context=pain_points, mode=apply` to also get playbook excerpts and key messages.

The 7 canonical AI solution patterns:

| Pattern | Description | Indicators |
|---|---|---|
| **Data Foundation** | Unify siloed data into a reliable intelligence layer | "our data is everywhere", "we can't trust the numbers", data quality complaints |
| **Hybrid Rules + LLM** | Combine deterministic business rules with LLM reasoning | Compliance-heavy domains, "AI can't override our policies", auditability needed |
| **Intelligent Automation** | Automate repetitive decisions + exception handling | High-volume manual work, SLA pressure, staffing constraints |
| **Predictive Intelligence** | Forecast risk, demand, or behavior | Underwriting, credit, fraud, capacity planning |
| **Agentic Workflow** | Multi-step autonomous task execution | Complex end-to-end processes, orchestration needs |
| **AI Governance** | Measure, audit, and control AI in production | Regulatory pressure, risk aversion, "how do we know it's working" |
| **AI-Powered Product** | Embed AI into customer-facing products | Differentiation goals, competitor pressure, revenue expansion |

### Tavant Capabilities Reference

- **Knowledge.AI** — enterprise knowledge management and intelligent search
- **Legacy Modernization** — modernizing aging platforms with AI
- **Agentic QE** — AI-driven quality engineering and testing
- **Data & Analytics** — data foundations, pipelines, BI
- **AI Governance** — responsible AI frameworks, measurement
- **Mortgage Domain AI** — LOS integration, underwriting automation, servicing intelligence

### Output Format — Pain Points

```
## Pain Point → AI Solution Mapping: [Company]

| # | Pain Point | AI Pattern | Tavant Capability | Fit Score | Notes |
|---|---|---|---|---|---|
| 1 | [verbatim or paraphrased pain] | [pattern name] | [Tavant service/accelerator] | High/Med/Low | [key risk or insight] |

## Recommended Entry Point
[Which use case to lead with, and why — consider: highest fit, lowest risk, fastest time-to-value, most senior sponsor]

## Flywheel Sequence (if multi-use-case)
[How use cases build on each other — reference ai-use-case-flywheel.md pattern if applicable]

## Risks & Objections
[Anticipated pushback and how to handle it]
```

---

## Shared Rules (all modes)

1. **Specificity over generality.** Names, dates, numbers, dollar amounts. "Revenue risk" is bad. "If we don't respond to the client's request by Friday, the QE opportunity ($400K est.) may route to a competitor who presented last week" is good.
2. **Never fabricate.** If the text doesn't contain enough information, say so. Don't invent signals, entities, or patterns to fill a template.
3. **Chief of staff quality.** Every output must be decision-ready. The user should be able to read it and act immediately without further research.
4. **Always check existing context.** Before flagging something as new, check PORTFOLIO.md, existing intel files, and recent daily briefs. Don't rediscover what's already known.
5. **Flag playbook candidates.** Any theme recurring across 3+ clients is a strong playbook candidate — flag it explicitly in any mode.
6. **Deep-dive triggers (signals mode).** Flag any signal that is (a) New + High Strength, (b) Escalating + involves money/timeline, or (c) Recurring across 3+ clients as **[DEEP-DIVE TRIGGER]**.
7. **A missing expected response is ALWAYS a signal** (signals mode) — flag it as Escalating with "last expected response: [date], now [X days] overdue."
8. **Patterns need names** (patterns mode) — make them action-oriented and memorable (e.g., "Governance-First AI Adoption", not "clients want governance"). Don't force patterns; if something only appears once, list it as client-specific.
9. **Always recommend an entry point** (pain-points mode) — don't leave it as "TBD."
10. **Hybrid Rules + LLM is a Tavant strength** (pain-points mode) — always flag pain points that map to this pattern.
11. **If 3+ pain points map, build a flywheel** (pain-points mode) — structure as a flywheel sequence, not isolated use cases.
12. **Fit scoring** (pain-points mode): High = Tavant has delivered this before; Medium = adjacent capability; Low = new territory.
13. **Be willing to say "nothing here"** — if the text is genuinely noise, explain why. An empty extraction is better than a forced one.

## Chaining

Outputs from this skill feed directly into:

| Mode | Downstream Skills |
|---|---|
| `signals` | `tvt-core-write(type=daily)` |
| `entities` | `tvt-intel-fanout`, `tvt-intel-deep`, `tvt-core-portfolio(op=patch)` — add prospect to Tier 3 |
| `patterns` | `tvt-core-write(type=playbook)` |
| `pain-points` | `tvt-core-write(type=intel)`, `tvt-sales-engagement-proposal`, `tvt-intel-deep` |
