# Playbook: Customer Research Methodology

> **Version:** 1.0 | **Source:** field-tested 5-step deep research process for client/prospect intelligence
> **Use when:** Preparing for a major engagement, building a presales pack, or scoping a new client relationship.
> **Output:** Complete client intelligence file at `research/intel/{Company}_Client_Intel_*.md`
> **Trigger skill:** `/g-customer-intel {Company}`

---

## Overview

This is Tavant's management-consulting-grade research methodology for understanding a client before engaging. It goes far beyond web scraping — it builds a complete picture of a company's financial structure, technology landscape, insider context, market position, and strategic fit with Tavant's capabilities.

The process is sequential. Each step builds on the previous one. Don't skip steps — the compounding intelligence is the point.

---

## Step 1: Financial & Business Structure

**Goal:** Understand how the company makes money, how it's organized, and where it sits in the value chain.

### What to Find

| Dimension | Details | Primary Sources |
|---|---|---|
| **Business units** | Names, leaders, what each unit does | SEC filings (10-K, 10-Q), annual reports, investor presentations |
| **Revenue by segment** | Revenue per business unit, growth trends, mix changes | SEC filings, earnings calls, analyst reports |
| **Cost structure** | Operating expenses, technology spend, headcount | 10-K filings, earnings transcripts |
| **Assets & liabilities** | Loan portfolios, MSR values, warehouse lines, debt structure | Balance sheet, SEC filings |
| **Ownership** | Public/private, major shareholders, PE/VC backing, parent company | SEC proxy statements, Crunchbase, news |
| **M&A history** | Recent acquisitions, divestitures, mergers | News, SEC filings, press releases |
| **Value chain position** | What market segment (prime, near-prime, sub-prime)? What part of the lending lifecycle? | Company website, regulatory filings, GSE data |
| **Source of business** | Where do loans come from? (dealers, brokers, retail, correspondent) | HMDA data, GSE loan-level data, company disclosures |

### For Unlisted Companies

Public filings won't exist. Use derivative means:
- **GSE data** — loans underwritten are reported to Fannie Mae, Freddie Mac, Ginnie Mae
- **HMDA data** — Home Mortgage Disclosure Act filings show volume, geography, demographics
- **State regulator filings** — NMLS, state licensing databases
- **Job postings** — headcount and tech stack signals
- **LinkedIn** — employee count trends, hiring patterns
- **Industry rankings** — Inside Mortgage Finance, HousingWire, National Mortgage News annual lists
- **Bond offerings / ABS deals** — if they securitize, deal documents are public

### Quality Check

You must be able to answer: "How does this company make money, and what are the 2-3 things that could break that model?" If you can't, the step is incomplete.

---

## Step 2: Technology Platform Mapping

**Goal:** Build a view of what platforms the company uses (or should use) to support each business unit end-to-end.

### The Lending Technology Stack

For any form of lending, the platform stack follows this lifecycle:

| Stage | Function | Common Platforms |
|---|---|---|
| **CRM** | Lead management, borrower pipeline | Salesforce, Velocify, Shape, GoHighLevel |
| **Loan Acquisition** | Point of sale, application intake | Encompass Consumer Connect, Blend, Maxwell, ICE PPE |
| **Loan Origination (LOS)** | Core loan processing and workflow | Encompass, Empower, MortgageBot, MortgageFlex |
| **Loan Underwriting** | Credit decision, risk assessment | DU/LP (GSE AUS), proprietary engines, AI/ML models |
| **Loan Pricing** | Rate lock, pricing engine, margin management | Optimal Blue, Polly, Mortech, Lender Price |
| **Loan Closing** | Doc prep, e-closing, notarization | DocMagic, Snapdocs, Notarize, BeSmartee |
| **Loan Servicing** | Payment processing, escrow, investor reporting | MSP (Black Knight), Sagent, FICS, LoanServ |
| **Loss Mitigation** | Default management, workout, foreclosure | MSP, FICS, internal tools |
| **Accounting** | GL, sub-ledger, loan accounting | Oracle, SAP, custom, LoanServ |
| **Reporting** | Regulatory, investor, management reporting | Cognos, Tableau, Power BI, custom |

### Process

1. Use GPT and Claude independently to assess the client's likely platform stack based on:
   - Public job postings (mention specific platforms)
   - Technology partner announcements
   - Conference presentations
   - Implementation case studies from vendors
   - Client's size and segment (determines platform tier)
2. Cross-reference the two assessments
3. Map gaps — where the client likely has manual processes or outdated systems
4. Identify **platform pain points** — where the tech stack creates friction

### Output

A matrix: Business Unit x Technology Stage x Known/Inferred Platform. Mark confidence level (confirmed / likely / unknown) for each cell.

---

## Step 3: Insider Intelligence

**Goal:** Ground the external research in internal knowledge that only Tavant has.

### Sources to Mine

| Source | What to Look For | How to Access |
|---|---|---|
| **People who worked on the account** | Reach out to anyone at Tavant who has touched this client in the last 10-15 years | Ask the senior AE, the delivery lead, check Salesforce history |
| **QBR decks** | Quarterly business reviews from past engagements | Search Notion, SharePoint, Google Drive |
| **Past SOWs and proposals** | Scope, pricing, what was proposed vs. what was delivered | Salesforce documents, shared drives |
| **Meeting notes** | Discovery call notes, executive conversations | Notion meeting notes, personal files |
| **Validated assessments** | Have internal contacts confirm/deny platform mapping from Step 2 | 1:1 conversations with a validated internal contact at the client |

### The Conversation

When you find someone who's worked with the client:
1. Share your Step 1-2 findings — "Here's what we've pieced together externally"
2. Ask them to validate or correct — "What's wrong? What's missing?"
3. Ask for the political map — "Who makes decisions? Who blocks? Who champions?"
4. Ask for the scars — "What went wrong last time? What would we do differently?"

### Quality Check

The insider step is what separates a generic research report from a Tavant competitive advantage. If you skip this, you're competing with every other consultancy that can read SEC filings.

---

## Step 4: Market & Impact Analysis

**Goal:** Understand what's happening in the client's market segment and how it will impact their financials, operating model, and technology needs.

### Analysis Framework

Ground this in insider knowledge from Step 3. Ask:

1. **What macro trends affect this client's segment?**
   - Interest rate environment → origination vs. servicing balance
   - Regulatory changes → compliance burden, new requirements
   - Consumer behavior shifts → digital expectations, channel preferences
   - Housing market dynamics → inventory, pricing, regional variation

2. **How will these trends impact the client specifically?**
   - Revenue model stress (e.g., refi volume collapse in rising rate environment)
   - Operating model pressure (e.g., need to cut costs per loan)
   - Technology modernization urgency (e.g., legacy systems can't support new channels)
   - Competitive pressure (e.g., fintechs eating market share in their segment)

3. **What does this mean for their IT platforms?**
   - Which platforms need replacement vs. augmentation?
   - Where does AI/automation create the most leverage?
   - What's the cost of inaction? (quantify if possible)

### Output

A narrative: "Given [market dynamics], this client will need to [strategic imperatives], which means their [technology/platform] needs to [change in specific ways]. Tavant's play is [specific entry point]."

---

## Step 5: Case Study Grounding

**Goal:** Map the themes from Steps 1-4 against Tavant's library of 80+ fintech case studies to provide concrete proof points and precedent.

### Process

1. Break the themes from Step 4 into sub-parts (e.g., "needs to reduce cost per loan" → underwriting automation, document processing, quality control automation, servicing efficiency)
2. For each sub-part, search the case study library for relevant examples
3. Match by: industry segment, company size, problem type, technology approach, outcome metrics
4. For each match, extract: what was the problem, what was built, what was the measurable outcome

### Case Study Sources

- Tavant case studies (internal library, website, marketing materials)
- Public implementation case studies from technology vendors
- Industry analyst reports (Forrester, Gartner, IDC) with named examples
- Conference presentations with real metrics

### Output

A mapping table: Client Theme → Sub-Part → Relevant Case Study → Key Metric. This becomes the "proof" section of any proposal or presales deck.

---

## Sequencing & Timing

| Step | Effort | Can Be Automated? | Depends On |
|---|---|---|---|
| 1. Financial & Business Structure | 2-4 hours | Mostly (SEC filings, web research) | Nothing |
| 2. Technology Platform Mapping | 2-3 hours | Partially (job postings, public info) | Step 1 (need to know business units) |
| 3. Insider Intelligence | 1-5 days | No (human conversations required) | Steps 1-2 (need something to validate) |
| 4. Market & Impact Analysis | 2-3 hours | Partially (market research + synthesis) | Step 3 (ground in insider knowledge) |
| 5. Case Study Grounding | 1-2 hours | Mostly (search + match) | Step 4 (need themes to ground) |

**Total:** 1-2 weeks for a thorough intelligence package. Steps 1-2 can run in the first day. Step 3 is the bottleneck — it depends on finding and scheduling conversations.

---

## Anti-Patterns

- **Skipping Step 3** — External research alone produces the same output anyone can produce. Insider intel is Tavant's edge.
- **Generic market analysis** — "The mortgage industry is undergoing digital transformation" is useless. Be specific: which segment, which clients, which platforms, what numbers.
- **Case studies without metrics** — "We built an AI solution for a lender" doesn't persuade. "We reduced underwriting time by 40% for a top-10 servicer" does.
- **Not validating platform mapping** — Job postings and conference talks can be misleading. Always validate with someone who's been inside.
- **Treating this as a one-time exercise** — The best client intelligence is continuously updated. Set up a refresh cadence.

---

_Last updated: 2026-04-28 | Next review: After first full execution on a live client_
