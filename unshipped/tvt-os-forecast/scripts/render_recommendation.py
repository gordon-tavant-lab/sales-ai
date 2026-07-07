#!/usr/bin/env python3
"""Map an MCTS solution leaf onto the pack's `output_template` (T121).

Takes a JSON solution dict (as produced by `tvt-core-mcts` via
`invoke_g_core_mcts.py`) and renders the active pack's Jinja2
`output_template.md.j2` against it. Outputs Markdown to stdout.

The mapping convention:

  - `ranked_actions[0]` becomes `recommendation.primary_action`.
  - `ranked_actions[1:]` become `recommendation.alternatives`.
  - `best_leaf.state` becomes `recommendation.terminal_state`.
  - `stats` becomes `recommendation.search_stats`.
  - `eval_floor` becomes `recommendation.eval_floor`.

Pack templates that opt out can simply reference whichever subset of the
fields they care about; missing fields render to empty strings.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT / "src"))


def build_recommendation(solution: dict, *, brief_id: str | None = None,
                         pack_name: str | None = None) -> dict:
    """Translate tvt-core-mcts solution into the recommendation context dict."""
    ranked = list(solution.get("ranked_actions", []))
    primary = ranked[0] if ranked else None
    return {
        "brief_id": brief_id,
        "pack": pack_name,
        "primary_action": primary,
        "alternatives": ranked[1:],
        "terminal_state": solution.get("best_leaf", {}).get("state", {}),
        "search_stats": solution.get("stats", {}),
        "eval_floor": solution.get("eval_floor", {}),
        "problem_id": solution.get("problem_id"),
    }


def render_with_pack(template_path: Path, recommendation: dict) -> str:
    """Render the Jinja2 template — best effort, with a fallback markdown body."""
    try:
        import jinja2
    except ImportError:
        return _fallback_markdown(recommendation)
    if not template_path.exists():
        return _fallback_markdown(recommendation)
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(str(template_path.parent)),
        autoescape=False,
        keep_trailing_newline=True,
    )
    tmpl = env.get_template(template_path.name)
    return tmpl.render(recommendation=recommendation, **recommendation)


def _fallback_markdown(rec: dict) -> str:
    """Domain-neutral fallback when the pack template is missing or jinja2 is unavailable."""
    primary = rec.get("primary_action") or {}
    alts = rec.get("alternatives", [])
    pack = rec.get("pack") or "(no-pack)"
    brief_id = rec.get("brief_id") or "(no-brief)"
    lines = [
        f"# Forecast Recommendation",
        "",
        f"**Pack**: {pack}",
        f"**Brief**: {brief_id}",
        f"**Problem**: {rec.get('problem_id')}",
        "",
        f"## Primary action",
        f"- `{primary.get('action_id', 'unknown')}` (expected_reward={primary.get('expected_reward', 0):.3f}, visits={primary.get('visits', 0)})",
        "",
        f"## Alternatives ({len(alts)})",
    ]
    for a in alts:
        lines.append(
            f"- `{a.get('action_id', '?')}` "
            f"(reward={a.get('expected_reward', 0):.3f}, visits={a.get('visits', 0)})"
        )
    lines.extend([
        "",
        "## Search stats",
        f"```json",
        json.dumps(rec.get("search_stats", {}), indent=2, default=str),
        "```",
        "",
        "## Eval floor",
        f"```json",
        json.dumps(rec.get("eval_floor", {}), indent=2, default=str),
        "```",
        "",
    ])
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(prog="render_recommendation")
    parser.add_argument("--solution", help="Path to solution JSON; default reads stdin.")
    parser.add_argument("--template", help="Path to pack output_template.md.j2 (optional).")
    parser.add_argument("--brief-id")
    parser.add_argument("--pack")
    args = parser.parse_args(argv)

    if args.solution:
        solution = json.loads(Path(args.solution).read_text(encoding="utf-8"))
    else:
        solution = json.loads(sys.stdin.read())

    rec = build_recommendation(
        solution, brief_id=args.brief_id, pack_name=args.pack,
    )

    if args.template:
        body = render_with_pack(Path(args.template), rec)
    else:
        body = _fallback_markdown(rec)

    sys.stdout.write(body)
    if not body.endswith("\n"):
        sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
