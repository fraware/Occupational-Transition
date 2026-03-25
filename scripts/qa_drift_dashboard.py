from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT_CSV = ROOT / "intermediate" / "drift" / "drift_dashboard.csv"
OUT_META = ROOT / "intermediate" / "drift" / "drift_dashboard_run_metadata.json"


def main() -> int:
    if not OUT_CSV.is_file():
        print(f"FAIL: missing {OUT_CSV}", file=sys.stderr)
        return 1
    if not OUT_META.is_file():
        print(f"FAIL: missing {OUT_META}", file=sys.stderr)
        return 1
    d = pd.read_csv(OUT_CSV)
    req = {
        "kpi_id",
        "current_value",
        "unit",
        "baseline_value",
        "delta_abs",
        "delta_rel",
        "alert_category",
    }
    if not req.issubset(set(d.columns)):
        print("FAIL: drift dashboard missing required columns", file=sys.stderr)
        return 1
    bad_alerts = set(d["alert_category"].astype(str).unique()) - {"info", "watch", "critical"}
    if bad_alerts:
        print(f"FAIL: invalid alert categories {sorted(bad_alerts)}", file=sys.stderr)
        return 1
    meta = json.loads(OUT_META.read_text(encoding="utf-8"))
    if meta.get("source_selection_mode") not in {"latest_mode", "freeze_mode"}:
        print("FAIL: invalid source_selection_mode in drift metadata", file=sys.stderr)
        return 1
    if int((d["alert_category"] == "critical").sum()) != int(meta.get("critical_alert_count", -1)):
        print("FAIL: critical alert count mismatch in metadata", file=sys.stderr)
        return 1
    if int((d["alert_category"] == "critical").sum()) > 0:
        print("FAIL: critical drift alerts present", file=sys.stderr)
        return 1
    print("QA OK: drift_dashboard")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
