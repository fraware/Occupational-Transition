"""Ticket QA (from scripts/qa_sector6_stress_monthly.py)."""

from __future__ import annotations

import json
import sys

import pandas as pd

from occupational_transition.paths import repo_root

EXPECT_COLS = [
    "month",
    "sector6_code",
    "sector6_label",
    "jolts_openings_rate",
    "jolts_hires_rate",
    "jolts_layoffs_rate",
    "jolts_stress_raw",
    "jolts_stress_pct",
    "ces_payroll_employment",
    "ces_payroll_contraction_12m_raw",
    "ces_payroll_contraction_12m_pct",
    "sector_stress_pct",
]


def main() -> int:
    root = repo_root()
    CSV_PATH = root / "intermediate" / "sector6_stress_monthly.csv"
    META_PATH = root / "intermediate" / "sector6_stress_monthly_run_metadata.json"
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
        "jolts_stress_pct",
        "ces_payroll_contraction_12m_pct",
        "sector_stress_pct",
    ):
        sub = df[c].dropna()
        if ((sub < -1e-9) | (sub > 1 + 1e-9)).any():
            errors.append(f"{c} out of [0,1] (non-null)")

    if df.duplicated(subset=["month", "sector6_code"]).any():
        errors.append("duplicate month x sector6_code")

    try:
        json.loads(META_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        errors.append(f"bad JSON metadata: {e}")

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("PASS qa_sector6_stress_monthly")
    return 0


if __name__ == "__main__":
    sys.exit(main())
