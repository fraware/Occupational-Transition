"""Thin wrapper for T-018 Figure A8 (LEHD benchmark)."""

from __future__ import annotations

from occupational_transition.paths import repo_root
from occupational_transition.pipelines.figureA8_t018 import run


def main() -> None:
    run(repo_root())


if __name__ == "__main__":
    main()
