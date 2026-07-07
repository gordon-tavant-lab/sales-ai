#!/usr/bin/env python3
"""
tvt-os-loop orchestrator — per spec-006 FR-078 (Q16 closed-loop staleness mechanism).

This is the runtime entry-point for the R³+L+F cognitive sequence orchestrated
by the tvt-os-loop skill. Before invoking any sub-skill, it reads the skill's
frontmatter (`requires.data` + `staleness_sla_seconds`), consults the source-
freshness registry, and bumps eval depth + emits OTel attributes when sources
are stale.

OTel attributes emitted (per spec-006 Entity 11):
  - gordon_os.staleness_breached: array of breached source IDs (FR-078)
  - gordon_os.active_packs: array of pack identifiers (FR-080)
  - gordon_os.extraneous_load_proxy: integer friction-signal count (FR-082, experimental)

Composition (per data-model.md):
  - Imports source_freshness module from g-core plugin (FR-076)
  - Reads SKILL.md frontmatter via the canonical 10-field schema (FR-073)
  - Bumps eval.depth one level on breach (FR-078)
  - Records to JSONL trace at ${CLAUDE_PLUGIN_DATA}/traces/<run_id>.jsonl

This is the v0.1 SCAFFOLD. Full R³+L+F invocation logic + LLM dispatch lives
in the tvt-os-loop skill body, which gets populated at Phase D-eve per FR-051.
This file establishes the staleness-check + telemetry plumbing so the
staleness_integration_test.py (SC-020) passes from Phase 2 onward.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


__all__ = [
    "check_staleness_for_skill",
    "emit_otel_attribute",
    "bump_eval_depth",
    "load_skill_frontmatter",
]


# ----- Source-freshness check (depends on g-core/lib/source_freshness.py) -----

def _import_source_freshness():
    """Lazy import — falls back to PATH-based subprocess call if module is unavailable."""
    try:
        # Preferred: direct import (when g-core's lib/ is on PYTHONPATH)
        from source_freshness import check_breach  # type: ignore[import-not-found]
        return check_breach
    except ImportError:
        pass

    # Fallback: try to add g-core/lib to sys.path
    plugin_root = os.environ.get("CLAUDE_PLUGIN_ROOT", "")
    if plugin_root:
        # plugin_root is g-os-cognitive's root; g-core is a sibling
        g_core_lib = Path(plugin_root).parent / "g-core" / "lib"
        if g_core_lib.exists():
            sys.path.insert(0, str(g_core_lib))
            try:
                from source_freshness import check_breach  # type: ignore[import-not-found]
                return check_breach
            except ImportError:
                pass
    return None


def check_staleness_for_skill(
    skill_id: str, requires_data: List[str], sla_seconds: Dict[str, int]
) -> List[str]:
    """Return list of source_ids that breach SLA per FR-078.

    Args:
        skill_id: skill being invoked (for logging context)
        requires_data: declared data sources from skill frontmatter
        sla_seconds: mapping {source_id: sla_seconds} from frontmatter

    Returns:
        Breached source_ids (empty list = all fresh).
    """
    check_breach = _import_source_freshness()
    if check_breach is None:
        # Defensive: registry unavailable → assume no breach (don't block)
        print(
            f"[tvt-os-loop] WARN: source_freshness module unavailable; "
            f"skipping staleness check for {skill_id}",
            file=sys.stderr,
        )
        return []

    # Only check sources that are both declared AND have an SLA
    sources_to_check = {
        source: sla_seconds[source] for source in requires_data if source in sla_seconds
    }
    if not sources_to_check:
        return []

    return check_breach(skill_id, sources_to_check)


# ----- Eval depth bumping (FR-078) -----

DEPTH_LADDER = ["light", "standard", "deep"]


def bump_eval_depth(current: str) -> str:
    """Bump eval depth one level per FR-078. Returns same value if already at top."""
    if current not in DEPTH_LADDER:
        return current
    idx = DEPTH_LADDER.index(current)
    if idx + 1 < len(DEPTH_LADDER):
        return DEPTH_LADDER[idx + 1]
    return current  # already at "deep"


# ----- OTel attribute emission (data-model.md Entity 11) -----

def trace_path(run_id: Optional[str] = None) -> Path:
    """Resolve the JSONL trace file path for the current run."""
    rid = run_id or os.environ.get("CLAUDE_SESSION_ID") or "unknown"
    plugin_data = os.environ.get("CLAUDE_PLUGIN_DATA")
    if plugin_data:
        base = Path(plugin_data) / "traces"
    else:
        project_dir = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
        base = Path(project_dir) / ".claude" / "state" / "traces"
    base.mkdir(parents=True, exist_ok=True)
    return base / f"{rid}.jsonl"


def emit_otel_attribute(
    name: str,
    value: Any,
    *,
    skill: Optional[str] = None,
    scope: str = "orchestrator",
    run_id: Optional[str] = None,
) -> None:
    """Append an OTel attribute record to the per-run JSONL trace.

    Records have shape:
        {timestamp, attribute, value, skill?, scope}

    Per FR-037, all engine-specific names use the `gordon_os.*` prefix
    (a legacy namespace string kept for trace compatibility).
    """
    if not name.startswith("gordon_os.") and not name.startswith("gen_ai."):
        print(
            f"[tvt-os-loop] WARN: emitting non-namespaced OTel attribute {name!r}",
            file=sys.stderr,
        )
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "attribute": name,
        "value": value,
        "scope": scope,
    }
    if skill:
        record["skill"] = skill

    try:
        with trace_path(run_id).open("a") as fp:
            fp.write(json.dumps(record) + "\n")
    except OSError as exc:
        print(f"[tvt-os-loop] WARN: trace write failed: {exc}", file=sys.stderr)


# ----- Frontmatter loader -----

def load_skill_frontmatter(skill_id: str) -> Optional[Dict[str, Any]]:
    """Load SKILL.md frontmatter for `skill_id` from installed plugin tree."""
    plugin_root = os.environ.get("CLAUDE_PLUGIN_ROOT")
    if not plugin_root:
        return None

    # Search this plugin first, then sibling plugins under marketplace plugins/
    plugin_dir = Path(plugin_root)
    search_roots = [plugin_dir]
    parent = plugin_dir.parent
    if parent.exists():
        search_roots.extend(p for p in parent.iterdir() if p.is_dir() and p != plugin_dir)

    for root in search_roots:
        candidate = root / "skills" / skill_id / "SKILL.md"
        if not candidate.exists():
            continue
        try:
            with candidate.open() as fp:
                text = fp.read()
        except OSError:
            continue
        return _parse_frontmatter(text)
    return None


def _parse_frontmatter(text: str) -> Optional[Dict[str, Any]]:
    try:
        import yaml
    except ImportError:
        return None
    if not text.startswith("---"):
        return None
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None
    try:
        data = yaml.safe_load(parts[1]) or {}
        return data if isinstance(data, dict) else None
    except yaml.YAMLError:
        return None


# ----- Orchestration entrypoint (CLI for hook + integration test) -----

def orchestrate_invocation(skill_id: str) -> Dict[str, Any]:
    """Run the pre-invocation staleness check + telemetry emission for a skill.

    Returns a dict describing the orchestrator's decision:
        {
            "skill_id": str,
            "breached_sources": List[str],
            "eval_depth_bumped_from": Optional[str],
            "eval_depth_bumped_to": Optional[str],
            "active_packs": List[str],
        }
    """
    fm = load_skill_frontmatter(skill_id) or {}
    requires_data = (fm.get("requires") or {}).get("data") or []
    sla_seconds = fm.get("staleness_sla_seconds") or {}
    eval_block = fm.get("eval") or {}
    declared_depth = eval_block.get("depth") or fm.get("eval_depth") or "light"

    breached = check_staleness_for_skill(skill_id, requires_data, sla_seconds)

    bumped_from: Optional[str] = None
    bumped_to: Optional[str] = None
    if breached:
        bumped_from = declared_depth
        bumped_to = bump_eval_depth(declared_depth)
        emit_otel_attribute(
            "gordon_os.staleness_breached",
            breached,
            skill=skill_id,
        )

    # Active packs: derive from skill metadata (per FR-080).
    # v0.1 scaffold: simple heuristic via skill family prefix.
    active_packs: List[str] = []
    family = skill_id.split("-")[1] if "-" in skill_id else ""
    if family in {"os", "core"}:
        active_packs = ["core"]  # not a domain pack invocation
    else:
        active_packs = [family]
    emit_otel_attribute(
        "gordon_os.active_packs",
        active_packs,
        skill=skill_id,
    )

    # T069 — cost_usd. The v0.1 scaffold doesn't dispatch through claude CLI,
    # so we read an env-passed cost (set by upstream invokers / tests). v0.2
    # captures this from the model response directly.
    cost_str = os.environ.get("GORDON_OS_INVOCATION_COST_USD")
    if cost_str:
        try:
            emit_otel_attribute(
                "gordon_os.cost_usd",
                float(cost_str),
                skill=skill_id,
            )
        except ValueError:
            pass

    # T072 — extraneous_load_proxy (FR-082, experimental per FR-083).
    # Friction-signal sum: retries, schema-violation backoffs, source breaches,
    # depth bumps. v0.1 scaffold counts what we can observe locally.
    friction_signals = 0
    if breached:
        friction_signals += len(breached)
    if bumped_from and bumped_to and bumped_from != bumped_to:
        friction_signals += 1
    emit_otel_attribute(
        "gordon_os.extraneous_load_proxy",
        friction_signals,
        skill=skill_id,
    )

    return {
        "skill_id": skill_id,
        "breached_sources": breached,
        "eval_depth_bumped_from": bumped_from,
        "eval_depth_bumped_to": bumped_to,
        "active_packs": active_packs,
        "extraneous_load_proxy": friction_signals,
    }


def _cli() -> int:
    import argparse

    parser = argparse.ArgumentParser(
        description="tvt-os-loop orchestrator (FR-078 staleness check + telemetry emission)"
    )
    parser.add_argument("skill_id", help="e.g., g-ops-morning")
    args = parser.parse_args()

    result = orchestrate_invocation(args.skill_id)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(_cli())
