"""Thin wrapper for T-003 Figure 2 Panel A (CPS hours by AI tercile)."""

from __future__ import annotations

from occupational_transition.paths import repo_root
from occupational_transition.pipelines.figure2_panelA_t003 import run


def main() -> None:
    run(repo_root())


if __name__ == "__main__":
    main()
