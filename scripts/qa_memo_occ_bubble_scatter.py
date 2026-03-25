"""
QA for figures/memo_occ_bubble_scatter.csv.

Enforces:
- Required columns present
- ai_relevance_tercile in {low, middle, high}
- Non-negative and finite numeric fields
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "figures" / "memo_occ_bubble_scatter.csv"

REQUIRED_COLS = [
    "occupation_group",
    "employment",
    "employment_share",
    "median_annual_wage",
    "ai_task_index",
    "ai_relevance_tercile",
]


def main() -> int:
    if not CSV.is_file():
        print(f"FAIL: missing {CSV}", file=sys.stderr)
        return 1
    df = pd.read_csv(CSV)
    missing = [c for c in REQUIRED_COLS if c not in df.columns]
    if missing:
        print(f"FAIL: missing columns {missing}", file=sys.stderr)
        return 1

    allowed = {"low", "middle", "high"}
    bad = sorted(set(df["ai_relevance_tercile"].astype(str)) - allowed)
    if bad:
        print(f"FAIL: unexpected ai_relevance_tercile values: {bad}", file=sys.stderr)
        return 1

    for col in ("employment", "employment_share", "median_annual_wage", "ai_task_index"):
        v = pd.to_numeric(df[col], errors="coerce")
        if v.isna().any():
            print(f"FAIL: NaNs in numeric column {col}", file=sys.stderr)
            return 1
    for col in ("employment", "employment_share", "median_annual_wage"):
        v = pd.to_numeric(df[col], errors="coerce")
        if (v < 0).any():
            print(f"FAIL: negative values in {col}", file=sys.stderr)
            return 1

    if df["occupation_group"].astype(str).str.strip().eq("").any():
        print("FAIL: empty occupation_group labels", file=sys.stderr)
        return 1

    print("QA OK:", CSV)
    return 0


if __name__ == "__main__":
    sys.exit(main())

