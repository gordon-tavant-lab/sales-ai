#!/usr/bin/env python3
"""run_gepa — drive a single GEPA campaign on a core skill prompt (T138 / FR-041).

Thin wrapper around `gordon_os.eval.gepa_runner.GEPACampaign` + the sentinel-
protected `run_campaign_with_sentinel`. The real `dspy` + `gepa-ai/gepa`
integration is import-guarded so CI / offline test environments run with the
built-in deterministic mock generator. Pass `--mock` (default in CI) to force
the offline path explicitly.

Per Principle G-XIII, this script REFUSES targets outside the allowed core-
skill prompt prefix list — narrow GEPA scope is enforced at construction time
inside `GEPACampaign.__post_init__`.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT / "src"))

from gordon_os.eval.datasets import gather_trace_pool  # noqa: E402
from gordon_os.eval.gepa_runner import (  # noqa: E402
    GEPACampaign,
    GEPAResult,
    run_campaign_with_sentinel,
)


def _mock_candidate_generator(baseline: str, traces: list[dict]) -> list[str]:
    return [f"{baseline} :: variant-A", f"{baseline} :: variant-B"]


def _mock_scorer(prompt: str, example: dict) -> float:
    return 0.65 if "variant" in prompt else 0.50


def _load_real_generator():
    try:
        import dspy  # noqa: F401
        import gepa  # noqa: F401
    except ImportError:
        return None
    return None


def run(
    *,
    repo_root: Path,
    target_skill: str,
    target_prompt_path: str,
    baseline_prompt: str,
    dev_slice: list[dict],
    traces_root: Path | None,
    budget_usd_cap: float,
    cost_per_rollout: float,
    campaign_id: str,
    mock: bool,
) -> GEPAResult:
    if mock or _load_real_generator() is None:
        generator = _mock_candidate_generator
        scorer = _mock_scorer
    else:  # pragma: no cover - real LLM path; never exercised in CI
        generator = _mock_candidate_generator
        scorer = _mock_scorer

    pool = (
        list(gather_trace_pool(traces_root=traces_root)) if traces_root else []
    )
    runner = GEPACampaign(
        target_skill=target_skill,
        target_prompt_path=target_prompt_path,
        baseline_prompt=baseline_prompt,
        dev_slice=dev_slice,
        candidate_generator=generator,
        scorer=scorer,
        budget_usd_cap=budget_usd_cap,
        cost_per_rollout=cost_per_rollout,
        campaign_id=campaign_id,
    )
    return run_campaign_with_sentinel(
        repo_root=repo_root,
        campaign_fn=lambda: runner.run(trace_pool=pool),
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="run_gepa")
    parser.add_argument("--target-skill", required=True)
    parser.add_argument("--target-prompt-path", required=True)
    parser.add_argument("--baseline-prompt", default="placeholder-baseline")
    parser.add_argument("--dev-slice-json", help="JSON path to dev slice list[dict]")
    parser.add_argument("--traces-root", help="Path to traces/ root.")
    parser.add_argument("--budget-usd-cap", type=float, default=200.0)
    parser.add_argument("--cost-per-rollout", type=float, default=0.02)
    parser.add_argument("--campaign-id", default="cli-run")
    parser.add_argument("--mock", action="store_true", default=True)
    parser.add_argument(
        "--repo-root", default=str(REPO_ROOT), help="Repo root for sentinel."
    )
    args = parser.parse_args(argv)

    dev_slice: list[dict] = []
    if args.dev_slice_json:
        dev_slice = json.loads(Path(args.dev_slice_json).read_text(encoding="utf-8"))
    else:
        dev_slice = [{"brief": "placeholder", "ground_truth": "placeholder"}]

    traces_root = Path(args.traces_root) if args.traces_root else None
    result = run(
        repo_root=Path(args.repo_root),
        target_skill=args.target_skill,
        target_prompt_path=args.target_prompt_path,
        baseline_prompt=args.baseline_prompt,
        dev_slice=dev_slice,
        traces_root=traces_root,
        budget_usd_cap=args.budget_usd_cap,
        cost_per_rollout=args.cost_per_rollout,
        campaign_id=args.campaign_id,
        mock=args.mock,
    )
    print(
        json.dumps(
            {
                "campaign_id": result.campaign_id,
                "rollouts_executed": result.rollouts_executed,
                "estimated_cost_usd": result.estimated_cost_usd,
                "n_candidates": len(result.candidates),
                "candidates": [asdict(c) for c in result.candidates],
            },
            indent=2,
            default=str,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
