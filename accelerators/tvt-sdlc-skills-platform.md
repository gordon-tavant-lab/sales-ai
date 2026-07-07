# TVT-SDLC: Enterprise AI-Assisted Software Development Lifecycle Platform

> **Tavant Accelerator** — Drop-in Claude Code skills, hooks, and integrations that give any dev team enterprise-grade AI-powered SDLC. This is reference/pitch material for a SEPARATE accelerator (not part of this plugin's own skill catalog) — cited by `tvt-sales-engagement-proposal` when a client's opportunity is engineering/dev-platform shaped. Its own skill names (`tvt-dev-commit`, `tvt-eval-audit`, etc.) and file-path examples describe that other project's build plan, not anything shipped here.

---

## Executive Summary

TVT-SDLC is a complete Claude Code plugin that standardizes the software development lifecycle for enterprise teams. It provides:

- **27 skills** covering coding, testing, security, deployment, evaluation, ops, and integrations
- **10 hooks** for deterministic quality enforcement (across 6 events)
- **MCP integrations** with Jira, Slack, Teams, GitHub
- **Native OpenTelemetry** observability with eval-first methodology
- **CI/CD automation** via GitHub Actions / GitLab CI

**Core principle:** "AI is only as good as the method to evaluate it." The eval layer is not optional — it's the foundation that makes everything else trustworthy and improvable.

---

## Architecture: 6-Layer Stack

```
┌─────────────────────────────────────────────────────────────────┐
│  Layer 5: EVAL & OBSERVABILITY                                  │
│  tvt-eval-* — Trace, measure, judge, improve                   │
├─────────────────────────────────────────────────────────────────┤
│  Layer 4: CI/CD PIPELINE                                        │
│  tvt-dev-cicd — GitHub Actions, quality gates, deploy gates     │
├─────────────────────────────────────────────────────────────────┤
│  Layer 3: ENTERPRISE INTEGRATIONS                               │
│  tvt-int-* — Jira, Slack, Teams, GitHub (MCP servers)           │
├─────────────────────────────────────────────────────────────────┤
│  Layer 2: HOOKS (Deterministic Automation)                      │
│  Safety, quality, audit — always fires, no exceptions           │
├─────────────────────────────────────────────────────────────────┤
│  Layer 1: SKILLS (Reusable Workflows)                           │
│  tvt-dev-* — commit, review, test, deploy, docs, security      │
├─────────────────────────────────────────────────────────────────┤
│  Layer 0: FOUNDATION                                            │
│  CLAUDE.md + .claude/settings.json — Standards & Permissions    │
└─────────────────────────────────────────────────────────────────┘
```

---

## Namespace Convention

```
tvt-{domain}-{action}
```

| Prefix | Scope | Audience |
|--------|-------|----------|
| `tvt-dev-*` | Build & Ship — daily SDLC actions | All developers |
| `tvt-eval-*` | Judge & Improve — observability, scoring, feedback | Tech leads, platform eng |
| `tvt-ops-*` | Run & Respond — incidents, status, runbooks | DevOps, SRE |
| `tvt-int-*` | Connect — enterprise tool integrations | Platform eng |

---

## Complete Skill Catalog

### tvt-dev-* — The Work (Build & Ship)

| # | Skill | Purpose | Trigger |
|---|-------|---------|---------|
| 1 | `tvt-dev-standards` | Scaffold CLAUDE.md + settings.json + hooks for a new repo | Manual `/tvt-dev-standards` |
| 2 | `tvt-dev-scaffold` | Generate boilerplate (components, services, modules) following team patterns | Manual |
| 3 | `tvt-dev-commit` | Conventional commits with smart staging, pre-commit validation | Manual |
| 4 | `tvt-dev-review` | Self-review before PR: lint, test, security, quality score | Manual |
| 5 | `tvt-dev-pr` | Create PR with structured description, Jira link, reviewer assignment | Manual |
| 6 | `tvt-dev-tdd` | Test-first development: write test → implement → verify | Manual |
| 7 | `tvt-dev-test` | Generate/run tests for changed files, coverage analysis | Manual + Auto-invoke |
| 8 | `tvt-dev-security` | OWASP Top 10 scan, dependency audit, secret detection | Manual + CI |
| 9 | `tvt-dev-docs` | Auto-generate API docs, ADRs, changelogs, README updates | Manual |
| 10 | `tvt-dev-infra` | Terraform/Docker/K8s manifest generation with validation | Manual |
| 11 | `tvt-dev-cicd` | Setup/manage GitHub Actions workflows, deploy gates | Manual |
| 12 | `tvt-dev-deploy` | Multi-environment deployment with safety checks and rollback | Manual |

### tvt-eval-* — The Judge (Trace, Measure, Improve)

| # | Skill | Purpose | Trigger |
|---|-------|---------|---------|
| 13 | `tvt-eval-trace` | Configure OpenTelemetry for team, enable distributed tracing | Manual (one-time setup) |
| 14 | `tvt-eval-score` | Run quality evaluation on recent changes (correctness/security/quality) | Manual + Stop hook |
| 15 | `tvt-eval-audit` | Setup and query the structured audit trail (compliance, debugging) | Manual + PostToolUse hook |
| 16 | `tvt-eval-dashboard` | Generate eval metrics summary, trends, team health report | Manual |
| 17 | `tvt-eval-improve` | Analyze failure patterns → suggest CLAUDE.md/hook/skill fixes | Manual |

### tvt-ops-* — The Runtime (Incidents, Status, Orchestration)

| # | Skill | Purpose | Trigger |
|---|-------|---------|---------|
| 18 | `tvt-ops-incident` | Incident response: triage, runbook execution, PagerDuty/Slack coordination | Manual |
| 19 | `tvt-ops-status` | Sync progress to Jira/Slack/Teams (standup automation) | Manual |
| 20 | `tvt-ops-runbook` | Generate/execute operational runbooks for common scenarios | Manual |

### tvt-int-* — The Connectors (Enterprise Integrations)

| # | Skill | Purpose | Trigger |
|---|-------|---------|---------|
| 21 | `tvt-int-jira` | Jira issue CRUD, JQL search, sprint management, transitions | Auto-invoke + Manual |
| 22 | `tvt-int-slack` | Post messages, read channels, thread replies, notifications | Auto-invoke + Manual |
| 23 | `tvt-int-teams` | Teams messaging, channel management, meeting notes | Auto-invoke + Manual |
| 24 | `tvt-int-github` | Advanced GitHub automation (beyond built-in): labels, milestones, releases | Auto-invoke + Manual |

### Compound Commands (Multi-Skill Chains)

| # | Skill | Chain | Purpose |
|---|-------|-------|---------|
| 25 | `tvt-dev-ship` | review → score → pr → status | Full shipping pipeline |
| 26 | `tvt-eval-report` | score + dashboard + improve | Weekly eval rollup with recommendations |
| 27 | `tvt-dev-onboard` | standards + trace + hooks setup | Bootstrap a new repo with full SDLC |

---

## Layer 2: Hooks (Deterministic Automation)

### Complete Hook Event Lifecycle

Claude Code exposes **31 hook events** across 7 cadences. TVT-SDLC uses the starred (★) ones in Phase 1:

| Cadence | Event | When It Fires | Can Block? | TVT Usage |
|---------|-------|---------------|------------|-----------|
| **Session** | `SessionStart` | Session begins or resumes | No | ★ Inject git/sprint context |
| **Session** | `Setup` | `--init-only` or `--init`/`--maintenance` in `-p` mode | No | CI environment prep |
| **Session** | `InstructionsLoaded` | CLAUDE.md or `.claude/rules/*.md` loaded | No | Observe instruction loads |
| **Session** | `SessionEnd` | Session terminates (matcher: clear/resume/logout/etc.) | No | ★ Final audit flush |
| **Turn** | `UserPromptSubmit` | User submits prompt, before Claude processes | Yes | ★ Append conventions |
| **Turn** | `UserPromptExpansion` | User-typed command expands into prompt | Yes | Validate skill invocations |
| **Turn** | `Stop` | Claude finishes responding | Yes (continues conversation) | ★ Run tests, compute score |
| **Turn** | `StopFailure` | Turn ends due to API error (matcher: error type) | No (output ignored) | Log failure, alert |
| **Tool** | `PreToolUse` | Before tool executes (can block/modify) | Yes | ★ Safety gates |
| **Tool** | `PermissionRequest` | Permission dialog appears | Yes (auto-decide) | Auto-approve safe ops |
| **Tool** | `PermissionDenied` | Auto-mode classifier denies | No | Log + optional retry |
| **Tool** | `PostToolUse` | After tool succeeds | **No** (context injection only) | ★ Format, lint, audit |
| **Tool** | `PostToolUseFailure` | After tool fails | No | Log failures |
| **Tool** | `PostToolBatch` | After parallel tool batch resolves | Yes | Batch audit summary |
| **Task** | `TaskCreated` | Task created via TaskCreate | Yes (rolls back) | Validate task scope |
| **Task** | `TaskCompleted` | Task marked complete | Yes | Validate task output |
| **Agent** | `SubagentStart` | Subagent spawned (matcher: agent type) | No | Inject subagent context |
| **Agent** | `SubagentStop` | Subagent completes (matcher: agent type) | Yes | Validate subagent output |
| **Agent** | `TeammateIdle` | Teammate about to go idle | Yes | Keep teammates working |
| **Context** | `ConfigChange` | Config file changes during session | Yes (except policy) | Log config mutations |
| **Context** | `CwdChanged` | Working directory changes | No | Reactive env management |
| **Context** | `FileChanged` | Watched file changes on disk (matcher: literal filenames) | No | Auto-reload .env |
| **Context** | `PreCompact` | Before context compaction (matcher: trigger) | Yes | Preserve critical context |
| **Context** | `PostCompact` | After compaction completes | No | Log token savings |
| **Worktree** | `WorktreeCreate` | Worktree created (must return path) | Yes (non-zero fails) | Custom VCS isolation |
| **Worktree** | `WorktreeRemove` | Worktree removed at exit/finish | No | Cleanup |
| **MCP** | `Elicitation` | MCP server requests user input | Yes (via action) | Auto-approve forms |
| **MCP** | `ElicitationResult` | User responds to elicitation | Yes (via action) | Validate responses |
| **Other** | `Notification` | Claude sends notification (matcher: type) | No | ★ Slack/Teams alert |

**⚠️ Important correction (v0.6):** `PostToolUse` is **non-blocking**. It can inject context via `additionalContext` or replace tool output via `updatedToolOutput`, but exit code 2 does NOT block the turn. Only `PostToolBatch` can block at the tool-batch level.

### Hook JSON Protocol (stdin/stdout)

Every hook handler receives JSON on **stdin** and may emit JSON on **stdout**. Choose ONE approach per hook: exit codes for simple allow/block, OR exit 0 with JSON for structured control. Claude Code ignores JSON when you exit 2.

**Common input fields (all events):**
```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/Users/dev/myproject",
  "hook_event_name": "PreToolUse"
}
```

**PreToolUse additional fields:**
```json
{
  "hook_event_name": "PreToolUse",
  "session_id": "...",
  "cwd": "/your/project",
  "transcript_path": "/tmp/transcript.jsonl",
  "tool_name": "Bash",
  "tool_input": { "command": "rm -rf /tmp/build" },
  "tool_use_id": "toolu_01ABC..."
}
```

**PostToolUse additional fields (NOTE: `inputs` plural, `response` not `tool_response`):**
```json
{
  "hook_event_name": "PostToolUse",
  "tool_name": "Write",
  "inputs": { "file_path": "src/auth.ts", "content": "..." },
  "response": { "type": "text", "text": "File written successfully" },
  "tool_use_id": "toolu_01ABC..."
}
```

**Stop hook additional fields:**
```json
{
  "hook_event_name": "Stop",
  "stop_hook_active": false,
  "last_assistant_message": "Done — I've applied all the changes."
}
```

**SessionStart additional fields:**
```json
{
  "hook_event_name": "SessionStart",
  "source": "startup"
}
```

**⚠️ CRITICAL: `stop_hook_active` prevents infinite loops.** Your Stop hook MUST check this field and exit early if `true`. Otherwise: Stop fires → hook blocks → Claude continues → Stop fires again → infinite loop.

### Decision Control (stdout JSON)

There are TWO distinct decision patterns depending on the event:

**Pattern 1: PreToolUse / PermissionRequest** — uses `hookSpecificOutput`:
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "Blocked: rm -rf is prohibited by team policy"
  }
}
```

`permissionDecision` values for PreToolUse:
- `"allow"` — bypass permission prompt, proceed immediately
- `"deny"` — cancel tool call, `permissionDecisionReason` sent to Claude
- `"ask"` — escalate to user for manual approval

PreToolUse can also **modify tool input** before execution:
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow",
    "updatedInput": { "command": "rm -rf /tmp/build --dry-run" }
  }
}
```

**Pattern 2: Stop / UserPromptSubmit / PostToolBatch / TaskCompleted** — uses top-level `decision`:
```json
{
  "decision": "block",
  "reason": "Tests failed — please fix before completing"
}
```

When `decision: "block"` is returned from a Stop hook, Claude reads the `reason` and continues the conversation (does NOT stop).

**⚠️ PostToolUse does NOT support `decision: "block"`.** It can only inject context or replace output (see above). To block at tool level, use `PreToolUse` (before) or `PostToolBatch` (after all parallel tools resolve).

**PostToolUse-specific context injection (exit 0 without blocking):**
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "File was auto-formatted by prettier"
  }
}
```

PostToolUse can also **replace tool output** before Claude sees it:
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "updatedToolOutput": "File written (auto-formatted)"
  }
}
```

### Exit Code Protocol

| Exit Code | Effect | JSON Processed? |
|-----------|--------|-----------------|
| 0 | Success — action proceeds | Yes (stdout parsed) |
| 2 | Block/error — stderr fed to Claude | No (JSON ignored) |
| Other (1, 3+) | Hook error — stderr shown to user, action proceeds | No |

**Where stdout appears by event:**
- `SessionStart`, `UserPromptSubmit`, `UserPromptExpansion`: stdout added to Claude's context
- All other events: stdout written to debug log only (not visible in transcript unless using `additionalContext`)

### Async Hooks

For long-running hooks that shouldn't block the session (e.g., Slack notifications, remote logging), use the `async` configuration field:

```jsonc
{
  "matcher": "",
  "hooks": [{
    "type": "command",
    "command": ".claude/hooks/notify-slack.sh",
    "async": true         // Claude continues immediately; hook runs in background
  }]
}
```

For hooks that run in background but should wake Claude if they find a problem:
```jsonc
{
  "matcher": "Write|Edit",
  "hooks": [{
    "type": "command",
    "command": ".claude/hooks/slow-security-scan.sh",
    "asyncRewake": true   // Runs in background; exit 2 wakes Claude with stderr
  }]
}
```

Use `async` for fire-and-forget (notifications, telemetry export, remote audit). Use `asyncRewake` for long-running validations that might need to interrupt (deep security scans, integration tests).

### Environment Variables Available to Hook Scripts

Hook scripts inherit the shell environment plus Claude Code-specific variables:

| Variable | Description | Example |
|----------|-------------|---------|
| `CLAUDE_PROJECT_DIR` | Project root directory (where `.claude/` lives) | `/Users/dev/myproject` |
| `CLAUDE_SESSION_ID` | Current session identifier | `sess_abc123` |
| `CLAUDE_CONVERSATION_DIR` | Directory for conversation state | `/tmp/.claude/conversations/...` |
| `HOME` | User's home directory | `/Users/dev` |
| `PATH` | Standard PATH (includes node_modules/.bin if applicable) | — |

**Best practice:** Always use `"$CLAUDE_PROJECT_DIR"` for paths in hook commands rather than relative paths. This ensures hooks work regardless of the working directory when Claude Code was launched.

### Matcher Syntax

Matchers filter which tools trigger a hook. Only applies to: `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest`, `PermissionDenied`.

| Pattern | Matches |
|---------|---------|
| `"Bash"` | Exact tool name |
| `"Write\|Edit"` | Pipe-separated OR |
| `"mcp__.*"` | Regex pattern |
| (empty string) | All tools |

**Advanced filtering with `if` field** (permission rule syntax — individual hook level):

The `if` field uses the same syntax as permission rules. It provides a secondary filter AFTER the matcher matches. The hook only spawns if the tool call matches the `if` pattern (or if a Bash command is too complex to parse — safe default). Only evaluated on tool events.

```jsonc
{
  "matcher": "Bash",
  "hooks": [{
    "type": "command",
    "command": "bash .claude/hooks/block-dangerous.sh",
    "if": "Bash(rm *)",        // Only fires for rm commands
    "timeout": 10,             // Seconds before timeout
    "statusMessage": "Checking safety..."  // Spinner text
  }]
}
```

### Hook Categories (TVT-SDLC)

| Category | Hook Event | Matcher | What It Does |
|----------|-----------|---------|--------------|
| **Safety** | PreToolUse | `Bash` | Block `rm -rf`, `git push --force`, `terraform destroy` |
| **Safety** | PreToolUse | `Write\|Edit` | Protect `.env`, CI configs, lockfiles from edits |
| **Safety** | PreToolUse | `Bash` | Block outbound network (prevent data exfiltration) |
| **Quality** | PostToolUse | `Edit\|Write` | Auto-format (prettier/black/gofmt per file type) |
| **Quality** | PostToolUse | `Edit\|Write` | Lint changed file only (fast, immediate feedback) |
| **Safety** | PreToolUse | `Edit\|Write` | Secret scan (block if credentials detected in content) |
| **Quality** | PostToolUse | `Edit\|Write` | Type check on .ts/.tsx files |
| **Eval** | PostToolUse | (all) | Audit log: every tool call → `.claude/audit.jsonl` |
| **Eval** | Stop | — | Run affected tests, log pass/fail |
| **Eval** | Stop | — | Quality score calculation |
| **Context** | SessionStart | — | Inject git status, branch, recent commits, sprint context |
| **Context** | UserPromptSubmit | — | Append `.claude/conventions.md` to every prompt |
| **Notify** | Notification | — | Slack/Teams notification when Claude needs human input |

### Hook Configuration Template

```jsonc
// .claude/settings.json (committed to Git, team-wide)
// Priority: user settings > project settings > local settings > managed policy > plugins
{
  "permissions": {
    "allow": [
      "Read(**)",
      "Glob(**)",
      "Grep(**)",
      "Bash(npm test *)",
      "Bash(npm run lint *)",
      "Bash(npm run build *)",
      "Bash(git status *)",
      "Bash(git diff *)",
      "Bash(git log *)"
    ],
    "deny": [
      "Bash(rm -rf *)",
      "Bash(git push --force *)",
      "Bash(terraform apply *)",
      "Bash(terraform destroy *)",
      "Bash(kubectl delete *)"
    ]
  },
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [{
          "type": "command",
          "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/block-dangerous.sh",
          "timeout": 10
        }]
      },
      {
        "matcher": "Write|Edit",
        "hooks": [{
          "type": "command",
          "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/protect-files.sh",
          "timeout": 5
        }]
      },
      {
        "matcher": "Write|Edit",
        "hooks": [{
          "type": "command",
          "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/secret-scan.sh",
          "timeout": 10
        }]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [{
          "type": "command",
          "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/auto-format.sh",
          "timeout": 15
        }]
      },
      {
        "matcher": "Edit|Write",
        "hooks": [{
          "type": "command",
          "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/lint-changed.sh",
          "timeout": 15
        }]
      },
      {
        "matcher": "",
        "hooks": [{
          "type": "command",
          "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/audit.sh",
          "timeout": 5
        }]
      }
    ],
    "UserPromptSubmit": [
      {
        "hooks": [{
          "type": "command",
          "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/conventions-inject.sh",
          "timeout": 5
        }]
      }
    ],
    "SessionStart": [
      {
        "hooks": [{
          "type": "command",
          "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/inject-context.sh"
        }]
      }
    ],
    "Stop": [
      {
        "hooks": [{
          "type": "command",
          "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/eval-session.sh",
          "timeout": 60
        }]
      }
    ],
    "Notification": [
      {
        "hooks": [{
          "type": "command",
          "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/notify-slack.sh",
          "async": true
        }]
      }
    ]
  }
}
```

### Hook Handler Types

| Type | Description | Communication | Use Case |
|------|-------------|---------------|----------|
| `command` | Shell command | JSON on stdin, exit codes + stdout/stderr | Most TVT hooks (scripts) |
| `http` | POST to URL | JSON request body, JSON response body | Remote eval services, webhooks |
| `mcp_tool` | Call an MCP server tool | Tool name + input args | Invoke Jira/Slack/custom MCP tools directly |
| `prompt` | Run an LLM prompt | Same JSON input/output format | LLM-as-Judge evaluation |
| `agent` | Spawn a subagent | Same JSON input/output format | Complex multi-step validation |

All five types use the same JSON protocol for event data. HTTP hooks use the event payload as the POST body, and the response body is the hook output.

### Hook Field Reference (Complete)

Every hook object (inside the `hooks` array) supports these fields:

| Field | Required | Type | Default | Description |
|-------|----------|------|---------|-------------|
| `type` | Yes | string | — | `"command"`, `"http"`, `"mcp_tool"`, `"prompt"`, or `"agent"` |
| `command` | If type=command | string | — | Shell command to execute |
| `url` | If type=http | string | — | HTTP endpoint to POST to |
| `timeout` | No | number | 600 (cmd), 30 (prompt), 60 (agent) | Seconds before canceling |
| `if` | No | string | — | Permission-rule-syntax filter (e.g., `"Bash(git *)"`, `"Edit(*.ts)"`). **Only evaluated on tool events** (`PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest`, `PermissionDenied`). On other events, a hook with `if` set **never runs**. Also fires if a Bash command is too complex to parse (safe default). |
| `statusMessage` | No | string | — | Custom spinner text shown to user while hook runs |
| `headers` | No | object | — | HTTP headers for `type: "http"`. Supports `$ENV_VAR` interpolation |
| `allowedEnvVars` | No | string[] | — | Restricts which env vars can be interpolated in `url`/`headers` (http hooks) |
| `async` | No | boolean | `false` | Run in background without blocking (command hooks only). Claude continues immediately. |
| `asyncRewake` | No | boolean | `false` | Run in background, wake Claude on exit code 2 (implies `async`). Useful for long-running checks that may need to interrupt. |
| `shell` | No | string | `"bash"` | `"bash"` or `"powershell"` — which shell executes the command |
| `once` | No | boolean | `false` | Run once per session then auto-removed (skill frontmatter hooks only; ignored in settings/agent) |

**Example — `if` field for fine-grained filtering:**
```jsonc
{
  "matcher": "Bash",
  "hooks": [{
    "type": "command",
    "command": ".claude/hooks/validate-git-push.sh",
    "if": "Bash(git push *)",   // Only fires on git push commands
    "timeout": 10,
    "statusMessage": "Validating push target..."
  }]
}
```

**Example — `mcp_tool` type (call MCP server directly from hook):**
```jsonc
{
  "matcher": "Bash",
  "hooks": [{
    "type": "mcp_tool",
    "server": "jira",
    "tool": "create_comment",
    "input": { "issue_key": "$JIRA_TICKET", "body": "Code change detected" }
  }]
}
```

**Example — `http` type with auth:**
```jsonc
{
  "matcher": "",
  "hooks": [{
    "type": "http",
    "url": "https://eval.internal.company.com/score",
    "timeout": 30,
    "headers": { "Authorization": "Bearer $EVAL_SERVICE_TOKEN" },
    "allowedEnvVars": ["EVAL_SERVICE_TOKEN"]
  }]
}
```

### Hook Test Cases (Phase 1)

| Hook | Input | Expected Behavior |
|------|-------|-------------------|
| `block-dangerous.sh` | `{"tool_name":"Bash","tool_input":{"command":"rm -rf /"}}` | Exit 2, stderr: "Blocked: destructive command" |
| `block-dangerous.sh` | `{"tool_name":"Bash","tool_input":{"command":"npm test"}}` | Exit 0 (pass-through) |
| `protect-files.sh` | `{"tool_name":"Write","tool_input":{"file_path":".env.local"}}` | Exit 2, stderr: "Protected file" |
| `protect-files.sh` | `{"tool_name":"Edit","tool_input":{"file_path":"src/app.ts"}}` | Exit 0 (pass-through) |
| `audit.sh` | Any PostToolUse event | Appends JSONL line to `.claude/audit.jsonl` |
| `eval-session.sh` | Stop event with `stop_hook_active: false` | Runs tests, writes score to `.claude/eval-log.jsonl` |
| `eval-session.sh` | Stop event with `stop_hook_active: true` | Exit 0 immediately (prevent infinite loop) |
| `conventions-inject.sh` | UserPromptSubmit (with `.claude/conventions.md` present) | Stdout contains conventions content |
| `conventions-inject.sh` | UserPromptSubmit (no conventions file) | Exit 0 silently (no output) |
| `inject-context.sh` | SessionStart | Stdout contains git branch, status, last 5 commits (stdout visible to Claude for this event) |

### Rollback Plan (Hooks)

To disable all TVT hooks without breaking existing workflow:
```bash
# Option 1: Comment out hooks key in settings.json
jq 'del(.hooks)' .claude/settings.json > tmp && mv tmp .claude/settings.json

# Option 2: Use local override to suppress
echo '{"hooks":{}}' > .claude/settings.local.json

# Option 3: Disable individual hooks by removing from array
# Each hook is independent — removing one doesn't affect others
```

---

## Layer 1: Skills (SKILL.md Specification)

### Frontmatter Reference

Every skill is a `SKILL.md` file in `.claude/skills/{skill-name}/`. YAML frontmatter between `---` markers configures behavior. All fields are optional. Only `description` is recommended.

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `name` | No | string | Lowercase + hyphens + numbers, max 64 chars. Defaults to directory name. |
| `description` | Recommended | string | What the skill does + when to use it. Claude matches user requests against this text. Front-load trigger phrases. Combined with `when_to_use`, truncated at 1,536 chars in skill listing. If omitted, uses first paragraph of markdown content. |
| `when_to_use` | No | string | Additional trigger context. Appended to description, counts toward 1,536-char cap. |
| `argument-hint` | No | string | Hint in `/` autocomplete menu (e.g., `"[file-or-directory]"`) |
| `arguments` | No | string | Expected arguments format (free-form or pattern) |
| `disable-model-invocation` | No | boolean | `true` = only manual `/name` invocation. Description removed from context entirely. Prevents preloading into subagents. Use for side-effect skills (commit, deploy). Default: `false` |
| `user-invocable` | No | boolean | `false` = hidden from `/` menu, Claude auto-invokes only. Description stays in context permanently. Default: `true` |
| `allowed-tools` | No | string/list | Tools pre-approved while skill is active (no per-use permission prompts). Space-separated string or YAML list. Pattern: `Bash(git add *)`. Does NOT restrict — unlisted tools remain callable via normal permissions. |
| `model` | No | string | `sonnet`, `opus`, `haiku`, full model ID, or `inherit` (default — matches main conversation) |
| `effort` | No | string | `low`, `medium`, `high`, or `max` |
| `context` | No | string | `fork` = run in isolated subagent (no access to conversation history). Skill body becomes subagent prompt — must contain explicit task instructions, not just guidelines. |
| `agent` | No | string | Subagent type when `context: fork`. Built-in: `Explore` (read-only, Haiku), `Plan` (read-only, inherits), `general-purpose` (all tools, inherits). Custom agents from `.claude/agents/` also valid. |
| `paths` | No | string/list | Glob patterns for auto-activation. Comma-separated string or YAML list. Only affects auto-invoke — manual `/name` always works regardless of paths. |
| `shell` | No | string | `bash` (default) or `powershell` |
| `hooks` | No | object | Hooks scoped to skill lifecycle. Same format as settings hooks. With `context: fork`, `Stop` hooks convert to `SubagentStop` events at runtime. |
| `mcp-servers` | No | string/list | MCP servers required by this skill |
| `permission-mode` | No | string | Permission level applied when skill runs |

**Security note:** Skills specifying `allowed-tools` or `hooks` require user approval before first use — the runtime treats them as elevated-permission requests.

**⚠️ Common pitfalls:**
- `user-invocable: false` + `disable-model-invocation: true` = unreachable skill (hidden from everything)
- `context: fork` with reference-only content = subagent produces empty output (needs explicit task)
- `paths` with `disable-model-invocation: true` = paths filter is useless (skill can't auto-activate anyway)

**Invocation matrix:**

| Frontmatter | User can invoke | Claude can invoke | When loaded into context |
|-------------|-----------------|-------------------|------------------------|
| (default) | Yes | Yes | Description always in context; full skill loads when invoked |
| `disable-model-invocation: true` | Yes | No | Description NOT in context; full skill loads when user invokes |
| `user-invocable: false` | No | Yes | Description always in context; full skill loads when invoked |

### Skill Directory Structure & Supporting Files

Skills support progressive disclosure: `SKILL.md` stays short, and supporting files provide details on demand. Claude reads them when needed, reducing upfront token cost.

```
.claude/skills/
└── tvt-eval-score/
    ├── SKILL.md          # Main entry — frontmatter + high-level flow
    ├── rubric.md         # Detailed scoring rubric (loaded on demand)
    ├── examples.md       # Example inputs → expected outputs
    └── scripts/
        └── run-score.sh  # Helper script Claude can execute
```

Reference supporting files from your `SKILL.md` so Claude knows they exist:
```markdown
For the full scoring rubric, read `rubric.md` in this directory.
For example outputs, see `examples.md`.
```

**Permission control for skills:**
```
# In project .claude/settings.json — deny specific skills
Skill(tvt-dev-deploy )    # Prefix match: blocks deploy and any args
Skill(tvt-ops-incident)   # Exact match: blocks only this skill
```

### Phase 1 Skill Implementations

#### tvt-dev-standards — Project Bootstrap

```yaml
---
name: tvt-dev-standards
description: >
  Bootstrap a project with Claude Code SDLC infrastructure. Creates CLAUDE.md,
  .claude/settings.json, hooks directory with safety/quality hooks, and
  .gitignore entries. Use when asked to "set up", "initialize", "bootstrap",
  "add standards", or "onboard this repo to Claude Code".
disable-model-invocation: true
allowed-tools:
  - Write
  - Read
  - Bash(mkdir *)
  - Bash(chmod *)
  - Bash(git add *)
  - Bash(cat *)
  - Glob
---

# TVT Dev Standards

Bootstrap this repository with Claude Code enterprise SDLC infrastructure.

## Process

1. **Check existing setup** — Look for existing `.claude/`, `CLAUDE.md`, `REVIEW.md`
2. **Prompt for project details:**
   - Language/framework (for lint/format config)
   - Test framework (for eval-session hook)
   - Protected file patterns (beyond defaults)
   - Team conventions (branch strategy, commit format)
3. **Create directory structure:**
   ```
   .claude/
   ├── settings.json
   ├── conventions.md
   ├── hooks/
   │   ├── block-dangerous.sh
   │   ├── protect-files.sh
   │   ├── secret-scan.sh
   │   ├── auto-format.sh
   │   ├── lint-changed.sh
   │   ├── audit.sh
   │   ├── eval-session.sh
   │   ├── inject-context.sh
   │   ├── conventions-inject.sh
   │   └── notify-slack.sh
   └── skills/
       └── (skills installed separately)
   ```
4. **Generate CLAUDE.md** from project details (use Layer 0 template)
5. **Generate REVIEW.md** from project details
6. **Set executable permissions** on all hook scripts: `chmod +x .claude/hooks/*.sh`
7. **Add .gitignore entries:**
   ```
   .claude/audit.jsonl
   .claude/eval-log.jsonl
   .claude/settings.local.json
   ```
8. **Stage for commit:** `git add .claude/ CLAUDE.md REVIEW.md`
9. **Report what was created** — list all files with one-line description each

## Rules

- NEVER overwrite existing CLAUDE.md without asking
- NEVER modify existing .claude/settings.json — merge with existing
- Ask before adding .gitignore entries if file already exists
- All hook scripts must be executable (chmod +x)
- Use project-appropriate tooling (prettier for JS/TS, black for Python, gofmt for Go)
```

#### tvt-eval-audit — Audit Trail

```yaml
---
name: tvt-eval-audit
description: >
  Setup and query the structured audit trail. Every Claude tool call
  is logged to .claude/audit.jsonl for compliance, debugging, and
  cost attribution. Use when asked about "audit", "what did Claude do",
  "compliance log", or "action history".
when_to_use: >
  Also invoke when the user asks to reconstruct a session or debug
  what went wrong in a previous interaction.
allowed-tools:
  - Read
  - Grep
  - Bash(cat .claude/audit.jsonl *)
  - Bash(jq * .claude/audit.jsonl)
  - Bash(wc -l .claude/audit.jsonl)
hooks:
  PostToolUse:
    - matcher: ""
      hooks:
        - type: command
          command: "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/audit.sh"
          timeout: 5
---

# TVT Eval Audit

You manage the structured audit trail at `.claude/audit.jsonl`.

## When invoked manually

1. Parse the user's query (e.g., "what did Claude edit today?", "show me all Bash commands")
2. Use `jq` to filter `.claude/audit.jsonl` by timestamp, tool name, or session
3. Present results in a readable table format

## Audit record format

Each line in `.claude/audit.jsonl` is:
```json
{"ts":"ISO-8601","session_id":"...","tool":"ToolName","detail":"...","file":"...","duration_ms":N}
```

## Query examples

- Last 10 actions: `jq -s '.[-10:]' .claude/audit.jsonl`
- All edits today: `jq -s '[.[] | select(.ts > "2026-05-04")]' .claude/audit.jsonl`
- Bash commands only: `jq -s '[.[] | select(.tool == "Bash")]' .claude/audit.jsonl`
```

#### tvt-eval-score — Quality Scoring

```yaml
---
name: tvt-eval-score
description: >
  Run quality evaluation on recent changes. Scores correctness (tests pass,
  types clean), quality (lint, complexity), and security (SAST, secrets).
  Use when asked to "score", "evaluate", "check quality", or "rate this code".
when_to_use: >
  Automatically triggered by the Stop hook after each session.
  Also invoke manually before creating a PR.
argument-hint: "[file-or-directory]"
allowed-tools:
  - Bash(npm test *)
  - Bash(npm run lint *)
  - Bash(npm run typecheck *)
  - Bash(npx eslint *)
  - Bash(git diff *)
  - Read
  - Grep
  - Glob
---

# TVT Eval Score

Evaluate code quality across three dimensions. Output a structured score.

## Scoring Process

1. **Identify scope**: Use `git diff --name-only HEAD~1` or the provided argument
2. **Correctness** (weight: 40%)
   - Run `npm test` (or project test command) → pass/fail
   - Run `npm run typecheck` → clean/errors
   - Check for runtime errors in test output
3. **Quality** (weight: 35%)
   - Run `npx eslint --format json` on changed files → error count
   - Compute cyclomatic complexity if tool available
   - Check for code duplication patterns
4. **Security** (weight: 25%)
   - Grep for hardcoded secrets (API keys, passwords, tokens)
   - Check for `eval()`, `dangerouslySetInnerHTML`, SQL concatenation
   - Run `npm audit --json` for dependency vulnerabilities

## Scoring Scale

| Score | Meaning | Action |
|-------|---------|--------|
| 9-10 | Excellent | Ship immediately |
| 7-8 | Good | Ship with minor notes |
| 5-6 | Acceptable | Fix issues before PR |
| 3-4 | Poor | Significant rework needed |
| 1-2 | Critical | Do not ship — security/correctness issues |

## Output Format

Write results to `.claude/eval-log.jsonl`:
```json
{
  "timestamp": "ISO-8601",
  "session_id": "from environment",
  "scope": "files evaluated",
  "scores": {
    "correctness": {"score": 9, "tests_pass": true, "types_clean": true, "details": "..."},
    "quality": {"score": 7, "lint_errors": 2, "complexity": "low", "details": "..."},
    "security": {"score": 10, "findings": 0, "details": "..."}
  },
  "overall": 8.5,
  "recommendation": "ship|fix|block",
  "issues": []
}
```
```

#### tvt-dev-commit — Conventional Commits

```yaml
---
name: tvt-dev-commit
description: >
  Create conventional commits with smart staging and validation.
  Analyzes changed files, generates a commit message following
  Conventional Commits spec, validates before committing.
  Use when asked to "commit", "save changes", or "stage and commit".
disable-model-invocation: true
allowed-tools:
  - Bash(git status *)
  - Bash(git add *)
  - Bash(git diff *)
  - Bash(git log *)
  - Bash(git commit *)
  - Read
  - Grep
---

# TVT Dev Commit

Create a conventional commit with smart staging and pre-commit validation.

## Process

1. Run `git status` to see all changes
2. Run `git diff` (staged) and `git diff HEAD` (all) to understand changes
3. Determine commit type from changes:
   - `feat:` — new feature (new files in src/, new exports)
   - `fix:` — bug fix (changes to existing logic, error handling)
   - `refactor:` — restructuring without behavior change
   - `test:` — test additions/modifications only
   - `docs:` — documentation only
   - `chore:` — config, dependencies, build tooling
   - `style:` — formatting only (should be rare with auto-format hooks)
4. Generate message: `{type}({scope}): {imperative description}`
   - Scope = primary directory/module affected
   - Description = what changed, imperative mood, <72 chars
5. Show the proposed commit to user for approval
6. Stage relevant files (prefer specific `git add` over `git add -A`)
7. Run pre-commit checks if configured
8. Create the commit

## Rules

- NEVER use `git add -A` or `git add .` — stage specific files
- NEVER commit .env, credentials, or secrets
- NEVER amend previous commits unless explicitly asked
- If pre-commit hook fails, fix the issue and create a NEW commit
- Add `Co-Authored-By: Claude <noreply@anthropic.com>` to all commits
```

---

## Layer 5: Eval & Observability (Deep Dive)

### Philosophy

The eval layer answers three questions at all times:

1. **Is it working?** → Tracing + metrics (tool calls succeed, tests pass)
2. **Is it working WELL?** → Quality evals (correct, secure, maintainable)
3. **Is it getting BETTER?** → Trend analysis (improvement over time)

### 5.1 Tracing (tvt-eval-trace)

Native OpenTelemetry support. Every LLM call, tool use, and hook execution becomes a span.

**Environment configuration (complete reference):**
```bash
# ──── Core enablement ────
CLAUDE_CODE_ENABLE_TELEMETRY=1                     # Required: metrics + logs
CLAUDE_CODE_ENHANCED_TELEMETRY_BETA=1              # Required for span tracing (also: ENABLE_ENHANCED_TELEMETRY_BETA)

# ──── Exporters (per signal, comma-separated) ────
OTEL_METRICS_EXPORTER=otlp          # otlp | prometheus | console | none
OTEL_LOGS_EXPORTER=otlp             # otlp | console | none
OTEL_TRACES_EXPORTER=otlp           # otlp | console | none

# ──── OTLP endpoint and protocol ────
OTEL_EXPORTER_OTLP_ENDPOINT=http://collector.company.com:4317
OTEL_EXPORTER_OTLP_PROTOCOL=grpc    # grpc | http/json | http/protobuf

# ──── Per-signal overrides (optional) ────
# OTEL_EXPORTER_OTLP_METRICS_PROTOCOL=grpc
# OTEL_EXPORTER_OTLP_METRICS_ENDPOINT=http://metrics.company.com:4318/v1/metrics
# OTEL_EXPORTER_OTLP_LOGS_PROTOCOL=grpc
# OTEL_EXPORTER_OTLP_LOGS_ENDPOINT=http://logs.company.com:4318/v1/logs
# OTEL_EXPORTER_OTLP_TRACES_PROTOCOL=http/protobuf
# OTEL_EXPORTER_OTLP_TRACES_ENDPOINT=http://traces.company.com:4318/v1/traces

# ──── Export intervals ────
# OTEL_METRIC_EXPORT_INTERVAL=60000    # Default: 60000ms (1 minute)
# OTEL_LOGS_EXPORT_INTERVAL=5000       # Default: 5000ms
# OTEL_TRACES_EXPORT_INTERVAL=5000     # Default: 5000ms

# ──── Auth ────
# OTEL_EXPORTER_OTLP_HEADERS="Authorization=Bearer your-token"
# For mTLS:
# OTEL_EXPORTER_OTLP_METRICS_CLIENT_KEY=/path/to/key
# OTEL_EXPORTER_OTLP_METRICS_CLIENT_CERTIFICATE=/path/to/cert

# ──── Privacy gates (progressively more verbose) ────
# OTEL_LOG_USER_PROMPTS=1              # Prompt text (redacted by default)
# OTEL_LOG_TOOL_DETAILS=1              # File paths, Bash commands, MCP/skill names
# OTEL_LOG_TOOL_CONTENT=1              # Tool input/output content (truncated 60KB). Requires tracing.
# OTEL_LOG_RAW_API_BODIES=1            # Full API request/response JSON (implies all above)
# OTEL_LOG_RAW_API_BODIES=file:/var/log/claude-bodies  # Untruncated bodies on disk

# ──── Metrics cardinality control ────
# OTEL_METRICS_INCLUDE_SESSION_ID=true     # Default: true
# OTEL_METRICS_INCLUDE_VERSION=false       # Default: false
# OTEL_METRICS_INCLUDE_ACCOUNT_UUID=true   # Default: true

# ──── Multi-team attributes ────
# OTEL_RESOURCE_ATTRIBUTES="department=engineering,team.id=platform,cost_center=eng-123"
# OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE=delta  # delta (default) | cumulative

# ──── Dynamic auth header helper ────
# Configure in .claude/settings.json: "otelHeadersHelper": "/bin/generate_otel_headers.sh"
# CLAUDE_CODE_OTEL_HEADERS_HELPER_DEBOUNCE_MS=1740000  # Refresh interval (default: 29 min)
```

**Starter config (local development — no infra needed):**
```bash
CLAUDE_CODE_ENABLE_TELEMETRY=1
CLAUDE_CODE_ENHANCED_TELEMETRY_BETA=1
OTEL_METRICS_EXPORTER=console
OTEL_LOGS_EXPORTER=console
OTEL_TRACES_EXPORTER=console
OTEL_METRIC_EXPORT_INTERVAL=1000   # 1 second for debugging
```

**Administrator managed policy (push to entire org via `~/.claude/settings.json` or managed config):**
```json
{
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
    "OTEL_METRICS_EXPORTER": "otlp",
    "OTEL_LOGS_EXPORTER": "otlp",
    "OTEL_EXPORTER_OTLP_PROTOCOL": "grpc",
    "OTEL_EXPORTER_OTLP_ENDPOINT": "http://collector.example.com:4317",
    "OTEL_EXPORTER_OTLP_HEADERS": "Authorization=Bearer example-token"
  }
}
```

**Span hierarchy (official):**
```
claude_code.interaction (one per user prompt)
├── claude_code.llm_request        (model, ttft_ms, input/output tokens, cost, cache)
├── claude_code.hook               (requires ENABLE_BETA_TRACING_DETAILED=1)
└── claude_code.tool
    ├── claude_code.tool.blocked_on_user   (permission wait: duration_ms, decision, source)
    ├── claude_code.tool.execution         (actual work: duration_ms, success, error)
    └── (Task tool) subagent → claude_code.llm_request / claude_code.tool spans
```

**Key span attributes:**

| Span | Attribute | Description | Gated By |
|------|-----------|-------------|----------|
| `claude_code.interaction` | `user_prompt_length` | Chars in prompt | — |
| `claude_code.interaction` | `interaction.sequence` | 1-based turn counter | — |
| `claude_code.interaction` | `interaction.duration_ms` | Wall-clock turn time | — |
| `claude_code.llm_request` | `model` | Model identifier | — |
| `claude_code.llm_request` | `ttft_ms` | Time to first token | — |
| `claude_code.llm_request` | `input_tokens` / `output_tokens` | Token counts | — |
| `claude_code.llm_request` | `cache_read_tokens` / `cache_creation_tokens` | Prompt caching | — |
| `claude_code.llm_request` | `cost_usd` | Per-request cost | — |
| `claude_code.llm_request` | `request_id` | Anthropic API request ID | — |
| `claude_code.llm_request` | `gen_ai.system` | Always `anthropic` (OTEL GenAI semconv) | — |
| `claude_code.tool` | `tool_name` | Tool name | — |
| `claude_code.tool` | `duration_ms` | Total time (permission + execution) | — |
| `claude_code.tool` | `result_tokens` | Approximate result token size | — |
| `claude_code.tool` | `file_path` | Target file (Read/Edit/Write) | `OTEL_LOG_TOOL_DETAILS` |
| `claude_code.tool` | `full_command` | Bash command | `OTEL_LOG_TOOL_DETAILS` |
| `claude_code.tool` | `skill_name` | Skill tool name | `OTEL_LOG_TOOL_DETAILS` |
| `claude_code.hook` | `hook_event` | e.g., `PreToolUse` | — |
| `claude_code.hook` | `hook_name` | e.g., `PreToolUse:Write` | — |
| `claude_code.hook` | `num_blocking` | Hooks that blocked | — |

**Standard resource attributes (on all signals):**

| Attribute | Description | Control |
|-----------|-------------|---------|
| `session.id` | Session UUID | `OTEL_METRICS_INCLUDE_SESSION_ID` (default: true) |
| `user.account_uuid` | Account UUID | `OTEL_METRICS_INCLUDE_ACCOUNT_UUID` (default: true) |
| `user.id` | Anonymous device/installation ID | Always |
| `user.email` | Email (OAuth only) | Always when available |
| `organization.id` | Org UUID | Always when available |
| `terminal.type` | `iTerm.app`, `vscode`, `cursor`, `tmux` | Always |
| `service.name` | Always `claude-code` | Always |

**Native metrics emitted:**

| Metric | Unit | What It Measures | Key Attributes |
|--------|------|-----------------|----------------|
| `claude_code.session.count` | count | Sessions started | `start_type`: fresh/resume/continue |
| `claude_code.lines_of_code.count` | count | Code added/removed | `type`: added/removed |
| `claude_code.pull_request.count` | count | PRs created | — |
| `claude_code.commit.count` | count | Git commits created | — |
| `claude_code.cost.usage` | USD | Token spend | `model`, `query_source`, `speed`, `effort` |
| `claude_code.token.usage` | tokens | Tokens used | `type`: input/output/cacheRead/cacheCreation |
| `claude_code.code_edit_tool.decision` | count | Permission decisions | `tool_name`, `decision`, `source`, `language` |
| `claude_code.active_time.total` | seconds | Active time | `type`: user/cli |

**Native events emitted (via `OTEL_LOGS_EXPORTER`):**

| Event | What It Captures | Key Attributes |
|-------|-----------------|----------------|
| `claude_code.user_prompt` | Every prompt submitted | `prompt_length`, `command_name` (gated) |
| `claude_code.tool_result` | Every tool execution outcome | `tool_name`, `success`, `duration_ms`, `decision_type` |
| `claude_code.api_request` | Model calls | `model`, `cost_usd`, `input/output_tokens`, `cache_*` |
| `claude_code.api_error` | API failures | `error`, `status_code`, `attempt` |
| `claude_code.tool_decision` | Permission decisions | `tool_name`, `decision`, `source` |
| `claude_code.hook_execution_start` | Hook begins | `hook_event`, `hook_name`, `num_hooks` |
| `claude_code.hook_execution_complete` | Hook finishes | `num_success`, `num_blocking`, `total_duration_ms` |
| `claude_code.skill_activated` | Skill invoked | `skill.name` (gated), `skill.source`, `invocation_trigger` |
| `claude_code.compaction` | Context compression | `trigger`, `pre_tokens`, `post_tokens` |
| `claude_code.mcp_server_connection` | MCP server connect/fail | `status`, `transport_type`, `server_scope` |
| `claude_code.permission_mode_changed` | Mode change | `from_mode`, `to_mode`, `trigger` |
| `claude_code.api_retries_exhausted` | All retries failed | `total_attempts`, `total_retry_duration_ms` |

**All events include correlation attribute `prompt.id` (UUID v4)** linking events produced while processing a single user prompt.

### 5.1.1 Analytics Admin API (Alternative to OTEL)

For organizations that don't want to run a collector, Anthropic provides a REST API for daily aggregated metrics:

```bash
# Requires Admin API key (sk-ant-admin...)
curl "https://api.anthropic.com/v1/organizations/usage_report/claude_code?\
starting_at=2026-05-04&limit=20" \
  --header "anthropic-version: 2023-06-01" \
  --header "x-api-key: $ADMIN_API_KEY"
```

Returns per-user daily aggregates: sessions, lines of code, commits, PRs, tool acceptance rates, model breakdown with costs. Supports cursor-based pagination. Data appears within 1 hour of activity. Free to use.

**When to use Analytics API vs OTEL:**
- Analytics API: Quick adoption dashboards, cost reporting, no infra needed
- OTEL: Real-time alerting, per-session debugging, custom dashboards, trace correlation

### 5.2 Quality Scoring (tvt-eval-score)

Three evaluation dimensions (informed by Meta CQS, ByteDance BitsAI-CR, Codility COMPASS):

| Dimension | What to Evaluate | Method |
|-----------|-----------------|--------|
| **Correctness** | Does the code do what it should? | Tests pass, types check, no runtime errors |
| **Quality** | Is it maintainable and clean? | Lint score, complexity, duplication, naming |
| **Security** | Is it safe? | SAST scan, dependency audit, secret detection |

**TypeScript interface (canonical schema):**
```typescript
interface EvalRecord {
  timestamp: string;       // ISO-8601
  session_id: string;      // From CLAUDE_SESSION_ID env
  scope: string;           // Files or directories evaluated
  scores: {
    correctness: {
      score: number;       // 1-10
      tests_pass: boolean;
      types_clean: boolean;
      details: string;     // Human-readable explanation
    };
    quality: {
      score: number;       // 1-10
      lint_errors: number;
      complexity: "low" | "medium" | "high";
      details: string;
    };
    security: {
      score: number;       // 1-10
      findings: number;
      details: string;
    };
  };
  overall: number;         // Weighted: correctness×0.40 + quality×0.35 + security×0.25
  recommendation: "ship" | "fix" | "block";
  issues: Array<{
    file: string;
    line: number;
    type: "correctness" | "quality" | "security";
    severity: "error" | "warning" | "info";
    detail: string;
  }>;
}
```

**Scoring output format (example):**
```json
{
  "timestamp": "2026-05-04T14:30:00Z",
  "session_id": "abc123",
  "scope": "src/auth/login.ts, src/auth/middleware.ts",
  "scores": {
    "correctness": { "score": 9, "tests_pass": true, "types_clean": true, "details": "All 42 tests pass" },
    "quality": { "score": 7, "lint_errors": 2, "complexity": "low", "details": "2 lint warnings in login.ts" },
    "security": { "score": 10, "findings": 0, "details": "No secrets, no injection vectors" }
  },
  "overall": 8.7,
  "recommendation": "ship",
  "issues": [
    { "file": "src/auth/login.ts", "line": 45, "type": "quality", "severity": "warning", "detail": "Missing null check on user.email" }
  ]
}
```

### 5.3 Audit Trail (tvt-eval-audit)

Structured JSONL log of every Claude action.

**TypeScript interface (canonical schema):**
```typescript
interface AuditRecord {
  ts: string;              // ISO-8601 UTC
  session_id: string;      // From CLAUDE_SESSION_ID env
  tool: string;            // Tool name: "Bash", "Read", "Edit", "Write", etc.
  detail: string;          // Primary identifier: command, file path, or first 100 chars
  file: string;            // File path if applicable, empty string otherwise
  duration_ms?: number;    // Optional: execution time
  hook_event?: string;     // If triggered by a hook: "PostToolUse", "PreToolUse"
}
```

**Example output (`.claude/audit.jsonl`):**
```jsonl
{"ts":"2026-05-04T14:02:11Z","session_id":"abc123","tool":"Bash","detail":"git status","file":""}
{"ts":"2026-05-04T14:02:15Z","session_id":"abc123","tool":"Read","detail":"src/auth/login.ts","file":"src/auth/login.ts"}
{"ts":"2026-05-04T14:02:18Z","session_id":"abc123","tool":"Edit","detail":"src/auth/login.ts","file":"src/auth/login.ts"}
{"ts":"2026-05-04T14:02:22Z","session_id":"abc123","tool":"Bash","detail":"npm test","file":""}
```

**Use cases:**
- Compliance (regulated industries, SOC 2)
- Debugging (reconstruct what went wrong)
- Improvement (mine failure patterns)
- Cost attribution (tokens per task type)

**Retention and rotation:** Audit files grow ~1KB per tool call. At ~200 tool calls/day, that's ~200KB/day. Recommend rotating weekly: `audit-2026-W18.jsonl`. The `tvt-eval-audit` skill can query across multiple files.

### 5.4 Continuous Improvement Loop (tvt-eval-improve)

```
TRACE → MEASURE → ANALYZE → IMPROVE → VERIFY → REPEAT
```

| Signal | Root Cause | Fix Action |
|--------|-----------|------------|
| Low test pass rate | Claude not running tests | Add Stop hook enforcement |
| High lint errors | Formatting ignored | Add PostToolUse auto-format hook |
| Security findings in PRs | Weak security rules | Strengthen CLAUDE.md, add PreToolUse block |
| Same mistake repeated | Pattern not captured | Add to CLAUDE.md or create new skill |
| Human rejects AI reviews >50% | Review prompt too noisy | Tune REVIEW.md, raise severity bar |
| Cost per session trending up | Context bloat | Improve skills, add compaction hooks |

### 5.5 LLM-as-Judge (Advanced)

Use a separate Claude call to evaluate output quality. Based on patterns from Meta CQS, ByteDance BitsAI-CR, and SWE-PRBench.

**Architecture pattern: Pointwise Rubric Evaluation (PRE)**

Each dimension is scored independently with specific criteria, then aggregated. This avoids the "halo effect" where one strong dimension inflates others.

**Evaluation rubric (scored 1-10 each):**

| # | Dimension | Score 9-10 | Score 5-6 | Score 1-2 |
|---|-----------|-----------|-----------|-----------|
| 1 | **Correctness** | All tests pass, types clean, no runtime errors, logic matches intent | Most tests pass, minor type issues, logic mostly correct | Tests fail, type errors, logic wrong |
| 2 | **Completeness** | Edge cases handled, error paths covered, null checks present | Happy path works, some edges missed | Missing critical error handling |
| 3 | **Security** | No vulnerabilities, input sanitized, auth correct | Minor issues (info leak, weak validation) | Injection, auth bypass, or data exposure |
| 4 | **Maintainability** | Clean structure, good naming, no duplication, clear flow | Readable but some complexity or coupling | Spaghetti code, poor naming, high complexity |
| 5 | **Test Quality** | New paths tested, assertions meaningful, edge cases covered | Some tests added but shallow | No tests, or tests that don't assert anything meaningful |
| 6 | **Standards** | Follows all CLAUDE.md conventions, consistent style | Mostly compliant, minor deviations | Ignores project conventions |

**Scoring aggregation:**
```
overall = (correctness × 0.25) + (completeness × 0.20) + (security × 0.25)
        + (maintainability × 0.15) + (test_quality × 0.10) + (standards × 0.05)
```

**LLM-as-Judge prompt template:**
```
You are a code review judge. Evaluate the following code change against each dimension independently.

<code_change>
{diff}
</code_change>

<project_standards>
{contents of CLAUDE.md}
</project_standards>

For EACH dimension, provide:
1. A score (1-10)
2. One sentence justification
3. Specific file:line references for issues

Output as JSON matching this schema:
{
  "dimensions": {
    "correctness": {"score": N, "reason": "...", "issues": [{"file": "...", "line": N, "detail": "..."}]},
    ...
  },
  "overall": N,
  "recommendation": "approve|comment|request_changes",
  "summary": "One paragraph summary"
}
```

**Integration with CI/CD (threshold configuration):**

**TypeScript interface:**
```typescript
interface EvalConfig {
  thresholds: {
    auto_approve: number;    // Score >= this → auto-approve PR (default: 8.0)
    comment_only: number;    // Score >= this → comment with scores (default: 6.0)
    request_changes: number; // Score < comment_only → request changes (default: 0.0)
  };
  weights: {
    correctness: number;     // Default: 0.25
    completeness: number;    // Default: 0.20
    security: number;        // Default: 0.25
    maintainability: number; // Default: 0.15
    test_quality: number;    // Default: 0.10
    standards: number;       // Default: 0.05
  };
  model: string;             // Model for LLM-as-Judge (default: claude-sonnet-4-6-20250514)
  max_cost_per_review: number; // Budget cap in USD (default: 0.25)
  security_floor: number;    // Any security score below this always blocks (default: 5)
  enabled_dimensions: string[]; // Subset to evaluate (default: all 6)
}
```

**Configuration file (`.claude/eval-config.json`):**
```jsonc
{
  "thresholds": {
    "auto_approve": 8.0,
    "comment_only": 6.0,
    "request_changes": 0.0
  },
  "weights": {
    "correctness": 0.25,
    "completeness": 0.20,
    "security": 0.25,
    "maintainability": 0.15,
    "test_quality": 0.10,
    "standards": 0.05
  },
  "model": "claude-sonnet-4-6-20250514",
  "max_cost_per_review": 0.25,
  "security_floor": 5,
  "enabled_dimensions": ["correctness", "completeness", "security", "maintainability", "test_quality", "standards"]
}
```

**Decision logic:**
- Score ≥ 8.0 → Auto-approve (if team enables)
- Score 6.0-7.9 → Comment with scores + issues
- Score < 6.0 → Request changes with blocking issues listed
- Any security score < 5 → Always request changes regardless of overall

### 5.6 Observability Stack Options

| Tier | Stack | Cost | Best For |
|------|-------|------|----------|
| **Starter** | Hooks → `.claude/audit.jsonl` + `.claude/eval-log.jsonl` | $0 | Solo/small team, Phase 1 |
| **Starter+** | Analytics Admin API (REST, daily aggregates) | $0 | Adoption dashboards without infra |
| **Team** | OpenTelemetry → Grafana/Prometheus/Jaeger | $50-200/mo | Mid-size, full control, real-time |
| **Enterprise** | OTEL → Datadog/Honeycomb/SigNoz | $200-1000/mo | Org-wide dashboards + alerting |
| **Enterprise + AI Eval** | Above + Langfuse/Braintrust/Arize/orq.ai | $100-500/mo (addl) | LLM-as-judge, A/B experiments |

### 5.7 Grafana Dashboard (PromQL Queries)

When metrics are exported to Prometheus (via OTEL Collector), metric names are converted from dot notation to Prometheus convention: `claude_code.token.usage` → `claude_code_token_usage_tokens_total`. If using VictoriaMetrics, enable `opentelemetry.usePrometheusNaming` flag.

**Architecture:**
```
Claude Code → OTLP (gRPC :4317) → OTel Collector → Prometheus scrape (:8889) → Prometheus → PromQL → Grafana
```

**Starter PromQL Queries (tvt-eval-dashboard outputs):**

| Panel | Query | Description |
|-------|-------|-------------|
| Total Cost (24h) | `sum(increase(claude_code_cost_usage_usd_total[24h]))` | Spend in last 24h |
| Cost by Model | `sum by (model)(increase(claude_code_cost_usage_usd_total[24h]))` | Spend breakdown |
| Token Usage Rate | `sum(rate(claude_code_token_usage_tokens_total[5m])) by (type)` | Input/output/cache token velocity |
| Sessions Today | `sum(increase(claude_code_session_count_total[24h]))` | Daily session count |
| Cache Hit Rate | `sum(rate(claude_code_token_usage_tokens_total{type="cacheRead"}[1h])) / (sum(rate(claude_code_token_usage_tokens_total{type="input"}[1h])) + sum(rate(claude_code_token_usage_tokens_total{type="cacheRead"}[1h])))` | Prompt caching efficiency |
| Lines of Code | `sum(increase(claude_code_lines_of_code_count_total[24h])) by (type)` | Code added/removed per day |
| PRs Created | `sum(increase(claude_code_pull_request_count_total[24h]))` | Daily PR count |
| Commits Created | `sum(increase(claude_code_commit_count_total[24h]))` | Daily commit count |
| Cost per Session | `sum(increase(claude_code_cost_usage_usd_total[24h])) / sum(increase(claude_code_session_count_total[24h]))` | Average session cost |
| Active Time | `sum(increase(claude_code_active_time_total_seconds_total[24h])) / 3600` | Total active hours |

**Alert rules (recommended):**
```yaml
# Prometheus alerting rules
groups:
  - name: claude-code-alerts
    rules:
      - alert: HighCostSession
        expr: increase(claude_code_cost_usage_usd_total[1h]) > 5
        for: 5m
        labels: { severity: warning }
        annotations:
          summary: "Claude Code session cost exceeds $5/hour"

      - alert: LowCacheHitRate
        expr: |
          sum(rate(claude_code_token_usage_tokens_total{type="cacheRead"}[1h]))
          / (sum(rate(claude_code_token_usage_tokens_total{type="input"}[1h]))
             + sum(rate(claude_code_token_usage_tokens_total{type="cacheRead"}[1h]))) < 0.3
        for: 15m
        labels: { severity: info }
        annotations:
          summary: "Prompt cache hit rate below 30% — consider restructuring prompts"

      - alert: NoSessions
        expr: sum(increase(claude_code_session_count_total[4h])) == 0
        for: 4h
        labels: { severity: info }
        annotations:
          summary: "No Claude Code sessions in 4 hours (working hours check)"
```

**OTel Collector config (minimal viable — `otel-collector.yaml`):**
```yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

exporters:
  prometheus:
    endpoint: 0.0.0.0:8889
    namespace: ""  # Don't add prefix — Claude Code metrics already namespaced
    resource_to_telemetry_conversion:
      enabled: true  # Promotes resource attributes (session.id, user.email) to metric labels

processors:
  batch:
    timeout: 10s
    send_batch_size: 1024

service:
  pipelines:
    metrics:
      receivers: [otlp]
      processors: [batch]
      exporters: [prometheus]
    logs:
      receivers: [otlp]
      processors: [batch]
      exporters: [prometheus]  # Or use loki exporter for Grafana Loki
```

**Docker Compose (local dev observability stack):**
```yaml
# docker-compose.observability.yml
version: "3.8"
services:
  otel-collector:
    image: otel/opentelemetry-collector-contrib:latest
    ports:
      - "4317:4317"   # OTLP gRPC
      - "4318:4318"   # OTLP HTTP
      - "8889:8889"   # Prometheus metrics endpoint
    volumes:
      - ./config/otel-collector.yaml:/etc/otelcol-contrib/config.yaml

  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./config/prometheus.yml:/etc/prometheus/prometheus.yml

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - ./config/grafana/datasources:/etc/grafana/provisioning/datasources
      - ./config/grafana/dashboards:/etc/grafana/provisioning/dashboards
```

**Claude Code env vars to connect:**
```bash
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export CLAUDE_CODE_ENHANCED_TELEMETRY_BETA=1
export OTEL_METRICS_EXPORTER=otlp
export OTEL_LOGS_EXPORTER=otlp
export OTEL_TRACES_EXPORTER=otlp
export OTEL_EXPORTER_OTLP_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
```

**Community dashboard reference:** [tcude/grafana-dashboards](https://github.com/tcude/grafana-dashboards/blob/main/applications/claudecode.yaml) provides a production-ready Grafana JSON model with panels for cost, tokens, sessions, and code metrics. Import directly via Grafana UI.

---

## Layer 3: Enterprise Integrations (MCP Servers)

### Recommended Stack

| System | MCP Server | Capabilities |
|--------|-----------|-------------|
| Jira | `cosmix/jira-mcp` or Fastn | Issue CRUD, JQL, sprint management |
| Slack | Official or Fastn | Messages, channels, threads |
| Teams | mcpgate or Fastn | Messages, channels |
| GitHub | Official `github-mcp-server` | PRs, issues, code search, reviews |
| Confluence | Enterprise MCP or Fastn | Documentation read/write |
| PagerDuty | Enterprise MCP | Incident management |
| Datadog | Enterprise MCP | Metrics, logs, dashboards |

### Integration Approaches (by team size)

| Approach | Setup | Best For |
|----------|-------|----------|
| Individual MCP servers | One server per tool | Small teams (1-5 devs) |
| MCP Gateway (mcpgate/Fastn) | Single endpoint, all tools | Mid-size teams (5-50 devs) |
| Custom Enterprise MCP | Self-built, 38+ tools | Large orgs (50+ devs) |

### Configuration Pattern

```jsonc
// .mcp.json (project root)
{
  "mcpServers": {
    "jira": {
      "command": "node",
      "args": ["./node_modules/@tvt/mcp-jira/dist/index.js"],
      "env": {
        "JIRA_BASE_URL": "${JIRA_URL}",
        "JIRA_API_TOKEN": "${JIRA_TOKEN}",
        "JIRA_USER_EMAIL": "${JIRA_EMAIL}"
      }
    },
    "slack": {
      "command": "node",
      "args": ["./node_modules/@tvt/mcp-slack/dist/index.js"],
      "env": {
        "SLACK_BOT_TOKEN": "${SLACK_TOKEN}"
      }
    }
  }
}
```

---

## Layer 4: CI/CD Integration

### GitHub Actions Workflows

> **Note:** `claude-code-action@v1` auto-detects mode (interactive vs automation) based on config.
> - Provide `prompt` → automation mode (runs immediately with that prompt)
> - Omit `prompt` → interactive mode (responds to `@claude` mentions in comments)
> - All CLI options go through `claude_args` (e.g., `--model`, `--max-turns`, `--allowedTools`)
> - Deprecated inputs (use `claude_args` instead): `model`, `allowed_tools`, `max_turns`, `custom_instructions`, `fallback_model`
> - `trigger_phrase` is still a valid v1 input (default: `@claude`)
> - Additional v1 inputs: `settings` (JSON string or path), `assignee_trigger`, `label_trigger`, `allowed_bots`, `plugins`, `plugin_marketplaces`

#### Autonomous PR Review (every PR)

```yaml
name: TVT Code Review
on:
  pull_request:
    types: [opened, synchronize]
    paths: ['src/**', 'lib/**', '*.ts', '*.tsx', '*.py']

jobs:
  review:
    if: github.event.pull_request.draft == false
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: |
            Review this PR. Focus on correctness, security, missing
            error handling. Skip formatting (handled by hooks).
            Be concise. One comment per issue.
          claude_args: |
            --model claude-sonnet-4-6-20250514
            --max-turns 5
            --allowedTools Read,Grep,Glob
```

#### Security Review (sensitive paths)

```yaml
name: TVT Security Review
on:
  pull_request:
    paths: ['src/auth/**', 'src/api/**', 'src/payments/**']

jobs:
  security:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: |
            Security review. Check for: injection, XSS, auth bypass,
            data exposure, SSRF, insecure crypto. Cite file:line.
          claude_args: |
            --model claude-opus-4-6-20250514
            --max-turns 8
            --allowedTools Read,Grep,Glob,Bash(npm audit *)
```

#### Quality Gate (eval-powered)

```yaml
name: TVT Quality Gate
on: [pull_request]

jobs:
  quality-gate:
    needs: [lint, test]
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: |
            CI passed. Score this PR 1-10 on correctness, quality,
            security. Output JSON with scores. If overall < 6,
            request changes. If >= 8, approve with praise.
          claude_args: "--model claude-sonnet-4-6-20250514 --max-turns 3"

  # Alternative: Interactive mode (responds to @claude in comments)
  interactive:
    if: |
      github.event_name == 'issue_comment' &&
      contains(github.event.comment.body, '@claude')
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write
    steps:
      - uses: actions/checkout@v4
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          trigger_phrase: "@claude"
          assignee_trigger: "claude"
          allowed_bots: "dependabot[bot],renovate[bot]"
          claude_args: "--model claude-sonnet-4-6-20250514 --max-turns 10"
```

#### Setup Hook (CI environment preparation)

```yaml
name: TVT CI Setup
on: [push, pull_request]

jobs:
  setup:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: "/tvt-dev-review"
          claude_args: |
            --model claude-sonnet-4-6-20250514
            --max-turns 5
            --allowedTools Read,Grep,Glob,Bash(npm test *),Bash(npm run lint *)
          settings: |
            {
              "hooks": {
                "PreToolUse": [{
                  "matcher": "Bash",
                  "hooks": [{"type": "command", "command": ".claude/hooks/block-dangerous.sh"}]
                }]
              }
            }
```

### TVT-SDLC as a Claude Code Plugin (Advanced)

For organizations wanting to distribute TVT-SDLC centrally, package it as a Claude Code plugin:

```yaml
# .github/workflows/tvt-review.yml — with plugin install
- uses: anthropics/claude-code-action@v1
  with:
    anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
    plugins: "tvt-sdlc@tavant-plugins"
    plugin_marketplaces: "https://github.com/tavant/claude-plugins.git"
    prompt: "/tvt-dev-review"
    claude_args: "--model claude-sonnet-4-6-20250514 --max-turns 5"
```

### Cost Controls

| Control | Method | Recommendation |
|---------|--------|---------------|
| Budget cap | `--max-budget-usd 0.50` in `claude_args` | Per CI run |
| Turn limit | `--max-turns 5` in `claude_args` | Prevent infinite loops |
| Path filters | `paths: ['src/**']` in workflow `on:` | Skip lockfiles/generated code |
| Skip drafts | `if: !github.event.pull_request.draft` | Don't review WIP |
| Model choice | Sonnet for reviews, Opus for security | Balance cost vs. depth |
| Sticky comment | `use_sticky_comment: "true"` | One comment per PR, updated in-place |
| Bot allowlist | `allowed_bots: "dependabot[bot]"` | Let bots trigger reviews selectively |

---

## Layer 0: Foundation (CLAUDE.md Template)

```markdown
# Project Standards — [Project Name]

## Architecture
- [Pattern]: e.g., Clean Architecture, Hexagonal, Microservices
- [Structure]: e.g., Feature-based directories
- [Key decisions]: Link to ADRs

## Coding Standards
- Language: [TypeScript strict / Python 3.11+ / etc.]
- Style: [Enforced by prettier/black — no manual formatting]
- Types: [Strict — no `any`, no implicit any]
- Error handling: [Explicit try-catch, typed errors, no silent failures]
- Naming: [PascalCase components, camelCase functions, UPPER_SNAKE constants]

## Testing
- Framework: [Jest / pytest / etc.]
- Minimum coverage: [80% for new code]
- Location: [Colocated with source files]
- Required: [Unit for all business logic, integration for API routes]

## Security
- Never commit secrets (use env vars via .env.local)
- Sanitize all user input at system boundaries
- Parameterized queries only (no string concatenation for SQL)
- Auth: [Method — JWT / session / etc.]

## Git
- Commits: Conventional Commits (feat:, fix:, chore:, docs:, refactor:)
- Branches: feature/, bugfix/, hotfix/, release/
- Merge: Squash to main
- PR: Requires 1 approval + CI green

## FORBIDDEN
- Never `rm -rf` or `git push --force`
- Never modify .env, .env.*, secrets/
- Never bypass CI checks
- Never disable TypeScript strict mode
- Never use `eval()` or dynamic code execution from user input

## Common Commands
- `npm run dev` — Start dev server
- `npm test` — Run test suite
- `npm run lint` — Run linter
- `npm run build` — Production build
- `npm run typecheck` — TypeScript validation
```

---

## Implementation Roadmap

### Phase 1: Foundation + Eval (Week 1-2) — Day-by-Day Plan

**Goal:** Immediate visibility, zero infrastructure cost. One senior engineer, one sprint.

**Prerequisites:**
- Node.js 18+ installed
- npm/bun available
- `jq` installed (for hook scripts)
- `prettier` in project devDependencies (or globally)
- ESLint configured for project language
- Git repository initialized with main branch
- No external services required (all file-based)

#### Day 1-2: Foundation Layer

| Task | Deliverable | Test |
|------|-------------|------|
| Create CLAUDE.md template | `CLAUDE.md` at project root | Claude respects all standards when prompted |
| Create settings.json | `.claude/settings.json` with permissions + hooks | `claude --print-config` shows hooks loaded |
| Create `.gitignore` entries | Ignore `audit.jsonl`, `eval-log.jsonl`, `settings.local.json` | `git status` doesn't show runtime files |
| Create hook directory structure | `.claude/hooks/` with all scripts | `ls .claude/hooks/*.sh` lists 10 scripts |
| Create `tvt-dev-standards` skill | `.claude/skills/tvt-dev-standards/SKILL.md` | `/tvt-dev-standards` in a fresh repo → creates full scaffold |
| Create `.claude/conventions.md` | Team conventions template | Content injected on every prompt via UserPromptSubmit hook |

#### Day 3-4: Safety Hooks

| Task | Deliverable | Test |
|------|-------------|------|
| `block-dangerous.sh` | Blocks `rm -rf`, `git push --force`, `terraform destroy` | `echo '{"tool_name":"Bash","tool_input":{"command":"rm -rf /"}}' \| bash .claude/hooks/block-dangerous.sh; echo $?` → exits 2 |
| `protect-files.sh` | Blocks writes to `.env*`, `*.lock`, `.github/workflows/*` | Same pattern with Write tool_input |
| `secret-scan.sh` | Scans written content for API keys, passwords, tokens | Write file with `AKIA...` → exit 2 |

**block-dangerous.sh implementation:**
```bash
#!/bin/bash
set -euo pipefail
INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')
[ -z "$COMMAND" ] && exit 0

# Pattern list — add project-specific patterns
BLOCKED_PATTERNS=(
  "rm -rf"
  "git push --force"
  "git push -f"
  "terraform destroy"
  "terraform apply -auto-approve"
  "kubectl delete namespace"
  "DROP TABLE"
  "DROP DATABASE"
)

for pattern in "${BLOCKED_PATTERNS[@]}"; do
  if echo "$COMMAND" | grep -qi "$pattern"; then
    echo "BLOCKED: Command matches prohibited pattern '$pattern'" >&2
    exit 2
  fi
done
exit 0
```

**protect-files.sh implementation:**
```bash
#!/bin/bash
set -euo pipefail
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')
[ -z "$FILE_PATH" ] && exit 0

# Protected file patterns
PROTECTED_PATTERNS=(
  ".env"
  ".env.*"
  "*.lock"
  "package-lock.json"
  "yarn.lock"
  "pnpm-lock.yaml"
  ".github/workflows/*"
  "Dockerfile"
  "docker-compose*.yml"
  ".claude/settings.json"
)

for pattern in "${PROTECTED_PATTERNS[@]}"; do
  # Use bash pattern matching (supports glob * but not full regex)
  if [[ "$FILE_PATH" == $pattern ]]; then
    echo "PROTECTED: '$FILE_PATH' matches protected pattern '$pattern'. Modify manually." >&2
    exit 2
  fi
done
exit 0
```

**secret-scan.sh implementation (PreToolUse — blocks write/edit BEFORE it happens):**
```bash
#!/bin/bash
set -euo pipefail
INPUT=$(cat)
# PreToolUse: uses "tool_input" (singular). Check content for Write, new_string for Edit.
CONTENT=$(echo "$INPUT" | jq -r '.tool_input.content // .tool_input.new_string // empty')
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // "unknown"')
[ -z "$CONTENT" ] && exit 0

# Secret patterns (regex)
SECRET_PATTERNS=(
  'AKIA[0-9A-Z]{16}'                    # AWS Access Key
  'sk-[a-zA-Z0-9]{20,}'                 # OpenAI/Stripe secret key
  'ghp_[a-zA-Z0-9]{36}'                 # GitHub personal access token
  'xox[baprs]-[a-zA-Z0-9-]+'            # Slack token
  'AIza[0-9A-Za-z_-]{35}'               # Google API key
  'password\s*[:=]\s*["\x27][^"\x27]+'  # Hardcoded passwords
  'api[_-]?key\s*[:=]\s*["\x27][^"\x27]{10,}' # Generic API keys
)

for pattern in "${SECRET_PATTERNS[@]}"; do
  if echo "$CONTENT" | grep -qEi "$pattern"; then
    echo "SECRET DETECTED in '$FILE_PATH': Content matches pattern for potential credential. Remove before committing." >&2
    exit 2
  fi
done
exit 0
```

#### Day 5-6: Quality + Audit Hooks

| Task | Deliverable | Test |
|------|-------------|------|
| `audit.sh` | Logs every tool call to `.claude/audit.jsonl` | Run any Claude session → verify JSONL appended |
| `lint-changed.sh` | ESLint on the specific file written | Edit a .ts file with lint error → output shows warning |
| `inject-context.sh` | Outputs git branch + status + last 5 commits | Run at session start → Claude sees context |

**lint-changed.sh implementation (PostToolUse — lint the file just written/edited):**
```bash
#!/bin/bash
set -euo pipefail
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.inputs.file_path // empty')
[ -z "$FILE_PATH" ] && exit 0
[ ! -f "$FILE_PATH" ] && exit 0

# Only lint lintable files
case "$FILE_PATH" in
  *.ts|*.tsx|*.js|*.jsx)
    LINT_OUTPUT=$(npx eslint --no-error-on-unmatched-pattern --format compact "$FILE_PATH" 2>&1) || true
    if [ -n "$LINT_OUTPUT" ]; then
      # Inject lint results as context — doesn't block, just informs Claude
      ESCAPED=$(echo "$LINT_OUTPUT" | head -20 | jq -Rs .)
      echo "{\"hookSpecificOutput\":{\"hookEventName\":\"PostToolUse\",\"additionalContext\":\"Lint results for $FILE_PATH: $ESCAPED\"}}"
    fi
    ;;
  *.py)
    LINT_OUTPUT=$(python -m flake8 --max-line-length=120 "$FILE_PATH" 2>&1) || true
    if [ -n "$LINT_OUTPUT" ]; then
      ESCAPED=$(echo "$LINT_OUTPUT" | head -20 | jq -Rs .)
      echo "{\"hookSpecificOutput\":{\"hookEventName\":\"PostToolUse\",\"additionalContext\":\"Lint results for $FILE_PATH: $ESCAPED\"}}"
    fi
    ;;
esac
exit 0
```

**audit.sh implementation:**
```bash
#!/bin/bash
set -euo pipefail
INPUT=$(cat)
TOOL=$(echo "$INPUT" | jq -r '.tool_name // "unknown"')
SESSION=$(echo "$INPUT" | jq -r '.session_id // "unknown"')
# PostToolUse uses "inputs" (plural), not "tool_input"
DETAIL=$(echo "$INPUT" | jq -r '.inputs // .tool_input | if .command then .command elif .file_path then .file_path else (. | tostring | .[:100]) end')
FILE=$(echo "$INPUT" | jq -r '(.inputs // .tool_input).file_path // ""')

AUDIT_FILE="${CLAUDE_PROJECT_DIR:-.}/.claude/audit.jsonl"
mkdir -p "$(dirname "$AUDIT_FILE")"

echo "{\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"session_id\":\"$SESSION\",\"tool\":\"$TOOL\",\"detail\":\"$DETAIL\",\"file\":\"$FILE\"}" >> "$AUDIT_FILE"
exit 0
```

**eval-session.sh implementation (Stop hook — MUST check `stop_hook_active`):**
```bash
#!/bin/bash
set -euo pipefail
INPUT=$(cat)

# CRITICAL: Prevent infinite loop. If this hook already triggered a continuation,
# stop_hook_active will be true. Exit immediately to let Claude finish.
ACTIVE=$(echo "$INPUT" | jq -r '.stop_hook_active // false')
if [ "$ACTIVE" = "true" ]; then
  exit 0
fi

SESSION=$(echo "$INPUT" | jq -r '.session_id // "unknown"')
EVAL_FILE="${CLAUDE_PROJECT_DIR:-.}/.claude/eval-log.jsonl"
mkdir -p "$(dirname "$EVAL_FILE")"

# Check if any code files were modified this session
CHANGED_FILES=$(git diff --name-only HEAD 2>/dev/null || echo "")
if [ -z "$CHANGED_FILES" ]; then
  # No code changes — skip eval
  exit 0
fi

# Run tests (capture result, don't fail the hook)
TEST_PASS=true
TEST_OUTPUT=$(npm test 2>&1) || TEST_PASS=false

# Run lint check
LINT_ERRORS=0
LINT_OUTPUT=$(npx eslint --format json $CHANGED_FILES 2>/dev/null) && \
  LINT_ERRORS=$(echo "$LINT_OUTPUT" | jq '[.[].errorCount] | add // 0') || true

# Compute simple score
SCORE=10
[ "$TEST_PASS" = "false" ] && SCORE=$((SCORE - 4))
[ "$LINT_ERRORS" -gt 0 ] && SCORE=$((SCORE - LINT_ERRORS))
[ "$SCORE" -lt 1 ] && SCORE=1

# Write eval record
RECOMMENDATION="ship"
[ "$SCORE" -lt 6 ] && RECOMMENDATION="fix"
[ "$SCORE" -lt 4 ] && RECOMMENDATION="block"

echo "{\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"session_id\":\"$SESSION\",\"scores\":{\"tests_pass\":$TEST_PASS,\"lint_errors\":$LINT_ERRORS},\"overall\":$SCORE,\"recommendation\":\"$RECOMMENDATION\"}" >> "$EVAL_FILE"

# If tests failed, block the stop and tell Claude to fix
if [ "$TEST_PASS" = "false" ]; then
  echo "{\"decision\":\"block\",\"reason\":\"Tests failed. Please fix failing tests before completing. Failures: $(echo "$TEST_OUTPUT" | tail -5)\"}"
  exit 0
fi

exit 0
```

**Key pattern:** The eval-session hook uses `decision: "block"` (not `continue: true`) to force Claude to keep working. This is the correct Stop hook continuation protocol.

**auto-format.sh implementation (PostToolUse — format after write/edit):**
```bash
#!/bin/bash
set -euo pipefail
INPUT=$(cat)
# PostToolUse uses "inputs" (plural) field
FILE_PATH=$(echo "$INPUT" | jq -r '.inputs.file_path // empty')
[ -z "$FILE_PATH" ] && exit 0
[ ! -f "$FILE_PATH" ] && exit 0

# Determine formatter by file extension
case "$FILE_PATH" in
  *.ts|*.tsx|*.js|*.jsx|*.json|*.css|*.scss|*.md|*.html)
    npx prettier --write "$FILE_PATH" 2>/dev/null || true
    ;;
  *.py)
    python -m black "$FILE_PATH" 2>/dev/null || true
    ;;
  *.go)
    gofmt -w "$FILE_PATH" 2>/dev/null || true
    ;;
  *.rs)
    rustfmt "$FILE_PATH" 2>/dev/null || true
    ;;
esac

# Return context to Claude about what happened
echo '{"hookSpecificOutput":{"hookEventName":"PostToolUse","additionalContext":"File auto-formatted"}}'
exit 0
```

**inject-context.sh implementation (SessionStart — stdout goes directly to Claude):**
```bash
#!/bin/bash
set -euo pipefail
# SessionStart stdout is added to Claude's context — this is how we inject project state

echo "## Current Project State"
echo ""
echo "**Branch:** $(git branch --show-current 2>/dev/null || echo 'unknown')"
echo "**Status:**"
git status --short 2>/dev/null | head -20 || echo "Not a git repo"
echo ""
echo "**Recent commits:**"
git log --oneline -5 2>/dev/null || echo "No commits"
echo ""

# If there's a sprint/iteration file, include it
if [ -f ".claude/sprint-context.md" ]; then
  echo "**Sprint context:**"
  cat .claude/sprint-context.md
fi

exit 0
```

**conventions-inject.sh implementation (UserPromptSubmit — append team priorities):**
```bash
#!/bin/bash
set -euo pipefail
# UserPromptSubmit: stdout is appended to Claude's context after the user's prompt.
# Use this to inject reminders, conventions, or sprint priorities into every interaction.

CONVENTIONS_FILE="${CLAUDE_PROJECT_DIR:-.}/.claude/conventions.md"
if [ -f "$CONVENTIONS_FILE" ]; then
  cat "$CONVENTIONS_FILE"
fi

exit 0
```

The conventions file (`.claude/conventions.md`) contains team reminders that apply to every prompt:
```markdown
## Active Conventions
- All new code requires tests (minimum: unit tests for business logic)
- Use named exports, not default exports
- Prefer early returns over nested conditionals
- When fixing bugs, add a regression test first
```

This hook requires a matching entry in `settings.json`:
```jsonc
"UserPromptSubmit": [
  {
    "hooks": [{
      "type": "command",
      "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/conventions-inject.sh",
      "timeout": 5
    }]
  }
]
```

**notify-slack.sh implementation (Notification — runs async via config field):**
```bash
#!/bin/bash
# This hook is configured with "async": true in settings.json,
# so Claude continues immediately without waiting for it to finish.
set -euo pipefail
INPUT=$(cat)

MESSAGE=$(echo "$INPUT" | jq -r '.message // "Claude needs attention"')
WEBHOOK_URL="${SLACK_WEBHOOK_URL:-}"

if [ -z "$WEBHOOK_URL" ]; then
  exit 0  # No webhook configured — silently skip
fi

curl -s -X POST "$WEBHOOK_URL" \
  -H 'Content-Type: application/json' \
  -d "{\"text\": \"Claude Code: $MESSAGE\"}" \
  > /dev/null 2>&1 || true

exit 0
```

#### Day 7-8: Eval Skills

| Task | Deliverable | Test |
|------|-------------|------|
| `tvt-eval-audit` SKILL.md | `.claude/skills/tvt-eval-audit/SKILL.md` | `/tvt-eval-audit` → shows audit summary |
| `tvt-eval-score` SKILL.md | `.claude/skills/tvt-eval-score/SKILL.md` | `/tvt-eval-score` → runs tests + outputs JSON score |
| `eval-session.sh` (Stop hook) | Invokes scoring at end of session | Complete a session → eval-log.jsonl updated |

#### Day 9-10: Commit Skill + Integration Test

| Task | Deliverable | Test |
|------|-------------|------|
| `tvt-dev-commit` SKILL.md | `.claude/skills/tvt-dev-commit/SKILL.md` | `/tvt-dev-commit` → creates conventional commit |
| End-to-end integration test | Full session: edit → auto-format → audit → eval → commit | All hooks fire, all logs written, commit passes |
| Documentation | README.md with setup instructions | New team member can install in <5 minutes |

#### Dependencies (npm packages)

```json
{
  "devDependencies": {
    "prettier": "^3.0.0",
    "eslint": "^9.0.0",
    "jq": "system"
  }
}
```

No external services. No API keys beyond `ANTHROPIC_API_KEY`. No Docker. No cloud infrastructure.

### Phase 2: Core Dev Skills (Week 3-4)

| Deliverable | Description |
|-------------|-------------|
| `tvt-dev-review` | Self-review workflow |
| `tvt-dev-pr` | Structured PR creation |
| `tvt-dev-tdd` | Test-first workflow |
| `tvt-dev-test` | Test generation for changed files |
| `tvt-dev-security` | OWASP + dependency scan |
| `tvt-dev-docs` | Documentation generation |

### Phase 3: Observability + Integrations (Week 5-6)

| Deliverable | Description |
|-------------|-------------|
| `tvt-eval-trace` | OpenTelemetry configuration skill |
| `tvt-eval-dashboard` | Metrics summary generation |
| `tvt-int-jira` | Jira MCP integration |
| `tvt-int-slack` | Slack MCP integration |
| `tvt-int-github` | GitHub advanced automation |
| `tvt-ops-status` | Progress sync to Jira/Slack |

### Phase 4: CI/CD + Compounds (Week 7-8)

| Deliverable | Description |
|-------------|-------------|
| `tvt-dev-cicd` | GitHub Actions workflow generator |
| PR Review workflow | `.github/workflows/tvt-review.yml` |
| Security Review workflow | `.github/workflows/tvt-security.yml` |
| Quality Gate workflow | `.github/workflows/tvt-quality-gate.yml` |
| `tvt-dev-ship` | Full shipping compound |
| `tvt-dev-onboard` | Repo bootstrap compound |

### Phase 5: Advanced + Improvement Loop (Week 9-10)

| Deliverable | Description |
|-------------|-------------|
| `tvt-eval-improve` | Failure pattern analysis → fix suggestions |
| `tvt-eval-report` | Weekly eval rollup compound |
| `tvt-dev-deploy` | Multi-env deployment |
| `tvt-dev-infra` | IaC generation |
| `tvt-ops-incident` | Incident response |
| `tvt-ops-runbook` | Runbook generation |
| LLM-as-Judge CI integration | Advanced quality gate with scoring |

---

## Distribution & Packaging

### Installation Options

```bash
# Option 1: npm package (recommended)
npx @tavant/tvt-sdlc init

# Option 2: Git submodule
git submodule add https://github.com/tavant/tvt-sdlc .claude/skills/tvt

# Option 3: Copy-paste (starter)
gh repo clone tavant/tvt-sdlc .claude/skills/tvt
```

### Directory Structure (Installed)

```
.claude/
├── settings.json              ← Permissions + hooks (team-wide)
├── settings.local.json        ← Personal overrides (gitignored)
├── conventions.md             ← Team conventions injected per prompt (committed)
├── hooks/
│   ├── block-dangerous.sh
│   ├── protect-files.sh
│   ├── auto-format.sh
│   ├── lint-changed.sh
│   ├── secret-scan.sh
│   ├── audit.sh
│   ├── eval-session.sh
│   ├── inject-context.sh
│   ├── conventions-inject.sh
│   └── notify-slack.sh
├── skills/
│   ├── tvt-dev-standards/SKILL.md   ← Phase 1 (project bootstrap)
│   ├── tvt-dev-scaffold/SKILL.md
│   ├── tvt-dev-commit/SKILL.md
│   ├── tvt-dev-review/SKILL.md
│   ├── tvt-dev-pr/SKILL.md
│   ├── tvt-dev-tdd/SKILL.md
│   ├── tvt-dev-test/SKILL.md
│   ├── tvt-dev-security/SKILL.md
│   ├── tvt-dev-docs/SKILL.md
│   ├── tvt-dev-infra/SKILL.md
│   ├── tvt-dev-cicd/SKILL.md
│   ├── tvt-dev-deploy/SKILL.md
│   ├── tvt-dev-ship/SKILL.md
│   ├── tvt-dev-onboard/SKILL.md
│   ├── tvt-eval-trace/SKILL.md
│   ├── tvt-eval-score/SKILL.md
│   ├── tvt-eval-audit/SKILL.md
│   ├── tvt-eval-dashboard/SKILL.md
│   ├── tvt-eval-improve/SKILL.md
│   ├── tvt-eval-report/SKILL.md
│   ├── tvt-ops-incident/SKILL.md
│   ├── tvt-ops-status/SKILL.md
│   ├── tvt-ops-runbook/SKILL.md
│   ├── tvt-int-jira/SKILL.md
│   ├── tvt-int-slack/SKILL.md
│   ├── tvt-int-teams/SKILL.md
│   └── tvt-int-github/SKILL.md
├── audit.jsonl                ← Audit log (gitignored)
└── eval-log.jsonl             ← Eval scores (gitignored)

CLAUDE.md                      ← Project standards (committed)
REVIEW.md                      ← Review-only instructions (see template below)
.mcp.json                      ← MCP server configuration (committed)
```

### REVIEW.md Template

`REVIEW.md` is loaded automatically by Claude Code when reviewing PRs (in GitHub Actions or local review). It constrains what the review focuses on.

```markdown
# Review Instructions

## Focus Areas (in priority order)
1. Security: injection, auth bypass, data exposure, SSRF
2. Correctness: logic errors, missing edge cases, type mismatches
3. Error handling: unhandled exceptions, silent failures
4. Breaking changes: API contract violations, schema changes

## Skip
- Formatting (handled by prettier/auto-format hooks)
- Naming style (handled by lint)
- Documentation completeness (separate concern)

## Severity Levels
- 🔴 BLOCKING: Must fix before merge (security, data loss, crashes)
- 🟡 SUGGESTION: Should fix but won't block (quality, readability)
- 🟢 NIT: Optional improvement (style preference)

## Output Format
One comment per issue. Include file:line reference.
Maximum 10 comments per review. Prioritize by severity.
```

---

## Competitive Positioning

### Comparison to Existing Solutions

| Feature | Jerry0022/dotclaude | CloudAI-X/workflow | **TVT-SDLC** |
|---------|--------------------|--------------------|--------------|
| Skills | 16 | 14 | 27 |
| Hooks | 13 | 14 | 13+ |
| Eval layer | Token tracking only | Session metrics only | **Full 6-dimension quality eval** |
| LLM-as-Judge | No | No | **Yes (CI/CD gated)** |
| OpenTelemetry native | No | No | **Yes (traces + metrics + logs)** |
| Enterprise integrations | GitHub only | GitHub only | **Jira + Slack + Teams + GitHub** |
| CI/CD quality gate | Basic | Basic | **Eval-powered scoring gate** |
| Improvement feedback loop | No | No | **Yes (pattern → fix → verify)** |
| Multi-language | Node/TS focused | Python focused | **Any stack** |
| Packaging | GitHub clone | npx install | **npm + submodule + copy** |

### TVT-SDLC Differentiators

1. **Eval-first** — Quality measurement is Layer 5, not an afterthought
2. **LLM-as-Judge** — AI evaluates AI output with structured scoring
3. **Continuous improvement loop** — Failure patterns automatically drive fixes
4. **Enterprise connectors** — Jira/Slack/Teams integration built-in
5. **Stack-agnostic** — Works with any language, any framework
6. **Compliance-ready** — Structured audit trail for regulated industries

---

## Success Metrics

### Adoption

| Metric | Target | How to Measure |
|--------|--------|---------------|
| Team daily active users | >80% of team | `claude_code.session.count` |
| Skills invocations/day | >5 per developer | `claude_code.skill_activated` events |
| Suggestion accept rate | >70% | Built-in analytics |

### Quality

| Metric | Target | How to Measure |
|--------|--------|---------------|
| Eval score (overall) | >7.5/10 average | `tvt-eval-score` output |
| Test pass rate after Claude edits | >95% | Stop hook eval |
| Security findings per PR | <1 average | CI security scan |
| Lint errors introduced | 0 (auto-fixed) | PostToolUse hook |

### Velocity

| Metric | Target | How to Measure |
|--------|--------|---------------|
| PRs with Claude Code (%) | >60% | Built-in analytics |
| Issue → PR cycle time | <4 hours | Jira + GitHub timestamps |
| Review turnaround time | <30 minutes | GitHub PR metrics |

### Cost

| Metric | Target | How to Measure |
|--------|--------|---------------|
| Cost per PR review | <$0.10 (Sonnet) | `claude_code.cost.usage` |
| Cost per session | <$1.00 average | `claude_code.cost.usage` |
| ROI vs manual effort | >5x | Time saved vs token cost |

---

## References & Prior Art

| Resource | What It Provides |
|----------|-----------------|
| [Anthropic Claude Code Docs — Hooks](https://docs.anthropic.com/en/docs/claude-code/hooks-guide) | Official hooks documentation |
| [Anthropic Claude Code Docs — Skills](https://docs.anthropic.com/en/docs/claude-code/skills) | Official skills documentation |
| [Anthropic Claude Code Docs — Monitoring](https://docs.anthropic.com/en/docs/claude-code/monitoring-usage) | OpenTelemetry integration |
| [Anthropic Claude Code Docs — GitHub Actions](https://github.com/anthropics/claude-code-action) | CI/CD integration (v1 action repo + docs) |
| [Jerry0022/dotclaude](https://github.com/Jerry0022/dotclaude) | Reference: 16 skills + 13 hooks DevOps plugin |
| [CloudAI-X/claude-workflow-v2](https://github.com/CloudAI-X/claude-workflow) | Reference: 14 skills + 14 hooks universal workflow |
| [AdrienTHOMAS/enterprise-mcp-server](https://github.com/AdrienTHOMAS/enterprise-mcp-server) | Reference: 38 tools across enterprise platforms |
| [fastnai/fastn-mcp](https://github.com/fastnai/fastn-mcp) | 250+ managed enterprise connectors |
| [mcpgate](https://mcpgate.de) | Self-hosted MCP gateway with policy hooks |
| [Meta CQS (Code Quality Score)](https://openreview.net/pdf/d3e87b6917b4c324d666c63a79df911ec7fb0fe6.pdf) | LLM-powered code quality evaluation at scale |
| [ByteDance BitsAI-CR](https://arxiv.org/html/2501.15134v1) | Automated code review with data flywheel |
| [Codility COMPASS](https://www.arxiv.org/pdf/2508.13757) | Multi-dimensional code eval: correctness, efficiency, quality |
| [SWE-PRBench](https://arxiv.org/pdf/2603.26130) | LLM-as-Judge for code review quality measurement |

---

## Design Decisions (Alternatives Considered)

### Hook handler type: `command` vs `http` vs `mcp_tool` vs `prompt` vs `agent`

| Option | Pros | Cons | Decision |
|--------|------|------|----------|
| **`command` (chosen)** | Zero infra, fast (<100ms), works offline, easy to debug | Script maintenance, no remote eval | Default for Phase 1-2 |
| `http` | Remote services, scalable, team-shared | Requires running server, latency, network dependency | Phase 3+ for centralized eval |
| `mcp_tool` | Direct MCP server invocation, no shell needed | Depends on MCP server being connected | Phase 3 for Jira/Slack integration hooks |
| `prompt` | LLM-powered decisions, flexible | Expensive per invocation ($0.01-0.10), slow (1-3s) | Phase 5 for LLM-as-Judge only |
| `agent` | Complex multi-step validation | Very expensive, slow (10-60s) | Not planned |

**Source:** [Claude Code Hooks Reference](https://docs.anthropic.com/en/docs/claude-code/hooks) — all 5 handler types: `command`, `http`, `mcp_tool`, `prompt`, `agent`.

### Eval approach: Deterministic vs LLM-as-Judge vs Hybrid

| Option | Pros | Cons | Decision |
|--------|------|------|----------|
| Deterministic only | Fast, cheap, reproducible | Misses semantic issues, false positives | Layer 2 hooks |
| LLM-as-Judge only | Catches subtle issues, context-aware | Expensive, non-deterministic, slow | CI gate only |
| **Hybrid (chosen)** | Best of both — fast checks + deep eval | More complex to configure | Hooks = deterministic; CI = LLM judge |

**Source:** Meta CQS uses hybrid (rule-based filter + LLM scoring). ByteDance BitsAI-CR uses deterministic pre-filter + LLM evaluation.

### CI/CD trigger strategy: Every PR vs Path-filtered vs Manual

| Option | Pros | Cons | Decision |
|--------|------|------|----------|
| Every PR | Complete coverage | Expensive, noisy on lockfile/config changes | Security review only |
| **Path-filtered (chosen)** | Cost-effective, relevant | May miss cross-cutting issues | Code review + quality gate |
| Manual (@claude) | Zero cost until invoked | Easy to forget, inconsistent | Interactive mode (always available) |

**Source:** [claude-code-action docs](https://github.com/anthropics/claude-code-action/blob/main/docs/usage.md) — path filters in workflow `on:` config.

### Observability: File-based vs OTEL vs Analytics API vs SaaS

| Option | Infra Cost | Best For | Decision |
|--------|-----------|----------|----------|
| **File-based (chosen for Phase 1)** | $0 | Solo/small team, getting started | `.claude/audit.jsonl` + `.claude/eval-log.jsonl` |
| Analytics Admin API | $0 | Adoption dashboards, daily aggregates | Phase 1 add-on (complements file-based) |
| OTEL → self-hosted (Grafana) | $50-200/mo | Mid-size team wanting dashboards | Phase 3 |
| OTEL → SaaS (Datadog/Honeycomb) | $200-1000/mo | Enterprise with existing observability | Phase 3+ |
| AI Eval platform (Langfuse/Braintrust) | $100-500/mo | Teams doing LLM-as-Judge at scale | Phase 5 |

**Source:** [Claude Code Monitoring docs](https://docs.anthropic.com/en/docs/claude-code/monitoring-usage) — native OTEL support with 8 metrics, 15+ event types, full span tracing (beta), privacy-gated content logging, and managed policy distribution. [Analytics Admin API](https://docs.anthropic.com/en/api/claude-code-analytics-api) — daily per-user aggregates via REST.

---

## Security Model

### Credential Storage

| Secret | Storage Location | Access Pattern |
|--------|-----------------|----------------|
| `ANTHROPIC_API_KEY` | GitHub Secrets / env var | CI workflows, local dev |
| `JIRA_API_TOKEN` | GitHub Secrets → env var in `.mcp.json` | MCP server at runtime |
| `SLACK_BOT_TOKEN` | GitHub Secrets → env var in `.mcp.json` | MCP server at runtime |
| `OTEL_EXPORTER_OTLP_HEADERS` | Environment variable | Collector auth |

**Rules:**
- NEVER in `.claude/settings.json` (committed to Git)
- NEVER in SKILL.md files
- Use `${ENV_VAR}` interpolation in `.mcp.json` (Claude Code resolves from environment)
- `.claude/settings.local.json` is gitignored — safe for personal tokens during dev

### Permission Boundaries

| Layer | Has Access To | Does NOT Have Access To |
|-------|--------------|------------------------|
| Hooks (scripts) | File system, env vars, network | Claude conversation content |
| Skills | Claude tools (gated by `allowed-tools`) | Direct file system (only through tools) |
| CI/CD | Repo code, GitHub API, secrets | Production infrastructure (blocked by deny rules) |
| MCP servers | Their configured API (Jira, Slack, etc.) | Other MCP servers, file system |

---

## Phase State Machine + Context Store

The phase state machine provides persistent project state that tracks lifecycle position, accumulated decisions, and deliverables. It enables phase-aware context switching — the same Claude instance behaves differently depending on what phase the project is in.

### `project-state.json` Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "required": ["project", "methodology", "current_phase", "phases", "phase_entered", "quality_gates_passed", "context_store"],
  "properties": {
    "project": {
      "type": "string",
      "description": "Project identifier (kebab-case)"
    },
    "methodology": {
      "type": "string",
      "enum": ["greenfield", "legacy-modernization", "microservices", "ml-data-science", "cloud-migration", "api-platform"],
      "description": "Active methodology specialization"
    },
    "current_phase": {
      "type": "integer",
      "minimum": 1,
      "maximum": 7,
      "description": "Current phase number (1-indexed)"
    },
    "phases": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["number", "name", "status"],
        "properties": {
          "number": { "type": "integer" },
          "name": { "type": "string" },
          "status": { "type": "string", "enum": ["pending", "active", "completed", "skipped"] },
          "entered_at": { "type": "string", "format": "date-time" },
          "completed_at": { "type": "string", "format": "date-time" }
        }
      },
      "minItems": 7,
      "maxItems": 7
    },
    "phase_entered": {
      "type": "string",
      "format": "date-time",
      "description": "ISO 8601 timestamp of current phase entry"
    },
    "quality_gates_passed": {
      "type": "array",
      "items": { "type": "integer" },
      "description": "Phase numbers whose quality gates have passed"
    },
    "context_store": {
      "type": "object",
      "required": ["decisions", "deliverables", "constraints", "risks"],
      "properties": {
        "decisions": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["id", "phase", "title", "choice", "rationale", "timestamp"],
            "properties": {
              "id": { "type": "string", "pattern": "^DEC-[0-9]{3}$" },
              "phase": { "type": "integer" },
              "title": { "type": "string" },
              "choice": { "type": "string" },
              "rationale": { "type": "string" },
              "alternatives_rejected": { "type": "array", "items": { "type": "string" } },
              "timestamp": { "type": "string", "format": "date-time" }
            }
          }
        },
        "deliverables": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["id", "phase", "name", "path", "status"],
            "properties": {
              "id": { "type": "string", "pattern": "^DEL-[0-9]{3}$" },
              "phase": { "type": "integer" },
              "name": { "type": "string" },
              "path": { "type": "string", "description": "Relative file path" },
              "status": { "type": "string", "enum": ["draft", "complete", "superseded"] },
              "produced_at": { "type": "string", "format": "date-time" }
            }
          }
        },
        "constraints": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["id", "phase", "description", "source"],
            "properties": {
              "id": { "type": "string", "pattern": "^CON-[0-9]{3}$" },
              "phase": { "type": "integer" },
              "description": { "type": "string" },
              "source": { "type": "string", "enum": ["requirement", "architecture", "compliance", "business", "technical"] },
              "impacts_phases": { "type": "array", "items": { "type": "integer" } }
            }
          }
        },
        "risks": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["id", "phase", "description", "likelihood", "impact", "mitigation"],
            "properties": {
              "id": { "type": "string", "pattern": "^RSK-[0-9]{3}$" },
              "phase": { "type": "integer" },
              "description": { "type": "string" },
              "likelihood": { "type": "string", "enum": ["low", "medium", "high"] },
              "impact": { "type": "string", "enum": ["low", "medium", "high", "critical"] },
              "mitigation": { "type": "string" },
              "status": { "type": "string", "enum": ["open", "mitigated", "accepted", "occurred"] }
            }
          }
        }
      }
    },
    "compliance_frameworks": {
      "type": "array",
      "items": { "type": "string", "enum": ["soc2", "hipaa", "pci-dss", "gdpr", "sox", "iso27001"] },
      "description": "Applicable compliance frameworks for this project"
    },
    "metadata": {
      "type": "object",
      "properties": {
        "created_at": { "type": "string", "format": "date-time" },
        "last_modified": { "type": "string", "format": "date-time" },
        "version": { "type": "integer", "description": "Incremented on every write" }
      }
    }
  }
}
```

### Example `project-state.json`

```json
{
  "project": "acme-platform",
  "methodology": "greenfield",
  "current_phase": 3,
  "phases": [
    { "number": 1, "name": "Discovery", "status": "completed", "entered_at": "2026-04-01T09:00:00Z", "completed_at": "2026-04-05T17:00:00Z" },
    { "number": 2, "name": "Architecture", "status": "completed", "entered_at": "2026-04-06T09:00:00Z", "completed_at": "2026-04-12T17:00:00Z" },
    { "number": 3, "name": "Foundation", "status": "active", "entered_at": "2026-04-13T09:00:00Z" },
    { "number": 4, "name": "Implementation", "status": "pending" },
    { "number": 5, "name": "Integration", "status": "pending" },
    { "number": 6, "name": "Testing & QA", "status": "pending" },
    { "number": 7, "name": "Launch", "status": "pending" }
  ],
  "phase_entered": "2026-04-13T09:00:00Z",
  "quality_gates_passed": [1, 2],
  "context_store": {
    "decisions": [
      {
        "id": "DEC-001",
        "phase": 2,
        "title": "Database selection",
        "choice": "PostgreSQL with pgvector",
        "rationale": "Need vector similarity search for AI features; pgvector avoids separate vector DB operational burden",
        "alternatives_rejected": ["Pinecone (vendor lock-in)", "Milvus (operational complexity)"],
        "timestamp": "2026-04-08T14:30:00Z"
      }
    ],
    "deliverables": [
      { "id": "DEL-001", "phase": 1, "name": "Requirements Document", "path": "docs/requirements.md", "status": "complete", "produced_at": "2026-04-04T16:00:00Z" },
      { "id": "DEL-002", "phase": 2, "name": "Architecture Decision Records", "path": "docs/adr/", "status": "complete", "produced_at": "2026-04-11T12:00:00Z" }
    ],
    "constraints": [
      { "id": "CON-001", "phase": 1, "description": "Must integrate with existing Oracle EBS via REST — no direct DB access", "source": "technical", "impacts_phases": [4, 5] }
    ],
    "risks": [
      { "id": "RSK-001", "phase": 2, "description": "pgvector performance at >10M vectors is unproven for our query patterns", "likelihood": "medium", "impact": "high", "mitigation": "Benchmark with synthetic 10M dataset in Phase 3", "status": "open" }
    ]
  },
  "compliance_frameworks": ["soc2", "gdpr"],
  "metadata": {
    "created_at": "2026-04-01T09:00:00Z",
    "last_modified": "2026-04-13T09:00:00Z",
    "version": 14
  }
}
```

### Skill: `tvt-dev-phase`

**Purpose:** Manage project phase lifecycle — initialize, advance, rewind, query status. Enforces quality gates before phase advancement.

```yaml
---
name: tvt-dev-phase
description: Project phase state machine — track, advance, and enforce lifecycle
allowed-tools: Read, Write, Edit, Bash(jq)
trigger_phrase: /phase
---
```

**Modes:**

| Mode | Trigger | Behavior |
|------|---------|----------|
| `init` | `/phase init <methodology>` | Create `project-state.json` with methodology preset, all phases pending, phase 1 active |
| `status` | `/phase` or `/phase status` | Display current phase, days in phase, quality gates passed, recent context entries |
| `advance` | `/phase advance` | Run quality gate check → if pass, advance to next phase → update timestamps |
| `rewind` | `/phase rewind [N]` | Move back to phase N (preserves context store, marks later phases as pending) |

**`init` mode:**

1. Validate `<methodology>` is one of: `greenfield`, `legacy-modernization`, `microservices`, `ml-data-science`, `cloud-migration`, `api-platform`
2. Check if `project-state.json` already exists — if yes, confirm overwrite
3. Infer `project` name from directory name or `package.json` name field
4. Write `project-state.json` with:
   - All 7 phases initialized (names vary by methodology)
   - Phase 1 set to `active`, rest `pending`
   - Empty context store arrays
   - `compliance_frameworks` prompted from user or empty
5. Output: "Initialized {project} with {methodology} methodology at Phase 1: {phase_name}"

**`status` mode:**

```
Project: acme-platform
Methodology: greenfield
Phase: 3/7 — Foundation (active 4 days)
Gates passed: [1] Discovery ✓  [2] Architecture ✓
Context: 1 decision, 2 deliverables, 1 constraint, 1 risk
Next gate: Foundation quality gate (see /phase advance --dry-run)
```

**`advance` mode:**

1. Load `project-state.json`
2. Load quality gate for current phase from phase-rules (see § Phase Rules + Quality Gates)
3. Check each gate criterion against context store deliverables:
   - Each criterion maps to a deliverable ID pattern or file existence check
   - Gate passes only if ALL criteria are satisfied (binary pass/fail)
4. If gate fails: output which criteria are unmet, do NOT advance
5. If gate passes: mark current phase `completed` with timestamp, advance `current_phase`, mark next phase `active`, update `phase_entered`
6. Write updated `project-state.json`
7. Output: "Advanced to Phase {N}: {name}. Quality gate for Phase {N-1} passed."

**`rewind` mode:**

1. Validate target phase < current_phase
2. Mark all phases > target as `pending` (clear their timestamps)
3. Mark target phase as `active`, update `phase_entered` to now
4. Preserve ALL context store entries (decisions/deliverables are historical record)
5. Remove target phase and later from `quality_gates_passed`
6. Output: "Rewound to Phase {N}: {name}. Context store preserved. Quality gates {N}+ cleared."

### Hook: `inject-context.sh` (Updated)

**Event:** `SessionStart` (fires once when Claude session begins)

**Purpose:** Read `project-state.json` and inject phase-specific rules into Claude's context via `additionalContext`.

```bash
#!/bin/bash
# inject-context.sh — SessionStart hook
# Reads project-state.json and injects phase-aware context

STATE_FILE="project-state.json"

if [ ! -f "$STATE_FILE" ]; then
  echo '{}' # No state file, no injection
  exit 0
fi

PHASE=$(jq -r '.current_phase' "$STATE_FILE")
METHODOLOGY=$(jq -r '.methodology' "$STATE_FILE")
PROJECT=$(jq -r '.project' "$STATE_FILE")
FRAMEWORKS=$(jq -r '.compliance_frameworks // [] | join(", ")' "$STATE_FILE")
DECISIONS=$(jq -r '.context_store.decisions | length' "$STATE_FILE")
DELIVERABLES=$(jq -r '.context_store.deliverables | length' "$STATE_FILE")
CONSTRAINTS=$(jq -r '[.context_store.constraints[] | select(.impacts_phases | contains(['"$PHASE"']))] | length' "$STATE_FILE")

# Load phase rules
RULES_FILE=".claude/methodology/phase-rules/0${PHASE}-*.rules.md"
RULES=""
if ls $RULES_FILE 1>/dev/null 2>&1; then
  RULES=$(cat $RULES_FILE)
fi

# Load methodology specialization
SPEC_FILE=".claude/methodology/specializations/${METHODOLOGY}.md"
SPEC=""
if [ -f "$SPEC_FILE" ]; then
  SPEC=$(cat "$SPEC_FILE")
fi

# Load relevant constraints for this phase
PHASE_CONSTRAINTS=$(jq -r '[.context_store.constraints[] | select(.impacts_phases | contains(['"$PHASE"']))] | map("- " + .description) | join("\n")' "$STATE_FILE")

# Build context injection
cat <<EOF
{
  "additionalContext": "## Project Context (Auto-Injected)\n\n**Project:** ${PROJECT} | **Phase:** ${PHASE}/7 | **Methodology:** ${METHODOLOGY}\n**Compliance:** ${FRAMEWORKS:-none}\n**Context store:** ${DECISIONS} decisions, ${DELIVERABLES} deliverables\n\n### Active Constraints for This Phase\n${PHASE_CONSTRAINTS:-None}\n\n### Phase Rules\n${RULES}\n\n### Methodology Notes\n${SPEC}"
}
EOF
```

**Hook registration in `settings.json`:**
```json
{
  "hooks": {
    "SessionStart": [
      {
        "type": "command",
        "command": ".claude/hooks/inject-context.sh"
      }
    ]
  }
}
```

### Context Store Operations

Skills interact with the context store through `project-state.json` read/write:

**Writing to context store** (any skill can append):
```bash
# Add a decision
jq '.context_store.decisions += [{"id":"DEC-003","phase":3,"title":"Auth library","choice":"Auth.js v5","rationale":"Native Next.js integration, OIDC support","alternatives_rejected":["Clerk (cost)","custom (time)"],"timestamp":"2026-04-14T10:00:00Z"}]' \
  project-state.json > tmp.json && mv tmp.json project-state.json
```

**Reading from context store** (later phases reference earlier outputs):
```bash
# Get all deliverables from prior phases
jq '[.context_store.deliverables[] | select(.phase < .current_phase)]' project-state.json

# Get constraints affecting current phase
jq '[.context_store.constraints[] | select(.impacts_phases | contains([3]))]' project-state.json
```

---

## Universal Prompt Pattern Library

Instead of 180+ verbose prompt templates, TVT-SDLC uses **12 universal patterns** — concise, composable, and variable-injected from the context store. Each pattern is ≤50 lines, methodology-agnostic, and combinable with specialization overlays.

### Design Principles

1. Each pattern ≤50 lines — concise enough to vectorize/embed for RAG
2. Variables injected from `project-state.json` context store at runtime
3. Patterns compose: universal pattern + specialization overlay + phase rules
4. Every pattern has: purpose, inputs, process, output format, anti-patterns
5. Patterns are methodology-agnostic — specializations modify them

### Pattern: Requirements Gathering

```markdown
# Pattern: requirements-gathering

## Purpose
Elicit, structure, and validate requirements from stakeholders or source material.

## Inputs
- {{source}} — stakeholder interview, document, ticket, or brief
- {{methodology}} — determines depth and format
- {{compliance_frameworks}} — triggers regulatory requirement capture
- {{prior_deliverables}} — existing docs to avoid duplication

## Process
1. Extract functional requirements as user stories (Given/When/Then)
2. Extract non-functional requirements (performance, security, scalability, compliance)
3. Identify assumptions — mark each with confidence level (high/medium/low)
4. Map dependencies between requirements
5. Flag requirements that conflict with existing constraints in context store
6. If compliance_frameworks present: add regulatory requirements section

## Output Format
- requirements.md with numbered items (REQ-001, REQ-002...)
- Each requirement: description, priority (must/should/could), source, acceptance criteria
- Assumptions section with confidence levels
- Dependencies graph (text-based)

## Anti-Patterns
- DON'T generate requirements without a source — every requirement traces to input
- DON'T mix solution design into requirements — requirements say WHAT, not HOW
- DON'T omit acceptance criteria — untestable requirements are not requirements
```

### Pattern: Architecture Decision

```markdown
# Pattern: architecture-decision

## Purpose
Evaluate architectural options and produce a decision record (ADR) with clear rationale.

## Inputs
- {{decision_title}} — what is being decided
- {{constraints}} — from context store constraints array
- {{prior_decisions}} — from context store decisions array
- {{compliance_frameworks}} — regulatory requirements that constrain choices
- {{tech_stack}} — language/framework context

## Process
1. State the problem and why a decision is needed now
2. List 2-4 viable options (no strawmen)
3. Evaluate each against: constraints, prior decisions, compliance, team capability, operational cost
4. Recommend one option with explicit rationale
5. Document consequences (positive and negative) of the choice
6. Record in context store as new decision entry

## Output Format
- ADR following Michael Nygard template: Title, Status, Context, Decision, Consequences
- Decision ID (DEC-NNN) for context store
- Alternatives rejected with one-line reason each

## Anti-Patterns
- DON'T present a single option as a "decision" — minimum 2 real alternatives
- DON'T decide without referencing constraints — every ADR cites relevant CON-NNN entries
- DON'T ignore compliance — if frameworks are active, every ADR addresses them
```

### Pattern: Implementation Scaffold

```markdown
# Pattern: implementation-scaffold

## Purpose
Generate initial code structure for a feature based on architecture decisions and requirements.

## Inputs
- {{feature_name}} — what is being built
- {{requirements}} — relevant REQ-NNN entries
- {{architecture_decisions}} — relevant DEC-NNN entries
- {{tech_stack}} — language, framework, patterns
- {{compliance_frameworks}} — security controls to embed

## Process
1. Map requirements to components/modules
2. Apply architecture decisions (patterns, boundaries, data flow)
3. Generate file structure with module boundaries
4. Write interface/type definitions first (contracts before implementation)
5. Add compliance controls inline (input validation, auth checks, audit logging)
6. Generate placeholder test files mirroring source structure

## Output Format
- File tree showing new/modified files
- Interface definitions and type contracts
- Implementation stubs with TODO markers for business logic
- Test file stubs with describe blocks matching source modules

## Anti-Patterns
- DON'T implement business logic in scaffold — interfaces and structure only
- DON'T skip compliance controls — they are part of the scaffold, not added later
- DON'T create files without corresponding test stubs
```

### Pattern: Test Strategy

```markdown
# Pattern: test-strategy

## Purpose
Design a testing approach that validates requirements and catches regressions.

## Inputs
- {{feature_name}} — what is being tested
- {{requirements}} — REQ-NNN entries with acceptance criteria
- {{architecture}} — component boundaries determine test boundaries
- {{compliance_frameworks}} — mandated testing (penetration, data validation)
- {{risk_level}} — from context store risks

## Process
1. Map each requirement's acceptance criteria to test cases
2. Classify tests: unit (isolated logic), integration (component boundaries), e2e (user flows)
3. Identify edge cases from constraints and risks in context store
4. Add compliance-mandated tests (input validation, auth bypass, data leakage)
5. Define test data strategy (fixtures, factories, or seeded DB)
6. Specify coverage targets per component (critical path: 90%+, utilities: 70%+)

## Output Format
- Test plan document with: scope, approach, test types, coverage targets
- Test case matrix: requirement → test case → type → priority
- Test data requirements

## Anti-Patterns
- DON'T test implementation details — test behavior and contracts
- DON'T skip negative tests — invalid inputs, auth failures, network errors
- DON'T set uniform coverage targets — critical paths need higher coverage
```

### Pattern: Security Review

```markdown
# Pattern: security-review

## Purpose
Identify security vulnerabilities and verify compliance controls in code changes.

## Inputs
- {{code_changes}} — diff or file paths under review
- {{compliance_frameworks}} — applicable framework controls
- {{prior_decisions}} — auth/crypto decisions from context store
- {{threat_model}} — if available from earlier phases

## Process
1. Scan for OWASP Top 10 vulnerabilities (injection, XSS, CSRF, SSRF, etc.)
2. Verify authentication/authorization on every endpoint or entry point
3. Check data handling: encryption at rest/transit, PII masking, retention
4. Verify input validation at system boundaries
5. Check secrets management (no hardcoded keys, proper env var usage)
6. Map findings to compliance control IDs if frameworks are active
7. Rate findings: Critical / High / Medium / Low

## Output Format
- Findings list: ID, severity, location (file:line), description, remediation
- Compliance mapping: finding → control ID → status (pass/fail)
- Summary: total findings by severity, blocking issues for phase advancement

## Anti-Patterns
- DON'T flag style issues as security findings
- DON'T report theoretical risks without a plausible attack vector
- DON'T skip compliance mapping when frameworks are configured
```

### Pattern: Integration Verification

```markdown
# Pattern: integration-verify

## Purpose
Verify that components integrate correctly across system boundaries.

## Inputs
- {{integration_points}} — APIs, queues, databases, external services
- {{contracts}} — interface definitions from architecture phase
- {{constraints}} — relevant CON-NNN entries (e.g., "no direct DB access")
- {{compliance_frameworks}} — data flow compliance requirements

## Process
1. List all integration boundaries (internal service-to-service, external APIs)
2. For each boundary: verify contract adherence (request/response schemas)
3. Test error propagation — failures at boundaries surface correctly
4. Verify timeout and retry behavior at each boundary
5. Check data transformation correctness (no silent data loss)
6. Validate compliance: data classification maintained across boundaries

## Output Format
- Integration matrix: component A → component B → contract → status
- Failed integrations with root cause and fix recommendation
- Data flow diagram showing classification labels at each hop

## Anti-Patterns
- DON'T test integrations through mocks alone — at least one real integration test per boundary
- DON'T ignore error paths — happy path integration is insufficient
- DON'T skip data classification tracking across boundaries
```

### Pattern: Quality Gate Check

```markdown
# Pattern: quality-gate-check

## Purpose
Evaluate whether all exit criteria for the current phase are satisfied.

## Inputs
- {{current_phase}} — phase number being evaluated
- {{quality_gates}} — gate criteria from phase-rules
- {{context_store}} — accumulated deliverables, decisions, constraints
- {{compliance_frameworks}} — framework-specific gate requirements

## Process
1. Load quality gate criteria for current phase
2. For each criterion: check deliverable exists AND meets acceptance criteria
3. For compliance gates: verify all framework-mandated artifacts present
4. Calculate: gates_passed / total_gates
5. Binary result: ALL pass = PASS, any fail = FAIL (no partial credit)
6. List unmet criteria with specific remediation steps

## Output Format
- PASS or FAIL (binary, no percentage)
- Per-criterion: ✓ pass or ✗ fail with reason
- If FAIL: ordered remediation list (highest-priority gap first)

## Anti-Patterns
- DON'T allow partial pass — quality gates are binary
- DON'T use subjective criteria — every gate must be mechanically verifiable
- DON'T skip compliance gates even if all functional gates pass
```

### Pattern: Documentation Generate

```markdown
# Pattern: documentation-generate

## Purpose
Produce technical documentation that stays accurate by deriving from source code and decisions.

## Inputs
- {{doc_type}} — API reference, architecture overview, runbook, onboarding guide
- {{source_files}} — code/config files to document
- {{decisions}} — relevant DEC-NNN entries for rationale sections
- {{audience}} — developer, operator, stakeholder

## Process
1. Extract structure from source (endpoints, types, configs, commands)
2. Add context from architecture decisions (the WHY behind the WHAT)
3. Include operational information (how to run, deploy, troubleshoot)
4. Add examples derived from test cases (guaranteed to be valid)
5. Flag any sections that may become stale — add source reference

## Output Format
- Markdown document with clear headings
- Code examples that are copy-paste runnable
- Cross-references to ADRs and requirements by ID

## Anti-Patterns
- DON'T write documentation that duplicates source code comments
- DON'T include information that will become stale without a maintenance mechanism
- DON'T write for a generic audience — target the specified reader
```

### Pattern: Observability Setup

```markdown
# Pattern: observability-setup

## Purpose
Instrument application with metrics, traces, and logs for production visibility.

## Inputs
- {{tech_stack}} — determines instrumentation library
- {{critical_paths}} — from requirements (what MUST be monitored)
- {{compliance_frameworks}} — audit logging requirements
- {{sla_targets}} — latency, availability, error rate targets

## Process
1. Identify critical paths requiring instrumentation (from requirements)
2. Define metrics: request rate, error rate, latency (p50/p95/p99) per endpoint
3. Define trace spans: entry point → dependencies → response
4. Define structured log format with correlation IDs
5. Add compliance audit events (who did what, when, to which data)
6. Set alerting thresholds based on SLA targets

## Output Format
- Instrumentation code for critical paths
- Dashboard definition (metrics + thresholds)
- Alert rules (condition + severity + notification channel)
- Audit event schema

## Anti-Patterns
- DON'T instrument everything — focus on critical paths and boundaries
- DON'T log PII in plain text — compliance requires masking
- DON'T set alerts without defining who responds and how
```

### Pattern: Launch Readiness

```markdown
# Pattern: launch-readiness

## Purpose
Comprehensive pre-launch verification that all systems are production-ready.

## Inputs
- {{deliverables}} — all DEL-NNN from context store
- {{quality_gates_passed}} — phases 1-6 must all pass
- {{compliance_frameworks}} — final compliance attestation requirements
- {{risks}} — open risks from context store

## Process
1. Verify all phase quality gates passed (1-6)
2. Run final security scan (SAST, DAST, dependency audit)
3. Verify observability: dashboards, alerts, runbooks all in place
4. Run load test against production-equivalent environment
5. Verify rollback plan exists and has been tested
6. Complete compliance checklist (framework-specific)
7. Sign-off: technical lead, security, compliance (if applicable)

## Output Format
- Launch readiness report: GO / NO-GO with blockers list
- Risk acceptance log (open risks with stakeholder sign-off)
- Runbook link, rollback procedure, escalation contacts

## Anti-Patterns
- DON'T launch with open Critical or High security findings
- DON'T launch without tested rollback — "we can fix forward" is not a plan
- DON'T skip compliance sign-off — post-launch findings are 10x more expensive
```

### Pattern: Refactoring Plan

```markdown
# Pattern: refactoring-plan

## Purpose
Plan a safe refactoring that improves code quality without changing behavior.

## Inputs
- {{target_code}} — files or modules to refactor
- {{motivation}} — why refactor now (tech debt metric, upcoming feature needs it)
- {{constraints}} — what must NOT change (public APIs, data formats, behavior)
- {{test_coverage}} — existing coverage to rely on as safety net

## Process
1. Identify what's wrong (code smells, duplication, coupling, complexity metrics)
2. Define the target state (what good looks like after refactoring)
3. Plan incremental steps — each step produces a working, deployable state
4. Verify test coverage is sufficient as safety net (add characterization tests if not)
5. Define rollback point for each step
6. Estimate risk per step (low/medium/high based on scope of change)

## Output Format
- Step-by-step refactoring plan (ordered, each step is independently deployable)
- Risk assessment per step
- Required test additions before refactoring begins
- Behavior verification checklist (what to test after each step)

## Anti-Patterns
- DON'T refactor without tests — add characterization tests first
- DON'T combine refactoring with feature work in the same commit
- DON'T refactor "while you're in there" — scope is explicit and bounded
```

### Pattern: Incident Response

```markdown
# Pattern: incident-response

## Purpose
Structure incident investigation and resolution when production issues occur.

## Inputs
- {{symptoms}} — what's broken (errors, latency, data issues)
- {{affected_systems}} — from architecture documentation
- {{recent_changes}} — deployments, config changes, dependency updates
- {{sla_impact}} — is SLA at risk or breached

## Process
1. Triage: severity (SEV1-4) based on user impact and SLA status
2. Identify blast radius — which users/data/services affected
3. Correlate with recent changes (deploy? config? dependency?)
4. Form hypothesis → test → confirm or reject
5. Implement fix or rollback (whichever is faster to restore service)
6. Write timeline (what happened, when, what was done)
7. Identify follow-up actions (root cause fix, monitoring gap, process improvement)

## Output Format
- Incident report: severity, timeline, root cause, resolution, follow-ups
- Post-mortem action items with owners and due dates

## Anti-Patterns
- DON'T spend 30 minutes debugging before checking recent deployments
- DON'T fix root cause before restoring service (rollback first, fix second)
- DON'T skip the post-mortem — incidents without follow-ups recur
```

---

## Methodology Specializations

Thin overlays (≤30 lines each) that modify universal patterns for specific project contexts. Loaded based on `methodology` field in `project-state.json`. Specializations do NOT duplicate universal pattern content — they only add overrides and constraints.

### Specialization: Greenfield

```markdown
# Specialization: greenfield

## Pattern Overrides
- requirements-gathering: Include "market validation" step — confirm problem exists before building
- architecture-decision: Favor simplicity — choose boring technology unless complexity is justified
- implementation-scaffold: Start with monolith; extract services only when measured need arises
- test-strategy: TDD by default — write tests before implementation for all new code

## Phase-Specific Constraints
- Phase 1: Focus on user problem validation, not solution design
- Phase 2: Architecture must be deployable on day 1 — no "we'll figure out deployment later"
- Phase 3: Foundation includes CI/CD pipeline — not deferred to Phase 7
- Phase 4: Feature flags for all user-facing features — enable incremental rollout
```

### Specialization: Legacy Modernization

```markdown
# Specialization: legacy-modernization

## Pattern Overrides
- requirements-gathering: Add "current system archaeology" — document existing behavior before changing
- architecture-decision: Must evaluate strangler fig vs big bang — default to strangler fig
- implementation-scaffold: Always produce adapter/anti-corruption layer first
- test-strategy: Characterization tests for existing behavior before any modification
- refactoring-plan: REQUIRED before any code change — no direct modification without plan

## Phase-Specific Constraints
- Phase 1: READ-ONLY. No code changes. Catalog existing behavior, data flows, and integration points
- Phase 2: Architecture must preserve existing data contracts — breaking changes require explicit migration plan
- Phase 3: Anti-corruption layer is the first deliverable — isolates new from old
- Phase 4: Each change must maintain backward compatibility until cutover
```

### Specialization: Microservices

```markdown
# Specialization: microservices

## Pattern Overrides
- architecture-decision: Must define service boundaries using domain events (not CRUD entities)
- implementation-scaffold: Each service gets independent CI/CD, database, and deployment
- integration-verify: Contract testing (Pact/consumer-driven) mandatory at every service boundary
- observability-setup: Distributed tracing required — correlation ID propagated across all services
- test-strategy: Include chaos engineering (network partition, service unavailability) in Phase 6

## Phase-Specific Constraints
- Phase 2: Define domain boundaries BEFORE choosing communication protocol
- Phase 3: Service mesh or API gateway decision must be made — no point-to-point by default
- Phase 5: Integration testing includes failure modes (circuit breakers, retries, timeouts)
- Phase 6: Load test must verify cascading failure handling (one service down ≠ system down)
```

### Specialization: ML / Data Science

```markdown
# Specialization: ml-data-science

## Pattern Overrides
- requirements-gathering: Add "success metric definition" — what quantitative improvement justifies deployment
- architecture-decision: Must address model versioning, experiment tracking, and training/serving split
- implementation-scaffold: Separate training pipeline, serving infrastructure, and evaluation harness
- test-strategy: Add data validation tests (schema drift, distribution drift, missing values)
- observability-setup: Model performance metrics (accuracy, latency, drift) alongside system metrics

## Phase-Specific Constraints
- Phase 1: Define success metric with baseline measurement — no ML without measurable improvement target
- Phase 2: Training and serving are separate concerns — never couple them architecturally
- Phase 3: Experiment tracking infrastructure before any model training
- Phase 4: Every model change has an eval run — no deployment without measured improvement
- Phase 6: Include fairness/bias testing if model affects humans
```

### Specialization: Cloud Migration

```markdown
# Specialization: cloud-migration

## Pattern Overrides
- requirements-gathering: Add "current infrastructure audit" — document what exists and its cost
- architecture-decision: Evaluate lift-and-shift vs re-platform vs re-architect for each component
- implementation-scaffold: Infrastructure-as-Code (Terraform/Pulumi) is primary deliverable, not app code
- test-strategy: Include disaster recovery test and failover verification
- launch-readiness: Must include cost projection comparison (before vs after migration)

## Phase-Specific Constraints
- Phase 1: Complete infrastructure inventory with cost attribution
- Phase 2: Migration strategy per component (7R framework: retain, retire, relocate, rehost, repurchase, replatform, refactor)
- Phase 3: Landing zone with networking, IAM, and guardrails before any workload moves
- Phase 5: DNS/traffic cutover plan with rollback procedure
- Phase 7: 30-day parallel run before decommissioning source systems
```

### Specialization: API Platform

```markdown
# Specialization: api-platform

## Pattern Overrides
- requirements-gathering: Add "consumer interview" — understand API consumers' needs directly
- architecture-decision: Must address versioning strategy (URL path, header, content negotiation)
- implementation-scaffold: OpenAPI/AsyncAPI spec is primary artifact — generate code from spec
- test-strategy: Contract tests from consumer perspective; backward compatibility tests for every change
- documentation-generate: API docs auto-generated from spec — human-written guides for complex flows

## Phase-Specific Constraints
- Phase 1: Identify ALL consumers (internal + external) — missing a consumer = breaking change risk
- Phase 2: Versioning and deprecation policy decided before any endpoint is published
- Phase 3: API gateway with rate limiting, auth, and usage tracking from day 1
- Phase 4: Every endpoint has: OpenAPI spec, integration test, rate limit, error schema
- Phase 6: Backward compatibility verified — no breaking changes without major version bump
```

---

## Phase Rules + Quality Gates

Each phase has concrete DO/DON'T rules that constrain Claude's behavior and a measurable quality gate (binary pass/fail) that must clear before advancing to the next phase.

### Phase 1: Discovery

**Rules:**
- DO: Ask clarifying questions, document assumptions, identify stakeholders
- DO: Research existing systems, integrations, and constraints
- DO: Capture non-functional requirements (performance, security, compliance, scale)
- DO: Write requirements in Given/When/Then format with acceptance criteria
- DON'T: Write application source code
- DON'T: Make architecture decisions (database choice, framework selection)
- DON'T: Create project scaffolding, CI/CD pipelines, or infrastructure
- DON'T: Estimate effort or timelines (insufficient information)

**Quality Gate:**
| Criterion | Verification Method |
|-----------|-------------------|
| Requirements document exists | File exists: `docs/requirements.md` |
| ≥5 functional requirements with acceptance criteria | Parse requirements.md for REQ-NNN with Given/When/Then |
| ≥3 non-functional requirements captured | Check for performance/security/scalability sections |
| Stakeholder map documented | File exists: `docs/stakeholders.md` OR section in requirements |
| Compliance requirements identified (if frameworks configured) | Check compliance section populated |
| All requirements traceable to source | Every REQ-NNN has a `Source:` field |
| Context store updated | `project-state.json` has ≥1 constraint entry |

### Phase 2: Architecture

**Rules:**
- DO: Evaluate multiple options for every significant decision
- DO: Document decisions as ADRs with rationale and rejected alternatives
- DO: Reference Phase 1 requirements by ID in architecture justification
- DO: Address all constraints from context store
- DO: Consider compliance requirements in every structural decision
- DON'T: Write application code (prototyping for validation is OK with explicit label)
- DON'T: Make decisions without referencing requirements (no "resume-driven development")
- DON'T: Choose technology without evaluating at least one alternative
- DON'T: Defer security architecture to later phases

**Quality Gate:**
| Criterion | Verification Method |
|-----------|-------------------|
| ≥3 ADRs documented | Count DEC-NNN entries in context store ≥3 |
| Architecture diagram exists | File exists: `docs/architecture.md` or `docs/ARCHITECTURE.md` |
| Every ADR references ≥1 requirement | Each DEC-NNN cites REQ-NNN in rationale |
| Data model defined | File exists: `docs/data-model.*` or schema file |
| Security architecture addressed | DEC-NNN exists with "security" or "auth" in title |
| Compliance controls mapped (if frameworks active) | Compliance section in architecture doc populated |
| Integration points identified | Section listing external dependencies with contracts |

### Phase 3: Foundation

**Rules:**
- DO: Set up project structure, build system, CI/CD pipeline
- DO: Implement core infrastructure (database connections, auth framework, logging)
- DO: Write infrastructure-as-code for deployment
- DO: Establish testing patterns (unit, integration, e2e frameworks configured)
- DO: Implement security foundations (auth, secrets management, input validation patterns)
- DON'T: Implement business features (only infrastructure and patterns)
- DON'T: Skip CI/CD setup — it's not optional or deferrable
- DON'T: Create manual deployment processes
- DON'T: Write tests without assertions (no empty test stubs counting as "done")

**Quality Gate:**
| Criterion | Verification Method |
|-----------|-------------------|
| CI pipeline runs on push | `.github/workflows/ci.yml` or equivalent exists and passes |
| Build succeeds | `npm run build` / `cargo build` / equivalent exits 0 |
| Test framework configured with ≥1 passing test | Test command exits 0 with ≥1 test case |
| Database connection working | Integration test or health check validates DB connectivity |
| Auth scaffold in place | Auth middleware/route exists (even if only returns 401/403) |
| Linting configured and passing | Lint command exits 0 |
| Deployment to staging works | Deploy script/workflow exists and has been executed once |
| Observability foundations | Structured logging configured; health endpoint responds |

### Phase 4: Implementation

**Rules:**
- DO: Implement features against requirements (reference REQ-NNN)
- DO: Write tests alongside implementation (not after)
- DO: Follow architecture decisions from Phase 2 (reference DEC-NNN)
- DO: Apply compliance controls as features are built (not bolted on later)
- DO: Keep commits atomic — one feature or fix per commit
- DON'T: Refactor architecture decisions without a new ADR
- DON'T: Skip input validation at system boundaries
- DON'T: Implement without tests (minimum: happy path + one error path per endpoint)
- DON'T: Introduce dependencies not evaluated in Phase 2

**Quality Gate:**
| Criterion | Verification Method |
|-----------|-------------------|
| All must-priority requirements implemented | REQ-NNN entries marked "must" have corresponding code |
| Test coverage ≥80% on critical paths | Coverage report on `src/domain/` or equivalent |
| No Critical/High security findings | Security scan (SAST) reports 0 Critical, 0 High |
| All endpoints have input validation | Each route/controller validates input schema |
| CI passes on all feature branches | CI status green for last 5 merges |
| API documentation matches implementation | OpenAPI spec (if applicable) matches actual responses |
| Feature flags for user-facing features (if greenfield) | Feature flag config exists |

### Phase 5: Integration

**Rules:**
- DO: Test all integration boundaries (service-to-service, external APIs, databases)
- DO: Verify error handling at every boundary (timeouts, retries, circuit breakers)
- DO: Validate data contracts between systems
- DO: Test with realistic data volumes
- DO: Verify compliance at data flow boundaries (classification, encryption, consent)
- DON'T: Test integrations only with mocks — at least one real integration test per boundary
- DON'T: Ignore error paths (network failures, timeouts, malformed responses)
- DON'T: Skip backward compatibility verification when integrating with existing systems
- DON'T: Defer security hardening (rate limiting, auth checks on all external-facing endpoints)

**Quality Gate:**
| Criterion | Verification Method |
|-----------|-------------------|
| Integration tests pass for all external boundaries | Integration test suite exits 0 |
| Error handling verified at each boundary | Tests cover timeout, 4xx, 5xx scenarios per integration |
| Contract tests pass (if microservices) | Pact/contract test suite exits 0 |
| Rate limiting active on external-facing endpoints | Test shows 429 response on limit breach |
| Data flows comply with classification requirements | Data flow diagram shows encryption/masking at boundaries |
| No direct database access across service boundaries | Architecture review confirms no cross-service DB queries |
| Retry/circuit-breaker behavior verified | Tests demonstrate graceful degradation |

### Phase 6: Testing & QA

**Rules:**
- DO: Run full regression suite (unit + integration + e2e)
- DO: Perform load testing against production-equivalent environment
- DO: Execute security testing (SAST, DAST, dependency audit)
- DO: Validate accessibility requirements (if applicable)
- DO: Run compliance verification (all framework checklists)
- DO: Test rollback procedures
- DON'T: Accept "works on my machine" — tests run in CI environment
- DON'T: Skip load testing ("we'll monitor in production")
- DON'T: Mark security findings as "won't fix" without explicit risk acceptance
- DON'T: Test only happy paths — include chaos/failure scenarios

**Quality Gate:**
| Criterion | Verification Method |
|-----------|-------------------|
| All test suites pass (unit, integration, e2e) | CI pipeline all-green |
| Load test meets SLA targets | p95 latency < target, error rate < target under expected load |
| 0 Critical + 0 High security findings | SAST + DAST + dependency scan reports |
| Compliance checklist complete (if frameworks active) | All controls verified with evidence |
| Rollback tested successfully | Rollback procedure executed and verified in staging |
| Performance regression: none | Current metrics ≤ baseline (no degradation) |
| Accessibility pass (if applicable) | WCAG 2.1 AA automated checks pass |

### Phase 7: Launch

**Rules:**
- DO: Execute launch readiness checklist (all previous gates MUST have passed)
- DO: Verify monitoring and alerting is active before launch
- DO: Confirm runbooks exist for known failure modes
- DO: Execute gradual rollout (canary → percentage → full)
- DO: Monitor key metrics for 24 hours post-launch
- DO: Document any open risks with explicit stakeholder acceptance
- DON'T: Launch with any Phase 6 quality gate failure unresolved
- DON'T: Launch without rollback plan tested in staging
- DON'T: Launch without on-call rotation and escalation path defined
- DON'T: Declare "done" before 24-hour stability period completes

**Quality Gate:**
| Criterion | Verification Method |
|-----------|-------------------|
| All previous phase gates passed (1-6) | `quality_gates_passed` contains [1,2,3,4,5,6] |
| Monitoring dashboards active with data flowing | Dashboard URL accessible, showing live metrics |
| Runbooks exist for top 5 failure modes | Files exist in `docs/runbooks/` |
| Rollback procedure documented and tested | Rollback executed successfully in staging within last 7 days |
| On-call rotation defined | PagerDuty/Opsgenie schedule configured |
| Stakeholder sign-off obtained | Approval recorded (PR comment, email, or signed document) |
| 24-hour stability after launch | No SEV1/SEV2 incidents in first 24 hours |

---

## Compliance-as-Code Engine

Six compliance frameworks mapped to concrete development controls. Controls are deduplicated — shared controls (access, encryption, audit) appear once and map to multiple frameworks. The engine integrates into hooks (block non-compliant patterns), quality gates (4th evaluation dimension), and PR templates.

### Framework → Development Control Mapping

#### SOC 2 (Trust Service Criteria)

| Control ID | Criterion | Development Control | Enforcement Point |
|-----------|-----------|-------------------|-------------------|
| CC6.1 | Logical access security | RBAC on repositories + pipelines; MFA on all dev accounts; network segmentation between environments | Hook: `PreToolUse` blocks deploy without RBAC evidence |
| CC6.3 | Access provisioned/deprovisioned | Quarterly access reviews; offboarding removes all access within 24h; no shared accounts | Quality gate: Phase 7 |
| CC7.1 | Configuration change detection | IaC drift detection; pipeline config monitoring; file integrity monitoring on production | Hook: `PostToolUse` logs all config changes |
| CC8.1 | Change authorization + implementation | Mandatory code review; approval workflows; deployment gates; automated testing; rollback capability; segregation of duties (author ≠ approver ≠ deployer) | Hook: `PreToolUse` blocks merge without review; Quality gate: all phases |
| CC8.2 | Code review and testing | Peer review required on all PRs; CI passes before merge; coverage thresholds enforced | PR template checklist |
| CC9.1 | Risk mitigation / vulnerability management | Dependency scanning (SCA); SAST on every PR; monthly vulnerability scans; CVSS-based prioritization | Hook: blocks merge with Critical/High findings |

#### HIPAA (Security Rule — 45 CFR § 164.312)

| Control ID | Requirement | Development Control | Enforcement Point |
|-----------|-------------|-------------------|-------------------|
| §164.312(a)(1) | Access control | Unique user IDs; no shared accounts; RBAC on all systems containing ePHI; emergency access procedure documented | Quality gate: Phase 3 |
| §164.312(a)(2)(iv) | Encryption and decryption | AES-256 at rest; TLS 1.2+ in transit; key management via HSM or vault; no plaintext ePHI in logs | Hook: blocks code containing plaintext health data patterns |
| §164.312(b) | Audit controls | All ePHI access logged (who, what, when); log retention ≥6 years; tamper-evident storage; regular log review | Quality gate: Phase 5 |
| §164.312(c)(1) | Integrity | Data validation on all ePHI inputs; checksums on stored data; backup verification | Quality gate: Phase 6 |
| §164.312(d) | Person/entity authentication | MFA required; session timeout ≤15 min; identity verification before ePHI access | Hook: blocks auth implementation without MFA |
| §164.312(e)(1) | Transmission security | TLS 1.2+ enforced; HSTS headers; no HTTP endpoints; encrypted internal service communication | Hook: blocks non-HTTPS endpoint creation |

#### PCI-DSS v4.0 (Requirement 6)

| Control ID | Requirement | Development Control | Enforcement Point |
|-----------|-------------|-------------------|-------------------|
| 6.1 | Processes defined and understood | Documented SDLC with security integrated; roles and responsibilities assigned | Quality gate: Phase 1 |
| 6.2.1 | Secure development practices | OWASP/SANS secure coding guidelines followed; industry best practices applied | Phase rules: all implementation phases |
| 6.2.2 | Developer training | Secure coding training annually; training records maintained | Quality gate: Phase 1 (team readiness) |
| 6.2.3 | Code review before release | All code reviewed (manual + automated SAST); review confirms secure coding compliance | Hook: blocks merge without review + SAST pass |
| 6.2.4 | Prevent common attacks | Input validation (SQL injection, XSS, CSRF, SSRF); output encoding; parameterized queries | Hook: SAST rules for OWASP Top 10 |
| 6.3.1 | Vulnerability identification | Monitor CVE feeds; CVSS-based risk ranking; track all findings to resolution | Quality gate: Phase 6 |
| 6.3.3 | Patch critical vulnerabilities | Critical (CVSS ≥9.0): 30 days; High (7.0-8.9): 90 days; documented risk acceptance for exceptions | Hook: dependency scan blocks outdated critical deps |
| 6.4.1 | Protect public-facing web apps | Annual application security assessment; WAF or equivalent; DAST scanning | Quality gate: Phase 6 |
| 6.5.1 | Change management | Change tickets with risk assessment; rollback plans; pre/post vulnerability scans; CAB approval | Hook: blocks deploy without change ticket reference |
| 6.5.3 | Environment separation | Dev/test/prod separated with access controls; no production data in lower environments | Quality gate: Phase 3 |
| 6.5.4 | Role separation | Developer ≠ deployer; reviewed and approved changes only reach production | Hook: enforces segregation in deploy pipeline |

#### GDPR (Articles 25, 32, 35)

| Control ID | Requirement | Development Control | Enforcement Point |
|-----------|-------------|-------------------|-------------------|
| Art. 25(1) | Data protection by design | Privacy impact assessment at design phase; data minimization in schema design; pseudonymization where possible; purpose limitation enforced in code | Quality gate: Phase 2 |
| Art. 25(2) | Data protection by default | Minimum data collection by default; no PII accessible without explicit user action; consent management built-in; data not shared without opt-in | Phase rules: Phase 4 |
| Art. 32(1)(a) | Pseudonymization + encryption | Personal data pseudonymized where feasible; AES-256 encryption at rest; TLS 1.2+ in transit; key rotation policy | Hook: blocks storing PII without encryption layer |
| Art. 32(1)(b) | Confidentiality, integrity, availability | Access controls, input validation, backup/restore procedures, uptime monitoring | Quality gate: Phase 5 |
| Art. 32(1)(c) | Restore availability after incident | Disaster recovery plan; RTO/RPO defined; backup restoration tested | Quality gate: Phase 6 |
| Art. 32(1)(d) | Regular testing of measures | Penetration testing; security assessment; control effectiveness review | Quality gate: Phase 6 |
| Art. 35 | Data Protection Impact Assessment | DPIA for high-risk processing; documented risk assessment; mitigation measures identified | Quality gate: Phase 1 (if high-risk data) |

#### SOX (Section 404 — IT General Controls)

| Control ID | Requirement | Development Control | Enforcement Point |
|-----------|-------------|-------------------|-------------------|
| ITGC-AM-1 | User authentication | MFA on all financial systems; strong password policy; no shared accounts | Quality gate: Phase 3 |
| ITGC-AM-2 | Role-based access control | RBAC with least privilege; documented role-permission mapping; formal access request process | Quality gate: Phase 3 |
| ITGC-AM-3 | Access reviews | Quarterly access reviews; prompt deprovisioning on role change/termination; documented evidence | Quality gate: Phase 7 |
| ITGC-AM-4 | Segregation of duties | No single person: initiate + approve + deploy; SoD matrix documented and enforced technically | Hook: enforces author ≠ approver in pipeline |
| ITGC-CM-1 | Change approval process | Formal change request → CAB approval → test → deploy; documented at every step | Hook: blocks deploy without approval reference |
| ITGC-CM-2 | Testing before production | All changes tested in non-production; test evidence documented; no direct production changes | Quality gate: Phase 4+ |
| ITGC-CM-3 | Documentation + version control | Complete audit trail: who changed what, when, why; version control on all code + config | Hook: `PostToolUse` logs all changes |
| ITGC-CM-4 | Emergency change process | Documented emergency procedure; post-hoc approval required; logged same as normal changes | Phase rules: documented in Phase 7 runbooks |
| ITGC-SD-1 | System development controls | SDLC documented; security integrated; changes validated before production | Quality gate: Phase 1 |

#### ISO 27001:2022 (Annex A — Technological Controls)

| Control ID | Requirement | Development Control | Enforcement Point |
|-----------|-------------|-------------------|-------------------|
| A.8.25 | Secure development lifecycle | SDLC with security at every phase; separate dev/test/prod; secure coding guidelines per language; security checkpoints at milestones | Quality gate: Phase 1 (SDLC defined) |
| A.8.26 | Application security requirements | Security requirements captured at design; documented in user stories/specs; management approval before development | Quality gate: Phase 2 |
| A.8.27 | Secure system architecture | Engineering principles documented; threat modeling performed; defense-in-depth applied; minimal attack surface | Quality gate: Phase 2 |
| A.8.28 | Secure coding | Secure coding guidelines per language; OWASP compliance; input validation; output encoding; no hardcoded secrets; code review for security | Hook: SAST enforcement; blocks hardcoded secrets |
| A.8.29 | Security testing | SAST + DAST + penetration testing; testing at development and acceptance phases; findings remediated before release | Quality gate: Phase 6 |
| A.8.30 | Outsourced development | Supplier security requirements documented; compliance verified; contractual obligations for secure development | Quality gate: Phase 1 (if outsourced) |
| A.8.31 | Separation of environments | Dev/test/prod isolated; access controls between environments; no production data in dev/test without masking | Quality gate: Phase 3 |
| A.8.33 | Test information | Test data does not contain production PII; data masking/anonymization for test environments; test data lifecycle managed | Hook: blocks copying production data to lower envs |

### Shared Controls (Deduplicated)

Controls that appear across multiple frameworks are implemented once and mapped to all applicable frameworks:

| Shared Control | Frameworks | Implementation |
|---------------|-----------|----------------|
| **Access Control (RBAC + MFA)** | SOC2 CC6.1, HIPAA §164.312(a), PCI-DSS 6.5.4, SOX ITGC-AM-1/2, ISO A.8.31 | Single IAM configuration; RBAC matrix; MFA enforcement |
| **Encryption (at-rest + in-transit)** | SOC2 CC6.1, HIPAA §164.312(a)(2)(iv)/§164.312(e), PCI-DSS 6.2.4, GDPR Art.32(1)(a), ISO A.8.28 | TLS 1.2+ everywhere; AES-256 at rest; key management via vault |
| **Audit Logging** | SOC2 CC7.1, HIPAA §164.312(b), SOX ITGC-CM-3, ISO A.8.25 | Structured logging; immutable log storage; retention per strictest framework |
| **Change Management** | SOC2 CC8.1, PCI-DSS 6.5.1, SOX ITGC-CM-1/2/3, ISO A.8.25 | PR-based workflow; mandatory review; approval gates; deployment audit trail |
| **Vulnerability Management** | SOC2 CC9.1, PCI-DSS 6.3.1/6.3.3, ISO A.8.29 | SCA + SAST + DAST; CVSS prioritization; SLA-based remediation |
| **Environment Separation** | PCI-DSS 6.5.3, SOX ITGC-CM-2, ISO A.8.31/A.8.33, GDPR Art.25 | Isolated environments; no prod data in dev; masked test data |
| **Segregation of Duties** | SOC2 CC8.1, PCI-DSS 6.5.4, SOX ITGC-AM-4 | Author ≠ reviewer ≠ deployer; technically enforced in pipeline |
| **Secure Coding Practices** | PCI-DSS 6.2.1/6.2.4, ISO A.8.28, HIPAA §164.312(c) | OWASP Top 10 prevention; input validation; parameterized queries; output encoding |

### Compliance Hook: `compliance-check.sh`

**Event:** `PreToolUse` (fires before file write, command execution)

```bash
#!/bin/bash
# compliance-check.sh — Block non-compliant patterns before they reach code
# Reads applicable frameworks from project-state.json

STATE_FILE="project-state.json"
if [ ! -f "$STATE_FILE" ]; then exit 0; fi

FRAMEWORKS=$(jq -r '.compliance_frameworks // [] | .[]' "$STATE_FILE")
if [ -z "$FRAMEWORKS" ]; then exit 0; fi

# Read tool input from stdin
INPUT=$(cat)
TOOL=$(echo "$INPUT" | jq -r '.tool_name // ""')
CONTENT=$(echo "$INPUT" | jq -r '.tool_input.content // .tool_input.command // ""')

VIOLATIONS=""

# Check for hardcoded secrets (all frameworks)
if echo "$CONTENT" | grep -qiE '(password|secret|api_key|token)\s*[:=]\s*["\x27][^"\x27]{8,}'; then
  VIOLATIONS="${VIOLATIONS}\n- BLOCKED: Hardcoded secret detected (SOC2 CC6.1, PCI-DSS 6.2.4, ISO A.8.28)"
fi

# Check for unencrypted PII patterns (HIPAA, GDPR)
if echo "$FRAMEWORKS" | grep -qE '(hipaa|gdpr)'; then
  if echo "$CONTENT" | grep -qiE '(ssn|social_security|date_of_birth|medical_record|diagnosis)' && \
     ! echo "$CONTENT" | grep -qiE '(encrypt|hash|mask|pseudonymize)'; then
    VIOLATIONS="${VIOLATIONS}\n- BLOCKED: Unprotected PII/PHI field (HIPAA §164.312(a)(2)(iv), GDPR Art.32(1)(a))"
  fi
fi

# Check for HTTP (non-HTTPS) endpoints (HIPAA, PCI-DSS)
if echo "$FRAMEWORKS" | grep -qE '(hipaa|pci-dss)'; then
  if echo "$CONTENT" | grep -qiE 'http://[^l][^o][^c]' 2>/dev/null; then
    VIOLATIONS="${VIOLATIONS}\n- BLOCKED: Non-HTTPS endpoint (HIPAA §164.312(e)(1), PCI-DSS 6.2.4)"
  fi
fi

# Check for direct production data copy (PCI-DSS, ISO, GDPR)
if echo "$FRAMEWORKS" | grep -qE '(pci-dss|iso27001|gdpr)'; then
  if echo "$CONTENT" | grep -qiE '(pg_dump|mysqldump|mongodump).*prod' && \
     echo "$CONTENT" | grep -qiE '(dev|test|staging|local)'; then
    VIOLATIONS="${VIOLATIONS}\n- BLOCKED: Production data copy to lower environment (PCI-DSS 6.5.3, ISO A.8.33, GDPR Art.25)"
  fi
fi

if [ -n "$VIOLATIONS" ]; then
  echo "{\"decision\": \"block\", \"reason\": \"Compliance violation(s) detected:${VIOLATIONS}\"}"
  exit 0
fi

echo '{}' # No violations — allow
exit 0
```

### Compliance Quality Gate Checklist

Added to each phase's quality gate when `compliance_frameworks` is non-empty in `project-state.json`:

| Phase | Compliance Gate Addition |
|-------|------------------------|
| 1 | SDLC documented with security integration (ISO A.8.25, PCI 6.1, SOX ITGC-SD-1) |
| 2 | Security requirements in architecture; DPIA if high-risk (GDPR Art.35, ISO A.8.26/A.8.27) |
| 3 | Environment separation verified; RBAC configured; encryption enabled (all frameworks) |
| 4 | Secure coding verified; no OWASP Top 10 in SAST; audit logging active (PCI 6.2, ISO A.8.28) |
| 5 | Integration compliance: data classification at boundaries; audit trail complete (HIPAA, SOC2) |
| 6 | Full security testing: SAST+DAST+SCA clean; penetration test (PCI 6.4.1, ISO A.8.29) |
| 7 | All framework checklists complete; evidence package assembled; sign-off recorded (all) |

### Eval Scoring: 4th Dimension — Compliance

`tvt-eval-score` adds compliance as a scoring dimension alongside correctness, quality, and security:

```json
{
  "dimensions": {
    "correctness": { "weight": 0.35 },
    "quality": { "weight": 0.25 },
    "security": { "weight": 0.20 },
    "compliance": { "weight": 0.20 }
  },
  "compliance_scoring": {
    "criteria": [
      { "id": "C1", "description": "No compliance hook violations triggered", "weight": 0.3 },
      { "id": "C2", "description": "Applicable framework controls addressed in code", "weight": 0.3 },
      { "id": "C3", "description": "Audit evidence generated (logs, documentation)", "weight": 0.2 },
      { "id": "C4", "description": "Data protection measures implemented (encryption, masking, minimization)", "weight": 0.2 }
    ]
  }
}
```

---

## Cross-Phase Continuity

The context store enables cross-phase continuity — later phases auto-reference earlier outputs, skills can read accumulated context, and phase advancement validates against accumulated deliverables.

### How Skills Interact with Context Store

Every skill can read from and write to the `context_store` in `project-state.json`:

**Reading (any skill, any phase):**
```bash
# Get all prior decisions relevant to current work
jq '.context_store.decisions[] | select(.title | test("auth|security"; "i"))' project-state.json

# Get constraints that affect the current phase
PHASE=$(jq '.current_phase' project-state.json)
jq --argjson p "$PHASE" '[.context_store.constraints[] | select(.impacts_phases | contains([$p]))]' project-state.json

# Get deliverables from prior phases
jq '[.context_store.deliverables[] | select(.phase < 4 and .status == "complete")]' project-state.json
```

**Writing (skills append after producing output):**
```bash
# Record a new decision
jq --arg ts "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  '.context_store.decisions += [{
    "id": "DEC-\(.context_store.decisions | length + 1 | tostring | ("000"[:-length] + .))",
    "phase": .current_phase,
    "title": "Authentication library",
    "choice": "Auth.js v5",
    "rationale": "Native Next.js integration and OIDC support",
    "alternatives_rejected": ["Clerk (cost)", "Custom (time)"],
    "timestamp": $ts
  }]' project-state.json > tmp.json && mv tmp.json project-state.json

# Record a new deliverable
jq --arg ts "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  '.context_store.deliverables += [{
    "id": "DEL-\(.context_store.deliverables | length + 1 | tostring | ("000"[:-length] + .))",
    "phase": .current_phase,
    "name": "API Design Document",
    "path": "docs/api-design.md",
    "status": "complete",
    "produced_at": $ts
  }]' project-state.json > tmp.json && mv tmp.json project-state.json
```

### Auto-Reference Pattern

When a skill invokes a universal pattern, the pattern resolver automatically injects relevant prior context:

1. **`inject-context.sh`** hook fires at SessionStart → injects phase + constraints + methodology
2. Skill loads pattern (e.g., `implementation-scaffold`)
3. Pattern has `{{prior_deliverables}}` variable → resolver queries context store for deliverables from earlier phases
4. Pattern has `{{constraints}}` variable → resolver queries constraints where `impacts_phases` includes current phase
5. Pattern has `{{prior_decisions}}` variable → resolver queries decisions from earlier phases
6. Claude receives: universal pattern + specialization overlay + phase rules + injected context from earlier phases

### Phase Advancement Validates Accumulation

`tvt-dev-phase advance` checks quality gates against the context store:

```
Phase 2 → 3 advancement requires:
  ✓ DEL-001 exists: Requirements Document (from Phase 1)
  ✓ DEC-001+ exists: ≥3 architecture decisions recorded
  ✓ CON-* checked: all Phase 1 constraints acknowledged in decisions
  ✗ FAIL if: 0 deliverables from Phase 2 in context store
```

### Context Store Version Control

Every write to `project-state.json` increments `metadata.version`. The file is committed to git alongside code, providing full history of decisions and deliverables. This means:

- `git log project-state.json` shows all context evolution
- `git diff` on the file shows exactly what changed between phases
- Rollback of a bad decision = `git revert` + `tvt-dev-phase rewind`
- No separate database or service needed — the state IS the file

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 0.7 | 2026-05-04 | **CodeForge-inspired methodology engine:** Added Phase State Machine + Context Store (complete JSON schema for `project-state.json`, `tvt-dev-phase` skill with 4 modes, updated `inject-context.sh` hook). Added Universal Prompt Pattern Library (12 patterns, each ≤50 lines, composable with variable injection). Added 6 Methodology Specializations (thin overlays ≤30 lines: greenfield, legacy-modernization, microservices, ml-data-science, cloud-migration, api-platform). Added Phase Rules + Quality Gates for all 7 phases (concrete DO/DON'T lists + measurable binary pass/fail gates). Added Compliance-as-Code Engine: 6 frameworks (SOC2 CC6-CC9, HIPAA §164.312, PCI-DSS v4.0 Req 6, GDPR Art.25/32/35, SOX Section 404 ITGCs, ISO 27001:2022 A.8.25-A.8.33) mapped to concrete development controls with actual control IDs. Shared controls deduplicated across frameworks. Added `compliance-check.sh` hook (PreToolUse blocker). Added compliance as 4th eval scoring dimension. Added Cross-Phase Continuity: context store read/write from skills, auto-reference pattern, phase advancement validates accumulation, version control via git. |
| 0.6 | 2026-05-04 | **Event completeness + blocking correction (final):** Fixed critical inaccuracy — `PostToolUse` is **non-blocking** (cannot use `decision: "block"`; can only inject context via `additionalContext` or replace output via `updatedToolOutput`). Moved `secret-scan.sh` from PostToolUse → PreToolUse (it must block before content is written). Added 11 missing hook events from official docs: `InstructionsLoaded`, `TaskCreated`, `TeammateIdle`, `CwdChanged`, `FileChanged`, `WorktreeCreate`, `WorktreeRemove`, `PostCompact`, `Elicitation`, `ElicitationResult`, `Notification` type matcher. Event table now shows all 31 official events across 7 cadences (was 19 across 3). Added 4 new hook fields: `async` (background execution via config, not stdout), `asyncRewake` (background + wake on exit 2), `shell` (bash/powershell choice), `once` (run once per session in skill hooks). Updated `notify-slack.sh` to use `async: true` config field instead of deprecated stdout JSON marker. Updated Decision Control section to clarify PostToolUse cannot block. |
| 0.5 | 2026-05-04 | **Hooks accuracy + Dashboard + Skills expansion:** Corrected `mcp_tool` hook type (DOES exist — was incorrectly denied in v0.3). Added complete Hook Field Reference table with all 7 fields (`type`, `command`/`url`, `timeout`, `if`, `statusMessage`, `headers`, `allowedEnvVars`). Clarified `if` field semantics — only evaluated on tool events, fires on too-complex-to-parse Bash as safe default. Added `http` hook example with auth headers. Added `mcp_tool` hook example for direct MCP invocation. Added `conventions-inject.sh` implementation (UserPromptSubmit hook). Added `.claude/conventions.md` pattern for per-prompt team reminders. Added `tvt-dev-standards` skill implementation (project bootstrap). Added complete Grafana/PromQL section (§5.7): 10 starter dashboard queries, 3 alert rules, OTel Collector config, Docker Compose stack, env vars, community dashboard reference. Documented Prometheus naming convention (`dot` → `underscore`). Added test cases for conventions-inject hook. |
| 0.4 | 2026-05-04 | **Observability deep dive:** Corrected span hierarchy to official `claude_code.interaction` root (not "Session"), added full span attributes table (ttft_ms, cache tokens, gen_ai.* semconv), added all privacy gates (OTEL_LOG_USER_PROMPTS, OTEL_LOG_TOOL_DETAILS, OTEL_LOG_TOOL_CONTENT, OTEL_LOG_RAW_API_BODIES), added metrics cardinality control, multi-team resource attributes, dynamic OTEL headers helper, mTLS auth option. Added `claude_code.commit.count` metric. Added 7 new events (tool_decision, permission_mode_changed, mcp_server_connection, api_retries_exhausted, at_mention, plugin_installed, api_request_body/response_body). Added Analytics Admin API as alternative to OTEL. Added TypeScript interfaces for EvalRecord, AuditRecord, and EvalConfig. Added audit log retention/rotation guidance. Added lint-changed.sh implementation. Added REVIEW.md template. Added `prompt.id` event correlation attribute. Added administrator managed policy config example. |
| 0.3 | 2026-05-04 | **Accuracy pass:** Fixed hooks JSON protocol (PostToolUse uses `inputs` plural, `response` not `tool_response`), corrected Stop hook continuation to use `decision: "block"` pattern, added `stop_hook_active` infinite loop prevention, added 5 missing events (TaskCompleted, SubagentStart, ConfigChange, PreCompact, SessionEnd "Can Block?" column), incorrectly removed `mcp_tool` type (corrected in v0.5), fixed model IDs to dated format (`claude-sonnet-4-6-20250514`), added async hooks pattern, added environment variables table, added all 7 Phase 1 script implementations (protect-files, secret-scan, auto-format, inject-context, eval-session, notify-slack, audit), corrected `trigger_phrase` as valid v1 input, added plugin distribution pattern, added skill supporting files pattern, added permission-mode and mcp-servers to frontmatter, added common pitfalls section |
| 0.2 | 2026-05-04 | Complete hooks protocol (JSON stdin/stdout, exit codes, all 15 events), SKILL.md frontmatter spec (14 fields), Phase 1 day-by-day plan with implementations, GitHub Actions v1 patterns, LLM-as-Judge rubric, design decisions, security model |
| 0.1 | 2026-05-04 | Initial specification — architecture, skill catalog, eval framework |

---

*TVT-SDLC is a Tavant AI Accelerator. Built on Claude Code's native extensibility.*
