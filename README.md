# sales-skills

**Your AI helper for selling smarter, not harder.**

Think of this like a really organized assistant sitting next to you. It doesn't replace you — it
just does the boring homework, keeps track of what's going on, and hands you what you need right
when you need it. You still make every call.

## The big idea

Microsoft's own sales teams have already figured something out, and it's the whole reason this
exists: **a seller spends more time wrestling with systems than actually talking to customers.**
Digging up account info, planning who to call, drafting outreach, tracking a deal, figuring out
who else to sell to at a company you already won — all of that is busywork sitting *between* the
moments that actually matter. That busywork is exactly what an AI assistant should be quietly
handling in the background, everywhere in your day, not just one part of it. That's the standard
we're holding ourselves to — a real assistant woven through the whole job, not a chatbot bolted
onto one step of it.

## What it helps you do

**Tells you who to call this week.**
You can't give every single customer your full attention — nobody can. This looks at everything
you're working on and picks the handful that matter most right now, so your time goes where it
actually pays off instead of being spread a little bit over everyone.

**Helps you write a smarter first message.**
Instead of a generic "just checking in," it does the homework first — what's going on at that
company, what they care about, who else they might be shopping around with — so your first message
sounds like you already understand their problem, not like a form letter.

**Gives you an honest read on how a deal is really going.**
Instead of a gut feeling, you get a simple, honest signal — is this deal in great shape, okay shape,
or shaky? And it's not afraid to say "not sure yet" instead of pretending to know more than it does.

**Learns from what actually happens.**
Every time a deal is won or lost, it checks itself against the real outcome — did it call that one
right or not — and gets sharper over time instead of just repeating the same guesses.

**Never does anything behind your back.**
It never sends an email, message, or note for you. It writes a draft, you read it, you decide, you
hit send. Same with anything it wants to remember about a deal — you get to check it first.

## Why it's worth using

Less time spent guessing who to chase and what to say, more time spent actually talking to the
customers most likely to say yes — and a clear, honest picture of how things are going so you (and
the team) always know what's working.

## Getting it installed

There are **two ways** to get this, depending on what you already use day to day. Pick the one
that matches your setup — you don't need both.

### Option A — you already use Claude Code (the terminal app)

This is the easier path if you have it, because updates arrive automatically later.

Once you have Claude Code open, run these two commands:

```
/plugin marketplace add git@gitlab.tavant.com:fintech-ai/sales-skills.git
/plugin install tvt-sales-skills@tvt-sales-skills
```

That's it — every skill in this toolkit is now available in that Claude Code session.

**If the first command says the host isn't allowed:** your organization has a plugin allowlist
turned on. That's an admin setting (`strictKnownMarketplaces` in Claude Code's managed settings) —
ask whoever manages your Claude Code rollout to add `gitlab.tavant.com` to it, then try again.

**If you're trying this from claude.ai's website (the "Directory" / Skills-Connectors-Plugins
panel) instead of the Claude Code terminal app:** stop — it will never work from there for this
option. That part of claude.ai runs in Anthropic's cloud and has no way to reach a repo that lives
behind Tavant's firewall, no matter which URL format you try. If you're on claude.ai and don't have
Claude Code, use Option B below instead.

### Option B — you use the Claude Desktop app (no terminal needed)

Claude Desktop can add this whole toolkit directly from its repository URL — no zip building,
no per-skill upload, no `releases/` snapshot to keep in sync.

1. In Claude Desktop, go to **Settings → Customize → Skills** (or wherever your version of the
   app surfaces adding a skill source by repository URL).
2. Add this repo's URL as a skill source.
3. Every skill in the toolkit becomes available, the same way `/plugin install` works in Claude
   Code — and it updates when this repo does, since it's reading the repo directly rather than a
   one-time uploaded snapshot.

If your version of Claude Desktop doesn't yet support adding a repository URL as a skill source,
fall back to `scripts/build-zips.sh` to build a one-off `.zip` for the specific skill you need and
upload it via **Create skill** — but that path won't auto-update, and a fresh build is your
responsibility to know when's needed.

## Your first 10 minutes

When in doubt, always start with `tvt-sales-engine` — it's the front door, and it routes you to
everything else in the toolkit. Here are three asks you can copy-paste right now:

**1. Find out who deserves your week.**

```
tvt-sales-engine "who should I focus on this week"
```

You get back a short, ranked focus list — the handful of deals worth your attention now, plus an
honest "parked" list of the rest. It needs one thing from you first: a small file listing your
deals. There's a ready-made example at `skills/tvt-sales-prospect/scripts/opportunities.example.json`
— copy it, replace the entries with your deals, and you're set.

**2. Do the homework before a call.**

```
tvt-sales-engine "research Acme Credit Union before my call"
```

You get back a proper account dossier — what's going on at the company, what they care about, and
who the players are — so you walk in sounding like you already understand their world.

**3. Get an honest read on your pipeline.**

```
tvt-sales-engine status
```

You get back a plain scorecard of how your whole book is doing — including where it honestly isn't
sure yet, instead of pretending. **This one needs a different example file than #1** — copy
`skills/tvt-sales-prospect/scripts/kpi_opportunities.example.json` instead (it tracks stage/amount/
dates, not the ranking fields from #1's file). Using #1's file here will fail with a raw error
instead of a scorecard.

One thing to know up front: **it drafts, you send — nothing goes to a client without you.**
