"""Thin wrapper for T-014 Figure A4 (ABS structural adoption)."""

from __future__ import annotations

from occupational_transition.paths import repo_root
from occupational_transition.pipelines.figureA4_t014 import run


def main() -> None:
    run(repo_root())


if __name__ == "__main__":
    main()
