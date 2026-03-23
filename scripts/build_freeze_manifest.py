"""
Write intermediate/freeze_manifest.json with SHA-256 hashes of key outputs.

Does not require network access. Intended for results-freeze documentation.

Usage:
    python scripts/build_freeze_manifest.py
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INTER = ROOT / "intermediate"
OUT = INTER / "freeze_manifest.json"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    INTER.mkdir(parents=True, exist_ok=True)

    figures = sorted((ROOT / "figures").glob("*.csv"))
    meta = sorted(INTER.glob("*run_metadata.json"))
    visual_man = INTER / "visuals_run_manifest.json"

    payload: dict[str, object] = {
        "generated_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "figures": {},
        "intermediate_run_metadata": {},
        "visuals_run_manifest": None,
    }

    for p in figures:
        rel = p.relative_to(ROOT).as_posix()
        payload["figures"][rel] = sha256_file(p) if p.is_file() else None

    for p in meta:
        rel = p.relative_to(ROOT).as_posix()
        payload["intermediate_run_metadata"][rel] = sha256_file(p) if p.is_file() else None

    if visual_man.is_file():
        payload["visuals_run_manifest"] = {
            "path": visual_man.relative_to(ROOT).as_posix(),
            "sha256": sha256_file(visual_man),
        }

    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Wrote {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
