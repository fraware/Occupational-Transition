"""Thin wrapper for T-013 Figure A3 (CPS supplement validation)."""

from __future__ import annotations

from occupational_transition.paths import repo_root
from occupational_transition.pipelines.figureA3_t013 import run


def main() -> None:
    run(repo_root())


if __name__ == "__main__":
    main()
