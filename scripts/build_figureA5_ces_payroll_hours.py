"""Thin wrapper for T-015 Figure A5 (CES payroll and hours)."""

from __future__ import annotations

from occupational_transition.paths import repo_root
from occupational_transition.pipelines.figureA5_t015 import run


def main() -> None:
    run(repo_root())


if __name__ == "__main__":
    main()
