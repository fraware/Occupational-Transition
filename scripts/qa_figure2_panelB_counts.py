"""QA for Figure 2 Panel B transition counts (T-004). Exit 1 on failure."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FIG_CSV = ROOT / "figures" / "figure2_panelB_transition_counts.csv"
META_JSON = ROOT / "intermediate" / "figure2_panelB_counts_run_metadata.json"
ATTRITION_CSV = ROOT / "intermediate" / "figure2_panelB_attrition_diagnostics.csv"
MATCH_REGIME_CSV = ROOT / "intermediate" / "figure2_panelB_match_regime_robustness.csv"
MISSING_MONTH_SENS_CSV = ROOT / "intermediate" / "figure2_panelB_missing_month_sensitivity.csv"

ALLOW_MISSING_MONTHS = {"2025-10"}

ALLOWED_STATES = (
    {f"occ22_{i:02d}" for i in range(1, 23)} | {"unemployed", "nilf"}
)

EXP_COLS = [
    "month",
    "origin_state",
    "destination_state",
    "weighted_transition_count",
]


def main() -> int:
    errors: list[str] = []

    if not FIG_CSV.is_file():
        errors.append(f"missing output: {FIG_CSV}")
        return _report(errors)

    df = pd.read_csv(FIG_CSV)
    if list(df.columns) != EXP_COLS:
        errors.append(f"columns must be {EXP_COLS}, got {list(df.columns)}")

    for col in EXP_COLS:
        if col in df.columns and df[col].isna().any():
            errors.append(f"NaN in {col}")

    ori = set(df["origin_state"].astype(str).unique())
    if not ori <= ALLOWED_STATES:
        bad = ori - ALLOWED_STATES
        errors.append(f"invalid origin_state labels: {sorted(bad)}")
    dst = set(df["destination_state"].astype(str).unique())
    if not dst <= ALLOWED_STATES:
        bad = dst - ALLOWED_STATES
        errors.append(f"invalid destination_state labels: {sorted(bad)}")

    dup = df.duplicated(
        ["month", "origin_state", "destination_state"],
        keep=False,
    )
    if dup.any():
        errors.append("duplicate month x origin_state x destination_state rows")

    if (df["weighted_transition_count"] < 0).any():
        errors.append("weighted_transition_count must be non-negative")

    wcol = "weighted_transition_count"
    by_m = df.groupby("month", as_index=False)[wcol].sum()
    if (by_m[wcol] <= 0).any():
        bad = by_m.loc[by_m[wcol] <= 0, "month"].tolist()
        msg = "positive origin mass required by month; non-positive: "
        errors.append(msg + str(bad))

    if str(df["month"].min()) != "2019-01":
        errors.append(
            "series must start at 2019-01 for origin month, got "
            f"{df['month'].min()}"
        )

    if not META_JSON.is_file():
        errors.append(f"missing metadata: {META_JSON}")
        return _report(errors)
    for extra in [ATTRITION_CSV, MATCH_REGIME_CSV, MISSING_MONTH_SENS_CSV]:
        if not extra.is_file():
            errors.append(f"missing diagnostics output: {extra}")

    meta = json.loads(META_JSON.read_text(encoding="utf-8"))
    allow = set(str(x) for x in (meta.get("allow_missing_months") or []))
    if allow != ALLOW_MISSING_MONTHS:
        errors.append(
            "metadata allow_missing_months must match QA allowlist "
            f"{ALLOW_MISSING_MONTHS}, got {allow}"
        )

    months_avail = [str(x) for x in (meta.get("months_available") or [])]
    if months_avail and str(months_avail[0]) != "2019-01":
        errors.append(
            "months_available must start at 2019-01, got "
            f"{months_avail[0]}"
        )

    # Each CSV origin month must appear as a pair origin in metadata.
    pairs = meta.get("pairs") or []
    origin_months_meta = {
        str(p.get("origin_month")) for p in pairs if p.get("origin_month")
    }
    months_in_csv = sorted(df["month"].astype(str).unique())
    unexpected = [m for m in months_in_csv if m not in origin_months_meta]
    if unexpected:
        errors.append(
            "CSV contains origin months not listed in metadata pairs "
            f"(first few unexpected): {unexpected[:5]}"
        )
    if ATTRITION_CSV.is_file():
        ad = pd.read_csv(ATTRITION_CSV)
        req = {
            "month",
            "stratum_type",
            "stratum_value",
            "n_origin",
            "n_matched",
            "match_rate_unweighted",
            "weighted_origin_mass",
            "weighted_matched_mass",
            "match_rate_weighted",
        }
        if not req.issubset(set(ad.columns)):
            errors.append("attrition diagnostics missing required columns")
    if MATCH_REGIME_CSV.is_file():
        mr = pd.read_csv(MATCH_REGIME_CSV)
        if set(mr.get("regime", pd.Series(dtype=str)).astype(str).unique()) != {
            "strict",
            "moderate",
            "permissive",
        }:
            errors.append("match regime robustness must include strict/moderate/permissive")
    if MISSING_MONTH_SENS_CSV.is_file():
        ms = pd.read_csv(MISSING_MONTH_SENS_CSV)
        need = {
            "observed_skip_allowlist",
            "interpolated_window_shift",
            "exclusion_window",
        }
        got = set(ms.get("scenario", pd.Series(dtype=str)).astype(str).unique())
        if got != need:
            errors.append("missing-month sensitivity must include three scenarios")

    return _report(errors)


def _report(errors: list[str]) -> int:
    if errors:
        print("QA failures:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1
    print("QA OK: figure2_panelB_transition_counts.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
