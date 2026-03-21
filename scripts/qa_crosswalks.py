"""
QA checks for PR-000 crosswalk outputs. Exit code 1 on failure.

Usage: python scripts/qa_crosswalks.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    occ_path = ROOT / "crosswalks" / "occ22_crosswalk.csv"
    sec_path = ROOT / "crosswalks" / "sector6_crosswalk.csv"
    reg_path = ROOT / "docs" / "data_registry.csv"

    errors: list[str] = []

    o = pd.read_csv(occ_path)
    dup_occ = o.duplicated(subset=["source_system", "source_occ_code"]).any()
    if dup_occ:
        errors.append(
            "occ22_crosswalk: duplicate (source_system, source_occ_code)"
        )

    prdt = o[o["source_system"] == "CPS_PRDTOCC1"]
    if len(prdt) != 23:
        errors.append(f"occ22: expected 23 PRDTOCC1 rows, got {len(prdt)}")
    for i in range(1, 23):
        row = prdt[prdt["source_occ_code"].astype(str) == str(i)]
        if row.empty or str(row.iloc[0]["occ22_id"]) == "":
            errors.append(f"occ22: PRDTOCC1={i} missing occ22_id")
    mil = prdt[prdt["source_occ_code"].astype(str) == "23"]
    if mil.empty:
        errors.append("occ22: PRDTOCC1=23 (Armed Forces) missing")
    else:
        mil_ex = str(mil.iloc[0]["is_military_excluded"]).lower()
        if mil_ex not in ("true", "1"):
            errors.append(
                "occ22: PRDTOCC1=23 should be is_military_excluded true"
            )

    s = pd.read_csv(sec_path)
    dup_sec = s.duplicated(subset=["source_program", "source_code"]).any()
    if dup_sec:
        errors.append(
            "sector6_crosswalk: duplicate (source_program, source_code)"
        )

    # In-scope rows must have sector6_code
    ins = s[s["is_in_scope"].astype(str) == "1"]
    empty_code = ins["sector6_code"].isna() | (
        ins["sector6_code"].astype(str) == ""
    )
    bad = ins[empty_code]
    if len(bad) > 0:
        msg = f"sector6: {len(bad)} in-scope rows missing sector6_code"
        errors.append(msg)

    r = pd.read_csv(reg_path)
    required_cols = [
        "dataset_id",
        "source_url",
        "snapshot_download_date",
    ]
    for c in required_cols:
        if c not in r.columns:
            errors.append(f"data_registry: missing column {c}")

    if errors:
        for e in errors:
            print(f"FAIL: {e}", file=sys.stderr)
        return 1

    print(
        "QA OK: occ22_crosswalk.csv, sector6_crosswalk.csv, data_registry.csv"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
