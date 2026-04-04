from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
from occupational_transition.reliability import load_thresholds

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures"
INTER = ROOT / "intermediate"
DRIFT_DIR = INTER / "drift"
OUT_CSV = DRIFT_DIR / "drift_dashboard.csv"
OUT_META = DRIFT_DIR / "drift_dashboard_run_metadata.json"
SNAPSHOT_CSV = DRIFT_DIR / "current_metric_snapshot.csv"
BASELINE_CSV = DRIFT_DIR / "baseline_metric_snapshot.csv"


def _alert(delta_abs: float, unit: str, tol: dict[str, float]) -> str:
    if pd.isna(delta_abs):
        return "info"
    if unit in {"share", "percentage_points"}:
        warn = tol["share_abs_warn"]
        critical = tol["share_abs_critical"]
    elif unit in {"hours"}:
        warn = tol["hours_abs_warn"]
        critical = tol["hours_abs_critical"]
    elif unit in {"rank"}:
        warn = tol["rank_abs_warn"]
        critical = tol["rank_abs_critical"]
    else:
        warn = tol["index_points_warn"]
        critical = tol["index_points_critical"]
    if delta_abs >= critical:
        return "critical"
    if delta_abs >= warn:
        return "watch"
    return "info"


def main() -> None:
    thresholds = load_thresholds()
    tol = thresholds["drift_tolerance"]
    source_selection_mode = os.environ.get("SOURCE_SELECTION_MODE", "latest_mode")
    DRIFT_DIR.mkdir(parents=True, exist_ok=True)

    frames = []
    for name in ("memo_dashboard_kpis.csv", "virginia_memo_kpis.csv"):
        p = FIG / name
        if p.is_file():
            d = pd.read_csv(p)
            keep = [c for c in ["kpi_id", "value", "unit"] if c in d.columns]
            if len(keep) == 3:
                d = d[keep].copy()
                d["source_table"] = name
                frames.append(d)
    if not frames:
        raise FileNotFoundError("No KPI tables found for drift dashboard.")

    current = pd.concat(frames, ignore_index=True).drop_duplicates(["kpi_id"], keep="last")
    current = current.rename(columns={"value": "current_value"})
    current.to_csv(SNAPSHOT_CSV, index=False)

    if BASELINE_CSV.is_file():
        baseline = pd.read_csv(BASELINE_CSV).rename(columns={"current_value": "baseline_value"})
        merged = current.merge(
            baseline[["kpi_id", "baseline_value"]],
            on="kpi_id",
            how="left",
        )
        merged["delta_abs"] = (pd.to_numeric(merged["current_value"], errors="coerce") - pd.to_numeric(merged["baseline_value"], errors="coerce")).abs()
        merged["delta_rel"] = merged["delta_abs"] / pd.to_numeric(merged["baseline_value"], errors="coerce").abs()
        merged["alert_category"] = [
            _alert(float(a) if pd.notna(a) else float("nan"), str(u), tol)
            for a, u in zip(merged["delta_abs"], merged["unit"])
        ]
        baseline_used = True
    else:
        if source_selection_mode == "freeze_mode":
            raise RuntimeError(
                "freeze_mode requires baseline_metric_snapshot.csv for comparability."
            )
        merged = current.copy()
        merged["baseline_value"] = pd.NA
        merged["delta_abs"] = pd.NA
        merged["delta_rel"] = pd.NA
        merged["alert_category"] = "info"
        baseline_used = False
        # Seed baseline for next run in latest_mode only.
        current.to_csv(BASELINE_CSV, index=False)

    merged.to_csv(OUT_CSV, index=False)
    meta = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "output_csv": str(OUT_CSV.relative_to(ROOT)).replace("\\", "/"),
        "current_snapshot_csv": str(SNAPSHOT_CSV.relative_to(ROOT)).replace("\\", "/"),
        "baseline_snapshot_csv": str(BASELINE_CSV.relative_to(ROOT)).replace("\\", "/"),
        "baseline_used": baseline_used,
        "critical_alert_count": int((merged["alert_category"] == "critical").sum()),
        "watch_alert_count": int((merged["alert_category"] == "watch").sum()),
        "info_alert_count": int((merged["alert_category"] == "info").sum()),
        "source_selection_mode": source_selection_mode,
    }
    OUT_META.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_META}")


if __name__ == "__main__":
    main()
