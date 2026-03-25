"""QA for intermediate/cps_occ22_exit_risk_monthly.csv. Exit 1 on failure."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "intermediate" / "cps_occ22_exit_risk_monthly.csv"
META_PATH = ROOT / "intermediate" / "cps_occ22_exit_risk_monthly_run_metadata.json"

EXPECT_COLS = [
    "month",
    "occ22_code",
    "occ22_label",
    "exit_risk_12m_raw",
    "exit_risk_12m_pct",
    "origin_mass_12m",
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

    sub = df["exit_risk_12m_pct"].dropna()
    if ((sub < -1e-9) | (sub > 1 + 1e-9)).any():
        errors.append("exit_risk_12m_pct out of [0,1]")

    raw = df["exit_risk_12m_raw"].dropna()
    if ((raw < -1e-9) | (raw > 1 + 1e-9)).any():
        errors.append("exit_risk_12m_raw out of [0,1] for non-null")

    if df.duplicated(subset=["month", "occ22_code"]).any():
        errors.append("duplicate month x occ22_code")

    try:
        json.loads(META_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        errors.append(f"bad JSON metadata: {e}")

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("PASS qa_cps_occ22_exit_risk_monthly")
    return 0


if __name__ == "__main__":
    sys.exit(main())
