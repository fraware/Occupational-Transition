"""
Build intermediate/sector6_stress_monthly.csv: JOLTS/CES sector-time stress index.

Run from repo root (after T-008 Figure 4 Panel A and T-009 Panel B):
    python scripts/build_sector6_stress_monthly.py
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from awes_alpi_common import percentile_rank_01, zscore_panel

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures"
INTER = ROOT / "intermediate"
JOLTS_CSV = FIG / "figure4_panelA_jolts_sector_rates.csv"
CES_CSV = FIG / "figure4_panelB_ces_sector_index.csv"
OUT_CSV = INTER / "sector6_stress_monthly.csv"
OUT_META = INTER / "sector6_stress_monthly_run_metadata.json"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    generated_at = datetime.now(timezone.utc).isoformat()
    INTER.mkdir(parents=True, exist_ok=True)

    for p in (JOLTS_CSV, CES_CSV):
        if not p.is_file():
            raise FileNotFoundError(f"Missing {p}; run Figure 4 builds first.")

    jt = pd.read_csv(JOLTS_CSV)
    ce = pd.read_csv(CES_CSV)

    jw = jt.pivot_table(
        index=["month", "sector6_code", "sector6_label"],
        columns="rate_name",
        values="rate_value",
        aggfunc="first",
    ).reset_index()

    jw = jw.rename(
        columns={
            "job_openings_rate": "jolts_openings_rate",
            "hires_rate": "jolts_hires_rate",
            "layoffs_discharges_rate": "jolts_layoffs_rate",
        }
    )

    for c in ("jolts_openings_rate", "jolts_hires_rate", "jolts_layoffs_rate"):
        jw[c] = pd.to_numeric(jw[c], errors="coerce")

    L = zscore_panel(jw["jolts_layoffs_rate"])
    O = zscore_panel(jw["jolts_openings_rate"])
    H = zscore_panel(jw["jolts_hires_rate"])
    jw["jolts_stress_raw"] = L - 0.5 * O - 0.5 * H
    jw["jolts_stress_pct"] = percentile_rank_01(jw["jolts_stress_raw"])

    ce = ce.rename(
        columns={"ces_payroll_employment_thousands": "ces_payroll_employment"}
    )
    ce["ces_payroll_employment"] = pd.to_numeric(
        ce["ces_payroll_employment"], errors="coerce"
    )
    ce = ce.sort_values(["sector6_code", "month"])
    ce["log_emp"] = np.log(ce["ces_payroll_employment"].clip(lower=np.nan))
    ce["log_emp_lag12"] = ce.groupby("sector6_code", sort=False)["log_emp"].shift(
        12
    )
    ce["ces_payroll_contraction_12m_raw"] = -(
        ce["log_emp"] - ce["log_emp_lag12"]
    )
    ce["ces_payroll_contraction_12m_pct"] = percentile_rank_01(
        ce["ces_payroll_contraction_12m_raw"]
    )

    merged = jw.merge(
        ce[
            [
                "month",
                "sector6_code",
                "ces_payroll_employment",
                "ces_payroll_contraction_12m_raw",
                "ces_payroll_contraction_12m_pct",
            ]
        ],
        on=["month", "sector6_code"],
        how="inner",
        validate="one_to_one",
    )

    merged["sector_stress_pct"] = (
        merged["jolts_stress_pct"].astype(float)
        + merged["ces_payroll_contraction_12m_pct"].astype(float)
    ) / 2.0

    col_order = [
        "month",
        "sector6_code",
        "sector6_label",
        "jolts_openings_rate",
        "jolts_hires_rate",
        "jolts_layoffs_rate",
        "jolts_stress_raw",
        "jolts_stress_pct",
        "ces_payroll_employment",
        "ces_payroll_contraction_12m_raw",
        "ces_payroll_contraction_12m_pct",
        "sector_stress_pct",
    ]
    merged = merged[col_order].sort_values(["month", "sector6_code"])
    merged.to_csv(OUT_CSV, index=False)

    meta = {
        "output_csv": str(OUT_CSV.relative_to(ROOT)).replace("\\", "/"),
        "generated_at_utc": generated_at,
        "formula_version": "sector stress v1",
        "jolts_formula": "z(layoffs) - 0.5*z(openings) - 0.5*z(hires); z over full panel.",
        "jolts_stress_pct": "percentile_rank of jolts_stress_raw over sector-month panel.",
        "ces_contraction": (
            "ces_payroll_contraction_12m_raw = -delta_12 log(ces_payroll_employment); "
            "employment from CES thousands column."
        ),
        "ces_payroll_contraction_12m_pct": (
            "percentile_rank of contraction over sector-month (non-null cells)."
        ),
        "sector_stress_pct": "mean of jolts_stress_pct and ces_payroll_contraction_12m_pct.",
        "source_files_sha256": {
            str(JOLTS_CSV.relative_to(ROOT)).replace("\\", "/"): sha256_file(
                JOLTS_CSV
            ),
            str(CES_CSV.relative_to(ROOT)).replace("\\", "/"): sha256_file(CES_CSV),
        },
        "row_count": int(len(merged)),
    }
    OUT_META.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(f"Wrote {OUT_CSV} ({len(merged)} rows)")


if __name__ == "__main__":
    main()
