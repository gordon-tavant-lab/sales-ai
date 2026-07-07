#!/usr/bin/env python3
"""Invoke tvt-core-mcts via the Skill tool with budget propagation (T120).

This wrapper is the boundary between Gordon OS's forecast step and the
domain-neutral tvt-core-mcts engine (Principle G-IV — Compose, Don't
Duplicate). The script:

  1. Reads an MCTSProblem JSON from --problem (or stdin).
  2. Builds the Skill-tool invocation payload, including budget constraints
     (max_iterations, wall_clock_seconds, max_cost_usd).
  3. Either prints the payload for a Claude session to dispatch, OR (when
     run under --dispatch with a bound subprocess hook) invokes a local
     pluggable dispatcher that returns ranked actions.

In production the Gordon OS orchestrator binds a dispatcher that calls
the Skill tool (skill="tvt-core-mcts", mode="run", problem=<payload>) and
maps the response into a ranked-actions list. In tests, the dispatcher
is mocked at this boundary — see tests/integration/test_forecast.py.
"""

from __future__ import annotations

import argparse
import json
import os
import shlex
import subprocess
import sys
from pathlib import Path


SKILL_NAME = "tvt-core-mcts"
SKILL_MODE = "run"


def build_skill_payload(problem: dict, *, max_iterations=None, wall_clock_seconds=None, max_cost_usd=None) -> dict:
    """Assemble the JSON payload handed to the Skill tool."""
    budget = {}
    constraints = problem.get("constraints", {}) or {}
    if max_iterations is None:
        max_iterations = constraints.get("max_iterations")
    if wall_clock_seconds is None:
        wall_clock_seconds = constraints.get("wall_clock_seconds")
    if max_cost_usd is None:
        max_cost_usd = constraints.get("max_cost_usd")

    if max_iterations is not None:
        budget["max_iterations"] = max_iterations
    if wall_clock_seconds is not None:
        budget["wall_clock_seconds"] = wall_clock_seconds
    if max_cost_usd is not None:
        budget["max_cost_usd"] = max_cost_usd

    return {
        "skill": SKILL_NAME,
        "mode": SKILL_MODE,
        "problem": problem,
        "budget": budget,
        "eval_floor": problem.get("eval_floor", {}),
    }


def dispatch_via_local_hook(payload: dict) -> dict:
    """Optional local dispatcher hook for non-Claude-session runs.

    Honors the GORDON_OS_MCTS_DISPATCHER env var; that command is invoked
    with the payload on stdin and is expected to return the solution JSON
    on stdout. Useful for CI / smoke tests against a local tvt-core-mcts.
    Returns an empty solution if no dispatcher is configured.
    """
    cmd = os.environ.get("GORDON_OS_MCTS_DISPATCHER")
    if not cmd:
        return {"ranked_actions": [], "stats": {"dispatch": "no_hook"}}
    parts = shlex.split(cmd)
    proc = subprocess.run(
        parts, input=json.dumps(payload).encode("utf-8"),
        stdout=subprocess.PIPE, check=False,
    )
    try:
        return json.loads(proc.stdout.decode("utf-8"))
    except json.JSONDecodeError:
        return {"ranked_actions": [], "stats": {"dispatch_error": "non_json_output"}}


def main(argv=None):
    parser = argparse.ArgumentParser(prog="invoke_g_core_mcts")
    parser.add_argument("--problem", help="Path to MCTSProblem JSON; default reads stdin.")
    parser.add_argument("--dispatch", action="store_true",
                        help="Invoke the local dispatcher hook and print the solution.")
    parser.add_argument("--max-iterations", type=int)
    parser.add_argument("--wall-clock-seconds", type=int)
    parser.add_argument("--max-cost-usd", type=float)
    args = parser.parse_args(argv)

    if args.problem:
        problem = json.loads(Path(args.problem).read_text(encoding="utf-8"))
    else:
        problem = json.loads(sys.stdin.read())

    payload = build_skill_payload(
        problem,
        max_iterations=args.max_iterations,
        wall_clock_seconds=args.wall_clock_seconds,
        max_cost_usd=args.max_cost_usd,
    )

    if args.dispatch:
        solution = dispatch_via_local_hook(payload)
        json.dump(solution, sys.stdout, indent=2, default=str)
    else:
        json.dump(payload, sys.stdout, indent=2, default=str)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
