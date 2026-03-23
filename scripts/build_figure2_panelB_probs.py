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
    }
    OUT_META.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    out.to_csv(OUT_CSV, index=False)

    print(f"Wrote {OUT_CSV} ({len(out)} rows). Metadata: {OUT_META}")


if __name__ == "__main__":
    main()
