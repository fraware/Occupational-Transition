"""Thin wrapper for T-010 Figure 5 capability matrix."""

from __future__ import annotations

from occupational_transition.paths import repo_root
from occupational_transition.pipelines.figure5_capability_t010 import (
    _CAPABILITY,
    DATASET_ORDER,
    EMPIRICAL_OBJECT_KEYS,
    OUT_COLS,
    run,
)

__all__ = [
    "DATASET_ORDER",
    "EMPIRICAL_OBJECT_KEYS",
    "OUT_COLS",
    "_CAPABILITY",
    "main",
    "run",
]


def main() -> None:
    run(repo_root())


if __name__ == "__main__":
    main()
