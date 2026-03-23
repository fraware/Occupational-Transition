"""Utility helpers for visual rendering scripts."""

from __future__ import annotations

import hashlib
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
FIG_DIR = ROOT / "figures"

TERCILE_ORDER = ["low", "middle", "high"]


def read_figure_csv(name: str) -> pd.DataFrame:
    path = FIG_DIR / name
    if not path.is_file():
        raise FileNotFoundError(f"missing figure CSV: {path}")
    return pd.read_csv(path)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            block = f.read(1 << 20)
            if not block:
                break
            h.update(block)
    return h.hexdigest()


def fmt_pct(x: float) -> str:
    return f"{x * 100:.1f}%"


def parse_month_col(df: pd.DataFrame, col: str = "month") -> pd.Series:
    return pd.to_datetime(df[col], format="%Y-%m", errors="coerce")
