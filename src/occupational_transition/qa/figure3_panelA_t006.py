"""QA for Figure 3 Panel A BTOS AI trends (T-006)."""

from __future__ import annotations

import json
import sys

import pandas as pd

from occupational_transition.paths import repo_root

EXP_COLS = [
    "period_start_date",
    "btos_period_id",
    "ai_use_current_rate",
    "ai_use_expected_6m_rate",
    "source_series_id",
    "evidence_directness",
]

MIN_PERIOD_START = "2023-08-28"
RATE_TOLERANCE = 1e-9


def main() -> int:
    root = repo_root()
    fig_csv = root / "figures" / "figure3_panelA_btos_ai_trends.csv"
    meta_json = (
        root / "intermediate" / "figure3_panelA_btos_ai_trends_run_metadata.json"
    )

    errors: list[str] = []

    if not fig_csv.is_file():
        errors.append(f"missing output: {fig_csv}")
        return _report(errors)

    df = pd.read_csv(fig_csv)
    if list(df.columns) != EXP_COLS:
        errors.append(f"columns must be {EXP_COLS}, got {list(df.columns)}")
        return _report(errors)

    for c in EXP_COLS:
        if c in df.columns and df[c].isna().any():
            errors.append(f"NaN in {c}")

    if not df.empty:
        if str(df["source_series_id"].iloc[0]) != "naics2_XX":
            errors.append("source_series_id must be naics2_XX for national stratum")
        if set(df["evidence_directness"].astype(str).unique()) != {"direct_published"}:
            errors.append("evidence_directness must be direct_published for T-006")

    for col in ("ai_use_current_rate", "ai_use_expected_6m_rate"):
        if col in df.columns:
            low = df[col].min()
            high = df[col].max()
            if low < -RATE_TOLERANCE or high > 1.0 + RATE_TOLERANCE:
                errors.append(f"{col} out of [0,1]: min={low} max={high}")

    if str(df["period_start_date"].min()) < MIN_PERIOD_START:
        errors.append(
            f"period_start_date must be on or after {MIN_PERIOD_START}, "
            f"got min={df['period_start_date'].min()}"
        )

    if not df["period_start_date"].is_monotonic_increasing:
        errors.append("period_start_date must be sorted ascending")

    dup = df.duplicated(["period_start_date", "btos_period_id"], keep=False)
    if dup.any():
        errors.append("duplicate period_start_date x btos_period_id rows")

    if meta_json.is_file():
        meta = json.loads(meta_json.read_text(encoding="utf-8"))
        if not meta.get("periods_sha256"):
            errors.append("metadata missing periods_sha256")
        if not meta.get("questions_sha256"):
            errors.append("metadata missing questions_sha256")
        n = len(df)
        hashes = meta.get("per_period_data_hashes") or []
        if len(hashes) != n:
            errors.append(
                "per_period_data_hashes length " f"{len(hashes)} != csv rows {n}"
            )
    else:
        errors.append(f"missing metadata: {meta_json}")

    return _report(errors)


def _report(errors: list[str]) -> int:
    if errors:
        print("QA failures:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1
    print("QA OK: figure3_panelA_btos_ai_trends.csv")
    return 0
