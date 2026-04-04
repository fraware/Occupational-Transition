"""Thin wrapper for T-025 (CPS occ22 exit risk monthly)."""

from __future__ import annotations

from occupational_transition.paths import repo_root
from occupational_transition.pipelines.cps_occ22_exit_risk_t025 import run


def main() -> None:
    run(repo_root())


if __name__ == "__main__":
    main()
