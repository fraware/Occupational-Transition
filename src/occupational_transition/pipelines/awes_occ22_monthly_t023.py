"""
Build metrics/awes_occ22_monthly.csv: Adoption-Weighted Exposure Score (AWES).

Run from repo root (after exposure components, sector weights, BTOS monthly):
    python scripts/build_awes_occ22_monthly.py
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
class AwesOcc22Paths:
    root: Path
    inter: Path
    metrics: Path
    exposure_csv: Path
    weights_csv: Path
    btos_csv: Path
    out_csv: Path
    out_meta: Path


def _awes_paths(root: Path) -> AwesOcc22Paths:
    inter = root / "intermediate"
    metrics = root / "metrics"
    return AwesOcc22Paths(
        root=root,
        inter=inter,
        metrics=metrics,
        exposure_csv=inter / "occ22_exposure_components.csv",
        weights_csv=inter / "occ22_sector_weights.csv",
        btos_csv=inter / "btos_sector_ai_use_monthly.csv",
        out_csv=metrics / "awes_occ22_monthly.csv",
        out_meta=inter / "awes_run_metadata.json",
    )


def run(root: Path) -> None:
    build_awes_occ22_monthly(_awes_paths(root))


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def build_awes_occ22_monthly(p: AwesOcc22Paths) -> None:
    generated_at = datetime.now(timezone.utc).isoformat()
    p.metrics.mkdir(parents=True, exist_ok=True)

    for path in (p.exposure_csv, p.weights_csv, p.btos_csv):
        if not path.is_file():
            raise FileNotFoundError(f"Missing input {path}")

    expo = pd.read_csv(p.exposure_csv)
    wlong = pd.read_csv(p.weights_csv)
    btos = pd.read_csv(p.btos_csv)

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
    out.to_csv(p.out_csv, index=False)

    meta = {
        "output_csv": str(p.out_csv.relative_to(p.root)).replace("\\", "/"),
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
            str(p.exposure_csv.relative_to(p.root)).replace("\\", "/"): sha256_file(
                p.exposure_csv
            ),
            str(p.weights_csv.relative_to(p.root)).replace("\\", "/"): sha256_file(
                p.weights_csv
            ),
            str(p.btos_csv.relative_to(p.root)).replace("\\", "/"): sha256_file(p.btos_csv),
        },
        "row_count": int(len(out)),
    }
    p.out_meta.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(f"Wrote {p.out_csv} ({len(out)} rows)")
