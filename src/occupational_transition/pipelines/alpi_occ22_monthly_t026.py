"""
Build metrics/alpi_occ22_monthly.csv: AI Labor Pressure Index (ALPI).

Run from repo root after AWES, sector stress, exit risk, and sector weights:
    python scripts/build_alpi_occ22_monthly.py
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from occupational_transition.awes_alpi_common import SECTOR6_ORDER, percentile_rank_01


@dataclass(frozen=True)
class AlpiOcc22Paths:
    root: Path
    inter: Path
    metrics: Path
    awes_csv: Path
    stress_csv: Path
    exit_csv: Path
    weights_csv: Path
    out_csv: Path
    out_meta: Path


def _alpi_paths(root: Path) -> AlpiOcc22Paths:
    inter = root / "intermediate"
    metrics = root / "metrics"
    return AlpiOcc22Paths(
        root=root,
        inter=inter,
        metrics=metrics,
        awes_csv=metrics / "awes_occ22_monthly.csv",
        stress_csv=inter / "sector6_stress_monthly.csv",
        exit_csv=inter / "cps_occ22_exit_risk_monthly.csv",
        weights_csv=inter / "occ22_sector_weights.csv",
        out_csv=metrics / "alpi_occ22_monthly.csv",
        out_meta=inter / "alpi_run_metadata.json",
    )


def run(root: Path) -> None:
    build_alpi_occ22_monthly(_alpi_paths(root))


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def build_alpi_occ22_monthly(p: AlpiOcc22Paths) -> None:
    generated_at = datetime.now(timezone.utc).isoformat()
    p.metrics.mkdir(parents=True, exist_ok=True)

    for path in (p.awes_csv, p.stress_csv, p.exit_csv, p.weights_csv):
        if not path.is_file():
            raise FileNotFoundError(f"Missing input {path}")

    awes = pd.read_csv(p.awes_csv)
    stress = pd.read_csv(p.stress_csv)
    exit_df = pd.read_csv(p.exit_csv)
    wlong = pd.read_csv(p.weights_csv)

    w_pivot = wlong.pivot_table(
        index="occ22_code",
        columns="sector6_code",
        values="sector_weight",
        aggfunc="first",
    ).reindex(columns=list(SECTOR6_ORDER), fill_value=0.0)

    swide = stress.pivot_table(
        index="month",
        columns="sector6_code",
        values="sector_stress_pct",
        aggfunc="first",
    ).reindex(columns=list(SECTOR6_ORDER))

    months = sorted(swide.index.astype(str).tolist())
    demand_rows: list[dict[str, object]] = []
    for m in months:
        srow = swide.loc[m].astype(float)
        dvec = w_pivot.dot(srow)
        for occ, val in dvec.items():
            demand_rows.append(
                {
                    "month": m,
                    "occ22_code": str(occ),
                    "demand_stress_occ_month": float(val),
                }
            )
    demand_long = pd.DataFrame(demand_rows)

    j = awes.merge(
        exit_df[["month", "occ22_code", "exit_risk_12m_pct"]],
        on=["month", "occ22_code"],
        how="inner",
    ).merge(demand_long, on=["month", "occ22_code"], how="inner")

    # Coverage flags already on awes_occ22_monthly.csv; do not re-merge weights
    # (duplicate column names would pandas-suffix and break output column list).
    j["alpi_raw"] = (
        j["awes_pct"].astype(float)
        + j["demand_stress_occ_month"].astype(float)
        + j["exit_risk_12m_pct"].astype(float)
    ) / 3.0
    j["alpi_pct"] = percentile_rank_01(j["alpi_raw"])

    out = j[
        [
            "month",
            "occ22_code",
            "occ22_label",
            "awes_pct",
            "demand_stress_occ_month",
            "exit_risk_12m_pct",
            "alpi_raw",
            "alpi_pct",
            "sector6_coverage_share",
            "coverage_flag_low",
        ]
    ].sort_values(["month", "occ22_code"])
    out.to_csv(p.out_csv, index=False)

    meta = {
        "output_csv": str(p.out_csv.relative_to(p.root)).replace("\\", "/"),
        "generated_at_utc": generated_at,
        "formula_version": "ALPI v1",
        "interpretation": (
            "ALPI is descriptive monitoring/prioritization index, not a causal "
            "treatment effect."
        ),
        "alpi_raw": (
            "equal-weight mean of awes_pct, demand_stress_occ_month, "
            "exit_risk_12m_pct."
        ),
        "demand_stress": (
            "sum_s w_{o,s} * sector_stress_pct_{s,t} from sector6_stress_monthly."
        ),
        "normalization_rules": {
            "alpi_pct": "percentile_rank of alpi_raw over all occ-month rows.",
        },
        "coverage_threshold_rule": "coverage_flag_low propagated from sector weights.",
        "source_files_sha256": {
            str(p.awes_csv.relative_to(p.root)).replace("\\", "/"): sha256_file(p.awes_csv),
            str(p.stress_csv.relative_to(p.root)).replace("\\", "/"): sha256_file(
                p.stress_csv
            ),
            str(p.exit_csv.relative_to(p.root)).replace("\\", "/"): sha256_file(p.exit_csv),
            str(p.weights_csv.relative_to(p.root)).replace("\\", "/"): sha256_file(
                p.weights_csv
            ),
        },
        "row_count": int(len(out)),
    }
    p.out_meta.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(f"Wrote {p.out_csv} ({len(out)} rows)")

