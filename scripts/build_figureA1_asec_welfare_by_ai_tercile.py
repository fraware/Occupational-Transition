"""Thin wrapper for T-011 Figure A1 (CPS ASEC welfare by AI tercile)."""

from __future__ import annotations

from occupational_transition.paths import repo_root
from occupational_transition.pipelines.figureA1_t011 import run


def main() -> None:
    run(repo_root())


if __name__ == "__main__":
    main()
