from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "figures" / "memo_btos_state_ai_use_latest.csv"


def main() -> int:
    if not CSV.is_file():
        print(f"FAIL: missing {CSV}", file=sys.stderr)
        return 1
    d = pd.read_csv(CSV)
    req = [
        "state_abbrev",
        "ai_use_current_rate",
        "btos_period_id",
        "strata_type",
        "missing_ai_current_rate",
        "missing_reason",
    ]
    missing_cols = [c for c in req if c not in d.columns]
    if missing_cols:
        print(f"FAIL: missing columns {missing_cols}", file=sys.stderr)
        return 1
    if d["state_abbrev"].duplicated().any():
        print("FAIL: duplicate state_abbrev", file=sys.stderr)
        return 1
    flag = pd.to_numeric(d["missing_ai_current_rate"], errors="coerce")
    if flag.isna().any() or not set(flag.dropna().unique()).issubset({0, 1}):
        print("FAIL: invalid missing_ai_current_rate", file=sys.stderr)
        return 1

    allowed_reasons = {"published", "fetch_failed", "no_ai_current_yes_row"}
    if not set(d["missing_reason"].astype(str)).issubset(allowed_reasons):
        bad = set(d["missing_reason"].astype(str)) - allowed_reasons
        print(f"FAIL: invalid missing_reason values: {sorted(bad)}", file=sys.stderr)
        return 1
    pub = d["missing_reason"].astype(str).eq("published")
    if not (pub == flag.eq(0)).all():
        print("FAIL: missing_reason must be published iff missing_ai_current_rate==0", file=sys.stderr)
        return 1

    v = pd.to_numeric(d["ai_use_current_rate"], errors="coerce")
    ok = flag.eq(0)
    if v[ok].isna().any():
        print("FAIL: NaN ai_use_current_rate where missing_ai_current_rate==0", file=sys.stderr)
        return 1
    if ((v[ok] < 0) | (v[ok] > 1)).any():
        print("FAIL: ai_use_current_rate outside [0,1] for published rows", file=sys.stderr)
        return 1
    print("QA OK:", CSV)
    return 0


if __name__ == "__main__":
    sys.exit(main())

