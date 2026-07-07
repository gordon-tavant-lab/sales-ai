#!/usr/bin/env python3
"""Thin wrapper for the tvt-os-loop skill (T060/T061).

Delegates to gordon_os.core.orchestrator.main so the Claude Code skill
bundle stays declarative and all business logic lives in the importable
library.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT / "src"))

from gordon_os.core.orchestrator import main  # noqa: E402


if __name__ == "__main__":
    raise SystemExit(main())
