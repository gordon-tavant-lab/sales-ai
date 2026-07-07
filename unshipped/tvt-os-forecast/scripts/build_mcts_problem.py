#!/usr/bin/env python3
"""Build an MCTSProblem from a brief markdown file + active pack (T119).

Thin CLI wrapper around gordon_os.core.forecast.build_mcts_problem — no
business logic. Reads a brief, resolves the active pack via the pack loader,
and prints the JSON-serializable problem to stdout.

Output shape matches specs/002-gordon-os/contracts/mcts-problem.schema.json
so downstream tools can re-validate before invocation.

Usage:
    python build_mcts_problem.py --brief briefs/foo.md \
        [--reward closed_form|llm_judged|vector] \
        [--max-iterations N] [--wall-clock-seconds S] [--max-cost-usd $]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT / "src"))

from gordon_os.core import brief as brief_mod  # noqa: E402
from gordon_os.core.forecast import build_mcts_problem  # noqa: E402


def _load_pack(brief_obj):
    try:
        from gordon_os.packs.pack_loader import PackLoader
    except Exception:
        return None
    try:
        loader = PackLoader()
        sel = loader.select(brief_obj)
        return loader.load(sel.pack_name)
    except Exception:
        return None


def main(argv=None):
    parser = argparse.ArgumentParser(prog="build_mcts_problem")
    parser.add_argument("--brief", required=True)
    parser.add_argument(
        "--reward",
        choices=["closed_form", "llm_judged", "vector"],
        default="closed_form",
    )
    parser.add_argument("--max-iterations", type=int, default=1000)
    parser.add_argument("--wall-clock-seconds", type=int, default=30)
    parser.add_argument("--max-cost-usd", type=float, default=1.0)
    parser.add_argument("--objectives", help="JSON list for vector reward")
    args = parser.parse_args(argv)

    brief_obj = brief_mod.parse_brief(Path(args.brief))
    pack = _load_pack(brief_obj)

    objectives = None
    if args.reward == "vector" and args.objectives:
        objectives = json.loads(args.objectives)

    problem = build_mcts_problem(
        brief_obj,
        pack,
        reward_form=args.reward,
        objectives=objectives,
        max_iterations=args.max_iterations,
        wall_clock_seconds=args.wall_clock_seconds,
        max_cost_usd=args.max_cost_usd,
    )

    json.dump(
        problem.model_dump(mode="json", exclude_none=True),
        sys.stdout,
        indent=2,
        default=str,
    )
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
