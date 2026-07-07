---
name: tvt-core-write
description: Universal writer — produces any canonical output file (daily
  intel, client intel, playbook, signal deep-dive, presales artifact) with built-in
  quality validation. Replaces 7 separate skills with a single multi-mode writer.
  Every file goes through create/update/append mechanics and automatic quality gate
  before being declared done.
layer: kernel
type: daily|intel|playbook|deep-dive|presales
inputs:
- name: type
  type: enum (daily|intel|playbook|deep-dive|presales)
  required: true
  description: Which output type to produce — determines template, file path, and
    quality profile
- name: content
  type: structured-data
  required: true
  description: The content payload — signals for daily, research findings for intel,
    pattern for playbook, signal for deep-dive, artifact spec for presales
- name: client_name
  type: text
  required: false
  description: Client/company name (required for intel, deep-dive, presales)
- name: mode
  type: enum (create|update|append|patch)
  required: false
  description: File write mode — defaults per type (create for new, update for living
    docs, append for same-day daily)
- name: artifact_type
  type: enum (executive-brief|use-case-framework|discovery-prep|proposal-narrative|workshop-agenda)
  required: false
  description: Presales sub-type (required when type=presales)
- name: changelog_entry
  type: text
  required: false
  description: What changed (added to changelog on update/patch)
outputs:
- name: file_path
  type: text
  description: Actual path written
- name: action_taken
  type: text
  description: created|updated|appended|patched
- name: quality_grade
  type: text
  description: PASS / PASS_WITH_GAPS / FAIL
depends_on: []
consumed_by:
- g-ops-morning
- tvt-intel-deep
- tvt-intel-fanout
- tvt-intel-flywheel
- tvt-sales-pack
trigger_phrases:
- write daily
- morning brief
- write intel for [client]
- research [client]
- create playbook
- extract playbook
- deep dive on [signal]
- unpack [topic]
- draft presales for [client]
- executive brief for [client]
- discovery prep for [client]
eval:
  mode: gate
  depth: standard
expected_impact: high
default_overhead: standard
---
# Universal Writer

Produces any canonical output file with built-in quality validation. One skill, five output types, consistent file mechanics, automatic quality gate.

**Quality bar:** Every output must meet **Chief of Staff level** — synthesized, substantive, decision-ready.

---

## File Mechanics (All Types)

Shared file I/O logic applied before and after writing content.

### Write Modes

#### `create` — New file
1. Resolve path variables: `{Client}` → company name, `{Date}` → YYYY-MM-DD, `{Month}` → "April", `{Year}` → "2026"
2. Check if file already exists
   - If exists: **error** unless caller specifies `--force`
   - If not: write the file
3. Confirm: "Created: {path}"

#### `update` — In-place update of existing file
1. Read the existing file
2. Replace content while preserving structure
3. Update the `> Last updated:` timestamp at the top (if present)
4. If file has a `## Changelog` section, append the changelog_entry with today's date
5. Confirm: "Updated: {path} — {changelog_entry}"

#### `append` — Same-day addition
Used for daily files when a second briefing happens on the same day.
1. Check if file for today exists
   - If not: create normally
   - If exists: create a new file with `_pm`, `_update`, or `_evening` suffix
2. Suffix determined by time of day or caller preference
3. Confirm: "Appended: {path}"

#### `patch` — Surgical section-level edit
Used for PORTFOLIO.md and other canonical files that should never be fully rewritten.
1. Read the existing file
2. Apply only the specific section changes provided
3. Update the `> Last updated:` timestamp
4. Confirm exactly which sections were modified

### Timestamp Format

```
> **Last updated:** YYYY-MM-DD (context note — e.g., "Evening — after the client call")
```

### Changelog Format

```markdown
## Changelog

| Date | Change | Source |
|---|---|---|
| 2026-04-10 | {changelog_entry} | {calling skill or "manual"} |
```

### File Mechanics Rules
- Never write to a path outside the workspace root
- Always resolve path variables before writing
- For `update` mode, the file MUST exist — error if it doesn't
- For `patch` mode, state changes explicitly before applying — an incorrect patch corrupts the source of truth
- Changelog entries must be specific: "Added Adam Boyd to decision-maker map" not "Updated file"

---

## Built-In Quality Gate (All Types)

Every write automatically validates the output before declaring done. This is NOT a separate step — it is the final phase of every write operation.

### Process

1. Identify the output type
2. Load the matching quality profile (see type sections below for dimensions)
3. Check each dimension against the written content
4. For each FAIL: provide specific remediation ("Missing: financial estimates — add a range with methodology referencing comparable deals")
5. Return overall grade:
   - **PASS** — all dimensions met
   - **PASS_WITH_GAPS** — 80%+ met, gaps are non-critical (flagged to the user)
   - **FAIL** — critical dimensions missing

### On FAIL
1. Automatically remediate the failing dimensions
2. Re-validate
3. If still FAIL after 2 remediation attempts → surface to the user: "Quality gate failed on [dimensions]. Here's what I tried. You need to decide: accept as-is, provide missing info, or skip."

### Anti-Pattern Detection

Flag these automatically in any output:
- **Generic filler:** "The company faces challenges typical of the industry" → DELETE and replace with specifics
- **TBD fields without methodology:** Never leave financial estimates as "TBD" — always provide a range with reasoning
- **"Schedule a meeting" as the first move:** Replace with specific outreach plan (who, what channel, what hook, what agenda)
- **Isolated findings with no connections:** Every finding must connect to at least one other finding or portfolio signal
- **Missing disqualification criteria:** Every intel file must say what would make this a bad deal
- **Missing timing windows:** Every opportunity must have a "window" — when it opens, closes, what happens if missed

---

## Type: `daily`

### File Path
```
./sales-intel/daily/daily_intel_YYYY-MM-DD.md
```
(created in your current project directory) Use today's date. Never overwrite — use `_update` or `_pm` suffix for same-day additions.

### Required Schema

```markdown
# Daily Intelligence — {YYYY-MM-DD}, {Day of Week}

## Portfolio Health Dashboard

| Engagement | Health | Change | Pipeline Value | Key Signal |
|---|---|---|---|---|
| [Name] | [Green/Yellow/Red] | [Up/Down/Flat] | [$est] | [1-line: what's driving the rating] |

**Portfolio total (probability-weighted):** ${total}

---

## Lead Story
{Pick the single most important signal today. Give it 2-3 paragraphs of real analysis:}
- What happened (specifics: who, what, when)
- Why it matters (implications for the engagement AND the portfolio)
- What you should do about it (specific action, not "monitor")
- What happens if you don't act (stakes/consequences)
- Cross-portfolio connections (does this affect other engagements?)

{If a signal warrants even deeper analysis, flag: **[DEEP-DIVE RECOMMENDED]** — this triggers a separate doc via type=deep-dive}

---

## Morning Scan — {HH:MM AM/PM ET}

### Action Required

{Numbered list. Each item is decision-ready:}
1. **[URGENCY: Critical/High/Medium] [Topic]** ([source])
   - From: [name and title]
   - Context: [2-3 sentences — include tone shifts, response time patterns, political signals]
   - **Decision needed:** [Yes/No]
   - **If yes — Options:**
     - (A) [Option with trade-off]
     - (B) [Option with trade-off]
   - **Recommendation:** [(A/B) because ...]
   - **If no — Monitor until:** [date or trigger event]

### Groups Intelligence
- **[Team/Channel]**: [Signal — include what's NOT being said if notable. "Tavant AI channel: no mention of Onity demo despite it being tomorrow — possible misalignment or low visibility"]

### Today's Schedule
- **[HH:MM AM/PM] ([duration])** — [Meeting name] ([platform])
  - **Prep needed:** [Yes: pull X from intel file, review Y / No]
  - **Objective:** [What you need to walk out with]
  - **Watch for:** [Political signals, budget cues, champion behavior to track]

### Tasks Due Today
- [Task with context — not just the task name but why it matters today]

### Teams Updates
- **[Channel/Person]**: [Signal — include reading between the lines: tone shifts, delayed responses, who was CC'd/dropped, escalation patterns]

---

## Intelligence Captured Today

{Structured signal table — every signal gets full treatment:}

| Signal | Type | Client | Strength | Implication | Decision Needed | Action |
|---|---|---|---|---|---|---|
| [Headline] | [New/Escalating/Recurring/Fading] | [Client] | [H/M/L] | [What this means — specific, not generic] | [Y/N] | [Specific action or "Monitor: next check [date]"] |

### Cross-Portfolio Connections
{REQUIRED section. Connect the dots across engagements:}
- "[Signal A] + [Signal B] = [implication]. For example: a client's QE expansion + a second client's staffing timeline = potential resource conflict next month. Sequence recommendation: [specific]"
- "[Pattern]: this mirrors what happened at [other client] — [what we learned there applies here]"

### Insider Insights & Dirt
{Subtle signals that require reading between the lines:}
- **Tone shifts:** [Who's getting formal? Who's getting casual? What changed?]
- **Response patterns:** [Who went from same-day to 3-day replies? Cooling signal.]
- **Political signals:** [New CCs, dropped CCs, escalation to exec, "looping in my boss"]
- **Budget signals:** [Asked for pricing = serious. Asked for "ranges" = shopping. Asked for references = near-decision.]
- **Silence signals:** [Expected response from X by Y — didn't come. What does that mean?]

---

## Portfolio Signals
{Only if any signal changes a PORTFOLIO.md engagement}
- **[Engagement]**: [What changed] → [Recommended PORTFOLIO.md update with specific field changes]

---

## Top 3 Actions Today
1. **[Most critical — specific, owned, timed]**
   - Why #1: [why this beats everything else for today]
   - Done when: [specific completion criteria]
2. **[Second priority]**
   - Why #2: [reasoning]
   - Done when: [criteria]
3. **[Third priority]**
   - Why #3: [reasoning]
   - Done when: [criteria]

---

## Deep-Dive Triggers
{List any signals flagged for separate deep-dive analysis}
- [ ] [Signal] — Reason for deep-dive: [why this needs more than a daily-brief-level treatment]
```

### Daily-Specific Rules
1. **Decision-ready, not just informative.** Every action item must end with "Decision needed: Yes/No" and if yes, present options with trade-offs and a recommendation.
2. **Cross-portfolio connections are mandatory.** At least one entry, even if "No cross-portfolio implications today."
3. **Portfolio Health Dashboard is mandatory.** Every active engagement gets a row with justified health ratings.
4. **Lead Story is mandatory.** If truly nothing happened, say so explicitly.
5. **Include insider reads.** Interpret tone, timing, silence, and political dynamics.
6. **Top 3 must be genuinely prioritized** with reasoning. Not 5 things crammed into 3.
7. **10-15 min read target.** Substantive but not bloated.
8. **Flag deep-dives.** New + High Strength, or Escalating + money/timeline, or Recurring across 3+ clients → **[DEEP-DIVE RECOMMENDED]**.
9. Write in past tense for captured intelligence, present tense for actions and recommendations.
10. After saving, confirm path with a 3-line summary: Lead story, portfolio health change, and top action.

### Daily Quality Dimensions
| Dimension | Requirement |
|---|---|
| Decision assessments | Every signal has Decision Needed: Yes/No |
| Cross-portfolio | At least 1 cross-engagement connection |
| Health dashboard | Every active engagement has 1-line health |
| Lead story | Top signal gets 2-3 paragraph treatment |
| Insider reads | At least 1 tone/silence/political observation |

---

## Type: `intel`

### File Path
```
./sales-intel/{Client}/{Client}_Client_Intel_{Month}_{Year}.md
```
Example: `./sales-intel/Anchor_Loans/Anchor_Loans_Client_Intel_April_2026.md`

**Living doc model:** If a file already exists for the client, UPDATE it — don't create a duplicate. Add a changelog entry. Monthly, regenerate the Executive Summary at the top.

### Required Schema

```markdown
# {Company} Client Intel — {Month Year}

> **Last updated:** {Date} | **Status:** {Active / Pipeline / Research}
> **Engagement tier:** {Tier 1 / 2 / 3} | **Owner:** {your name}
> **Pipeline value:** ${estimate} ({methodology}) | **Window:** {when opportunity opens/closes}

---

## Executive Summary (1-page state of the engagement)
{Monthly refresh. 3-5 paragraphs covering: where we stand, what changed, what's next, key risk, key opportunity. This is the "if you only read one section" section.}

---

## Company Profile

### Identity & Niche
- **Industry:** [sector, sub-vertical, and where they sit in the value chain]
- **What makes them unique:** [their special sauce — what differentiates them from competitors]
- **Size:** [revenue, employees, loan volume, AUM, or other scale indicators — with source]
- **Business model:** [how they make money, not just what they do]
- **Headquarters:** [location] | **Footprint:** [geographic/market coverage]

### Strategic Position
- **Competitive position:** [market rank, market share if known, strengths vs. peers]
- **Key competitors:** [named, with what they compete on]
- **Products/services that matter to us:** [specific product lines relevant to our engagement]
- **Niche/specialization:** [what they're known for, what they do better than anyone]

### Recent Strategic Moves
- **M&A activity:** [acquisitions, divestitures, partnerships — last 24 months]
- **Product launches:** [new products, platforms, capabilities announced]
- **Reorgs/leadership changes:** [exec hires, departures, restructuring]
- **Capital activity:** [funding rounds, capex signals, cost-cutting, tech investment]
- **Pivots/strategy shifts:** [any directional changes in business strategy]

### Technology Landscape
- **Core platforms:** [LOS, servicing system, CRM, data infrastructure — named products]
- **Known tech stack:** [languages, cloud provider, key vendors]
- **Tech investment signals:** [job postings, conference talks, press releases about tech]
- **AI/data maturity:** [where they are on the AI adoption curve, with evidence]

---

## Active Initiatives & Projects
{What they're actually working on right now — not what we think they should work on}

| Initiative | Description | Stage | Evidence Source | Relevance to Tavant |
|---|---|---|---|---|
| [Name] | [What it is] | [Planning/Active/Stalled] | [How we know] | [Why we care] |

---

## People & Relationships

### Decision-Maker Map

| Name | Title | Background | Role in Decision | Motivations/Pain | Relationship Status | Last Contact |
|---|---|---|---|---|---|---|
| [Name] | [Title] | [Where they came from, tenure, what they're known for] | [Economic Buyer / Champion / Influencer / Blocker / Technical Evaluator] | [What keeps them up at night — personal career motivations + professional pain] | [New / Cold / Warm / Hot / Tavant advocate] | [Date + context] |

### Org Dynamics
- **Who's rising:** [names and why — recently promoted, given new mandate, executive sponsor of key initiative]
- **Who's a potential blocker:** [names and why — risk-averse, loyal to incumbent, leaving soon]
- **Who's the real decision-maker:** [formal authority vs. actual influence — sometimes the CDO decides, not the CTO]
- **Internal politics:** [tensions between departments, competing priorities, budget fights]

### Tavant Connection Map
- **Existing relationships:** [who at Tavant knows anyone at this company — from meetings, conferences, past work]
- **LinkedIn connections:** [any 1st/2nd degree connections worth leveraging]
- **Referral paths:** [can anyone introduce us? Board members, shared investors, industry connections]

---

## Pain Points & Challenges

{Number each. Be SPECIFIC — not "data issues" but "mortgage origination data fragmented across 4 LOS systems with 47% manual rekeying rate per MBA benchmarks."}

1. **[Pain Point Name]:** [specific description with scale/impact]
   - **Evidence:** [source — earnings call quote, job posting, meeting note, news article, with URL if available]
   - **Business impact:** [quantified cost, risk, lost revenue, compliance exposure, customer impact]
   - **Urgency:** [High / Medium / Low] — [reason with timeline: "High — regulatory deadline Q3 2026"]
   - **Confirmed vs. inferred:** [Client stated this / We infer from indicators]

---

## AI Opportunities

{Map each pain point to an AI opportunity, drawing on the pattern library in `tvt-core-lookup(mode=playbook-match)`.}

| Pain Point # | AI Opportunity | Pattern | Tavant Capability | Confidence | Est. Value |
|---|---|---|---|---|---|
| 1 | [specific opportunity] | [pattern name] | [Knowledge.AI / Agentic QE / etc.] | High/Med/Low | [$range] |

**Recommended Entry Point:** [lead use case with full rationale — why this one first, what makes it low-risk + high-visibility, who sponsors it]

**Flywheel Sequence (if applicable):**
[Use Case 1] → enables → [Use Case 2] → enables → [Use Case 3]
{Explain the logic: why does UC1 unlock UC2? What data/trust/relationship does it build?}

---

## Competitive Landscape

### Who Has This Work Today
| Vendor/Partner | What They Do | Contract Status | Strengths | Weaknesses (Our Entry Angle) |
|---|---|---|---|---|
| [Name] | [Specific scope] | [Active / Expiring YYYY / Unknown] | [Why client chose them] | [Where they're failing or limited] |

### Who Else Is Circling
- [Firm name]: [what we know about their pursuit — RFP response, relationship, pitch]

### Switching Cost Assessment
- **Technical:** [integration complexity, data migration, retraining]
- **Political:** [champion loyalty to incumbent, sunk cost, career risk of switching]
- **Financial:** [contract penalties, overlapping costs, budget cycle timing]

### Our Differentiation
- [Specific angle: "Unlike Accenture, we can demo a working prototype in 3 weeks because of Knowledge.AI"]

---

## Money & Timing

### Financial Signals
- **Estimated initial engagement:** [$X-Y range] — methodology: [comparable deals, scope estimate, etc.]
- **Total account potential (12-month):** [$X-Y range] — [reasoning]
- **Budget cycle:** [fiscal year timing, when budgets are set, when discretionary spend is available]
- **Procurement process:** [RFP? Sole source? Preferred vendor list? Who approves what threshold?]

### Timing & Window
- **Decision timeline:** [when they need to decide, what's driving the deadline]
- **Opportunity window:** [when it opens, when it closes, what happens if we miss it]
- **Key dates:** [budget freezes, regulatory deadlines, conference appearances, board meetings]

---

## Tavant Fit Assessment
- **Fit score:** [High / Medium / Low]
- **Why we win:** [specific reasons — prior delivery, domain expertise, speed, relationship, accelerators]
- **Risk factors:** [what could make this hard — specific, not generic]
- **Relevant accelerators:** [Knowledge.AI, Legacy Modernization, Agentic QE — with specific applicability]
- **Comparable deliveries:** [similar work we've done, with outcomes if available]

---

## Actionable First Move

### Value Proposition (in their language)
[2-3 sentences positioning Tavant in terms of THEIR pain, not our capabilities]

### First Outreach Plan
- **Target contact:** [Name, Title — why them first]
- **Channel:** [Email / LinkedIn / Warm intro via [Name] / Conference meeting]
- **Opening hook:** [1-sentence opener that references their specific situation]
- **First meeting agenda:** [3-4 bullet agenda for a 30-min discovery call]

### Anticipated Objections & Counters
1. **"We already have [incumbent]"** → [specific counter]
2. **"We're not ready for AI yet"** → [specific counter]
3. **"[Other objection]"** → [specific counter]

### 30-60-90 Day Roadmap
- **30 days:** [specific milestone — discovery complete, champion identified, use case validated]
- **60 days:** [specific milestone — prototype demo, business case built, exec sponsor aligned]
- **90 days:** [specific milestone — SOW signed, team mobilized, first sprint underway]

### Disqualification Criteria
{What would make this NOT worth pursuing — be honest}
- [Criterion 1: e.g., "If they require on-prem only and won't consider cloud, our accelerators don't apply"]
- [Criterion 2]

---

## Recommended Plays
{Reference specific playbooks from ${CLAUDE_PLUGIN_ROOT}/playbooks/ that apply}

1. **[Playbook name]:** [why it applies, how to adapt it for this client, which sections are most relevant]

---

## Research Notes & Sources
| Source Type | Reference | Date Accessed | Key Finding |
|---|---|---|---|
| [Company website / LinkedIn / SEC filing / News / Job posting / Meeting / Industry report] | [URL or reference] | [Date] | [1-line key takeaway] |

**Research completeness:** [X unique sources / minimum 5 required] — [Complete / Gaps identified below]

**Research gaps (what we still don't know):**
- [ ] [Gap 1 — how to fill it]
- [ ] [Gap 2 — how to fill it]

---

## Changelog
| Date | What Changed | Source |
|---|---|---|
| {Date} | {What was added/updated} | {Research / Meeting / Signal / Review} |
```

### Intel-Specific Rules
1. **No surface-level filler.** Every statement must be specific, evidenced, and actionable.
2. **No TBD financial fields.** Always provide a range with methodology, even if rough.
3. **Every pain point must have evidence.** Mark inferred pain explicitly.
4. **"Recommended Entry Point" is required** — never leave it blank.
5. **"Disqualification Criteria" is required** — name the conditions under which it's not worth pursuing.
6. **Living doc:** Update existing files, don't create duplicates. Refresh Executive Summary monthly.
7. **Minimum 5 unique sources** for a new intel file. Fewer = flag as incomplete.
8. **Every finding connects** — no isolated facts. Each piece of intel references how it affects opportunity, timing, or approach.
9. **Update the changelog** on every edit.
10. After saving, confirm path and note sections needing enrichment from your insider knowledge.

### Intel Quality Dimensions
| Dimension | Requirement | How to Check |
|---|---|---|
| Executive Summary | 3-5 substantive paragraphs, not a Wikipedia summary | Length + specificity |
| Sources | Minimum 5 unique URLs | Count distinct URLs |
| People | Minimum 3 named individuals with backgrounds | Count named people with titles |
| Pain Points | Minimum 3 numbered with evidence sources | Count evidenced pain points |
| Financials | Revenue/budget estimates with methodology (not TBD) | Check for dollar figures + reasoning |
| Competitive | At least 1 named incumbent vendor | Check competitive landscape section |
| First Move | Specific action plan (not "schedule a meeting") | Check for email/meeting specifics |
| Disqualification | Listed criteria for when NOT to pursue | Section exists and is non-empty |
| Timing | Window defined — when it opens, closes | Check for dates/deadlines |
| Connections | Linked to at least 1 other engagement or pattern | Cross-reference check |

**Critical:** If fewer than 5 sources, ALWAYS fail — non-negotiable.

---

## Type: `playbook`

### File Path
```
${CLAUDE_PLUGIN_ROOT}/playbooks/{kebab-case-name}.md
```
Example: `ai-governance-first.md`, `data-foundation-entry-point.md`

Check existing playbooks in `${CLAUDE_PLUGIN_ROOT}/playbooks/` before creating — update rather than duplicate.

### Required Schema

```markdown
# Playbook: {Title}

> **Version:** {X.Y} | **Source:** {client(s) that originated this pattern}
> **Use when:** {one-sentence trigger — when should the reader reach for this playbook?}

---

## The Pattern

{2-4 sentences describing the core insight. What is the repeatable move? Why does it work?}

```
{Optional: ASCII diagram if the pattern has a structure worth visualizing}
```

---

## When to Use

**Good fit:**
- [Indicator 1 — specific client/situation signal]
- [Indicator 2]

**Poor fit / avoid when:**
- [Counter-indicator 1]
- [Counter-indicator 2]

---

## How to Apply

### Step 1: [Phase name]
[What to do and say in this phase. Be specific — what questions to ask, what to show, what to position.]

### Step 2: [Phase name]
[...]

### Step 3: [Phase name]
[...]

---

## Key Messages

> "[Signature line or positioning statement — something you can say in the room]"

- [Supporting message 1]
- [Supporting message 2]

---

## Objection Handling

| Objection | Response |
|---|---|
| "[Common pushback]" | "[How to address it]" |

---

## Evidence & Examples

| Client | How It Was Applied | Outcome |
|---|---|---|
| [Client] | [Brief description] | [Result or status] |

---

## Related Playbooks
- [`{playbook-name}.md`]({playbook-name}.md) — [why it's related]

---

## Assets & References
- [Deck / accelerator / template that supports this play]

---
*Version history: {Date} — {what changed}*
```

### Playbook-Specific Rules
1. The "Use when" trigger line must be specific enough that the reader can make the call in 5 seconds.
2. Every playbook needs at least one real evidence example — even if the outcome is TBD.
3. "Key Messages" must include at least one signature line you can say out loud in a client room.
4. Increment the version number on every meaningful update.
5. After writing, add the playbook to `${CLAUDE_PLUGIN_ROOT}/playbooks/README.md` if a README exists.

### Playbook Quality Dimensions
| Dimension | Requirement |
|---|---|
| Multi-client evidence | Referenced at 2+ clients |
| Steps | Concrete how-to-apply steps |
| Key messages | Specific language to use with clients |
| When NOT to use | Scope boundaries defined |

---

## Type: `deep-dive`

### File Path
```
./sales-intel/daily/deep-dive_{topic-slug}_{YYYY-MM-DD}.md
```
Example: `deep-dive_newrez-qe-expansion_2026-04-09.md`

**Trigger:** Any signal flagged as **[DEEP-DIVE RECOMMENDED]** or **[DEEP-DIVE TRIGGER]** in the daily brief. Also triggered manually when the user says "deep dive on [signal]" or "unpack [topic]."

### Required Schema

```markdown
# Deep Dive: {Topic}
> **Date:** {YYYY-MM-DD} | **Client:** {Client name} | **Trigger:** {What triggered this analysis}
> **Classification:** [Opportunity / Risk / Decision Required / Strategic Shift]
> **Urgency:** [Act Today / Act This Week / Monitor Closely / Background Awareness]

---

## The Signal
{What happened — specifics. Names, dates, exact quotes if available.}
- **Source:** [where this came from]
- **When:** [date/time of the signal]
- **Who's involved:** [named individuals and their roles]

---

## Context: What We Already Know
{Pull from intel file, PORTFOLIO.md, and previous daily briefs. Don't make the reader remember — bring the context forward.}

- **Engagement history:** [How did we get here? Key milestones in this relationship.]
- **Previous signals:** [Related signals from prior days/weeks. How does this new signal change the picture?]
- **Stakeholder positions:** [Where key people stood before this signal. Has anyone shifted?]
- **Portfolio context:** [How does this fit into the broader portfolio? Resource implications? Timing conflicts?]

---

## Analysis: Why This Matters

### Interpretation Scenarios
{Don't settle for one read. Lay out 2-3 plausible interpretations:}

**Scenario A (Most Likely — {probability}%):** [interpretation]
- Evidence for: [what supports this reading]
- Evidence against: [what contradicts it]
- Implication: [what it means for our engagement]

**Scenario B ({probability}%):** [interpretation]
- Evidence for: [...]
- Evidence against: [...]
- Implication: [...]

**Scenario C ({probability}%):** [interpretation, if applicable]
- [...]

### What This Changes
- **Our understanding of the account:** [how does this update our mental model?]
- **Our competitive position:** [does this help or hurt us vs. incumbents/competitors?]
- **Our timeline:** [does this accelerate, delay, or create a new deadline?]
- **Our relationship map:** [new allies, new blockers, shifted dynamics?]

---

## Stakeholder Map (for this signal)

| Person | Role | Position Before Signal | Position After Signal | Motivation |
|---|---|---|---|---|
| [Name] | [Title] | [Where they stood] | [Where they likely stand now] | [What's driving their behavior] |

---

## Options & Trade-offs

{Present 2-3 concrete courses of action:}

### Option A: {Name — e.g., "Move Aggressively"}
- **What to do:** [specific steps, specific people, specific timing]
- **Pros:** [why this could work]
- **Cons:** [risks and costs]
- **Resource requirement:** [time, people, money]
- **Expected outcome:** [what success looks like]

### Option B: {Name — e.g., "Strategic Patience"}
- **What to do:** [...]
- **Pros:** [...]
- **Cons:** [...]
- **Resource requirement:** [...]
- **Expected outcome:** [...]

### Option C: {Name — e.g., "Pivot Approach"} (if applicable)
- [...]

---

## Recommendation

**Recommended option:** [A/B/C]

**Why:** [2-3 sentences on the reasoning — reference evidence, timing, and risk appetite]

**Specific next steps:**
1. [Action] — [Owner: you / Tavant team / Client contact] — [By when]
2. [Action] — [Owner] — [By when]
3. [Action] — [Owner] — [By when]

**Decision deadline:** [When do you need to decide? What happens if you don't?]

---

## Risk Assessment

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| [What could go wrong] | [H/M/L] | [What happens if it does] | [How to reduce/avoid it] |

---

## Follow-up Triggers
{What should you watch for to know if the situation is evolving?}
- [ ] [Trigger 1: "If [person] responds by [date] with [type of response], escalate to Option A"]
- [ ] [Trigger 2: "If no response by [date], switch to Option B"]
- [ ] [Trigger 3: "If [competitor signal], immediately [action]"]
```

### Deep-Dive-Specific Rules
1. **This is analysis, not summary.** Don't restate what happened — interpret it.
2. **Multiple scenarios are required.** Never present just one interpretation.
3. **Options must be specific and actionable.** Not "follow up" but "send the client sponsor a Slack DM referencing the QE org-building mandate, propose a 30-min working session, target Thursday."
4. **Bring context forward.** Pull from existing intel files and PORTFOLIO.md so the reader doesn't need to cross-reference manually.
5. **Name the decision deadline.** Every deep-dive must say when a decision is needed and what happens if it's missed.
6. **Keep it to 2-3 pages.** Deep but focused. Every paragraph must earn its place.
7. After saving, give the user a 2-sentence summary: "The signal means [X]. Recommended move: [Y] by [Z date]."

### Deep-Dive Quality Dimensions
| Dimension | Requirement |
|---|---|
| Multiple scenarios | At least 2 interpretation scenarios |
| Options | At least 2 courses of action with trade-offs |
| Recommendation | Specific action with timing and owner |
| Risk assessment | What could go wrong + mitigation |

---

## Type: `presales`

### File Path
```
./sales-intel/{Client}/{artifact_type}_{Client}_{YYYY-MM-DD}.md
```
Example: `./sales-intel/Anchor_Loans/executive-brief_Anchor_Loans_2026-04-10.md`

### Artifact Sub-Types

| Sub-Type | Use When | Format |
|---|---|---|
| **executive-brief** | First meeting with a senior buyer; need a 1-pager | 1 page: context, problem, solution, why Tavant, ask |
| **use-case-framework** | Presenting 3+ connected AI opportunities | Flywheel structure: foundation → intelligence → automation → product |
| **discovery-prep** | Preparing for a discovery call | Questions to ask, hypotheses to validate, listening points |
| **proposal-narrative** | Responding to a requirement or advancing a deal | Problem → approach → solution → evidence → next steps |
| **workshop-agenda** | Running a client AI workshop | Timed agenda, discussion prompts, output artifacts expected |

### Inputs Required

Before composing, read:
1. `./sales-intel/{Client}/{Client}_Client_Intel_*.md` — for pain points, fit, contacts, context
2. Relevant playbooks from `${CLAUDE_PLUGIN_ROOT}/playbooks/` — for positioning and messaging
3. Current PORTFOLIO.md entry — for stage, owner, and next action context

### Required Schema

```markdown
# {Artifact Type}: {Company} — {Topic}
*{Date} | {Author: your name, your title — Tavant}*

---

## Situation
[2-3 sentences: what's true about the client's world right now that creates the opening for this conversation]

## Problem
[The specific pain we're addressing — concrete, not generic. Use the client's language where possible.]

## Our Approach
[How Tavant would solve it — lead with the pattern, then the specifics. Reference playbook if applicable.]

## Why This Works
[Evidence: prior delivery, domain expertise, accelerators. 2-3 bullets max.]

## Why Tavant
[Differentiation from alternatives. Specific, not generic.]

## What We're Proposing
[The specific ask or next step — a workshop, POC, discovery engagement, proposal]

## Anticipated Questions
[2-3 likely objections and responses]

---
*Sources: {list of intel files and playbooks used}*
```

### Presales-Specific Rules
1. **Open with the client's situation** — not with Tavant's capabilities. Lead with their world, not ours.
2. **Every claim about Tavant capability must be grounded** in a real accelerator, playbook, or delivery example.
3. **"What We're Proposing" must be concrete** — not "let's have a conversation."
4. **List the sources used** (which intel file, which playbooks) for traceability.
5. **For workshop artifacts:** always include a timed agenda and explicit "outputs by end of day" section.
6. **Never start from a blank page.** Compose from what already exists — client intel + relevant playbooks + Tavant accelerators.

### Presales Quality Dimensions
| Dimension | Requirement |
|---|---|
| Opens with client | First section is client's world, not Tavant's |
| Specific ask | Clear next step (not generic "let's talk") |
| Grounded in intel | References specific findings from intel file |
| Objection handling | At least 2 anticipated objections with counters |

---

## Shared Rules (All Types)

1. **Chief of Staff quality bar.** Every output should feel like a Chief of Staff briefing a President: synthesized, substantive, decision-ready. Not a summary — an intelligence product.
2. **No generic filler.** If a sentence could apply to any company, delete it. Replace with specifics.
3. **Every finding connects.** No isolated facts. Each piece of information must reference how it affects the engagement, portfolio, or approach.
4. **Names, numbers, dates.** Surface level = "the company is growing." Chief of Staff level = named individuals, dollar figures with methodology, specific dates and deadlines.
5. **Quality gate is automatic.** After writing content, validate against the type's quality dimensions. Remediate FAILs before surfacing to the user. PASS_WITH_GAPS is acceptable for quick intel (P2 research). FAIL is never acceptable for full intel or daily briefs.
6. **File mechanics are non-negotiable.** Path variables resolved. Timestamps updated. Changelogs appended. Existing files updated, not duplicated.
7. **Confirm on completion.** After writing, always confirm: the file path, a brief summary of what was written, and the quality grade.

---

# Format Factory Modes (FR-013 / Q3 — spec-006 consolidation)

**Added 2026-05-23 per spec-006 FR-013**: tvt-core-write absorbs the format-factory family (`g-create-pdf`, `g-create-doc`, `tvt-create-pptx`, `g-create-xlsx`) as **modes**. Alias stubs at the old IDs route invocations here per FR-015.

## When to use format-factory mode vs canonical-output mode

| Caller wants… | Use |
|---|---|
| Daily/intel/playbook/deep-dive/presales Markdown output | `type=daily|intel|playbook|deep-dive|presales` (existing — above) |
| A PDF / DOCX / PPTX / XLSX file for any purpose | `mode=pdf|docx|pptx|xlsx` (this section) |

These dimensions are **mutually exclusive** for a single invocation. A caller passes `type=intel` OR `mode=pdf` — not both. If both, `mode` wins (format factory dispatch).

## Mode: pdf — PDF generation

**Invocation**: `tvt-core-write mode=pdf content="..." output_path="..."`

**Procedure**:
1. Receive a `content` payload (Markdown, structured dict, or raw text) and an `output_path`
2. Resolve any path variables (`{Date}`, `{Client}`, etc.) in `output_path` per existing File Mechanics
3. Generate the PDF using the first available tool, in order:
   - **`pandoc`** (best for Markdown → PDF): `pandoc input.md -o output.pdf`
   - **`weasyprint`** if installed: HTML/CSS → PDF
   - **`wkhtmltopdf`** if installed: HTML → PDF
   - **`reportlab`** (Python lib; install if absent): programmatic PDF construction
   - **fallback**: write HTML, surface to user with note "no PDF tool available; install pandoc"
4. Verify output exists at the resolved path
5. Confirm: `Created PDF: {path}` (or update/append per existing write modes)

**Edge cases**:
- Existing PDF at path: error unless `--force` (same rule as canonical modes)
- Content too long for single page: paginate; preserve heading hierarchy
- Images in content: inline via base64 or local path resolution
- Tables: render as flowable tables (reportlab) or HTML tables (pandoc/weasyprint)

**Equivalence to legacy `g-create-pdf`**: any invocation that worked against the legacy skill MUST produce equivalent output when routed via `tvt-core-write mode=pdf`. Enforced by `tests/alias_equivalence.py` per FR-016 / SC-006.

## Mode: docx — Word document generation

**Invocation**: `tvt-core-write mode=docx content="..." output_path="..."`

**Procedure**:
1. Receive content (Markdown preferred, or structured dict with `title`, `headings`, `paragraphs`, `tables`)
2. Resolve `output_path` per File Mechanics
3. Generate the DOCX using the first available tool:
   - **`pandoc`** (best for Markdown → DOCX): `pandoc input.md -o output.docx`
   - **`python-docx`** if installed: programmatic DOCX construction
   - **`docx-js`** (Node-based; see legacy g-create-doc reference materials)
   - **fallback**: write Markdown, surface "no DOCX tool available; install pandoc"
4. Apply standard styling: title h1, section headers h2/h3, body 11pt, tables with borders
5. Verify + confirm

**Equivalence to legacy `g-create-doc`**: any invocation against legacy `g-create-doc` MUST produce equivalent output when routed here. Enforced by `tests/alias_equivalence.py`.

## Mode: pptx — PowerPoint generation

**Invocation**: `tvt-core-write mode=pptx content="..." output_path="..." [template=...]`

**Procedure**:
1. Receive content as **slide structure** (list of slides; each with title + bullets + optional notes + optional layout hint)
2. Resolve `output_path` per File Mechanics
3. Generate the PPTX:
   - **`python-pptx`** if installed: programmatic PPTX construction (preferred for fidelity)
   - **`pandoc`** (Markdown → PPTX): basic, works for simple decks
   - **`pptxgenjs`** (Node-based; see legacy tvt-create-pptx reference)
   - **fallback**: write Markdown outline, surface "no PPTX tool available"
4. Optional `template=` arg specifies a base PPTX template to apply (matches legacy `tvt-create-pptx` brand-applied flow)
5. For screenshot mode (legacy `tvt-create-pptx mode=screenshot`): use `libreoffice --headless --convert-to png` per slide
6. Verify + confirm

**Equivalence to legacy `tvt-create-pptx`**: both default create mode AND screenshot mode covered.

## Mode: xlsx — Spreadsheet generation

**Invocation**: `tvt-core-write mode=xlsx content="..." output_path="..."`

**Procedure**:
1. Receive content as **tabular structure** (list of sheets; each with headers + rows + optional formulas + optional formatting)
2. Resolve `output_path` per File Mechanics
3. Generate the XLSX:
   - **`openpyxl`** if installed: programmatic XLSX construction (preferred for formula support)
   - **`pandas` + `xlsxwriter`** if both installed: dataframe-driven generation
   - **`pandoc`** (limited; only basic tables)
   - **fallback**: write CSV, surface "no XLSX tool available; install openpyxl"
4. For multi-sheet workbooks: each sheet a separate dict entry in content
5. Apply standard formatting: header row bold, column widths auto-fit, number formats per column type
6. Verify + confirm

**Equivalence to legacy `g-create-xlsx`**: any invocation that worked against the legacy skill, including its existing `office/` dir helpers and `recalc.py` formula recompute, must produce equivalent output.

## Tool-availability fallback ladder

For every format mode above, the procedure follows this dependency-resolution ladder:

```
1. Try the most-direct tool (pandoc for md→x; format-specific library for structured input)
2. If missing, try next-best (system tool or alternative lib)
3. If all preferred tools missing, fallback to a degraded format (HTML for PDF, Markdown for DOCX/PPTX, CSV for XLSX)
4. Always emit a clear message about what tool was used and what would improve output (e.g., "install pandoc for native PDF support")
```

This matches the standard pattern used across this skill family: LLM dispatches to whatever tooling is available, gracefully degrades, never silently fails.

## Schema-conforming frontmatter (per FR-073 / Q15)

The frontmatter above predates the spec-006 10-field schema. Frontmatter will be conformed to schema at T042 (Phase 3 / Phase D-eve). Target shape (for reference; applied at T042):

```yaml
name: tvt-core-write            # matches dir name (was incorrectly 'tvt-core-write')
description: Universal writer — canonical outputs (daily/intel/playbook/deep-dive/presales) + format factory (pdf/docx/pptx/xlsx). Replaces g-create-pdf/doc/pptx/xlsx via mode= dispatch per FR-013.
layer: kernel                 # 4-primitive kernel per FR-039
expected_impact: high         # writes ship to consumers
default_overhead: standard    # eval depth — bumped to deep for client-facing per FR-026
requires:
  primitives: [tvt-core-eval]   # quality gate
produces:
  artifact: draft             # or intel-file when type=intel
  side_effects:
    - "writes <output_path> in the requested format"
eval:
  mode: gate                  # client-facing artifacts per FR-025 categorical rule
  depth: standard
trigger_phrases:
  - write daily / morning brief / write intel / create playbook / deep dive
  - draft presales / executive brief / discovery prep
  - create pdf / write pdf
  - create docx / write doc / draft a memo
  - create pptx / write deck / build slides
  - create xlsx / write spreadsheet
modes: [daily, intel, playbook, deep-dive, presales, pdf, docx, pptx, xlsx]
user_invocable: true
```
