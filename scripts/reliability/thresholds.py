from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PATH = ROOT / "config" / "reliability_thresholds.json"


def load_thresholds(path: Path | None = None) -> dict[str, Any]:
    cfg_path = path or DEFAULT_PATH
    if not cfg_path.is_file():
        raise FileNotFoundError(f"Missing reliability config: {cfg_path}")
    return json.loads(cfg_path.read_text(encoding="utf-8"))
