"""Thin wrapper for T-016 Figure A6 (BED churn)."""

from __future__ import annotations

from occupational_transition.paths import repo_root
from occupational_transition.pipelines.figureA6_t016 import run


def main() -> None:
    run(repo_root())


if __name__ == "__main__":
    main()
