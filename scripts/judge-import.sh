#!/usr/bin/env bash
# Import-readiness judge — the gate a marketplace publish must pass.
#
# Deterministic half: tests/test_import_readiness.py (checks C1-C12, ratchet baseline).
# LLM half:           rubrics/import-readiness.md (run via tvt-os-judge, one judge/skill).
#
# Usage:
#   scripts/judge-import.sh              # ratchet mode — fail on regressions vs baseline
#   scripts/judge-import.sh --strict     # publish gate — fail on ANY open finding
#   scripts/judge-import.sh --rebaseline # regenerate the baseline (deliberate act:
#                                        #   only after triaging every change; never to
#                                        #   make a regression disappear)

set -euo pipefail
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

MODE="${1:-}"

case "$MODE" in
  --rebaseline)
    python3 tests/test_import_readiness.py --write-baseline
    echo ""
    echo "Baseline rewritten. Diff it, justify every change in the commit message."
    ;;
  --strict)
    echo "== Publish gate (strict): every open finding fails =="
    IMPORT_GATE_STRICT=1 python3 -m pytest tests/test_import_readiness.py -q
    echo ""
    echo "Deterministic gate clean. Now run the LLM half before publishing:"
    echo "  invoke tvt-os-judge with rubrics/import-readiness.md across skills/*,"
    echo "  record the run as docs/import-readiness-judge-\$(date +%F).md"
    ;;
  "")
    echo "== Ratchet mode: regressions vs tests/import-gate-baseline.yml fail =="
    python3 -m pytest tests/test_import_readiness.py -q
    open=$(python3 - <<'EOF'
import yaml, pathlib
p = pathlib.Path("tests/import-gate-baseline.yml")
d = yaml.safe_load(p.read_text()) if p.exists() else {}
print(sum(len(v) for v in (d.get("findings") or {}).values()))
EOF
)
    echo ""
    echo "No regressions. Known-open findings still in the baseline: $open"
    echo "(publish requires 0 — burn them down, then: scripts/judge-import.sh --strict)"
    ;;
  *)
    echo "usage: scripts/judge-import.sh [--strict|--rebaseline]" >&2
    exit 2
    ;;
esac
