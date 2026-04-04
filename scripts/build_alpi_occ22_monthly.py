"""Thin wrapper for T-026 (ALPI occ22 monthly)."""

from __future__ import annotations

from occupational_transition.paths import repo_root
from occupational_transition.pipelines.alpi_occ22_monthly_t026 import run


def main() -> None:
    run(repo_root())


if __name__ == "__main__":
    main()
