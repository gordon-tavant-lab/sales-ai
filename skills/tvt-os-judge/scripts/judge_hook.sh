#!/usr/bin/env bash
# tvt-os-judge hook entrypoint
#
# Usage: judge_hook.sh <event_type>
#   event_type ∈ {post_tool_use, stop, subagent_stop}
#
# Reads JSON event payload from stdin (Claude Code convention).
# Decides whether to invoke tvt-os-judge based on:
#   - matched artifact paths (specs/, intel/tech/, ADRs.md, src/, etc.)
#   - debounce window (don't re-judge same file within 90s)
#   - g-dev-build state (Stop / SubagentStop gate when build is active)
#
# Returns JSON to stdout for blocking decisions, or just exits 0 for advisory.
#
# IMPORTANT: Do NOT use `exit 2` to block — see SKILL.md "Production scars".
# Use {"decision":"block","reason":"..."} JSON instead.

set -euo pipefail

EVENT_TYPE="${1:-unknown}"
WORKSPACE_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"
JUDGE_LOG_DIR="${WORKSPACE_DIR}/.claude-evals/judge"
PENDING_FILE="${JUDGE_LOG_DIR}/pending.jsonl"
DEBOUNCE_SECS=90
SESSION_CAP=20
BUILD_STATE_FILE="${WORKSPACE_DIR}/.specify/build-state.json"

mkdir -p "$JUDGE_LOG_DIR"
touch "$PENDING_FILE"

# Read event payload from stdin
EVENT_JSON="$(cat || echo '{}')"

# Stub: in v1.0 the judge is invoked manually by the user via /tvt-os-judge.
# This hook script records pending judgements and surfaces them in the next
# assistant turn (advisory mode for PostToolUse).
#
# Full automatic invocation requires either:
#   (a) The Claude Code Agent SDK callable from a shell script (planned v1.1)
#   (b) Anthropic API key configured + an HTTP call to a judge worker
#
# For v1.0, the hook only:
#   - Records "judgeable artifacts produced" to pending.jsonl
#   - On Stop hook: if pending file has entries, returns a JSON message asking
#     the next assistant turn to invoke /tvt-os-judge
#   - Never auto-blocks in v1.0 (manual /tvt-os-judge BLOCKs work fine)

case "$EVENT_TYPE" in
  post_tool_use)
    # Advisory only — log artifact for next-turn surfacing.
    # Parse tool name + file path from event JSON if possible.
    TOOL_NAME="$(echo "$EVENT_JSON" | python3 -c 'import sys, json; d=json.load(sys.stdin); print(d.get("tool_name",""))' 2>/dev/null || echo "")"
    FILE_PATH="$(echo "$EVENT_JSON" | python3 -c 'import sys, json; d=json.load(sys.stdin); print(d.get("tool_input",{}).get("file_path","") or d.get("tool_input",{}).get("path",""))' 2>/dev/null || echo "")"

    # Filter: only act on Write/Edit/MultiEdit
    if [[ "$TOOL_NAME" != "Write" && "$TOOL_NAME" != "Edit" && "$TOOL_NAME" != "MultiEdit" ]]; then
      exit 0
    fi

    # Filter: only judgeable paths
    if [[ -z "$FILE_PATH" ]]; then
      exit 0
    fi

    # Match include patterns
    case "$FILE_PATH" in
      *"specs/"*"/spec.md" | \
      *"specs/"*"/plan.md" | \
      *"specs/"*"/tasks.md" | \
      *"intel/tech/"*".md" | \
      *"/ADRs.md" | \
      *"/DESIGN_DOSSIER.md" | \
      *"/CLAUDE.md" | \
      *"/goal-weights.yaml" | \
      *".specify/memory/constitution.md")
        # Exclude judge's own research (prevent recursion)
        case "$FILE_PATH" in
          *"intel/tech/semantic_research/judge_"*) exit 0 ;;
          *".claude-evals/"*) exit 0 ;;
        esac

        # Debounce — skip if we've recorded this artifact in the last DEBOUNCE_SECS
        NOW="$(date +%s)"
        if [[ -s "$PENDING_FILE" ]]; then
          LAST_TS="$(grep -F "\"path\":\"$FILE_PATH\"" "$PENDING_FILE" 2>/dev/null | tail -1 | python3 -c 'import sys, json; line=sys.stdin.read().strip(); print(json.loads(line).get("ts",0)) if line else print(0)' 2>/dev/null || echo 0)"
          if (( NOW - LAST_TS < DEBOUNCE_SECS )); then
            exit 0
          fi
        fi

        # Session cap
        SESSION_COUNT="$(wc -l < "$PENDING_FILE" 2>/dev/null || echo 0)"
        if (( SESSION_COUNT >= SESSION_CAP )); then
          exit 0
        fi

        # Record the pending judgement
        echo "{\"ts\":$NOW,\"event\":\"post_tool_use\",\"path\":\"$FILE_PATH\",\"tool\":\"$TOOL_NAME\"}" >> "$PENDING_FILE"
        ;;
    esac
    exit 0
    ;;

  stop | subagent_stop)
    # On turn end: if pending judgements exist, surface a message to the next
    # assistant turn asking it to invoke /tvt-os-judge for the queued artifacts.
    if [[ -s "$PENDING_FILE" ]]; then
      # Build a compact summary of pending artifacts (unique paths only)
      PENDING_PATHS="$(python3 -c '
import json, sys
seen = set()
with open("'"$PENDING_FILE"'") as f:
    for line in f:
        try:
            d = json.loads(line)
            seen.add(d["path"])
        except Exception:
            continue
print("\n".join(sorted(seen)))
' 2>/dev/null || echo "")"

      if [[ -n "$PENDING_PATHS" ]]; then
        # Check if /g-dev-build is in flight (gate mode)
        GATE_MODE="false"
        if [[ -f "$BUILD_STATE_FILE" ]]; then
          GATE_MODE="$(python3 -c 'import json,sys; d=json.load(open("'"$BUILD_STATE_FILE"'")); print("true" if d.get("active",False) else "false")' 2>/dev/null || echo false)"
        fi

        # In v1.0 we do NOT auto-block from the shell hook (see SKILL.md).
        # We emit an additionalContext message so the next assistant turn
        # invokes /tvt-os-judge on the queued artifacts.
        REASON="tvt-os-judge: $(echo "$PENDING_PATHS" | wc -l | tr -d ' ') judgeable artifact(s) modified this turn. Recommended: /tvt-os-judge to review."

        cat <<EOF
{
  "decision": "approve",
  "reason": "$REASON",
  "additionalContext": "Artifacts pending judgement:\n$(echo "$PENDING_PATHS" | sed 's/^/  - /')\n\nGate mode active: $GATE_MODE\nInvoke /tvt-os-judge to review."
}
EOF

        # Rotate the pending file so we don't double-surface
        mv "$PENDING_FILE" "${PENDING_FILE}.$(date +%s).archived" 2>/dev/null || true
        touch "$PENDING_FILE"
      fi
    fi
    exit 0
    ;;

  *)
    # Unknown event type — be permissive
    exit 0
    ;;
esac
