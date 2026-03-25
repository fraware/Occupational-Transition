"""QA for intermediate/btos_sector_ai_use_monthly.csv. Exit 1 on failure."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

from awes_alpi_common import SECTOR6_ORDER

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "intermediate" / "btos_sector_ai_use_monthly.csv"
META_PATH = ROOT / "intermediate" / "btos_sector_ai_use_monthly_run_metadata.json"

EXPECT_COLS = [
    "month",
    "sector6_code",
    "sector6_label",
    "btos_ai_use_share_raw",
    "btos_ai_use_share_3m",
]


def main() -> int:
    errors: list[str] = []
    if not CSV_PATH.is_file():
        errors.append(f"missing {CSV_PATH}")
    if not META_PATH.is_file():
        errors.append(f"missing {META_PATH}")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1

    df = pd.read_csv(CSV_PATH)
    if list(df.columns) != EXPECT_COLS:
        errors.append(f"columns must be {EXPECT_COLS}, got {list(df.columns)}")

    for c in ("btos_ai_use_share_raw", "btos_ai_use_share_3m"):
        if (df[c] < -1e-9).any() or (df[c] > 1 + 1e-9).any():
            errors.append(f"{c} out of [0,1]")

    for m, g in df.groupby("month"):
        got = set(g["sector6_code"].astype(str))
        if got != set(SECTOR6_ORDER):
            errors.append(f"month {m}: sectors {got} != SECTOR6")

    try:
        json.loads(META_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        errors.append(f"bad JSON metadata: {e}")

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("PASS qa_btos_sector_ai_use_monthly")
    return 0


if __name__ == "__main__":
    sys.exit(main())
