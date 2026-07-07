#!/usr/bin/env bash
# Run every shipped skill's standalone test_*.py suite, each in its own subprocess.
#
# Why not one pytest run: several skills ship a same-named script (score.py, common.py) with
# no package __init__.py-based namespacing between them. A single pytest process collecting
# `from score import ...` from two different scripts/ dirs hits Python's global sys.modules
# cache and silently reuses whichever one it imported first — a wrong-module-tested bug that
# won't raise an error, it'll just quietly test the wrong file. Running each suite as its own
# `python3 test_X.py` subprocess (exactly how each file's own docstring says to run it)
# sidesteps the collision entirely. See pytest.ini for the corresponding pytest scoping.
#
# Usage: scripts/run_all_tests.sh

set -uo pipefail  # not -e: we want to run every suite and report all failures, not stop at the first

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

pass=0
fail=0
failed_suites=()

while IFS= read -r -d '' test_file; do
  dir="$(dirname "$test_file")"
  name="$(basename "$test_file")"
  rel="${test_file#"$REPO_ROOT"/}"
  echo "== $rel =="
  if (cd "$dir" && python3 "$name" 2>&1 | tail -5); then
    pass=$((pass + 1))
  else
    fail=$((fail + 1))
    failed_suites+=("$rel")
  fi
  echo ""
done < <(find skills -iname "test_*.py" -not -path "*/.pytest_cache/*" -print0 | sort -z)

echo "== summary =="
echo "$pass suite(s) passed, $fail suite(s) failed"
if [ "$fail" -gt 0 ]; then
  echo "failed: ${failed_suites[*]}"
  exit 1
fi
