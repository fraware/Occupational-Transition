"""Thin wrapper for T-023 (AWES occ22 monthly)."""

from __future__ import annotations

from occupational_transition.paths import repo_root
from occupational_transition.pipelines.awes_occ22_monthly_t023 import run


def main() -> None:
    run(repo_root())


if __name__ == "__main__":
    main()
