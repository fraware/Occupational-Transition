"""QA for Figure A2 SIPP event-study output (T-012). Exit 1 on failure."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FIG_CSV = ROOT / "figures" / "figureA2_sipp_event_study.csv"
META_JSON = ROOT / "intermediate" / "figureA2_sipp_event_study_run_metadata.json"

TERCILES_SET = {"low", "middle", "high"}

EXP_COLS = [
    "event_time",
    "ai_relevance_tercile",
    "mean_employment_rate",
    "mean_monthly_income",
    "mean_snap_participation",
    "sum_person_weight",
]


def main() -> int:
    errors: list[str] = []

    if not FIG_CSV.is_file():
        errors.append(f"missing output: {FIG_CSV}")
        return _report(errors)

    df = pd.read_csv(FIG_CSV)
    if list(df.columns) != EXP_COLS:
        errors.append(f"columns must be {EXP_COLS}, got {list(df.columns)}")

    if df.isnull().any().any():
        errors.append("unexpected nulls in output CSV")

    if not df["event_time"].is_monotonic_increasing:
        errors.append("rows must be sorted by event_time then tercile")

    if int(df["event_time"].min()) < -12:
        errors.append("event_time must be >= -12")
    if int(df["event_time"].max()) > 24:
        errors.append("event_time must be <= 24")

    if 0 not in set(df["event_time"].unique()):
        errors.append("event_time must include 0 (transition month)")

    if not set(df["ai_relevance_tercile"].unique()) <= TERCILES_SET:
        errors.append(f"invalid tercile labels: {df['ai_relevance_tercile'].unique()}")

    dup = df.duplicated(["event_time", "ai_relevance_tercile"], keep=False)
    if dup.any():
        errors.append("duplicate event_time x ai_relevance_tercile rows")

    by_k = df.groupby("event_time")["ai_relevance_tercile"].apply(lambda s: set(s.astype(str)))
    bad = by_k[by_k.apply(len) != 3]
    if not bad.empty:
        errors.append(f"event_time values without exactly 3 terciles: {bad.to_dict()}")

    if (df["mean_employment_rate"] < 0).any() or (df["mean_employment_rate"] > 1).any():
        errors.append("mean_employment_rate must be in [0, 1]")
    if (df["mean_snap_participation"] < 0).any() or (df["mean_snap_participation"] > 1).any():
        errors.append("mean_snap_participation must be in [0, 1]")
    if (df["mean_monthly_income"] < 0).any():
        errors.append("mean_monthly_income must be nonnegative")
    if (df["sum_person_weight"] <= 0).any():
        errors.append("sum_person_weight must be positive")

    exp_tercile_order = ["low", "middle", "high"]
    for k, grp in df.groupby("event_time", sort=False):
        got = grp["ai_relevance_tercile"].astype(str).tolist()
        if got != exp_tercile_order:
            errors.append(f"event_time {k}: rows must be ordered {exp_tercile_order}, got {got}")

    if not META_JSON.is_file():
        errors.append(f"missing metadata: {META_JSON}")
    else:
        meta = json.loads(META_JSON.read_text(encoding="utf-8"))
        if meta.get("weight_variable") != "WPFINWGT":
            errors.append("metadata weight_variable must be WPFINWGT")
        if not meta.get("weight_note"):
            errors.append("metadata must include weight_note")
        if not meta.get("transition_definition"):
            errors.append("metadata must include transition_definition")
        srcs = meta.get("sources") or []
        if len(srcs) < 1:
            errors.append("metadata sources must list at least one SIPP panel")
        for s in srcs:
            if not s.get("zip_sha256") or not s.get("download_url"):
                errors.append("each metadata source needs zip_sha256 and download_url")
        ry = list(meta.get("sipp_panel_release_years") or [])
        if ry != [2022, 2023, 2024]:
            errors.append(f"metadata sipp_panel_release_years must be [2022,2023,2024], got {ry}")

        lin = meta.get("lineage_file_sha256") or {}
        for rel, h in lin.items():
            p = ROOT / rel
            if not p.is_file():
                errors.append(f"missing lineage file for hash check: {p}")
            else:
                hh = hashlib.sha256()
                with p.open("rb") as f:
                    for chunk in iter(lambda: f.read(1 << 20), b""):
                        hh.update(chunk)
                if hh.hexdigest() != h:
                    errors.append(f"lineage hash mismatch for {rel}")

    return _report(errors)


def _report(errors: list[str]) -> int:
    if errors:
        print("QA failures:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1
    print("QA OK: figureA2_sipp_event_study.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
