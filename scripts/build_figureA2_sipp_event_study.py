"""Thin wrapper for T-012 Figure A2 (SIPP event study)."""

from __future__ import annotations

from occupational_transition.paths import repo_root
from occupational_transition.pipelines.figureA2_t012 import run


def main() -> None:
    run(repo_root())


if __name__ == "__main__":
    main()
