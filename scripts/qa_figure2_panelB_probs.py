"""
QA for Figure 2 Panel B transition probabilities (T-005). Exit 1 on failure.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FIG_CSV = ROOT / "figures" / "figure2_panelB_transition_probs.csv"
META_JSON = ROOT / "intermediate" / "figure2_panelB_probs_run_metadata.json"
COUNTS_META = ROOT / "intermediate" / "figure2_panelB_counts_run_metadata.json"

EXP_COLS = [
    "month",
    "origin_state",
    "record_type",
    "destination_state",
    "weighted_transition_count",
    "origin_mass",
    "transition_probability",
    "metric_name",
    "metric_value",
]

RECORD_MATRIX = "matrix"
RECORD_SUMMARY = "summary"

SUMMARY_METRICS = (
    "retention_rate",
    "occ_switch_rate",
    "unemployment_entry_rate",
    "nilf_entry_rate",
)

ROW_SUM_TOLERANCE = 1e-9

OCC_PREFIX = "occ22_"


def _is_occ(s: str) -> bool:
    return str(s).startswith(OCC_PREFIX)


def main() -> int:
    errors: list[str] = []

    if not FIG_CSV.is_file():
        errors.append(f"missing output: {FIG_CSV}")
        return _report(errors)

    df = pd.read_csv(FIG_CSV)
    if list(df.columns) != EXP_COLS:
        errors.append(f"columns must be {EXP_COLS}, got {list(df.columns)}")

    req = {"month", "origin_state", "record_type"}
    for c in req:
        if c in df.columns and df[c].isna().any():
            errors.append(f"NaN in required column {c}")

    mat = df[df["record_type"] == RECORD_MATRIX].copy()
    summ = df[df["record_type"] == RECORD_SUMMARY].copy()

    if mat.empty:
        errors.append("no matrix rows")

    # Matrix row checks
    if not mat.empty:
        bad_dest = mat["destination_state"].isna() | (
            mat["destination_state"] == ""
        )
        if bad_dest.any():
            errors.append("matrix rows must have destination_state")
        if mat["transition_probability"].isna().any():
            errors.append("NaN in matrix transition_probability")
        if mat["origin_mass"].isna().any():
            errors.append("NaN in matrix origin_mass")
        if mat["weighted_transition_count"].isna().any():
            errors.append("NaN in matrix weighted_transition_count")
        low = mat["transition_probability"].min()
        high = mat["transition_probability"].max()
        if low < -ROW_SUM_TOLERANCE or high > 1.0 + ROW_SUM_TOLERANCE:
            errors.append(
                "matrix transition_probability out of [0,1]: "
                f"min={low} max={high}"
            )

        dup = mat.duplicated(
            ["month", "origin_state", "destination_state"],
            keep=False,
        )
        if dup.any():
            errors.append("duplicate matrix month x origin_state x destination_state")

        sums = mat.groupby(["month", "origin_state"], sort=False)[
            "transition_probability"
        ].sum()
        bad = sums[np.abs(sums - 1.0) > ROW_SUM_TOLERANCE]
        if not bad.empty:
            errors.append(
                "matrix row probabilities must sum to 1 per month x "
                f"origin_state (first bad): {bad.head().to_dict()}"
            )

    # Summary row checks
    if not summ.empty:
        if summ["metric_name"].isna().any():
            errors.append("NaN in summary metric_name")
        bad_m = set(summ["metric_name"].unique()) - set(SUMMARY_METRICS)
        if bad_m:
            errors.append(
                f"invalid summary metric_name values: {sorted(bad_m)}"
            )
        dup_s = summ.duplicated(
            ["month", "origin_state", "metric_name"],
            keep=False,
        )
        if dup_s.any():
            errors.append("duplicate summary month x origin_state x metric_name")

        for _, row in summ.iterrows():
            name = str(row["metric_name"])
            val = row["metric_value"]
            origin = str(row["origin_state"])
            if name == "occ_switch_rate" and not _is_occ(origin):
                if not pd.isna(val):
                    errors.append(
                        "occ_switch_rate must be NA for non-occ origin "
                        f"{origin} at {row['month']}"
                    )
            elif not pd.isna(val):
                v = float(val)
                if v < -ROW_SUM_TOLERANCE or v > 1.0 + ROW_SUM_TOLERANCE:
                    errors.append(
                        f"summary {name} out of [0,1] at "
                        f"{row['month']} {origin}: {v}"
                    )

    if str(df["month"].min()) != "2019-01":
        errors.append(
            f"series must start at 2019-01, got {df['month'].min()}"
        )

    if not META_JSON.is_file():
        errors.append(f"missing metadata: {META_JSON}")
    else:
        meta = json.loads(META_JSON.read_text(encoding="utf-8"))
        dep = meta.get("dependency_t004") or {}
        if not dep.get("counts_csv_sha256"):
            errors.append("metadata missing dependency_t004.counts_csv_sha256")

    if COUNTS_META.is_file() and not df.empty:
        cmeta = json.loads(COUNTS_META.read_text(encoding="utf-8"))
        pairs = cmeta.get("pairs") or []
        origin_months = {
            str(p.get("origin_month")) for p in pairs if p.get("origin_month")
        }
        months_mat = set(mat["month"].astype(str).unique())
        unexpected = sorted(months_mat - origin_months)
        if unexpected:
            errors.append(
                "matrix origin months not in T-004 pair origins "
                f"(sample): {unexpected[:5]}"
            )

    return _report(errors)


def _report(errors: list[str]) -> int:
    if errors:
        print("QA failures:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1
    print("QA OK: figure2_panelB_transition_probs.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
