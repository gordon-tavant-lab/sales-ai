# Sales Skills SDK — The Lego Block Reference

> **Status:** v0.1 — living document
> **Companion to:** `sales-pattern-intelligence.md` (patterns = programs built from these blocks)
> **Primary source:** Notion meeting notes & transcripts — every internal strategy meeting with sales leaders is a training dataset. Run `/distill-sales` after processing meeting notes to extract new skill evidence.
> **Mental model:** Sales is a programming language. Patterns are programs. Skills are the primitives. You don't memorize programs — you master the primitives and compose on the fly.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                    SALES RUNTIME                         │
│                                                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │  SENSE   │→ │ PROCESS  │→ │  ACT     │              │
│  │  skills  │  │  skills  │  │  skills  │              │
│  └──────────┘  └──────────┘  └──────────┘              │
│       ↑              ↑             ↑                    │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │ CONTROL  │  │ MEMORY   │  │ COMPOSE  │              │
│  │ FLOW     │  │ (state)  │  │ (combos) │              │
│  └──────────┘  └──────────┘  └──────────┘              │
└─────────────────────────────────────────────────────────┘
```

Every sales interaction is a loop: **SENSE → PROCESS → ACT**, governed by **CONTROL FLOW**, informed by **MEMORY** (relationship state), and made powerful by **COMPOSITION** (chaining skills).

---

## Layer 1: SENSE — Input & Detection Skills

_Like `read()`, `listen()`, `scan()`. These are how you take in information._

### `SENSE.read_signal(statement) → Signal`

**What it does:** Interpret a client statement and classify the signal.

**Signature:**
```
Input:   raw client statement (verbal, email, body language)
Output:  { type, confidence, implied_need, hidden_meaning }
```

**Signal types:**
| Type | Example | What it really means |
|---|---|---|
| `BUY_SIGNAL` | "How fast can we start?" | They've decided; now it's logistics |
| `INTEREST_SIGNAL` | "That's interesting, tell me more" | Engaged but not committed; keep going |
| `AUTHORITY_SIGNAL` | "I'd need to run this by my VP" | You're not talking to the decision maker |
| `BUDGET_SIGNAL` | "We have limited spending capacity" | Price matters; lead with value, then cost |
| `URGENCY_SIGNAL` | "We need this before Q3" | Time pressure = leverage |
| `FEAR_SIGNAL` | "What if it doesn't work?" | Risk is the blocker, not interest |
| `NOISE` | "Yeah, I have some projects for you" | Could mean anything — validate before acting |

**Levels of mastery:**
1. **Beginner:** Can identify signals after the meeting (in review)
2. **Intermediate:** Can identify signals in real-time during the meeting
3. **Advanced:** Can create conditions that force signals to surface
4. **Expert (the senior AE):** Can read signals from what the client *doesn't* say

**How to practice:** After every meeting, replay the transcript. Mark every statement. Classify it. Compare your read with what actually happened next.

**Observed in the wild (fill in your own once you have transcripts to review):**
- A stated interest with no follow-up action, over many months, is `INTEREST_SIGNAL` sustained — not `BUY_SIGNAL`. Don't over-read patience as momentum.
- A technical evaluator's detailed feasibility question in a live demo is usually `INTEREST_SIGNAL` at high confidence, not idle curiosity.

---

### `SENSE.read_room() → RoomState`

**What it does:** Assess the live dynamics of a meeting — who's engaged, who's checked out, who's the real decision maker, what's the energy.

**Signature:**
```
Input:   observation of meeting participants
Output:  { energy_level, power_map, engagement_map, blockers }
```

**What to read:**
| Cue | Meaning |
|---|---|
| Person asks detailed technical questions | Evaluator — needs to be satisfied before deal moves |
| Person is quiet but everyone looks at them before answering | Decision maker — even if they don't have the title |
| Person keeps bringing up cost/timeline | Budget holder or project manager — practical blocker |
| Person nods but never asks questions | Passive supporter or disengaged — clarify later |
| Person challenges every point | Either skeptic (win them) or competitor's champion (navigate around) |
| Cross-talk and energy | Healthy engagement — they care about this |
| Silence after your key point | Either confusion or processing — ask "does this land?" |

**Levels:**
1. **Beginner:** Notice who talks the most
2. **Intermediate:** Map who defers to whom
3. **Advanced:** Shift your approach mid-meeting based on room dynamics
4. **Expert:** Pre-seed the room (pre-call the decision maker, brief your champion)

---

### `SENSE.detect_pain(conversation) → PainPoint[]`

**What it does:** Extract the actual problems from what clients say (and don't say).

**Signature:**
```
Input:   client conversation or context
Output:  [ { pain, severity, awareness, willingness_to_pay } ]
```

**Pain taxonomy:**
| Category | Client says | Real pain |
|---|---|---|
| **Process pain** | "It takes forever to..." | Manual workflow that could be automated |
| **Knowledge pain** | "Nobody knows how this works" | Institutional knowledge trapped in people's heads |
| **Quality pain** | "We keep finding errors after the fact" | QA is reactive, not proactive |
| **Scale pain** | "It works but it won't scale" | Architecture or process bottleneck |
| **Compliance pain** | "The auditors keep flagging..." | Regulatory pressure exceeding current capability |
| **Cost pain** | "We can't afford to keep..." | Doing something expensive that AI can reduce |
| **Speed pain** | "By the time we get the data..." | Insight arrives after the decision window |

**Key insight:** Clients describe *symptoms*. Your job is to diagnose the *disease*. "It takes forever to process documents" is a symptom. The disease might be: no OCR pipeline, bad data architecture, or manual exception handling.

**Observed:** "we can't rely on our current vendor's documentation" reads as Knowledge pain on the surface — but the deeper disease is often broken change-management process, not a documentation gap. Diagnose past the symptom.

---

### `SENSE.map_stakeholders(account) → StakeholderMap`

**What it does:** Identify who matters, what they care about, and how they influence the decision.

**Signature:**
```
Input:   account context, meeting participants, org chart signals
Output:  { champions, blockers, decision_makers, influencers, end_users }
```

**Stakeholder archetypes:**

| Archetype | Cares about | How to engage | Example |
|---|---|---|---|
| **Champion** | Innovation, career advancement | Feed them wins they can take to their boss | (a champion you've worked with) |
| **Budget holder** | ROI, risk reduction, cost control | Speak in dollars saved, not technology deployed | (a budget holder you've worked with) |
| **Technical evaluator** | Feasibility, architecture fit | Deep-dive demos, answer hard questions honestly | (a technical evaluator you've worked with) |
| **Executive sponsor** | Strategic impact, competitive position | Big picture, industry trends, "what your peers are doing" | (an executive sponsor you've worked with) |
| **Blocker** | Status quo, their own relevance | Understand their fear; make them part of the solution, not the problem | (watch for these) |
| **End user** | "Will this make my job easier?" | Show the UX, not the architecture | (end users of a deployed solution) |

**Levels:**
1. **Beginner:** Know everyone's name and title
2. **Intermediate:** Know everyone's motivation and influence
3. **Advanced:** Build different pitch angles for different stakeholders in the same meeting
4. **Expert:** Turn blockers into champions

---

## Layer 2: PROCESS — Analysis & Strategy Skills

_Like `if/else`, `map()`, `filter()`, `sort()`. These are how you think._

### `PROCESS.frame_value(capability, client_context) → ValueProposition`

**What it does:** Translate a Tavant capability into a client-specific value statement.

**Signature:**
```
Input:   what we can do + what they care about
Output:  "For [you], this means [specific outcome] because [specific reason]"
```

**The framing formula:**
```
WRONG: "We have a Knowledge.AI platform with RAG and agentic architecture"
RIGHT: "Your loan officers will find the right investor guideline in 30 seconds
        instead of 15 minutes — because Knowledge.AI has already read every
        guideline document you have and knows which page answers which question"
```

**Anti-patterns:**
- Leading with technology, not outcomes
- Using jargon the client didn't use first
- Claiming value without a proof point
- Generic value ("save time and money") instead of specific ("reduce doc review from 15 min to 30 sec")

**The stack:**
```
Feature → Capability → Benefit → Value → Proof
  ↓           ↓           ↓        ↓        ↓
"RAG"     "Answers     "Faster   "$2M/yr   "Deployed this
          from your    decisions  saved     and saw
          own docs"    on loans"  on staff" 50-75% speedup"
```

**Never stop before you reach "Value" in a client conversation.** Features and capabilities are for internal discussions.

---

### `PROCESS.position_cost(solution, client_budget) → PricingStrategy`

**What it does:** Frame cost as an advantage, not a barrier.

**Three pricing modes:**

**Mode 1: Undercut** — when competing against big firms
```python
if client.competitors == ["big-name SI #1", "big-name SI #2"]:
    strategy = "Accelerator leverage — we already have 80%, you pay for 20%"
```

**Mode 2: Options** — when client budget is unclear
```python
if client.budget == UNKNOWN:
    present([
        Option("Basic",    cost="$X",   scope="Core problem solved, off-the-shelf tools"),
        Option("Standard", cost="$2X",  scope="Custom solution with accelerators"),
        Option("Premium",  cost="$3X",  scope="Full platform with ongoing AI ops")
    ])
    # Let client self-select. Their choice reveals budget.
```

**Mode 3: Value anchor** — when you have strong proof
```python
if proof_point.exists:
    strategy = "This costs $X. It replaces $10X of manual effort. ROI in 3 months."
    # Only works when you can quantify the alternative cost
```

**Key insight from the senior AE:** *"Oh, by the way, we already have an accelerator that does 80% of this."* Every accelerator in Tavant's portfolio is a pricing weapon — it converts custom development cost into configuration cost.

---

### `PROCESS.assess_timing(deal_signals) → TimingDecision`

**What it does:** Decide whether to push, wait, or pivot.

```python
def assess_timing(signals):
    if signals.buy_signals > 2 and signals.urgency == HIGH:
        return PUSH       # "Let's scope this week"

    if signals.interest == HIGH and signals.urgency == LOW:
        return NURTURE     # "Let me show you something next month"

    if signals.interest == HIGH and signals.blockers > 0:
        return REMOVE_BLOCKERS  # "What would need to be true for this to move?"

    if signals.interest == LOW:
        return PROVOKE     # "Your competitor just did X. Are you thinking about this?"

    if signals.noise > signals.signal:
        return VALIDATE    # "Help me understand — are you exploring or deciding?"

    return PATIENCE        # the senior AE on a credit-bureau client: 1 year. Still right.
```

**The timing spectrum:**

```
PROVOKE ←──── VALIDATE ←──── NURTURE ←──── PUSH ←──── CLOSE
  │               │              │             │           │
 "Wake up"    "Clarify"     "Stay warm"   "Accelerate"  "Sign"
```

**Most common mistake:** Pushing when you should be nurturing. Second most common: Nurturing when you should be pushing.

**Observed (track your own examples here):**
- A relationship can move PATIENCE → NURTURE → PUSH over many months as a workshop finally gets scheduled.
- A demo that lands well converts NURTURE → PUSH within the same week — action items are the tell.

---

### `PROCESS.match_pattern(client_problem) → KnownSolution`

**What it does:** Map a new client's problem to a solved problem from another engagement.

```python
PATTERN_LIBRARY = {
    "knowledge_trapped_in_people": {
        "solution": "Knowledge.AI + interview capture",
        "proven_at": [],  # fill in your own engagements as you validate this
        "accelerator": "Knowledge.AI"
    },
    "document_processing_bottleneck": {
        "solution": "LLM extraction + rules validation",
        "proven_at": [],
        "accelerator": "DMA (Data Migration Assistant)"
    },
    "testing_at_scale": {
        "solution": "AI test generation from code + requirements",
        "proven_at": [],
        "accelerator": "QE Accelerator suite"
    },
    "legacy_code_undocumented": {
        "solution": "Code analysis → behavioral design → documentation",
        "proven_at": [],
        "accelerator": "Dev Studio (Ignite)"
    },
    "data_migration_mapping": {
        "solution": "AI field mapping with confidence scoring",
        "proven_at": [],
        "accelerator": "Lender Onboarding Portal"
    },
    "compliance_at_volume": {
        "solution": "Continuous AI-driven QC + anomaly detection",
        "proven_at": [],
        "accelerator": "TBD"
    }
}

def match(client_problem):
    for pattern, solution in PATTERN_LIBRARY.items():
        if similarity(client_problem, pattern) > THRESHOLD:
            return solution  # "We've solved this before. Let me show you."
    return NEW_PATTERN  # Worth solving; may become next accelerator
```

**This is a compounding advantage.** The more engagements you see, the richer this library becomes. Every solved problem = a weapon for the next deal.

---

### `PROCESS.read_politics(org_context) → PoliticalMap`

**What it does:** Understand the invisible forces that determine whether a deal moves.

**Political patterns to recognize:**

| Pattern | Signs | Strategy |
|---|---|---|
| **Budget politics** (CapEx vs OpEx) | "That's an operational expense, not capital" | Reframe the work to fit the available budget category |
| **Vendor politics** | "We're not an approved vendor yet" | Find the side door (GCP credits, partner channels, pilot programs) |
| **Turf politics** | "That's really [other team]'s domain" | Get invited by both sides, or pick the side with budget |
| **Champion risk** | Champion is junior and can't push alone | Give them materials to sell upward; offer to present to their boss |
| **Not-invented-here** | "We'd prefer to build our own" | Respect it; offer accelerators as "starting points, not finished products" |

**Observed:** a year-long maze can be pure politics — CapEx/OpEx classification, vendor approval process, budget cycles — with the technology never actually being the issue. Navigate all of it by being patient and helpful with the process itself, not by pushing on the tech.

---

## Layer 3: ACT — Output & Execution Skills

_Like `print()`, `write()`, `send()`, `deploy()`. These are how you deliver._

### `ACT.demo(prototype, client_context) → Reaction`

**What it does:** Show, don't tell. The prototype is the proof.

**The demo formula:**
```
1. BRIDGE     (30 sec)  "You told us [their problem]. We built this."
2. SHOW       (5 min)   Live demo against real-looking data
3. COMPARE    (2 min)   "Here's what this looks like without AI" → "Here's with"
4. SPECIFICS  (3 min)   "For your [X], this would mean [Y]"
5. HAND OVER  (2 min)   "Want to try it? / Want to see your data in it?"
```

**Anti-patterns:**
- Demoing features instead of outcomes
- Showing a generic demo without client-specific framing
- Apologizing for what's not built yet (instead: "this is Phase 1; Phase 2 adds...")
- Running long — 10-12 min max, then let them react

**Power moves:**
- **Live data:** If you can run their actual data (or realistic synthetic data), the conversation shifts from "could this work?" to "this already works"
- **Side-by-side:** Show the old way vs. the new way. The contrast sells itself.
- **Break it intentionally:** Show an edge case, show the AI flagging it for human review. This builds trust in the system.

**Observed:** a side-by-side comparison of naive approaches (string matching, off-the-shelf ChatGPT) vs. a purpose-built multi-phase approach — the side-by-side IS the sale.

---

### `ACT.tell_story(pattern, client_context) → Narrative`

**What it does:** Wrap a solution in a narrative that makes the client see themselves in it.

**Story structure:**
```
1. MIRROR       "You're dealing with [exactly their situation]"
2. EMPATHIZE    "Every [role] we talk to has this same challenge"
3. REFRAME      "But what if the problem isn't [symptom] — it's [root cause]?"
4. PROOF        "Here's what happened when [similar client] approached it this way"
5. BRIDGE       "For you, that would look like [specific application]"
```

**Never say:**
- "Our platform can..." (feature-first)
- "We're the best at..." (claims without proof)
- "You should..." (prescriptive before you've earned the right)

**Always say:**
- "What we've seen across the industry is..." (pattern, not opinion)
- "A lender similar to you..." (relevant proof without naming names)
- "The question we'd want to answer together is..." (collaborative, not pushy)

**Observed:** a strong opener names an uncomfortable truth before pitching anything — *"Most lenders are automating the wrong things. They're using AI to go faster inside broken processes."* This is `tell_story()` at expert level.

---

### `ACT.ask(context, relationship_depth) → Proposal`

**What it does:** Make the commercial ask — propose work, request commitment.

**The ask calibration:**

```python
def calibrate_ask(relationship_depth, signal_strength):

    if relationship_depth == NEW and signal_strength < MEDIUM:
        return ask_for_next_meeting()
        # "Can we schedule a follow-up to go deeper on [specific topic]?"

    if relationship_depth == DEVELOPING and signal_strength >= MEDIUM:
        return ask_for_workshop_or_poc()
        # "What if we did a 2-day workshop to scope this out?"

    if relationship_depth == MATURE and signal_strength >= HIGH:
        return ask_for_sow()
        # "We're ready to put a proposal together. What do you need from us?"

    if relationship_depth == MATURE and signal_strength == BUY:
        return ask_for_signature()
        # "Here's the SOW. When can we start?"
```

**The ask progression ladder:**

```
Level 0:  "Can I send you some materials?"           ← Weak. Avoidable.
Level 1:  "Can we schedule 30 minutes next week?"     ← Gets a next step
Level 2:  "Can we do a half-day workshop with your team?"  ← Gets engagement
Level 3:  "Let us build a quick POC on your data"     ← Gets investment
Level 4:  "Here's what the full engagement looks like" ← Gets commitment
Level 5:  "Sign here"                                 ← Gets revenue
```

**Never end a meeting below Level 1.** Always leave with a next step.

**The quid-pro-quo pattern:**
```python
while not earned_right_to_ask:
    give_value()           # Brainstorm, share ideas, demo capabilities
    create_dependence()     # Client starts relying on your insights
    wait_for_shift()        # Client asks "how would you..." instead of "could you..."

# Now the ask feels natural, not transactional
propose_work()
```

---

### `ACT.follow_up(meeting, commitments) → Momentum`

**What it does:** Convert meeting energy into forward motion before it decays.

**The 24-hour rule:** Every meeting gets a follow-up within 24 hours. Period.

**Follow-up template:**
```
Subject: [Meeting topic] — Next steps from [date]

Hi [name],

Thanks for [specific thing — not generic "your time"].

Here's what we heard:
- [Pain point 1 in their words]
- [Pain point 2]

Here's what we committed to:
- [ ] [Tavant action] by [date]
- [ ] [Tavant action] by [date]

Here's what we're asking from you:
- [ ] [Client action] by [date]

Next meeting: [proposed date/time]

[signature]
```

**Why this matters:** The follow-up email is a contract. It creates accountability on both sides. It also forces you to articulate what you heard — which the client will correct if you got it wrong (which is valuable).

---

### `ACT.pivot(situation, new_information) → NewStrategy`

**What it does:** Change direction mid-engagement when circumstances shift.

**Pivot triggers:**
| Trigger | Old plan | New plan |
|---|---|---|
| Client reveals budget constraint | Full custom solution | Accelerator-led approach |
| New stakeholder enters | Technical pitch | Reset with executive framing |
| Competitor revealed | Differentiate on features | Differentiate on speed-to-value |
| Scope creep emerging | Deliver everything | "Let's phase this — Phase 1 is [core], Phase 2 is [expansion]" |
| Champion leaves the company | Depends on champion | Rebuild relationship with successor |
| Client internal politics shift | One path | Find the new power center |

**Observed:** a client engagement can pivot multiple times — interface change, org-merge scope change, budget-category change. Each pivot is a fresh `SENSE → PROCESS → ACT` cycle. Don't fight the pivots — surf them.

---

### `ACT.wait(strategy) → Patience`

**What it does:** The hardest skill. Do nothing, but do it intentionally.

```python
def strategic_wait(context):
    """
    Waiting is not inaction. It's:
    - Staying visible without being pushy
    - Building proof while they deliberate
    - Preparing for the moment they say 'go'
    """
    maintain_light_contact()     # Occasional value-add touchpoint
    build_proof_in_background()  # Prototype, case study, demo
    monitor_for_triggers()       # Org change, budget cycle, competitor move
    resist_urge_to_push()        # The deal will come when conditions align
```

**When to wait vs. when to push:**
| Wait when | Push when |
|---|---|
| Client is navigating internal process | Client has asked for a proposal |
| Budget cycle hasn't aligned yet | Budget is available and time-bound |
| Champion is building internal support | Champion says "I need help convincing my boss" |
| You don't have proof yet | You have a demo that matches their need |
| Relationship is still shallow | Relationship is deep enough to handle directness |

**Observed:** a year of waiting can be *strategic*, not passive — learning the org, navigating the process, building relationship depth the whole time. When the moment comes, you're not starting from zero, you're cashing in a year of investment.

---

## Layer 4: CONTROL FLOW — Decision & Orchestration Skills

_Like `if/else`, `while`, `try/catch`, `async`. These govern when and how you use the other skills._

### `CONTROL.escalation_logic(situation) → Response`

```python
def should_escalate(situation):
    if situation.blocker_type == "TECHNICAL":
        bring_in("tech-lead", "AI-lead")  # Tech depth resolves technical doubt

    elif situation.blocker_type == "COMMERCIAL":
        bring_in("the senior AE", "the practice lead")    # Leadership resolves commercial hesitation

    elif situation.blocker_type == "POLITICAL":
        bring_in("the delivery lead", "account_owner")  # Relationship resolves political friction

    elif situation.blocker_type == "PROOF":
        build_demo()                     # Demos resolve "can you actually do this?"

    elif situation.blocker_type == "TRUST":
        wait_and_nurture()               # Time resolves trust deficits
```

### `CONTROL.meeting_flow(meeting_type) → Agenda`

```python
MEETING_PROGRAMS = {
    "first_meeting": [
        SENSE.detect_pain,          # 60% of time — listen
        ACT.tell_story,             # 20% — one powerful insight
        ACT.demo,                   # 10% — if you have a relevant prototype
        ACT.ask(level=1),           # 10% — get the next meeting
    ],
    "workshop": [
        ACT.demo,                   # 35% — flex capability
        SENSE.detect_pain,          # 40% — brainstorm together
        PROCESS.frame_value,        # 15% — connect pain to solutions
        ACT.ask(level=2),           # 10% — propose POC or scoping
    ],
    "poc_review": [
        ACT.demo,                   # 50% — show what you built
        SENSE.read_room,            # 20% — gauge reaction
        PROCESS.position_cost,      # 20% — here's the full engagement
        ACT.ask(level=4),           # 10% — propose SOW
    ],
    "executive_briefing": [
        ACT.tell_story,             # 40% — industry insight, not feature list
        PROCESS.match_pattern,      # 30% — "your peers are doing X"
        ACT.demo,                   # 20% — one powerful proof point
        ACT.ask(level=2),           # 10% — "let's explore this with your team"
    ],
}
```

### `CONTROL.deal_lifecycle() → Pipeline`

```python
DEAL_STATES = {
    "COLD":       { "focus": "PROVOKE + SENSE", "duration": "weeks-months" },
    "INTERESTED": { "focus": "SENSE + NURTURE", "duration": "weeks" },
    "EXPLORING":  { "focus": "DEMO + WORKSHOP", "duration": "1-4 weeks" },
    "EVALUATING": { "focus": "POC + PROOF",     "duration": "2-6 weeks" },
    "DECIDING":   { "focus": "ASK + REMOVE BLOCKERS", "duration": "1-2 weeks" },
    "CLOSING":    { "focus": "SOW + SIGNATURE", "duration": "days" },
    "WON":        { "focus": "DELIVER + EXPAND", "duration": "ongoing" },
}

# Key insight: most deals stall in EVALUATING because sellers
# don't know how to transition from "showing" to "asking"
```

---

## Layer 5: COMPOSE — Skill Combinations (The Real Power)

_Like function composition `f(g(x))`. These are the compound moves._

### The "Signature Sequence" — Long-Cycle Enterprise Deal

```python
def signature_sequence(account):
    # Phase 1: Establish (months)
    while not relationship.mature:
        ACT.follow_up(value_add=True)
        SENSE.map_stakeholders(account)
        PROCESS.read_politics(account)
        ACT.wait(strategy="nurture")

    # Phase 2: Position (weeks)
    pain = SENSE.detect_pain(account)
    solution = PROCESS.match_pattern(pain)
    value = PROCESS.frame_value(solution, account)

    # Phase 3: Prove (days-weeks)
    demo = ACT.demo(build_prototype(solution))
    reaction = SENSE.read_room(demo)

    # Phase 4: Close
    if reaction.positive:
        ACT.ask(level=4)  # SOW
    else:
        PROCESS.assess_timing(reaction)
        # Loop back to Phase 2 with new information
```

### The "Tech Blitz" — Fast-Track Technical Deal

```python
def tech_blitz(problem):
    # Skip relationship building — lead with proof
    demo = ACT.demo(build_rapid_prototype(problem))
    reaction = SENSE.read_room(demo)

    if reaction.impressed:
        ACT.ask(level=3)  # "Let us do this for real"
    elif reaction.skeptical:
        ACT.demo(deeper_proof)  # Double down on proof
    elif reaction.confused:
        ACT.tell_story(simplify(problem))  # Reframe
```

### The "Tech Bridge" — Tech-Led Value Creation

```python
def tech_bridge_pattern(client_meeting):
    """
    A repeatable signature move:
    Hear the problem → build proof fast → let the proof do the selling
    """
    # In the meeting: listen like a developer debugging
    pain = SENSE.detect_pain(client_meeting)
    pattern = PROCESS.match_pattern(pain)

    # After the meeting: build like a hackathon
    if pattern.known:
        prototype = customize_accelerator(pattern.accelerator, client_context)
    else:
        prototype = rapid_build(pain, 3_days)

    # Next meeting: demo like a founder
    reaction = ACT.demo(prototype, framed_as="proof, not product")

    # The bridge: connect technical proof to business value
    value = PROCESS.frame_value(prototype.capabilities, client.business_outcomes)
    ACT.tell_story(value)

    # Hand off to sales to close
    ACT.ask(level=3)  # "Want us to do this against your real data?"
```

---

## Skill Assessment: Where Am I Today?

_Rate yourself honestly. Update monthly._

| Skill | Current Level (1-5) | Evidence | Next Level Action |
|---|---|---|---|
| `SENSE.read_signal` | 2 | Can identify in transcript review, not yet live | Practice live classification in next 3 meetings |
| `SENSE.read_room` | 2 | Aware of dynamics but don't adjust in real-time | In next meeting, note power map within first 5 min |
| `SENSE.detect_pain` | 3 | Good at technical pain; learning business/political pain | Ask "what's the business impact?" after every technical pain |
| `SENSE.map_stakeholders` | 2 | Know names and titles; learning motivations | Before next meeting, hypothesize each person's motivation |
| `PROCESS.frame_value` | 3 | Can do it in writing; practicing live | Prep 3 value statements before each meeting |
| `PROCESS.position_cost` | 2 | Understand the concepts; haven't done it live | Study how the senior AE presents options in next meeting |
| `PROCESS.assess_timing` | 1 | Still learning when to push vs wait | Ask the senior AE "why now?" after every deal decision |
| `PROCESS.match_pattern` | 3 | Growing — each engagement adds to the library | Document every new pattern in pattern library |
| `PROCESS.read_politics` | 1 | a credit-bureau client politics caught me off guard | Study CapEx/OpEx and procurement for next 3 clients |
| `ACT.demo` | 4 | Strongest skill — a working prototype proves this | Polish the bridge from demo to business value |
| `ACT.tell_story` | 2 | Have the POV; practicing the delivery | Write and rehearse 3 client-specific stories |
| `ACT.ask` | 1 | Haven't made a commercial ask yet | Set goal: make one Level 2 ask in next 2 weeks |
| `ACT.follow_up` | 3 | Consistent but could be more strategic | Add value-add content to every follow-up |
| `ACT.pivot` | 2 | Can recognize when to pivot; slow to execute | Practice "what would I do if [X] changed?" before meetings |
| `ACT.wait` | 2 | Intellectually understand; emotionally hard | Study the senior AE's patience on a credit-bureau client as model |

---

## Weekly Practice Protocol

```
MONDAY:    Review last week's meetings → log new patterns
           Update skill self-assessment if evidence changed

BEFORE EACH MEETING:
           - Which skills will I practice today?
           - What's my hypothesis for the room (stakeholders, signals)?
           - What's the minimum ask I'll make?

AFTER EACH MEETING:
           - What signals did I miss?
           - What would the senior AE/the tech lead have done differently?
           - What pattern goes into the library?

FRIDAY:    Review observation log → update sales-pattern-intelligence.md
           One thing I'll do differently next week
```

---

## Version History

| Version | Date | What Changed |
|---|---|---|
| v0.1 | 2026-04-08 | Initial SDK from 8 meeting notes. Core skills defined. Self-assessment baseline. |

---

_Companion file:_
- `sales-pattern-intelligence.md` — observed patterns (the "programs" built from these skills)
