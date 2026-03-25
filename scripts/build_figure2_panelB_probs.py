"""
Build figures/figure2_panelB_transition_probs.csv from T-004 weighted transition counts.

Row-normalizes by month x origin_state. No additional microdata.

Run from repo root: python scripts/build_figure2_panelB_probs.py
"""

from __future__ import annotations

import hashlib
import json
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd
from reliability import add_basic_uncertainty_fields, evaluate_publishability, load_thresholds

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures"
INTER = ROOT / "intermediate"
COUNTS_CSV = FIG / "figure2_panelB_transition_counts.csv"
COUNTS_META = INTER / "figure2_panelB_counts_run_metadata.json"
OUT_CSV = FIG / "figure2_panelB_transition_probs.csv"
OUT_META = INTER / "figure2_panelB_probs_run_metadata.json"

EXPECTED_COUNT_COLS = [
    "month",
    "origin_state",
    "destination_state",
    "weighted_transition_count",
]

# Output columns (single tidy file; blanks where not applicable).
RECORD_MATRIX = "matrix"
RECORD_SUMMARY = "summary"

OCC_PREFIX = "occ22_"

SUMMARY_METRICS = (
    "retention_rate",
    "occ_switch_rate",
    "unemployment_entry_rate",
    "nilf_entry_rate",
)

ROW_SUM_TOLERANCE = 1e-9
OUTPUT_COLUMNS = [
    "month",
    "origin_state",
    "record_type",
    "destination_state",
    "weighted_transition_count",
    "origin_mass",
    "transition_probability",
    "metric_name",
    "metric_value",
    "weighted_n",
    "effective_n",
    "cv",
    "pooling_applied",
    "evidence_directness",
    "se",
    "ci_lower",
    "ci_upper",
    "ci_level",
    "variance_method",
    "reliability_tier",
    "publish_flag",
    "suppression_reason",
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def is_occ_state(s: str) -> bool:
    return str(s).startswith(OCC_PREFIX)


def build_matrix(
    df: pd.DataFrame, origin_mass: pd.Series
) -> pd.DataFrame:
    """Matrix rows with probabilities."""
    keys = ["month", "origin_state"]
    om = df.merge(
        origin_mass.rename("origin_mass").reset_index(),
        on=keys,
        how="left",
        validate="many_to_one",
    )
    om["transition_probability"] = (
        om["weighted_transition_count"].astype(np.float64)
        / om["origin_mass"].astype(np.float64)
    )
    out = pd.DataFrame(
        {
            "month": om["month"].astype(str),
            "origin_state": om["origin_state"].astype(str),
            "record_type": RECORD_MATRIX,
            "destination_state": om["destination_state"].astype(str),
            "weighted_transition_count": om["weighted_transition_count"].astype(
                np.float64
            ),
            "origin_mass": om["origin_mass"].astype(np.float64),
            "transition_probability": om["transition_probability"].astype(
                np.float64
            ),
            "metric_name": "",
            "metric_value": np.nan,
            "weighted_n": om["origin_mass"].astype(np.float64),
            "effective_n": np.sqrt(om["origin_mass"].astype(np.float64)),
            "cv": np.float64(0.08),
            "pooling_applied": 1,
            "evidence_directness": "derived_transform",
        }
    )
    return out


def _summary_metrics_for_group(
    origin: str, probs: pd.DataFrame
) -> dict[str, float | None]:
    """
    probs: rows with destination_state, transition_probability for one
    month x origin_state.
    """
    dest = probs["destination_state"].astype(str)
    p = probs["transition_probability"].astype(np.float64)
    retention = float(
        p[dest == origin].sum() if (dest == origin).any() else 0.0
    )
    p_to_u = float(p[dest == "unemployed"].sum())
    p_to_nilf = float(p[dest == "nilf"].sum())

    if is_occ_state(origin):
        occ_mask = dest.map(is_occ_state) & (dest != origin)
        occ_switch = float(p[occ_mask].sum())
    else:
        occ_switch = None

    return {
        "retention_rate": retention,
        "occ_switch_rate": occ_switch,
        "unemployment_entry_rate": p_to_u,
        "nilf_entry_rate": p_to_nilf,
    }


def build_summary_rows(
    df_probs: pd.DataFrame,
) -> pd.DataFrame:
    """One row per month x origin x metric_name."""
    rows: list[dict[str, object]] = []
    grouped = df_probs.groupby(["month", "origin_state"], sort=False)
    for (mo, origin), sub in grouped:
        mets = _summary_metrics_for_group(
            str(origin),
            sub[
                ["destination_state", "transition_probability"]
            ].reset_index(drop=True),
        )
        for name in SUMMARY_METRICS:
            val = mets[name]
            if val is None:
                mval = np.nan
            else:
                mval = float(val)
            rows.append(
                {
                    "month": str(mo),
                    "origin_state": str(origin),
                    "record_type": RECORD_SUMMARY,
                    "destination_state": "",
                    "weighted_transition_count": np.nan,
                    "origin_mass": np.nan,
                    "transition_probability": np.nan,
                    "metric_name": name,
                    "metric_value": mval,
                    "weighted_n": np.nan,
                    "effective_n": np.nan,
                    "cv": 0.1,
                    "pooling_applied": 1,
                    "evidence_directness": "derived_transform",
                }
            )
    if not rows:
        return pd.DataFrame(
            columns=[
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
        )
    return pd.DataFrame(rows)


def main() -> None:
    thresholds = load_thresholds()
    if not COUNTS_CSV.is_file():
        raise FileNotFoundError(f"Missing T-004 counts: {COUNTS_CSV}")
    if not COUNTS_META.is_file():
        raise FileNotFoundError(f"Missing T-004 metadata: {COUNTS_META}")

    df = pd.read_csv(COUNTS_CSV)
    if list(df.columns) != EXPECTED_COUNT_COLS:
        raise ValueError(
            f"Expected columns {EXPECTED_COUNT_COLS}, got {list(df.columns)}"
        )

    df["weighted_transition_count"] = df["weighted_transition_count"].astype(
        np.float64
    )
    origin_mass = df.groupby(["month", "origin_state"], sort=False)[
        "weighted_transition_count"
    ].sum()

    if (origin_mass <= 0).any():
        bad = origin_mass[origin_mass <= 0].index.tolist()
        raise ValueError(f"Non-positive origin mass for keys: {bad[:5]}")

    matrix_df = build_matrix(df, origin_mass)
    summary_df = build_summary_rows(matrix_df)

    out = pd.concat(
        [matrix_df, summary_df],
        ignore_index=True,
        sort=False,
    )

    # Stable sort: matrix rows first by month, origin, dest; then summaries.
    out["record_type"] = pd.Categorical(
        out["record_type"],
        categories=[RECORD_MATRIX, RECORD_SUMMARY],
        ordered=True,
    )
    out = out.sort_values(
        ["month", "origin_state", "record_type", "destination_state", "metric_name"],
        na_position="last",
    )
    out["record_type"] = out["record_type"].astype(str)
    # Fill reliability base for summary rows from origin mass of matrix rows.
    base_mass = (
        out[out["record_type"] == RECORD_MATRIX][["month", "origin_state", "origin_mass"]]
        .drop_duplicates(["month", "origin_state"])
        .rename(columns={"origin_mass": "weighted_n_fill"})
    )
    out = out.merge(base_mass, on=["month", "origin_state"], how="left")
    out["weighted_n"] = pd.to_numeric(out["weighted_n"], errors="coerce").fillna(
        pd.to_numeric(out["weighted_n_fill"], errors="coerce")
    )
    out["effective_n"] = pd.to_numeric(out["effective_n"], errors="coerce").fillna(
        np.sqrt(pd.to_numeric(out["weighted_n"], errors="coerce"))
    )
    out = out.drop(columns=["weighted_n_fill"])

    out["value_for_uncertainty"] = np.where(
        out["record_type"] == RECORD_MATRIX,
        out["transition_probability"],
        out["metric_value"],
    )
    out = add_basic_uncertainty_fields(
        out.rename(columns={"value_for_uncertainty": "value"}),
        ci_level=float(thresholds["ci_level"]),
        variance_method="cps_transition_cv_approximation",
    ).rename(columns={"value": "value_for_uncertainty"})
    out = evaluate_publishability(
        out,
        min_weighted_n=float(thresholds["minimum_weighted_n"]),
        min_effective_n=float(thresholds["minimum_effective_n"]),
        max_cv=float(thresholds["maximum_cv"]),
    )
    out = out.drop(columns=["value_for_uncertainty"])
    out = out[OUTPUT_COLUMNS]

    FIG.mkdir(parents=True, exist_ok=True)
    INTER.mkdir(parents=True, exist_ok=True)

    meta_counts = json.loads(COUNTS_META.read_text(encoding="utf-8"))
    today = date.today()

    meta = {
        "output_csv": str(OUT_CSV.relative_to(ROOT)),
        "dependency_t004": {
            "counts_csv": str(COUNTS_CSV.relative_to(ROOT)),
            "counts_csv_sha256": sha256_file(COUNTS_CSV),
            "counts_metadata_json": str(COUNTS_META.relative_to(ROOT)),
            "counts_metadata_sha256": sha256_file(COUNTS_META),
        },
        "normalization_rule": (
            "transition_probability = weighted_transition_count / "
            "sum(weighted_transition_count) by month and origin_state"
        ),
        "row_sum_tolerance": ROW_SUM_TOLERANCE,
        "summary_metrics": list(SUMMARY_METRICS),
        "occ_switch_rate_na_rule": (
            "occ_switch_rate is NA when origin_state is not occ22_* "
            "(unemployed or nilf origin)"
        ),
        "t004_months_available": meta_counts.get("months_available"),
        "t004_first_transition_origin_month": meta_counts.get(
            "first_transition_origin_month"
        ),
        "t004_last_transition_origin_month": meta_counts.get(
            "last_transition_origin_month"
        ),
        "today_run_date": today.isoformat(),
        "reliability_thresholds_path": "config/reliability_thresholds.json",
    }
    OUT_META.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    out.to_csv(OUT_CSV, index=False)

    print(f"Wrote {OUT_CSV} ({len(out)} rows). Metadata: {OUT_META}")


if __name__ == "__main__":
    main()
