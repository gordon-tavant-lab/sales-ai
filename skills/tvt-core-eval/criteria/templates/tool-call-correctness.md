# Tool-Call Correctness Rubric

Use for AI agent outputs that invoke external tools: function calls, MCP server
calls, shell commands, API calls. Critical for agentic systems where wrong tool
selection or wrong arguments cascade into real-world consequences.

## Criterion 1: Right tool selected (weight: 5)

**What to look for:** The tool chosen matches the task. No wrong tools used; no
right tools missed.

**Score 1.0:** Optimal tool for the task.
**Score 0.5:** Suboptimal but workable tool chosen (e.g., grep when ast-grep
would be cleaner).
**Score 0.0:** Wrong tool used (e.g., Bash for what should be Read; web search
for what's already in the context).

**Source:** AgentBench tool-use category; SWE-bench tool-selection metric.

## Criterion 2: Arguments valid and correct (weight: 5)

**What to look for:** All required arguments present; types correct; values
make sense for the task.

**Score 1.0:** All arguments correct.
**Score 0.5:** Minor argument issue (e.g., relative path when absolute preferred).
**Score 0.0:** Required argument missing, wrong type, hallucinated argument
(e.g., a flag that doesn't exist), or value that obviously doesn't fit (file path
to a file that doesn't exist).

**Source:** ToolBench; Function-calling evals.

## Criterion 3: Sequence / dependency order (weight: 4)

**What to look for:** When multiple tools are called, the order makes sense.
Reads before writes, listing before specific access, auth before authenticated
calls.

**Score 1.0:** Correct order; parallel where independent.
**Score 0.5:** One avoidable inefficiency (e.g., serial when parallel possible).
**Score 0.0:** Critical order violation (write to file before reading it; call
authenticated endpoint before auth).

**Source:** AgentBench multi-step tool-use category.

## Criterion 4: Error handling (weight: 4)

**What to look for:** When a tool call fails or returns unexpected data, the
agent recognizes it and adapts (retries, fallbacks, asks user) rather than
proceeding as if it succeeded.

**Score 1.0:** Errors recognized and handled correctly.
**Score 0.5:** Error noted but not adapted to.
**Score 0.0:** Error ignored or treated as success; downstream actions taken
on bad data.

**Source:** SWE-bench error-recovery patterns.

## Criterion 5: No unnecessary tool calls (weight: 3)

**What to look for:** Tool calls that don't serve the task aren't made. No
"checking" things twice. No exploratory Bash calls that the model should already
know the answer to from context.

**Score 1.0:** All tool calls serve the task.
**Score 0.5:** 1–2 unnecessary calls (mild context-burning).
**Score 0.0:** Multiple unnecessary calls (significant cost / latency waste).

**Source:** common agent-eval anti-pattern.
