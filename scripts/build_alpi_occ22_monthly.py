"""
Build metrics/alpi_occ22_monthly.csv: AI Labor Pressure Index (ALPI).

Run from repo root after AWES, sector stress, exit risk, and sector weights:
    python scripts/build_alpi_occ22_monthly.py
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from awes_alpi_common import SECTOR6_ORDER, percentile_rank_01

ROOT = Path(__file__).resolve().parents[1]
INTER = ROOT / "intermediate"
METRICS = ROOT / "metrics"
AWES_CSV = METRICS / "awes_occ22_monthly.csv"
STRESS_CSV = INTER / "sector6_stress_monthly.csv"
EXIT_CSV = INTER / "cps_occ22_exit_risk_monthly.csv"
WEIGHTS_CSV = INTER / "occ22_sector_weights.csv"
OUT_CSV = METRICS / "alpi_occ22_monthly.csv"
OUT_META = INTER / "alpi_run_metadata.json"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    generated_at = datetime.now(timezone.utc).isoformat()
    METRICS.mkdir(parents=True, exist_ok=True)

    for p in (AWES_CSV, STRESS_CSV, EXIT_CSV, WEIGHTS_CSV):
        if not p.is_file():
            raise FileNotFoundError(f"Missing input {p}")

    awes = pd.read_csv(AWES_CSV)
    stress = pd.read_csv(STRESS_CSV)
    exit_df = pd.read_csv(EXIT_CSV)
    wlong = pd.read_csv(WEIGHTS_CSV)

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
    out.to_csv(OUT_CSV, index=False)

    meta = {
        "output_csv": str(OUT_CSV.relative_to(ROOT)).replace("\\", "/"),
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
            str(AWES_CSV.relative_to(ROOT)).replace("\\", "/"): sha256_file(AWES_CSV),
            str(STRESS_CSV.relative_to(ROOT)).replace("\\", "/"): sha256_file(
                STRESS_CSV
            ),
            str(EXIT_CSV.relative_to(ROOT)).replace("\\", "/"): sha256_file(EXIT_CSV),
            str(WEIGHTS_CSV.relative_to(ROOT)).replace("\\", "/"): sha256_file(
                WEIGHTS_CSV
            ),
        },
        "row_count": int(len(out)),
    }
    OUT_META.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(f"Wrote {OUT_CSV} ({len(out)} rows)")


if __name__ == "__main__":
    main()
