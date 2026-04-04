"""Thin wrapper for T-007 Figure 3 Panel B BTOS workforce effects."""

from __future__ import annotations

from occupational_transition.paths import repo_root
from occupational_transition.pipelines.figure3_panelB_t007 import run


def main() -> None:
    run(repo_root())


if __name__ == "__main__":
    main()
