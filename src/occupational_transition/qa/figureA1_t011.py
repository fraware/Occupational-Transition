"""Ticket QA (from scripts/qa_figureA1_asec_welfare_by_ai_tercile.py)."""

from __future__ import annotations

import hashlib
import json
import sys

import pandas as pd

from occupational_transition.paths import repo_root

TERCILES_SET = {"low", "middle", "high"}

EXP_COLS = [
    "year",
    "ai_relevance_tercile",
    "mean_annual_income",
    "poverty_rate",
    "mean_weeks_worked",
    "unemployment_incidence",
    "sum_asec_person_weight",
]


def main() -> int:
    root = repo_root()
    FIG_CSV = root / "figures" / "figureA1_asec_welfare_by_ai_tercile.csv"
    META_JSON = (
        root / "intermediate" / "figureA1_asec_welfare_by_ai_tercile_run_metadata.json"
    )
    errors: list[str] = []

    if not FIG_CSV.is_file():
        errors.append(f"missing output: {FIG_CSV}")
        return _report(errors)

    df = pd.read_csv(FIG_CSV)
    if list(df.columns) != EXP_COLS:
        errors.append(f"columns must be {EXP_COLS}, got {list(df.columns)}")

    if df.isnull().any().any():
        errors.append("unexpected nulls in output CSV")

    if not df["year"].is_monotonic_increasing:
        errors.append("year must be strictly ascending by row order")

    years_sorted = sorted(int(x) for x in df["year"].unique())
    if any(y < 2019 for y in years_sorted):
        errors.append("all years must be >= 2019")

    if not set(df["ai_relevance_tercile"].unique()) <= TERCILES_SET:
        errors.append(f"invalid tercile labels: {df['ai_relevance_tercile'].unique()}")

    dup = df.duplicated(["year", "ai_relevance_tercile"], keep=False)
    if dup.any():
        errors.append("duplicate year x ai_relevance_tercile rows")

    by_y = df.groupby("year")["ai_relevance_tercile"].apply(
        lambda s: set(s.astype(str))
    )
    bad = by_y[by_y.apply(len) != 3]
    if not bad.empty:
        errors.append(f"years without exactly 3 terciles: {bad.to_dict()}")

    exp_tercile_order = ["low", "middle", "high"]
    for y, grp in df.groupby("year", sort=False):
        got = grp["ai_relevance_tercile"].astype(str).tolist()
        if got != exp_tercile_order:
            errors.append(
                f"year {y}: rows must be ordered {exp_tercile_order}, got {got}"
            )

    if (df["poverty_rate"] < 0).any() or (df["poverty_rate"] > 1).any():
        errors.append("poverty_rate must be in [0, 1]")
    if (df["unemployment_incidence"] < 0).any() or (
        df["unemployment_incidence"] > 1
    ).any():
        errors.append("unemployment_incidence must be in [0, 1]")

    if (df["mean_annual_income"] < 0).any():
        errors.append("mean_annual_income must be nonnegative")
    if (df["mean_weeks_worked"] < 0).any() or (df["mean_weeks_worked"] > 52).any():
        errors.append("mean_weeks_worked must be in [0, 52]")
    if (df["sum_asec_person_weight"] <= 0).any():
        errors.append("sum_asec_person_weight must be positive for all rows")

    if not META_JSON.is_file():
        errors.append(f"missing metadata: {META_JSON}")
    else:
        meta = json.loads(META_JSON.read_text(encoding="utf-8"))
        if meta.get("weight_variable") != "A_FNLWGT":
            errors.append("metadata weight_variable must be A_FNLWGT")
        if not meta.get("weight_scaling_rule"):
            errors.append("metadata must include weight_scaling_rule")
        if not meta.get("poverty_indicator"):
            errors.append("metadata must include poverty_indicator")
        ry = [int(x) for x in (meta.get("retained_years") or [])]
        if years_sorted != ry:
            errors.append(
                f"CSV years {years_sorted} must match metadata retained_years {ry}"
            )

        sources = meta.get("sources") or []
        if len(sources) != len(years_sorted):
            errors.append("metadata sources length must match distinct years in CSV")
        for s in sources:
            if not s.get("zip_sha256") or not s.get("download_url"):
                errors.append("each metadata source needs zip_sha256 and download_url")

        lin = meta.get("lineage_file_sha256") or {}
        for rel, h in lin.items():
            p = root / rel
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
    print("QA OK: figureA1_asec_welfare_by_ai_tercile.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
