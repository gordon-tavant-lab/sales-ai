# Deep-Research Query Library — 9 dimensions, ~37 queries

The web-research procedure `tvt-intel-deep`, `tvt-intel-customer`, and `tvt-intel-fanout` run
before writing any intel file. Fan the queries below out in parallel batches per dimension,
substituting `{Company}` (and `{Industry}` where present) with the actual research target.
Not every query will return useful results for every company — that's expected. The
**minimum bar is 5 unique contributing sources** across all dimensions combined (per each
calling skill's own Step 1 requirement); fewer than 5 means the research is incomplete, not
a shorter-than-usual report.

## A — Company overview & financials
1. "{Company}" annual report OR 10-K OR investor presentation
2. "{Company}" revenue OR funding round OR valuation 2026
3. "{Company}" ownership structure OR parent company OR subsidiaries
4. "{Company}" headcount OR employee count site:linkedin.com

## B — Leadership & organization
5. "{Company}" CEO OR CTO OR "Chief AI Officer" OR "Chief Digital Officer"
6. "{Company}" leadership team OR executive bio
7. "{Company}" org chart OR reporting structure {industry}
8. "{Company}" recent leadership hire OR departure 2026

## C — Technology stack & platform
9. "{Company}" technology stack OR platform architecture
10. "{Company}" vendor OR "case study" site:*.com -site:{company-domain}
11. "{Company}" API OR integration partner
12. "{Company}" job posting engineer OR "software developer" (stack signals via requirements)

## D — Competitive landscape
13. "{Company}" competitors OR "vs" comparison {industry}
14. "{Company}" market share OR industry ranking
15. "{Company}" competitive displacement OR "lost to" OR "switched from"
16. "{Company}" analyst report OR Gartner OR Forrester

## E — Pain points & challenges
17. "{Company}" challenges OR pain point OR "struggling with" {industry}
18. "{Company}" customer complaint OR review site:trustpilot.com OR site:g2.com
19. "{Company}" regulatory action OR compliance issue OR lawsuit
20. "{Company}" operational inefficiency OR manual process {industry}

## F — Recent news & signals
21. "{Company}" news 2026
22. "{Company}" press release site:prnewswire.com OR site:businesswire.com
23. "{Company}" earnings call transcript
24. "{Company}" acquisition OR merger OR partnership announcement

## G — Regulatory & compliance context ({industry}-specific)
25. "{Company}" {industry} regulatory requirement OR compliance framework
26. "{Company}" audit OR examination OR consent order
27. "{Company}" data privacy OR security incident

## H — Partnerships & vendor relationships
28. "{Company}" partnership OR "strategic alliance" 2026
29. "{Company}" vendor relationship OR "powered by" OR "in partnership with"
30. "{Company}" RFP OR procurement OR vendor selection {industry}

## I — Growth & expansion signals
31. "{Company}" expansion OR "new market" OR "new product" 2026
32. "{Company}" hiring surge OR "we're hiring" {industry}
33. "{Company}" investment OR "Series" funding round recent
34. "{Company}" conference OR speaking engagement OR thought leadership
35. "{Company}" digital transformation OR AI initiative OR automation strategy
36. "{Company}" customer growth OR user base OR "market leader"
37. "{Company}" strategic priority OR roadmap OR "next chapter"

## Coverage-gap reporting

After running all applicable queries, report per dimension: `covered` (2+ useful sources),
`thin` (1 source), or `gap` (0 sources). A `gap` in dimension E (pain points) or D
(competitive landscape) is the most consequential — those two dimensions are what turn
research into an actionable first-move, per the Chief-of-Staff quality bar these skills
target. Don't silently drop a gap; name it in the output so the reader knows what's
unverified vs. simply absent.
