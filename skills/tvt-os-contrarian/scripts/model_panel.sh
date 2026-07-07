#!/usr/bin/env bash
# model_panel.sh — fan a prompt out to a panel of DIFFERENT model families.
#
# The contrarian's keystone tool. Each provider answers INDEPENDENTLY (no
# cross-contamination) wearing a distinct expert persona, so the objections
# come from genuinely different minds — which is the only real defense against
# same-family self-preference (tvt-os-judge's #1 documented bias).
#
# Usage:
#   model_panel.sh --prompt "<the idea/claim to attack>" [options]
#   echo "<prompt>" | model_panel.sh --stdin
#
# Options:
#   --prompt TEXT     The idea/claim/artifact to interrogate (or --stdin).
#   --stdin           Read prompt from stdin.
#   --task TEXT       What each model should DO (default: adversarial critique).
#   --providers a,b   Comma list of provider ids to use (default: all enabled).
#   --personas a,b    Override persona assignment, positional to providers.
#   --probe           Only print which providers are reachable, then exit.
#   --timeout SEC     Per-provider timeout (default 60).
#   --out FILE        Write combined JSON here (default: stdout).
#
# Output: JSON array, one object per provider:
#   {id, family, persona, same_family, status: ok|skipped|error, latency_s, text, note}
#
# Design rules:
#   - NEVER fatal on a single provider failure. Skip + log, keep the panel alive.
#   - Parallel fan-out (background jobs), bounded by --timeout.
#   - Pure shell + curl + aws + python3 (for JSON). No pip installs.

set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REG="$HERE/providers.yml"

# Portable timeout: macOS lacks `timeout`; coreutils ships `gtimeout`. If neither
# exists, TO() runs the command unbounded (the AWS/curl client timeouts still cap it).
if command -v timeout >/dev/null 2>&1; then TO() { timeout "$@"; }
elif command -v gtimeout >/dev/null 2>&1; then TO() { gtimeout "$@"; }
else TO() { shift; "$@"; }   # drop the duration arg, run unbounded
fi

PROMPT=""; USE_STDIN=0; PROBE=0; TIMEOUT=60; OUT=""
TASK='Attack this idea. Give your 3 sharpest, most specific objections, the single most likely failure mode, and one piece of disconfirming evidence or a base rate that argues against it. Be concrete. If you would change your mind given new evidence, say what evidence. Do not be agreeable. Max 180 words.'
PROVIDERS_FILTER=""; PERSONAS_OVERRIDE=""

while [ $# -gt 0 ]; do
  case "$1" in
    --prompt) PROMPT="$2"; shift 2;;
    --stdin) USE_STDIN=1; shift;;
    --task) TASK="$2"; shift 2;;
    --providers) PROVIDERS_FILTER="$2"; shift 2;;
    --personas) PERSONAS_OVERRIDE="$2"; shift 2;;
    --probe) PROBE=1; shift;;
    --timeout) TIMEOUT="$2"; shift 2;;
    --out) OUT="$2"; shift 2;;
    *) echo "unknown arg: $1" >&2; exit 64;;
  esac
done

[ "$USE_STDIN" = 1 ] && PROMPT="$(cat)"
if [ "$PROBE" = 0 ] && [ -z "$PROMPT" ]; then
  echo "model_panel.sh: --prompt or --stdin required" >&2; exit 64
fi

# --- Parse providers.yml with python3 into a TSV the bash loop can read ------
# Columns: id  kind  model_id  family  region  aws_profile  api_key_env  persona  same_family  enabled
PARSED="$(python3 - "$REG" "$PROVIDERS_FILTER" "$PERSONAS_OVERRIDE" <<'PY'
import sys, re
reg, filt, pov = sys.argv[1], sys.argv[2], sys.argv[3]
try:
    import yaml  # noqa
    data = yaml.safe_load(open(reg))
except Exception:
    # minimal hand-parser fallback if pyyaml absent: not expected, but safe.
    data = None
if not data:
    sys.exit(0)
personas = data.get("personas", {})
want = [x.strip() for x in filt.split(",") if x.strip()] if filt else None
pov_list = [x.strip() for x in pov.split(",") if x.strip()] if pov else []
rows = []
for i, p in enumerate(data.get("providers", [])):
    if not p.get("enabled", False):
        continue
    pid = p.get("id","")
    if want and pid not in want:
        continue
    persona_key = p.get("default_persona","skeptical_operator")
    persona_txt = personas.get(persona_key, persona_key)
    if pov_list and len(rows) < len(pov_list):
        ov = pov_list[len(rows)]
        persona_txt = personas.get(ov, ov)
        persona_key = ov
    rows.append([
        pid, p.get("kind",""), p.get("model_id",""), p.get("family",""),
        p.get("region","us-east-1"), p.get("aws_profile",""),
        p.get("api_key_env",""), persona_key,
        "1" if p.get("same_family") else "0",
        persona_txt.replace("\t"," ").replace("\n"," ").strip(),
    ])
# Use US (unit separator, \x1f) as the field delimiter, NOT tab. `read` with a
# whitespace IFS collapses consecutive delimiters and drops empty fields (e.g.
# an empty aws_profile shifts every later column). \x1f is non-whitespace so
# empty fields are preserved positionally.
for r in rows:
    print("\x1f".join(r))
PY
)"

if [ -z "$PARSED" ]; then
  echo "model_panel.sh: no enabled providers parsed from $REG" >&2
  exit 70
fi

TMPDIR_PANEL="$(mktemp -d)"
trap 'rm -rf "$TMPDIR_PANEL"' EXIT

# --- JSON-escape helper ------------------------------------------------------
jesc() { python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))'; }

# --- Per-provider callers. Each writes a JSON object to $TMPDIR_PANEL/$id.json
call_bedrock() {  # id model_id region profile persona_txt same_family
  local id="$1" model="$2" region="$3" profile="$4" persona="$5" sf="$6"
  local usr="$TASK"$'\n\n---\n'"$PROMPT"
  local msgs sysarg resp t0 t1
  # Build the two JSON args separately. converse takes --system / --messages /
  # --inference-config as distinct params (NOT a single --cli-input-json body).
  msgs=$(python3 -c 'import json,sys; print(json.dumps([{"role":"user","content":[{"text":sys.argv[1]}]}]))' "$usr")
  sysarg=$(python3 -c 'import json,sys; print(json.dumps([{"text":sys.argv[1]}]))' "$persona")
  t0=$(date +%s)
  resp=$(TO "$TIMEOUT" aws bedrock-runtime converse \
      --profile "$profile" --region "$region" --model-id "$model" \
      --system "$sysarg" --messages "$msgs" \
      --inference-config '{"maxTokens":700,"temperature":0.7}' 2>"$TMPDIR_PANEL/$id.err")
  local rc=$?; t1=$(date +%s)
  if [ $rc -ne 0 ]; then
    # retry with us. inference-profile prefix if not already prefixed
    if [[ "$model" != us.* && "$model" != global.* ]]; then
      resp=$(TO "$TIMEOUT" aws bedrock-runtime converse \
          --profile "$profile" --region "$region" --model-id "us.$model" \
          --system "$sysarg" --messages "$msgs" \
          --inference-config '{"maxTokens":700,"temperature":0.7}' 2>"$TMPDIR_PANEL/$id.err")
      rc=$?; t1=$(date +%s)
    fi
  fi
  if [ $rc -ne 0 ]; then
    emit_err "$id" bedrock_converse "$model" "$(head -c 200 "$TMPDIR_PANEL/$id.err")" "$sf"
    return
  fi
  local text; text=$(echo "$resp" | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d["output"]["message"]["content"][0]["text"])' 2>/dev/null)
  emit_ok "$id" "$model" "$persona" "$sf" $((t1-t0)) "$text"
}

call_gemini() {  # id model_id keyenv persona_txt same_family
  local id="$1" model="$2" keyenv="$3" persona="$4" sf="$5"
  local key; key="$(printenv "$keyenv" || true)"
  if [ -z "$key" ]; then emit_skip "$id" gemini "$model" "no $keyenv" "$sf"; return; fi
  local full="$persona"$'\n\n'"$TASK"$'\n\n---\n'"$PROMPT"
  local body t0 t1 resp
  # 2.5-pro is a thinking model: reasoning tokens count against maxOutputTokens,
  # so a low ceiling returns empty content with finishReason MAX_TOKENS. Give headroom.
  body=$(python3 -c 'import json,sys; print(json.dumps({"contents":[{"parts":[{"text":sys.argv[1]}]}],"generationConfig":{"maxOutputTokens":4000,"temperature":0.7}}))' "$full")
  t0=$(date +%s)
  resp=$(TO "$TIMEOUT" curl -s "https://generativelanguage.googleapis.com/v1beta/models/$model:generateContent?key=$key" \
      -H 'Content-Type: application/json' -d "$body" 2>"$TMPDIR_PANEL/$id.err")
  t1=$(date +%s)
  local text; text=$(echo "$resp" | python3 -c 'import json,sys
d=json.load(sys.stdin)
parts=d["candidates"][0].get("content",{}).get("parts",[])
print("".join(p.get("text","") for p in parts))' 2>/dev/null)
  if [ -z "$text" ]; then emit_err "$id" gemini "$model" "$(echo "$resp" | head -c 200)" "$sf"; return; fi
  emit_ok "$id" "$model" "$persona" "$sf" $((t1-t0)) "$text"
}

call_openai() {  # id model_id keyenv persona_txt same_family
  local id="$1" model="$2" keyenv="$3" persona="$4" sf="$5"
  local key; key="$(printenv "$keyenv" || true)"
  if [ -z "$key" ]; then emit_skip "$id" openai "$model" "no $keyenv" "$sf"; return; fi
  local body t0 t1 resp
  body=$(python3 -c 'import json,sys; print(json.dumps({"model":sys.argv[1],"messages":[{"role":"system","content":sys.argv[2]},{"role":"user","content":sys.argv[3]}],"max_tokens":600,"temperature":0.7}))' "$model" "$persona" "$TASK"$'\n\n---\n'"$PROMPT")
  t0=$(date +%s)
  resp=$(TO "$TIMEOUT" curl -s https://api.openai.com/v1/chat/completions \
      -H "Authorization: Bearer $key" -H 'Content-Type: application/json' -d "$body" 2>"$TMPDIR_PANEL/$id.err")
  t1=$(date +%s)
  local text; text=$(echo "$resp" | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d["choices"][0]["message"]["content"])' 2>/dev/null)
  if [ -z "$text" ]; then emit_err "$id" openai "$model" "$(echo "$resp" | head -c 200)" "$sf"; return; fi
  emit_ok "$id" "$model" "$persona" "$sf" $((t1-t0)) "$text"
}

call_ollama() {  # id model_id persona_txt same_family
  local id="$1" model="$2" persona="$3" sf="$4"
  if ! command -v ollama >/dev/null 2>&1; then emit_skip "$id" ollama "$model" "ollama not installed" "$sf"; return; fi
  if ! ollama list 2>/dev/null | awk 'NR>1{print $1}' | grep -q "^${model%%:*}"; then
    emit_skip "$id" ollama "$model" "model not pulled (run: ollama pull $model)" "$sf"; return
  fi
  local full="$persona"$'\n\n'"$TASK"$'\n\n---\n'"$PROMPT"
  local t0 t1 text; t0=$(date +%s)
  text=$(TO "$TIMEOUT" ollama run "$model" "$full" 2>"$TMPDIR_PANEL/$id.err")
  t1=$(date +%s)
  if [ -z "$text" ]; then emit_err "$id" ollama "$model" "$(head -c 200 "$TMPDIR_PANEL/$id.err")" "$sf"; return; fi
  emit_ok "$id" "$model" "$persona" "$sf" $((t1-t0)) "$text"
}

call_claude_note() {  # id model_id persona_txt same_family
  # Claude is the SAME family as the writer; we do not self-call here. Instead we
  # emit a directive for the orchestrating assistant to fill the domain-anchor
  # seat itself. Flagged same_family so synthesis discounts agreement with it.
  local id="$1" model="$2" persona="$3" sf="$4"
  emit_skip "$id" claude_note "$model" "same-family anchor: orchestrator fills this seat inline (persona: domain_architect)" "$sf"
}

emit_ok()   { python3 -c 'import json,sys; print(json.dumps({"id":sys.argv[1],"model":sys.argv[2],"persona":sys.argv[3],"same_family":sys.argv[4]=="1","status":"ok","latency_s":int(sys.argv[5]),"text":sys.argv[6]}))' "$1" "$2" "$3" "$4" "$5" "$6" > "$TMPDIR_PANEL/$1.json"; }
emit_skip() { python3 -c 'import json,sys; print(json.dumps({"id":sys.argv[1],"kind":sys.argv[2],"model":sys.argv[3],"same_family":sys.argv[5]=="1","status":"skipped","note":sys.argv[4]}))' "$1" "$2" "$3" "$4" "$5" > "$TMPDIR_PANEL/$1.json"; }
emit_err()  { python3 -c 'import json,sys; print(json.dumps({"id":sys.argv[1],"kind":sys.argv[2],"model":sys.argv[3],"same_family":sys.argv[5]=="1","status":"error","note":sys.argv[4]}))' "$1" "$2" "$3" "$4" "$5" > "$TMPDIR_PANEL/$1.json"; }
export -f emit_ok emit_skip emit_err
export TMPDIR_PANEL TASK PROMPT TIMEOUT

# --- Probe mode: just report reachability -----------------------------------
if [ "$PROBE" = 1 ]; then
  echo "Provider reachability (profile <your-aws-profile>):"
  while IFS=$'\x1f' read -r id kind model family region profile keyenv pkey sf persona; do
    case "$kind" in
      bedrock_converse) ok=$(aws bedrock-runtime converse --profile "$profile" --region "$region" --model-id "$model" --messages '[{"role":"user","content":[{"text":"ping"}]}]' --inference-config '{"maxTokens":5}' >/dev/null 2>&1 && echo reachable || (aws bedrock-runtime converse --profile "$profile" --region "$region" --model-id "us.$model" --messages '[{"role":"user","content":[{"text":"ping"}]}]' --inference-config '{"maxTokens":5}' >/dev/null 2>&1 && echo "reachable (us.* profile)" || echo unreachable));;
      gemini|openai) [ -n "$(printenv "$keyenv" || true)" ] && ok="key set" || ok="SKIP (no $keyenv)";;
      ollama) command -v ollama >/dev/null 2>&1 && { ollama list 2>/dev/null | awk 'NR>1{print $1}' | grep -q "^${model%%:*}" && ok="pulled" || ok="SKIP (not pulled)"; } || ok="SKIP (not installed)";;
      claude_note) ok="inline (same-family anchor)";;
      *) ok="?";;
    esac
    printf "  %-14s %-26s %-16s %s\n" "$id" "$model" "$family" "$ok"
  done < <(printf '%s\n' "$PARSED")
  exit 0
fi

# --- Fan out in parallel -----------------------------------------------------
while IFS=$'\x1f' read -r id kind model family region profile keyenv pkey sf persona; do
  case "$kind" in
    bedrock_converse) call_bedrock "$id" "$model" "$region" "$profile" "$persona" "$sf" & ;;
    gemini)           call_gemini  "$id" "$model" "$keyenv" "$persona" "$sf" & ;;
    openai)           call_openai  "$id" "$model" "$keyenv" "$persona" "$sf" & ;;
    ollama)           call_ollama  "$id" "$model" "$persona" "$sf" & ;;
    claude_note)      call_claude_note "$id" "$model" "$persona" "$sf" & ;;
  esac
done < <(printf '%s\n' "$PARSED")
wait

# --- Combine into one JSON array, preserving registry order ------------------
COMBINED=$(python3 - "$TMPDIR_PANEL" <<'PY'
import json, os, sys, glob
d = sys.argv[1]
out = []
for f in sorted(glob.glob(os.path.join(d, "*.json"))):
    try:
        out.append(json.load(open(f)))
    except Exception:
        pass
print(json.dumps(out, indent=2))
PY
)

if [ -n "$OUT" ]; then echo "$COMBINED" > "$OUT"; echo "panel written to $OUT" >&2; else echo "$COMBINED"; fi
