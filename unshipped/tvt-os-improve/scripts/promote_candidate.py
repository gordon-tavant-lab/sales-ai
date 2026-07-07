#!/usr/bin/env python3
"""promote_candidate — run the combined promotion gate on a candidate (T138 / T136).

Loads candidate + baseline score arrays from JSON, invokes
`gordon_os.eval.promotion_gate.evaluate_promotion`, and prints a
`PromotionRecord` JSON to stdout. Exit code 0 on PROMOTED, 2 on any rejection
so this composes cleanly with CI / shell pipelines.

The promotion gate is conjunctive: stat-sig (paired bootstrap + Holm) AND
frozen-sentinel stable AND cross-pack regression check passes (G-VI).
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT / "src"))

from gordon_os.eval.promotion_gate import (  # noqa: E402
    PromotionOutcome,
    evaluate_promotion,
)


def _load_json(path: str) -> dict | list:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="promote_candidate")
    parser.add_argument("--candidate-id", required=True)
    parser.add_argument(
        "--scores-json",
        required=True,
        help=(
            "Path to JSON with keys: baseline_dev, candidate_dev, "
            "baseline_sentinel, candidate_sentinel, baseline_pack_scores, "
            "candidate_pack_scores."
        ),
    )
    parser.add_argument("--alpha", type=float, default=0.05)
    parser.add_argument("--resamples", type=int, default=1000)
    parser.add_argument("--sentinel-delta-min-ratio", type=float, default=0.5)
    parser.add_argument("--cross-pack-tolerance", type=float, default=0.0)
    args = parser.parse_args(argv)

    data = _load_json(args.scores_json)
    if not isinstance(data, dict):
        print(
            f"ERROR: scores-json must be a JSON object (mapping), got {type(data).__name__}.",
            file=sys.stderr,
        )
        return 2

    # Defense in depth (merged-state review #2): empty score arrays silently
    # produce 0.0 baseline / 0.0 candidate / 0.0 delta — yielding a vacuous PASS
    # at the cross-pack gate instead of REJECT. Treat empty arrays at the CLI
    # boundary as a hard failure with a clear error rather than silently letting
    # the gate pass on missing data.
    for key in ("baseline_dev", "candidate_dev", "baseline_sentinel", "candidate_sentinel"):
        if not data.get(key):
            print(
                f"ERROR: '{key}' is empty or missing — refusing to evaluate promotion. "
                f"Missing dev/sentinel slices are an automatic regression, not a pass.",
                file=sys.stderr,
            )
            return 2
    if not data.get("baseline_pack_scores") or not data.get("candidate_pack_scores"):
        print(
            "ERROR: per-pack score dicts are empty or missing — refusing to evaluate. "
            "At least one active pack must contribute scores (G-VI cross-pack regression).",
            file=sys.stderr,
        )
        return 2
    empty_packs = [
        p
        for p, scores in data["candidate_pack_scores"].items()
        if not scores
    ]
    if empty_packs:
        print(
            f"ERROR: pack(s) {empty_packs} have empty candidate score arrays. "
            f"Missing DEV slice for a registered pack is an automatic regression "
            f"(merged-state review #2).",
            file=sys.stderr,
        )
        return 2

    # Per-pack scores arrive as arrays (mirroring dev/sentinel shape on the
    # wire); evaluate_promotion -> cross_pack_regression operates on scalar
    # floats. Aggregate to mean here. np.mean accepts scalar inputs too, so
    # callers may pass either array or scalar values per pack.
    baseline_pack_scalar = {
        pack: float(np.mean(np.asarray(v, dtype=float)))
        for pack, v in data["baseline_pack_scores"].items()
    }
    candidate_pack_scalar = {
        pack: float(np.mean(np.asarray(v, dtype=float)))
        for pack, v in data["candidate_pack_scores"].items()
    }

    record = evaluate_promotion(
        candidate_id=args.candidate_id,
        baseline_dev=np.asarray(data["baseline_dev"], dtype=float),
        candidate_dev=np.asarray(data["candidate_dev"], dtype=float),
        baseline_sentinel=np.asarray(data["baseline_sentinel"], dtype=float),
        candidate_sentinel=np.asarray(data["candidate_sentinel"], dtype=float),
        baseline_pack_scores=baseline_pack_scalar,
        candidate_pack_scores=candidate_pack_scalar,
        alpha=args.alpha,
        resamples=args.resamples,
        sentinel_delta_min_ratio=args.sentinel_delta_min_ratio,
        cross_pack_tolerance=args.cross_pack_tolerance,
    )

    payload = asdict(record)
    payload["outcome"] = record.outcome.value
    print(json.dumps(payload, indent=2, default=str))
    return 0 if record.outcome == PromotionOutcome.PROMOTED else 2


if __name__ == "__main__":
    raise SystemExit(main())
