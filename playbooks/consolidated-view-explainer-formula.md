# The Consolidated-View Explainer — Construction Formula

> Reverse-engineered from a real mortgage-insurance client's lifecycle documentation.
> A repeatable formula for a 5–7 page document that **explains a complex multi-part system AND argues for a design decision** — without sounding like a sales pitch.
> Use this when you need to make a domain look inevitable and a recommendation look obvious.

---

## 0. What this document actually is (read this first)

On the surface it's a calm, neutral "here's how the three MI processes fit together." That framing is the trick. It is really a **build-the-case document** with a hidden argument arc:

> *These things are already one system → here's how the pieces connect → therefore you should run them as one estate / one warehouse.*

The reader feels they are being **informed**, not sold. By the time the recommendation arrives (§7), it reads as the natural conclusion of facts already accepted — not an opinion. **That is the entire effect to reproduce.**

Three forces make it work, and every technique below serves one of them:

| Force | What it does | Where it lives |
|---|---|---|
| **Coherence** | Makes a sprawling domain feel simple and inevitable | One mental model, repeated vocabulary, parallel structure |
| **Credibility** | Makes claims trustworthy, not promotional | Named real standards, stated trade-offs, captions that don't oversell |
| **Compression** | Lets a busy exec extract the thesis in 30 seconds | Layered reading, framing sentences, takeaway box, summary |

---

## 1. The macro-structure (the skeleton)

Nine sections in a deliberate rhetorical sequence. The **order is the argument** — it walks from neutral description to a recommendation:

```
COVER        Scope contract — what this is, what it covers, how it relates to other docs
 │
 1. ONE PICTURE        Simplest mental model. One verb per actor. The spine.        ┐
 2. HOW THEY OVERLAP   They're not separate islands (Venn). Shared center + seams.  │ DESCRIBE
 3. SIDE BY SIDE       Structured comparison table. Parallel columns.               ┘ (build the model)
 │
 4. HOW THEY CONNECT   From → To → Why table. The handoffs as explicit edges.       ┐ RELATE
 5. DATA MOVEMENT      The artifact grows as it moves. Progressive chain.           ┘ (show the wiring)
 │
 6. SHARED FOUNDATION  They already stand on one platform. → "one estate."          ┐ SET UP
 │                                                                                  ┘ the claim
 7. THE CASE           "Each can run its own X. But one Y is stronger." + trade-off. ← THE ARGUMENT
 8. UNIFYING PRINCIPLE The single rule that explains why it all looks alike.        ← THE INSIGHT
 │
 9. SUMMARY            Three bolded bullets. Thesis restated. + one-line takeaway.  ← THE ANCHOR
```

**Why this order is load-bearing:** §1–6 are almost impossible to disagree with — they're just describing what exists. Each accepted section is a brick. §7 then spends that accumulated agreement on the one claim that's actually contestable ("consolidate the warehouse"). You can't reorder this; the recommendation only lands because the description came first.

### The reusable section arc (domain-agnostic)

1. **The system in one picture** — establish the simplest model
2. **How the parts overlap** — they're connected, not separate
3. **The parts side by side** — structured comparison
4. **How the parts connect** — explicit handoffs/edges
5. **How the [data/value/artifact] moves** — the dynamic view
6. **The shared foundation** — what they have in common
7. **The case for [your recommendation]** — the argument + the trade-off
8. **The unifying principle** — the one idea that explains the whole
9. **Summary** — restate in 3 bullets + a one-liner

---

## 2. The micro-structure (every section is the same shape)

This rhythm repeats on every page — it's what makes the doc feel authoritative and easy to skim:

```
## N. Section title                         ← verb-y, plain-language, numbered
[accent rule under heading]

One or two framing sentences.               ← states the takeaway BEFORE the visual
The second sentence often does the work.    ← e.g. "They are not separate islands."

[ONE artifact: a figure OR a table — almost never both, never prose-heavy]

Figure N. Caption that restates the point.  ← italic; re-says the takeaway in different words
```

**Rules that make the rhythm work:**
- **One idea per section.** If a section needs two artifacts, it's two sections.
- **Framing sentence first.** Never make the reader decode a diagram cold — tell them what they're about to see, then show it. The visual confirms; it doesn't reveal.
- **The caption is a second chance at the thesis.** A skimmer who reads only headings + captions should still get the whole argument. Captions paraphrase the point, they don't describe the picture ("Figure 2. The overlap — shared data at the centre; the hand-off, the policy of record... at the seams").
- **Tables for comparison, figures for flow.** Comparing parallel things → table with consistent columns. Showing movement/relationship → diagram.

---

## 3. The visual vocabulary (only ~5 artifact types, reused)

The document never invents a new diagram style. It reuses a tiny kit, which is why it feels designed rather than assembled:

| Artifact | Job | Example in source |
|---|---|---|
| **Swimlane / column blocks** | Show parallel processes and their internal stages | Fig 1: Origination / Servicing / Claims columns |
| **Venn (2–3 circles)** | Show overlap + name what lives in each intersection | Fig 2: shared center + named seams |
| **Comparison table** | Parallel attributes across the same set of things | §3 (Purpose / Core flow / Anchor entity / Bucket) |
| **From → To → Why table** | Make relationships/handoffs explicit and auditable | §4 connections table |
| **Progressive-disclosure chain** | Show one thing growing/transforming as it moves | Fig 3: MI App → +premium → +adjudication → lake |
| **Callout box** | Quarantine the single most important sentence | §6 "The one-line takeaway" |

**Design discipline that signals seriousness:**
- Consistent **header/footer** every page (doc title left · scope tag right; companion line + page number at bottom). Cheap to do, huge credibility payoff.
- **Color = meaning, not decoration.** Each domain owns one color (blue/green/purple) and keeps it across every figure. Dark-navy table header rows, light alternating row shading.
- **Restraint.** No icons-for-icons'-sake, no gradients, no clip art. White space does the work.

---

## 4. The argument & validation engine (the part most people miss)

This is what separates this doc from a generic "overview." The persuasion is structural, not loud.

### 4.1 The "earned recommendation" pattern (§7)
The single most reusable move. The template:

> "Each [part] can run its own [X]. **But** one consolidated [Y] — fed by all [parts] — is stronger."

Then a bulleted **"Why [Y] beats [separate Xs]"** list, each bullet a **bolded benefit lead-in** + one supporting sentence:
- *One source of truth.* (the numbers tie out once)
- *End-to-end history.* (the full story in one place)
- *Cheaper, faster reporting.*
- *Stronger [capability A].* / *Stronger [capability B].*

### 4.2 Name the trade-off — out loud
The list ends with a bullet titled **"The trade-off."** It states the cost/risk of the recommendation and how to mitigate it. **This is the credibility keystone.** A doc that only lists benefits reads as a pitch; a doc that names its own downside reads as analysis. Always include one.

### 4.3 Validation techniques (how claims earn trust without footnotes)
- **Drop real, checkable proper nouns.** NAIC, PMIERs, HMDA, SOX, reinsurance, ERP, GL. These anchor abstract claims to a reality the reader recognizes — instant grounding, zero citations needed.
- **Anchor entities & fixed vocabulary.** Every domain gets one "anchor entity" (MI Application / Certificate / Claim) and the *same* verbs recur ("commits," "maintains," "pays"). Repetition with variation = internal coherence = feels true.
- **A unifying principle that predicts the pattern (§8).** "The same placement rule holds in every domain — *which is why the three look alike.*" Explaining *why* the structure recurs is far more convincing than asserting that it does. This converts observation into law.
- **Layered framing of the same idea.** The thesis appears as: a sentence (§1) → proven across §2–8 → a callout box one-liner (§6) → three bullets (§9). Same claim, four resolutions. By the fourth, it feels settled.

---

## 5. The copy / tone rules

- **Verbs over nouns.** "Origination *issues* the commitment. Servicing *activates and maintains*... Claims *pays* loss." Active, short, declarative.
- **Plain headings.** "How the domains connect," not "Inter-Domain Integration Architecture."
- **Framing sentence carries the load.** The most important sentence in each section is the one *before* the visual.
- **Bold lead-ins on every bullet** so the page is scannable at a glance.
- **One "money sentence" per doc**, quarantined in a callout box. Write the whole doc so that sentence is the inevitable conclusion. (Source: *"Three processes, one lifecycle, one platform... deterministic cores owning the money and AI working the edges under human approval."*)
- **No adjectives doing argumentative work.** Not "a powerful, best-in-class warehouse" — instead "the numbers tie out once." Concrete consequence beats hype.

---

## 6. The fill-in-the-blanks template

Copy this and replace the brackets. If you can't fill a blank, you don't understand that part of the system yet — which is the point.

```markdown
KICKER: [DOCUMENT TYPE IN CAPS — e.g. "CONSOLIDATED VIEW"]
# [System name]
## [Part A] · [Part B] · [Part C]

> One view of [the N parts]: how they connect and overlap, how [data/value]
> moves, and the case for [your recommendation].
> Companion to [the deeper source docs, if any].

## 1. [The system] in one picture
[Part A] [verb]s the [thing]. [Part B] [verb]s and maintains it. [Part C] [verb]s [outcome].
They are joined by clear handoffs, and a [feedback loop] carries [signal] back to [origin].
[FIGURE: swimlane columns — one per part, internal stages stacked below]

## 2. How the parts overlap
They are not separate islands. They share [core data] and one [platform], and meet at clear seams.
[FIGURE: Venn — shared center labeled; each pairwise seam named]

## 3. The parts side by side
[TABLE: Part | Purpose | Core flow | Anchor entity | [your 5th column]]

## 4. How the parts connect
[TABLE: From | To | What flows / why]

## 5. How [the artifact] moves
The [artifact] grows as it moves. [A] perfects it, [B] maintains it, [C] [acts] against it.
[FIGURE: progressive chain — [Artifact] → +[fields] → +[fields] → [sink]]

## 6. The shared foundation
All [N] stand on the same platform — which lets them be built and run as one estate.
[TABLE: Shared element | What it provides across all N]

## 7. The case for [recommendation]
Each [part] can run its own [X]. But one consolidated [Y] — fed by all [N] — is stronger.
[FIGURE: the consolidated end-state]
**Why [Y] beats separate [X]s:**
- **[Benefit 1].** [one sentence]
- **[Benefit 2].** [one sentence]
- **[Benefit 3].** [one sentence]
- **The trade-off.** [the honest cost + how to mitigate]   ← never omit

## 8. The unifying principle
The same [principle] holds in every part — which is why they all look alike.
- **[Layer 1] owns [the authoritative thing].**
- **[Layer 2] predicts and prioritizes.**
- **[Layer 3] reads, extracts and drafts.**
- **A person approves what [commits/pays].**

> **The one-line takeaway**
> [The single sentence the entire doc exists to make land.]

## 9. Summary
- **[Point 1].** [restate]
- **[Point 2].** [restate]
- **[Recommendation].** [restate with the trade-off acknowledged]
```

---

## 7. The 10-point quality checklist

Before any doc in this format ships:

1. ☐ Can a reader get the full thesis from **headings + captions alone**?
2. ☐ Does **every section have exactly one** framing sentence and one artifact?
3. ☐ Is there **one mental model** carried start to finish (not three competing ones)?
4. ☐ Does the vocabulary stay **fixed** (same anchor entities, same verbs)?
5. ☐ Are there **3–5 real, checkable proper nouns** grounding the abstract claims?
6. ☐ Is the **trade-off named out loud** in the recommendation section?
7. ☐ Is there a **unifying principle** that explains *why* the structure recurs?
8. ☐ Is the thesis stated **at least 3 times** at different resolutions (sentence / box / bullets)?
9. ☐ Is there **one quarantined money sentence** the whole doc builds toward?
10. ☐ Does the recommendation read as **inevitable** because §1–6 already won agreement?

---

## 8. When to use this format (and when not to)

**Use it when:** you need to align stakeholders on how a complex multi-part system fits together *and* steer them toward a decision — architecture choices, consolidation/platform cases, "should we build this as one thing or many" debates, domain explainers that precede a proposal.

**Don't use it when:** you need a true neutral reference (drop §7's argument), a single-idea one-pager (too much scaffolding), or a hard financial business case (this earns *conceptual* agreement, not ROI sign-off — pair it with a numbers deck).

**The deepest lesson:** the document's authority comes from *withholding* the recommendation until it's unavoidable. Describe first, argue last, and name your own trade-off. Most people invert this and lead with the ask — which is exactly why their docs read as sales and this one reads as truth.
```
