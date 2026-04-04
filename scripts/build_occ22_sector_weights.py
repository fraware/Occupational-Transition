"""Thin wrapper for T-021 (occ22 sector weights)."""

from __future__ import annotations

from occupational_transition.paths import repo_root
from occupational_transition.pipelines.occ22_sector_weights_t021 import run


def main() -> None:
    run(repo_root())


if __name__ == "__main__":
    main()
