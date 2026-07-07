#!/usr/bin/env bash
# tvt-os-judge v1.2 — dependency liveness check
#
# Usage: check_dep_liveness.sh <artifact-path-or-dir>
#
# Extracts named dependencies, queries their upstream status via gh CLI, and
# emits JSON to stdout. Exit 0 = all live; exit 1 = at least one archived
# dep referenced as load-bearing (judge should set decision axis to 0.0).

set -uo pipefail

ARTIFACT="${1:-}"
if [[ -z "$ARTIFACT" ]]; then
  echo '{"error":"usage: check_dep_liveness.sh <artifact-path>"}' >&2
  exit 2
fi

if [[ ! -e "$ARTIFACT" ]]; then
  echo "{\"error\":\"artifact not found: $ARTIFACT\"}" >&2
  exit 2
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PATTERNS_FILE="${SCRIPT_DIR}/dep_liveness_patterns.yml"

export ARTIFACT_PATH="$ARTIFACT"
export PATTERNS_FILE_PATH="$PATTERNS_FILE"

python3 <<'PYTHON'
import json, os, re, sys, subprocess
from pathlib import Path
from datetime import datetime, timezone

artifact = Path(os.environ["ARTIFACT_PATH"])
patterns_file = Path(os.environ["PATTERNS_FILE_PATH"])

files = []
if artifact.is_dir():
    for ext in ("*.md", "*.py", "*.yml", "*.yaml", "*.toml", "*.json"):
        files.extend(artifact.rglob(ext))
else:
    files = [artifact]

# Capture github.com/<owner>/<repo>
gh_re = re.compile(r"github\.com/([A-Za-z0-9_.\-]+)/([A-Za-z0-9_.\-]+)")

# Known framework names that may appear without a URL (configurable)
KNOWN = {
    "Kuzu": ("kuzudb", "kuzu"),
    "Apache AGE": ("apache", "age"),
    "CloudNativePG": ("cloudnative-pg", "cloudnative-pg"),
    "Langfuse": ("langfuse", "langfuse"),
    "Memgraph": ("memgraph", "memgraph"),
    "OpenTofu": ("opentofu", "opentofu"),
    "Pulumi": ("pulumi", "pulumi"),
    "Crossplane": ("crossplane", "crossplane"),
    "Mem0": ("mem0ai", "mem0"),
    "Graphiti": ("getzep", "graphiti"),
    "HippoRAG": ("OSU-NLP-Group", "HippoRAG"),
}

# Load operator allowlist
allow = set()
if patterns_file.exists():
    try:
        import yaml
        cfg = yaml.safe_load(patterns_file.read_text()) or {}
        for entry in cfg.get("allowlist", []):
            allow.add(entry.lower())
    except Exception:
        pass

deps = {}
SKIP_PATH = "skills/tvt-os-judge/scripts"
SKIP_BLOCK = re.compile(
    r"<!--\s*dep-liveness:skip\s*-->.*?<!--\s*/dep-liveness:skip\s*-->",
    re.DOTALL,
)

for f in files:
    try:
        text = f.read_text(errors="ignore")
    except Exception:
        continue
    if SKIP_PATH in str(f):
        continue
    text = SKIP_BLOCK.sub("", text)

    for m in gh_re.finditer(text):
        owner = m.group(1)
        repo = m.group(2).rstrip(".,;):>")
        if repo.lower() in ("blob", "tree", "raw", "issues", "pull", "wiki", "releases"):
            continue
        key = f"github:{owner}/{repo}"
        if key.split(":", 1)[1].lower() in allow:
            continue
        deps[key] = (owner, repo)

    lower = text.lower()
    for name, (owner, repo) in KNOWN.items():
        if name.lower() in lower:
            key = f"github:{owner}/{repo}"
            if key.split(":", 1)[1].lower() in allow:
                continue
            deps[key] = (owner, repo)

results = []
any_archived = False
now = datetime.now(timezone.utc)

for key, (owner, repo) in deps.items():
    entry = {"dep": key, "owner": owner, "repo": repo}
    try:
        out = subprocess.run(
            ["gh", "api", f"repos/{owner}/{repo}", "--jq", ".archived,.pushed_at,.html_url"],
            capture_output=True, text=True, timeout=8,
        )
        if out.returncode != 0:
            entry["status"] = "unknown"
            entry["error"] = out.stderr.strip()[:200]
            results.append(entry)
            continue
        lines = out.stdout.strip().split("\n")
        archived = lines[0].lower() == "true"
        pushed_at = lines[1] if len(lines) > 1 else ""
        html_url = lines[2] if len(lines) > 2 else f"https://github.com/{owner}/{repo}"
        entry["archived"] = archived
        entry["last_commit_date"] = pushed_at
        entry["evidence_url"] = html_url
        if archived:
            entry["status"] = "ARCHIVED"
            any_archived = True
        else:
            try:
                last = datetime.fromisoformat(pushed_at.replace("Z", "+00:00"))
                age_days = (now - last).days
                if age_days > 365:
                    entry["status"] = "EOL"
                elif age_days > 180:
                    entry["status"] = "STALE"
                else:
                    entry["status"] = "LIVE"
                entry["age_days"] = age_days
            except Exception:
                entry["status"] = "unknown"
        results.append(entry)
    except subprocess.TimeoutExpired:
        entry["status"] = "timeout"
        results.append(entry)
    except FileNotFoundError:
        entry["status"] = "gh-cli-missing"
        results.append(entry)

order = {"ARCHIVED": 0, "EOL": 1, "STALE": 2, "LIVE": 3, "unknown": 4, "timeout": 5, "gh-cli-missing": 5}
results.sort(key=lambda r: order.get(r.get("status", "unknown"), 99))

summary = {
    "artifact": str(artifact),
    "deps_checked": len(results),
    "archived_count": sum(1 for r in results if r.get("archived")),
    "eol_count": sum(1 for r in results if r.get("status") == "EOL"),
    "any_archived": any_archived,
    "results": results,
}
print(json.dumps(summary, indent=2))
sys.exit(1 if any_archived else 0)
PYTHON
