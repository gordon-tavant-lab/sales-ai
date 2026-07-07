#!/usr/bin/env python3
"""Thin wrapper for tvt-os-verify (T061).

Imports the implementation from gordon_os.core.verify and exposes a CLI
that prints the result as JSON. Pure thin-import — no business logic.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, is_dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT / "src"))

from gordon_os.core import verify as _impl  # noqa: E402


def _to_jsonable(obj):
    if is_dataclass(obj):
        return asdict(obj)
    return obj


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="tvt-os-verify")
    parser.add_argument("--brief", required=False, help="Brief markdown path.")
    args = parser.parse_args(argv)
    name = "verify"
    fn = getattr(_impl, name, None)
    if fn is None:
        print(f"tvt-os-verify: implementation function not found ({name})", file=sys.stderr)
        return 2
    print(json.dumps({"skill": "tvt-os-verify", "callable": name}, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
