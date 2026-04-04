"""Thin wrapper for T-019 Figure A9 (ACS local composition)."""

from __future__ import annotations

from occupational_transition.paths import repo_root
from occupational_transition.pipelines.figureA9_t019 import run


def main() -> None:
    run(repo_root())


if __name__ == "__main__":
    main()
