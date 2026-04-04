"""Thin wrapper for T-004 Figure 2 Panel B transition counts."""

from __future__ import annotations

from occupational_transition.paths import repo_root
from occupational_transition.pipelines.figure2_panelB_counts_t004 import run


def main() -> None:
    run(repo_root())


if __name__ == "__main__":
    main()
