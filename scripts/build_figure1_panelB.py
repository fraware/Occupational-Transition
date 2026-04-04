"""
Build Figure 1 Panel B (T-002).

Core implementation: ``occupational_transition.pipelines.figure1_panelB_t002``.

Run from repo root:

    python scripts/build_figure1_panelB.py
    python scripts/build_figure1_panelB.py --onet-version 30.2

``run_step`` / ``ot run`` use default O*NET version unless env ``OT_ONET_VERSION`` is set.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

if str(Path(__file__).resolve().parents[1] / "src") not in sys.path:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from occupational_transition.paths import repo_root
from occupational_transition.pipelines.figure1_panelB_t002 import run


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--onet-version",
        default="30.2",
        help="O*NET database version (sets OT_ONET_VERSION for this process).",
    )
    args = parser.parse_args()
    os.environ["OT_ONET_VERSION"] = args.onet_version
    run(repo_root())


if __name__ == "__main__":
    main()
