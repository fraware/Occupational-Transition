"""Thin wrapper for T-017 Figure A7 (QCEW state benchmark)."""

from __future__ import annotations

from occupational_transition.paths import repo_root
from occupational_transition.pipelines.figureA7_t017 import run


def main() -> None:
    run(repo_root())


if __name__ == "__main__":
    main()
