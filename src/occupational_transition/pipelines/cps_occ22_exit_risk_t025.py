"""
Build intermediate/cps_occ22_exit_risk_monthly.csv from CPS matched-month
transition probabilities (unemployment + NILF exit from employment by occ22).

Uses trailing 12 calendar months (origin months) pooled weighted rates.

Run from repo root (after T-005):
    python scripts/build_cps_occ22_exit_risk_monthly.py
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from occupational_transition.awes_alpi_common import (
    occ22_code_from_id,
    percentile_rank_01,
)


@dataclass(frozen=True)
class CpsOcc22ExitRiskPaths:
    root: Path
    fig: Path
    inter: Path
    probs_csv: Path
    cross: Path
    out_csv: Path
    out_meta: Path


def _cps_exit_paths(root: Path) -> CpsOcc22ExitRiskPaths:
    fig = root / "figures"
    inter = root / "intermediate"
    return CpsOcc22ExitRiskPaths(
        root=root,
        fig=fig,
        inter=inter,
        probs_csv=fig / "figure2_panelB_transition_probs.csv",
        cross=root / "crosswalks" / "occ22_crosswalk.csv",
        out_csv=inter / "cps_occ22_exit_risk_monthly.csv",
        out_meta=inter / "cps_occ22_exit_risk_monthly_run_metadata.json",
    )


def run(root: Path) -> None:
    build_cps_occ22_exit_risk_monthly(_cps_exit_paths(root))


RECORD_MATRIX = "matrix"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_occ22_labels(cross: Path) -> pd.DataFrame:
    cx = pd.read_csv(cross)
    pr = cx[cx["source_system"] == "CPS_PRDTOCC1"].copy()
    pr = pr[pr["source_occ_code"].astype(str) != "23"]
    pr["occ22_id"] = pr["occ22_id"].astype(int)
    pr["occ22_code"] = pr["occ22_id"].map(occ22_code_from_id)
    return pr[["occ22_code", "occ22_label"]].drop_duplicates()


def build_cps_occ22_exit_risk_monthly(p: CpsOcc22ExitRiskPaths) -> None:
    generated_at = datetime.now(timezone.utc).isoformat()
    p.inter.mkdir(parents=True, exist_ok=True)

    if not p.probs_csv.is_file():
        raise FileNotFoundError(f"Missing {p.probs_csv}; run T-005 first.")

    probs = pd.read_csv(p.probs_csv)
    mat = probs[probs["record_type"] == RECORD_MATRIX].copy()
    mat["month"] = mat["month"].astype(str)
    mat["origin_state"] = mat["origin_state"].astype(str)
    mat = mat[mat["origin_state"].str.startswith("occ22_")]

    om = (
        mat.groupby(["month", "origin_state"], sort=False, as_index=False)
        .agg(origin_mass=("origin_mass", "first"))
        .rename(columns={"origin_state": "occ22_code"})
    )

    exit_sub = mat[mat["destination_state"].isin(["unemployed", "nilf"])].copy()
    p_exit = (
        exit_sub.groupby(["month", "origin_state"], sort=False, as_index=False)[
            "transition_probability"
        ]
        .sum()
        .rename(
            columns={
                "origin_state": "occ22_code",
                "transition_probability": "p_exit",
            }
        )
    )

    base = om.merge(p_exit, on=["month", "occ22_code"], how="left")
    base["p_exit"] = base["p_exit"].fillna(0.0).astype(float)
    base["origin_mass"] = base["origin_mass"].astype(float)
    base["exit_weighted"] = base["p_exit"] * base["origin_mass"]

    labels = load_occ22_labels(p.cross)
    base = base.merge(labels, on="occ22_code", how="left")
    base = base.sort_values(["occ22_code", "month"], kind="mergesort")
    g = base.groupby("occ22_code", sort=False, group_keys=False)
    num = g["exit_weighted"].transform(
        lambda s: s.rolling(12, min_periods=1).sum()
    )
    den = g["origin_mass"].transform(
        lambda s: s.rolling(12, min_periods=1).sum()
    )
    base["exit_risk_12m_raw"] = num / den
    base["origin_mass_12m"] = den

    out = base[
        [
            "month",
            "occ22_code",
            "occ22_label",
            "exit_risk_12m_raw",
            "origin_mass_12m",
        ]
    ].copy()
    out["exit_risk_12m_pct"] = percentile_rank_01(out["exit_risk_12m_raw"])

    col_order = [
        "month",
        "occ22_code",
        "occ22_label",
        "exit_risk_12m_raw",
        "exit_risk_12m_pct",
        "origin_mass_12m",
    ]
    out = out[col_order].sort_values(["month", "occ22_code"]).reset_index(drop=True)
    out.to_csv(p.out_csv, index=False)

    meta = {
        "output_csv": str(p.out_csv.relative_to(p.root)).replace("\\", "/"),
        "generated_at_utc": generated_at,
        "formula_version": "CPS exit risk 12m v1",
        "definition": (
            "exit_risk_12m_raw = sum_tau p(U union NILF|occ, tau)*mass_tau / sum_tau mass_tau "
            "for tau over trailing 12 origin months ending at month."
        ),
        "exit_risk_12m_pct": "percentile_rank of raw over all occ-month rows (non-null).",
        "source_files_sha256": {
            str(p.probs_csv.relative_to(p.root)).replace("\\", "/"): sha256_file(p.probs_csv),
        },
        "crosswalk_file": str(p.cross.relative_to(p.root)).replace("\\", "/"),
        "row_count": int(len(out)),
    }
    p.out_meta.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(f"Wrote {p.out_csv} ({len(out)} rows)")
