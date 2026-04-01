"""
Run strict ticket-by-ticket rebuild + QA with checkpoints and log.

Usage:
    python scripts/run_full_clean_rebuild_acceptance.py
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from occupational_transition.manifests import FULL_REBUILD_STEPS, post_gates  # noqa: E402
from occupational_transition.orchestration import run_acceptance_steps  # noqa: E402


def main() -> int:
    env = {
        "PYTHONWARNINGS": ",".join(
            [
                "error::FutureWarning",
                "error::pandas.errors.SettingWithCopyWarning",
            ]
        )
    }
    source_mode = os.environ.get("SOURCE_SELECTION_MODE")
    if source_mode:
        env["SOURCE_SELECTION_MODE"] = source_mode
    return run_acceptance_steps(
        root=ROOT,
        steps=FULL_REBUILD_STEPS,
        gates=post_gates(ROOT),
        env_overrides=env,
    )


if __name__ == "__main__":
    sys.exit(main())
