"""Load config/paper_scope.toml (paper vs library boundaries)."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

from occupational_transition.paths import repo_root


def load_paper_scope(root: Path | None = None) -> dict[str, Any]:
    root = root if root is not None else repo_root()
    path = root / "config" / "paper_scope.toml"
    with path.open("rb") as f:
        return tomllib.load(f)
