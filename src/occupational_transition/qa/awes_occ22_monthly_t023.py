"""Ticket QA (from scripts/qa_awes_occ22_monthly.py)."""

from __future__ import annotations

import json
import sys

import pandas as pd

from occupational_transition.paths import repo_root

EXPECT_COLS = [
    "month",
    "occ22_code",
    "occ22_label",
    "exposure_pct",
    "adoption_mix_occ_month",
    "awes_raw",
    "awes_pct",
    "sector6_coverage_share",
    "coverage_flag_low",
]


def main() -> int:
    root = repo_root()
    CSV_PATH = root / "metrics" / "awes_occ22_monthly.csv"
    META_PATH = root / "intermediate" / "awes_run_metadata.json"
    BTOS_PATH = root / "intermediate" / "btos_sector_ai_use_monthly.csv"
    errors: list[str] = []
    for p in (CSV_PATH, META_PATH, BTOS_PATH):
        if not p.is_file():
            errors.append(f"missing {p}")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1

    df = pd.read_csv(CSV_PATH)
    if list(df.columns) != EXPECT_COLS:
        errors.append(f"columns must be {EXPECT_COLS}, got {list(df.columns)}")

    for c in (
        "exposure_pct",
        "adoption_mix_occ_month",
        "awes_raw",
        "awes_pct",
        "sector6_coverage_share",
    ):
        if (df[c] < -1e-9).any() or (df[c] > 1 + 1e-9).any():
            errors.append(f"{c} out of [0,1]")

    if not set(df["coverage_flag_low"].unique()) <= {0, 1}:
        errors.append("coverage_flag_low must be 0 or 1")

    btos = pd.read_csv(BTOS_PATH)
    start = str(btos["month"].min())
    sub = df[df["month"] >= start]
    exp_n = 22 * sub["month"].nunique()
    if len(sub) != exp_n:
        errors.append(
            f"after BTOS start {start}: expected {exp_n} rows (22 x months), "
            f"got {len(sub)}"
        )

    for m, g in sub.groupby("month"):
        if len(g) != 22:
            errors.append(f"month {m}: expected 22 occupations, got {len(g)}")

    try:
        meta = json.loads(META_PATH.read_text(encoding="utf-8"))
        req = ("formula_version", "source_files_sha256", "generated_at_utc")
        for k in req:
            if k not in meta:
                errors.append(f"metadata missing {k}")
    except json.JSONDecodeError as e:
        errors.append(f"bad JSON metadata: {e}")

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("PASS qa_awes_occ22_monthly")
    return 0


if __name__ == "__main__":
    sys.exit(main())
