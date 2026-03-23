"""Shared helpers for robustness logs under intermediate/robustness/."""

from __future__ import annotations

import datetime as dt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ROB_DIR = ROOT / "intermediate" / "robustness"


def ensure_rob_dir() -> Path:
    ROB_DIR.mkdir(parents=True, exist_ok=True)
    return ROB_DIR


def write_report(name: str, body: str) -> Path:
    ensure_rob_dir()
    p = ROB_DIR / name
    header = (
        f"# {name}\n\n"
        f"- Generated UTC: {dt.datetime.now(dt.timezone.utc).isoformat()}\n\n"
    )
    p.write_text(header + body + "\n", encoding="utf-8")
    return p
