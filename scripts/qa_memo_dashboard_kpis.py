from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "figures" / "memo_dashboard_kpis.csv"

REQ = [
    "kpi_id",
    "kpi_label",
    "value",
    "unit",
    "reference_period",
    "change_value",
    "change_unit",
    "change_window",
    "source_primary",
    "source_path_or_endpoint",
    "notes_limits",
    "weighted_n",
    "effective_n",
    "cv",
    "se",
    "ci_lower",
    "ci_upper",
    "ci_level",
    "variance_method",
    "reliability_tier",
    "publish_flag",
    "suppression_reason",
    "pooling_applied",
    "evidence_directness",
]


def main() -> int:
    if not CSV.is_file():
        print(f"FAIL: missing {CSV}", file=sys.stderr)
        return 1
    d = pd.read_csv(CSV)
    miss = [c for c in REQ if c not in d.columns]
    if miss:
        print(f"FAIL: missing columns {miss}", file=sys.stderr)
        return 1
    if d["kpi_id"].duplicated().any():
        print("FAIL: duplicate kpi_id", file=sys.stderr)
        return 1
    vals = pd.to_numeric(d["value"], errors="coerce")
    if vals.isna().any():
        print("FAIL: non-numeric value column", file=sys.stderr)
        return 1
    # Some KPIs legitimately use unit=share for *differences* (can be negative) or for
    # sums of shares (can exceed 1). Restrict [0,1] checks to rate-like KPI ids.
    rate_like = d["kpi_id"].astype(str).str.endswith("_rate")
    share_rates = rate_like & d["unit"].astype(str).eq("share")
    if ((vals[share_rates] < 0) | (vals[share_rates] > 1)).any():
        print("FAIL: rate-like share KPI value outside [0,1]", file=sys.stderr)
        return 1
    allowed_directness = {"direct_published", "derived_transform", "proxy_mapping"}
    got_directness = set(d["evidence_directness"].astype(str).unique())
    if not got_directness.issubset(allowed_directness):
        print("FAIL: invalid evidence_directness", file=sys.stderr)
        return 1
    if d["publish_flag"].isna().any():
        print("FAIL: publish_flag contains NA", file=sys.stderr)
        return 1
    print("QA OK:", CSV)
    return 0


if __name__ == "__main__":
    sys.exit(main())

