"""Thin wrapper for T-022 (BTOS sector AI use monthly)."""

from __future__ import annotations

from occupational_transition.paths import repo_root
from occupational_transition.pipelines.btos_sector_ai_use_t022 import run


def main() -> None:
    run(repo_root())


if __name__ == "__main__":
    main()
