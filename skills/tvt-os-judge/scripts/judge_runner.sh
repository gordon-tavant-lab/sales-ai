#!/usr/bin/env bash
# hook_id: gordon_os.judge_runner
#
# Per spec-006 FR-035 / FR-041 / D6:
# 4-axis judge invoked on Stop event. Composite ≥0.85 PASS, 0.70-0.85 WARN,
# <0.70 BLOCK (exit 2 to block, exit 0 to allow). Sync hook with 30s timeout +
# log+allow fallback (declared in plugin.json).
#
# Emits gordon_os.judge_score OTel attribute regardless of verdict.
#
# Per FR-030 (Q4 workspace-override semantics): self-check and defer if a
# workspace-level judge hook exists with matching hook_id.

set -euo pipefail

HOOK_ID="gordon_os.judge_runner"

# Workspace-override self-check (FR-030)
WORKSPACE_HOOKS_DIR="${CLAUDE_PROJECT_DIR:-${PWD}}/.claude/hooks"
if [[ -d "$WORKSPACE_HOOKS_DIR" ]]; then
  if grep -lrE "^# hook_id: ${HOOK_ID}$" "$WORKSPACE_HOOKS_DIR" >/dev/null 2>&1; then
    echo "[${HOOK_ID}] workspace override present; plugin hook deferring" >&2
    exit 0
  fi
fi

# v0.1 scaffold: CLAUDE_PLUGIN_ROOT unused today (no composed-skill lookup wired
# yet) — not hard-required, so this stub still runs under a zip-upload install.
# v0.1 scaffold: the judge runner ships as a stub that emits an info-level
# log + records a synthetic gordon_os.judge_score of 1.0. Full 4-axis
# scoring lives in the tvt-os-judge skill body, which gets populated at
# Phase D-eve per FR-051 (Q14 late snapshot). The actual judge logic
# composes tvt-core-eval + tvt-os-contrarian per the tvt-os-judge skill design.
#
# This stub establishes the hook plumbing without blocking the orchestration
# loop during Phase 2 / scaffold. Once Phase D-eve copies skill bodies,
# this script is replaced or augmented to invoke the judge skill directly
# via the claude CLI.

TRACES_DIR="${CLAUDE_PLUGIN_DATA:-${CLAUDE_PROJECT_DIR:-${PWD}}/.claude/state}/traces"
mkdir -p "$TRACES_DIR"

RUN_ID="${CLAUDE_SESSION_ID:-unknown}"
TIMESTAMP="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

cat >> "${TRACES_DIR}/${RUN_ID}.jsonl" <<EOF
{"timestamp": "${TIMESTAMP}", "attribute": "gordon_os.judge_score", "value": 1.0, "scope": "stop_hook", "hook": "${HOOK_ID}", "note": "v0.1 scaffold stub — full judge implementation lands at Phase D-eve"}
EOF

# Phase 2 scaffold default: allow (exit 0). Full BLOCK semantics (exit 2)
# go live when the tvt-os-judge skill body is copied at Phase D-eve.
exit 0
