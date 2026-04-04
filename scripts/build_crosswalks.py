"""Thin wrapper for PR-000 crosswalk and data_registry snapshot refresh."""

from __future__ import annotations

from occupational_transition.paths import repo_root
from occupational_transition.pipelines.pr000_crosswalks import run


def main() -> None:
    run(repo_root())


if __name__ == "__main__":
    main()
