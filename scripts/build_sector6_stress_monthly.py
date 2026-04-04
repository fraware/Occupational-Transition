"""Thin wrapper for T-024 (sector6 stress monthly)."""

from __future__ import annotations

from occupational_transition.paths import repo_root
from occupational_transition.pipelines.sector6_stress_monthly_t024 import run


def main() -> None:
    run(repo_root())


if __name__ == "__main__":
    main()
