"""
Build metrics/awes_occ22_monthly.csv: Adoption-Weighted Exposure Score (AWES).

Run from repo root (after exposure components, sector weights, BTOS monthly):
    python scripts/build_awes_occ22_monthly.py
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
EXPOSURE_CSV = INTER / "occ22_exposure_components.csv"
WEIGHTS_CSV = INTER / "occ22_sector_weights.csv"
BTOS_CSV = INTER / "btos_sector_ai_use_monthly.csv"
OUT_CSV = METRICS / "awes_occ22_monthly.csv"
OUT_META = INTER / "awes_run_metadata.json"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    generated_at = datetime.now(timezone.utc).isoformat()
    METRICS.mkdir(parents=True, exist_ok=True)

    for p in (EXPOSURE_CSV, WEIGHTS_CSV, BTOS_CSV):
        if not p.is_file():
            raise FileNotFoundError(f"Missing input {p}")

    expo = pd.read_csv(EXPOSURE_CSV)
    wlong = pd.read_csv(WEIGHTS_CSV)
    btos = pd.read_csv(BTOS_CSV)

    w_pivot = wlong.pivot_table(
        index="occ22_code",
        columns="sector6_code",
        values="sector_weight",
        aggfunc="first",
    ).reindex(columns=list(SECTOR6_ORDER), fill_value=0.0)

    cov = wlong.groupby("occ22_code", as_index=False).agg(
        sector6_coverage_share=("sector6_coverage_share", "first"),
        coverage_flag_low=("coverage_flag_low", "first"),
    )

    bwide = btos.pivot_table(
        index="month",
        columns="sector6_code",
        values="btos_ai_use_share_3m",
        aggfunc="first",
    ).reindex(columns=list(SECTOR6_ORDER))

    months = sorted(bwide.index.astype(str).tolist())
    occ_rows = expo[["occ22_code", "occ22_label", "exposure_pct"]].drop_duplicates()

    out_blocks: list[pd.DataFrame] = []
    for month in months:
        a_row = bwide.loc[month].astype(float)
        adop = w_pivot.dot(a_row)
        block = occ_rows.copy()
        block["month"] = month
        block["adoption_mix_occ_month"] = block["occ22_code"].map(adop).astype(float)
        block["exposure_pct"] = block["exposure_pct"].astype(float)
        block["awes_raw"] = block["exposure_pct"] * block["adoption_mix_occ_month"]
        out_blocks.append(block)

    out = pd.concat(out_blocks, ignore_index=True)
    out = out.merge(cov, on="occ22_code", how="left")
    out["awes_pct"] = percentile_rank_01(out["awes_raw"])

    col_order = [
        "month",
        "occ22_code",
        "occ22_label",
        "exposure_pct",
        "adoption_mix_occ_month",
        "awes_raw",
        "awes_pct",
        "sector6_coverage_share",
        "coverage_flag_low",
    ]
    out = out[col_order].sort_values(["month", "occ22_code"]).reset_index(drop=True)
    out.to_csv(OUT_CSV, index=False)

    meta = {
        "output_csv": str(OUT_CSV.relative_to(ROOT)).replace("\\", "/"),
        "generated_at_utc": generated_at,
        "formula_version": "AWES v1",
        "interpretation": (
            "AWES_raw = exposure_pct * adoption_mix; adoption_mix uses OEWS sector "
            "weights and smoothed BTOS sector AI-use shares. Descriptive only."
        ),
        "normalization_rules": {
            "exposure_pct": "Percentile rank of ATI across 22 occ (from exposure file).",
            "awes_pct": "Percentile rank of awes_raw across all occ-month rows.",
        },
        "smoothing_choices": "BTOS input uses btos_ai_use_share_3m (3-month trailing).",
        "coverage_threshold_rule": "coverage_flag_low from occ22_sector_weights.csv",
        "source_files_sha256": {
            str(EXPOSURE_CSV.relative_to(ROOT)).replace("\\", "/"): sha256_file(
                EXPOSURE_CSV
            ),
            str(WEIGHTS_CSV.relative_to(ROOT)).replace("\\", "/"): sha256_file(
                WEIGHTS_CSV
            ),
            str(BTOS_CSV.relative_to(ROOT)).replace("\\", "/"): sha256_file(BTOS_CSV),
        },
        "row_count": int(len(out)),
    }
    OUT_META.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(f"Wrote {OUT_CSV} ({len(out)} rows)")


if __name__ == "__main__":
    main()
