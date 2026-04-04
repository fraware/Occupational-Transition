"""Thin wrapper for T-020 Figure A10 (NLS long-run)."""

from __future__ import annotations

from occupational_transition.paths import repo_root
from occupational_transition.pipelines.figureA10_t020 import run


def main() -> None:
    run(repo_root())


if __name__ == "__main__":
    main()
