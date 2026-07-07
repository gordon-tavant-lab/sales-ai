#!/usr/bin/env python3
"""calibration_warmup — record / inspect calibration warmup state (T140 / Q8).

Thin CLI over `gordon_os.eval.calibration_warmup`. Per Q8 / FR-040:
- Before 25 resolved outcomes accumulate per (pack, prediction_class), the GEPA
  reward formula OMITS `calibration_factor` (warmup_active=True).
- At/after the 25th outcome, warmup clears and calibration folds in as a
  multiplier in the composite reward.

Subcommands:
  record   — append one resolved outcome to state.
  status   — print current state for a (pack, prediction_class).
  factor   — print the calibration factor (None if warmup_active).
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT / "src"))

from gordon_os.eval.calibration_warmup import (  # noqa: E402
    CalibrationWarmupState,
    DEFAULT_THRESHOLD,
    record_outcome,
    warmup_factor,
)


def _default_state_path() -> Path:
    return REPO_ROOT / "state" / "calibration" / "warmup_progress.json"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="calibration_warmup")
    parser.add_argument(
        "--state-path",
        default=str(_default_state_path()),
        help="JSON state file (default: state/calibration/warmup_progress.json).",
    )
    parser.add_argument(
        "--threshold", type=int, default=DEFAULT_THRESHOLD,
        help=f"Outcomes required to clear warmup (default: {DEFAULT_THRESHOLD}).",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    record = sub.add_parser("record", help="Append one resolved outcome.")
    record.add_argument("--pack", required=True)
    record.add_argument("--prediction-class", required=True)
    record.add_argument("--score", type=float, required=True)

    status = sub.add_parser("status", help="Show current state.")
    status.add_argument("--pack", required=True)
    status.add_argument("--prediction-class", required=True)

    factor = sub.add_parser("factor", help="Print calibration factor or null.")
    factor.add_argument("--pack", required=True)
    factor.add_argument("--prediction-class", required=True)

    args = parser.parse_args(argv)
    state_path = Path(args.state_path)

    if args.cmd == "record":
        state = record_outcome(
            state_path,
            pack=args.pack,
            prediction_class=args.prediction_class,
            outcome_score=args.score,
            threshold=args.threshold,
        )
        print(json.dumps(asdict(state), indent=2))
        return 0

    if args.cmd == "status":
        state = CalibrationWarmupState.load(
            state_path,
            pack=args.pack,
            prediction_class=args.prediction_class,
            threshold=args.threshold,
        )
        print(json.dumps(asdict(state), indent=2))
        return 0

    if args.cmd == "factor":
        f = warmup_factor(
            state_path,
            pack=args.pack,
            prediction_class=args.prediction_class,
            threshold=args.threshold,
        )
        print(json.dumps({"calibration_factor": f}))
        return 0

    parser.error("unknown subcommand")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
