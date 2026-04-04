"""Thin wrapper for T-009 Figure 4 Panel B CES sector index."""

from __future__ import annotations

from occupational_transition.paths import repo_root
from occupational_transition.pipelines.figure4_panelB_t009 import run


def main() -> None:
    run(repo_root())


if __name__ == "__main__":
    main()
