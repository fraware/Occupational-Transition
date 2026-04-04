"""Ticket QA (from scripts/qa_occ22_sector_weights.py)."""

from __future__ import annotations

import json
import sys

import pandas as pd

from occupational_transition.paths import repo_root

EXPECT_COLS = [
    "occ22_code",
    "occ22_label",
    "sector6_code",
    "sector6_label",
    "oews_occ_sector_employment",
    "oews_occ_total_employment",
    "sector_weight",
    "sector6_coverage_share",
    "coverage_flag_low",
]

SUM_TOL = 1e-6


def main() -> int:
    root = repo_root()
    CSV_PATH = root / "intermediate" / "occ22_sector_weights.csv"
    META_PATH = root / "intermediate" / "occ22_sector_weights_run_metadata.json"
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

    if len(df) != 22 * 6:
        errors.append(f"expected 132 rows (22x6), got {len(df)}")

    for c in ("sector_weight", "sector6_coverage_share"):
        if (df[c] < 0 - 1e-12).any() or (df[c] > 1 + 1e-12).any():
            errors.append(f"{c} out of [0,1]")

    for occ, g in df.groupby("occ22_code"):
        s = float(g["sector_weight"].sum())
        emp_sum = float(g["oews_occ_sector_employment"].sum())
        if emp_sum > 0 and abs(s - 1.0) > SUM_TOL:
            errors.append(f"{occ}: sector_weight sum {s}, expected 1")
        if emp_sum == 0 and abs(s) > SUM_TOL:
            errors.append(f"{occ}: zero employment in S6 but weights sum {s}")

        cov = g["sector6_coverage_share"].astype(float).unique()
        if len(cov) != 1:
            errors.append(f"{occ}: inconsistent coverage")
        cf = g["coverage_flag_low"].astype(int).unique()
        if len(cf) != 1:
            errors.append(f"{occ}: inconsistent coverage_flag_low")
        if (cov[0] < 0.60) != bool(cf[0]):
            errors.append(f"{occ}: coverage_flag_low mismatch with threshold 0.60")

    try:
        json.loads(META_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        errors.append(f"bad JSON metadata: {e}")

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("PASS qa_occ22_sector_weights")
    return 0


if __name__ == "__main__":
    sys.exit(main())
