from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_thresholds(path: Path | None = None) -> dict[str, Any]:
    """Load reliability thresholds JSON.

    When ``path`` is omitted, uses ``repo_root() / "config" / "reliability_thresholds.json"``.
    """
    if path is None:
        from occupational_transition.paths import repo_root

        cfg_path = repo_root() / "config" / "reliability_thresholds.json"
    else:
        cfg_path = path
    if not cfg_path.is_file():
        raise FileNotFoundError(f"Missing reliability config: {cfg_path}")
    return json.loads(cfg_path.read_text(encoding="utf-8"))
