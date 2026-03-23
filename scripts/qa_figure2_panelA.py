"""QA for Figure 2 Panel A outputs (T-003). Exit 1 on failure."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FIG_CSV = ROOT / "figures" / "figure2_panelA_hours_by_ai_tercile.csv"
META_JSON = ROOT / "intermediate" / "figure2_panelA_run_metadata.json"

ALLOW_MISSING_MONTHS = {"2025-10"}
TERCILES = {"low", "middle", "high"}


def main() -> int:
    errors: list[str] = []

    if not FIG_CSV.is_file():
        errors.append(f"missing output: {FIG_CSV}")
        return _report(errors)

    df = pd.read_csv(FIG_CSV)
    exp_cols = [
        "month",
        "ai_relevance_tercile",
        "mean_usual_weekly_hours",
        "sum_composite_weight",
    ]
    if list(df.columns) != exp_cols:
        errors.append(f"columns must be {exp_cols}, got {list(df.columns)}")

    if df["month"].isna().any():
        errors.append("NaN in month")
    if df["ai_relevance_tercile"].isna().any():
        errors.append("NaN in ai_relevance_tercile")
    if df["mean_usual_weekly_hours"].isna().any():
        errors.append("NaN in mean_usual_weekly_hours")
    if df["sum_composite_weight"].isna().any():
        errors.append("NaN in sum_composite_weight")

    if not set(df["ai_relevance_tercile"].unique()) <= TERCILES:
        errors.append(f"invalid tercile labels: {df['ai_relevance_tercile'].unique()}")

    dup = df.duplicated(["month", "ai_relevance_tercile"], keep=False)
    if dup.any():
        errors.append("duplicate month x ai_relevance_tercile rows")

    by_m = df.groupby("month")["ai_relevance_tercile"].apply(lambda s: set(s.astype(str)))
    bad_counts = by_m[by_m.apply(len) != 3]
    if not bad_counts.empty:
        errors.append(f"months without exactly 3 terciles: {bad_counts.to_dict()}")

    if (df["sum_composite_weight"] <= 0).any():
        errors.append("sum_composite_weight must be positive for all rows")

    low = df["mean_usual_weekly_hours"].min()
    high = df["mean_usual_weekly_hours"].max()
    if low < 1 or high > 99:
        errors.append(f"mean_usual_weekly_hours out of 1..99 range: min={low} max={high}")

    if str(df["month"].min()) != "2019-01":
        errors.append(f"series must start at 2019-01, got {df['month'].min()}")

    if META_JSON.is_file():
        meta = json.loads(META_JSON.read_text(encoding="utf-8"))
        proc = [str(x) for x in (meta.get("months_processed") or [])]
        allow = set(str(x) for x in (meta.get("allow_missing_months") or []))
        if allow != ALLOW_MISSING_MONTHS:
            errors.append(
                f"metadata allow_missing_months must match QA allowlist {ALLOW_MISSING_MONTHS}, got {allow}"
            )
        months_in_csv = df.drop_duplicates(subset=["month"], keep="first")["month"].astype(str).tolist()
        if proc and months_in_csv != proc:
            diff_at = next(
                (i for i, ab in enumerate(zip(months_in_csv, proc)) if ab[0] != ab[1]),
                None,
            )
            errors.append(
                "CSV month sequence must equal metadata months_processed "
                f"(len csv={len(months_in_csv)} meta={len(proc)}, first_diff_i={diff_at})"
            )
    else:
        errors.append(f"missing metadata: {META_JSON}")

    return _report(errors)


def _report(errors: list[str]) -> int:
    if errors:
        print("QA failures:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1
    print("QA OK: figure2_panelA_hours_by_ai_tercile.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
