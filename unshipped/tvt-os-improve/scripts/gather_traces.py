#!/usr/bin/env python3
"""gather_traces — emit a date-windowed cross-domain trace pool (T138 / T137).

Reads `traces/<YYYY>/<MM>/<run_id>/trace.jsonl` from the configured root and
prints the matching records as JSON lines on stdout. Read-only / idempotent.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT / "src"))

from gordon_os.eval.datasets import gather_trace_pool  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="gather_traces")
    parser.add_argument(
        "--traces-root",
        default=str(REPO_ROOT / "traces"),
        help="Path to the traces/ directory (default: <repo>/traces).",
    )
    parser.add_argument("--start", help="ISO date / datetime for window start.")
    parser.add_argument("--end", help="ISO date / datetime for window end (exclusive).")
    parser.add_argument(
        "--pack",
        action="append",
        help="Restrict to records with pack in {...}. Pass multiple times.",
    )
    parser.add_argument(
        "--limit", type=int, default=0, help="Max records (0 = unlimited)."
    )
    args = parser.parse_args(argv)

    traces_root = Path(args.traces_root)
    count = 0
    for record in gather_trace_pool(
        traces_root=traces_root,
        start=args.start,
        end=args.end,
        packs=args.pack if args.pack else None,
    ):
        sys.stdout.write(json.dumps(record) + "\n")
        count += 1
        if args.limit and count >= args.limit:
            break
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
