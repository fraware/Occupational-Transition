"""QA for metrics/alpi_occ22_monthly.csv. Exit 1 on failure."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "metrics" / "alpi_occ22_monthly.csv"
META_PATH = ROOT / "intermediate" / "alpi_run_metadata.json"

EXPECT_COLS = [
    "month",
    "occ22_code",
    "occ22_label",
    "awes_pct",
    "demand_stress_occ_month",
    "exit_risk_12m_pct",
    "alpi_raw",
    "alpi_pct",
    "sector6_coverage_share",
    "coverage_flag_low",
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

    for c in (
        "awes_pct",
        "demand_stress_occ_month",
        "exit_risk_12m_pct",
        "alpi_raw",
        "alpi_pct",
        "sector6_coverage_share",
    ):
        if (df[c] < -1e-9).any() or (df[c] > 1 + 1e-9).any():
            errors.append(f"{c} out of [0,1]")

    if not set(df["coverage_flag_low"].unique()) <= {0, 1}:
        errors.append("coverage_flag_low must be 0 or 1")

    if df.duplicated(subset=["month", "occ22_code"]).any():
        errors.append("duplicate month x occ22_code")

    exp = (
        df["awes_pct"].astype(float)
        + df["demand_stress_occ_month"].astype(float)
        + df["exit_risk_12m_pct"].astype(float)
    ) / 3.0
    if (exp - df["alpi_raw"].astype(float)).abs().max() > 1e-6:
        errors.append("alpi_raw differs from equal-weight mean of components")

    try:
        meta = json.loads(META_PATH.read_text(encoding="utf-8"))
        for k in ("formula_version", "source_files_sha256", "generated_at_utc"):
            if k not in meta:
                errors.append(f"metadata missing {k}")
    except json.JSONDecodeError as e:
        errors.append(f"bad JSON metadata: {e}")

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("PASS qa_alpi_occ22_monthly")
    return 0


if __name__ == "__main__":
    sys.exit(main())
