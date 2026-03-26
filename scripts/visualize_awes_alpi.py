from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from viz_style import STYLE, apply_matplotlib_style, save_dual
from viz_utils import ROOT, parse_month_col, sha256_file

METRICS = ROOT / "metrics"
INTER = ROOT / "intermediate"

AWES_CSV = METRICS / "awes_occ22_monthly.csv"
ALPI_CSV = METRICS / "alpi_occ22_monthly.csv"
OUT_META = INTER / "awes_alpi_visuals_run_metadata.json"


def _read_metrics(path: Path) -> pd.DataFrame:
    if not path.is_file():
        raise FileNotFoundError(f"missing metrics file: {path}")
    return pd.read_csv(path)


def render_awes_top20_latest(awes: pd.DataFrame) -> str:
    latest = str(awes["month"].max())
    d = awes[awes["month"].astype(str) == latest].copy()
    d = d.sort_values("awes_pct", ascending=False).head(20)
    d = d.sort_values("awes_pct", ascending=True)

    fig, ax = plt.subplots(figsize=(10.8, 6.2))
    ax.barh(d["occ22_label"], d["awes_pct"], color=STYLE.high_color)
    ax.set_title(f"AWES percentile by occupation (top 20, {latest})")
    ax.set_xlabel("AWES percentile (0-1)")
    ax.set_ylabel("")
    p, _ = save_dual(fig, "awes_top20_latest")
    return p.stem


def render_alpi_top20_latest(alpi: pd.DataFrame) -> str:
    latest = str(alpi["month"].max())
    d = alpi[alpi["month"].astype(str) == latest].copy()
    d = d.sort_values("alpi_pct", ascending=False).head(20)
    d = d.sort_values("alpi_pct", ascending=True)

    fig, ax = plt.subplots(figsize=(10.8, 6.2))
    ax.barh(d["occ22_label"], d["alpi_pct"], color=STYLE.middle_color)
    ax.set_title(f"ALPI percentile by occupation (top 20, {latest})")
    ax.set_xlabel("ALPI percentile (0-1)")
    ax.set_ylabel("")
    p, _ = save_dual(fig, "alpi_top20_latest")
    return p.stem


def render_awes_alpi_monthly_median(
    awes: pd.DataFrame, alpi: pd.DataFrame
) -> str:
    a = (
        awes.groupby("month", as_index=False)["awes_pct"]
        .median()
        .rename(columns={"awes_pct": "awes_median"})
    )
    b = (
        alpi.groupby("month", as_index=False)["alpi_pct"]
        .median()
        .rename(columns={"alpi_pct": "alpi_median"})
    )
    d = a.merge(b, on="month", how="inner")
    d["month_dt"] = parse_month_col(d, "month")
    d = d.sort_values("month_dt")

    fig, ax = plt.subplots(figsize=(10.2, 4.8))
    ax.plot(d["month_dt"], d["awes_median"], color=STYLE.high_color, label="AWES median")
    ax.plot(
        d["month_dt"],
        d["alpi_median"],
        color=STYLE.middle_color,
        label="ALPI median",
    )
    ax.set_title("Monthly median AWES and ALPI percentiles")
    ax.set_xlabel("Month")
    ax.set_ylabel("Median percentile (0-1)")
    ax.legend()
    p, _ = save_dual(fig, "awes_alpi_monthly_median")
    return p.stem


def render_awes_vs_alpi_latest_scatter(
    awes: pd.DataFrame, alpi: pd.DataFrame
) -> str:
    latest_awes = str(awes["month"].max())
    latest_alpi = str(alpi["month"].max())
    latest = min(latest_awes, latest_alpi)

    a = awes[awes["month"].astype(str) == latest][
        ["occ22_code", "occ22_label", "awes_pct", "coverage_flag_low"]
    ].copy()
    b = alpi[alpi["month"].astype(str) == latest][
        ["occ22_code", "alpi_pct"]
    ].copy()
    d = a.merge(b, on="occ22_code", how="inner")

    fig, ax = plt.subplots(figsize=(8.8, 6.2))
    ok = d[pd.to_numeric(d["coverage_flag_low"], errors="coerce").fillna(0).eq(0)]
    low = d[pd.to_numeric(d["coverage_flag_low"], errors="coerce").fillna(0).eq(1)]

    ax.scatter(
        ok["awes_pct"],
        ok["alpi_pct"],
        color=STYLE.high_color,
        label="coverage ok",
    )
    if not low.empty:
        ax.scatter(
            low["awes_pct"],
            low["alpi_pct"],
            color="#7f7f7f",
            marker="x",
            label="low coverage flag",
        )
    ax.set_title(f"AWES vs ALPI by occupation ({latest})")
    ax.set_xlabel("AWES percentile (0-1)")
    ax.set_ylabel("ALPI percentile (0-1)")
    ax.legend()
    p, _ = save_dual(fig, "awes_vs_alpi_latest_scatter")
    return p.stem


def main() -> None:
    apply_matplotlib_style()
    awes = _read_metrics(AWES_CSV)
    alpi = _read_metrics(ALPI_CSV)

    stems = [
        render_awes_top20_latest(awes),
        render_alpi_top20_latest(alpi),
        render_awes_alpi_monthly_median(awes, alpi),
        render_awes_vs_alpi_latest_scatter(awes, alpi),
    ]

    meta = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "inputs": {
            "metrics/awes_occ22_monthly.csv": sha256_file(AWES_CSV),
            "metrics/alpi_occ22_monthly.csv": sha256_file(ALPI_CSV),
        },
        "stems": stems,
        "notes_limits": (
            "Visuals are descriptive transforms of AWES/ALPI metrics only; "
            "no interpolation or synthetic data imputation."
        ),
    }
    OUT_META.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print("Wrote AWES/ALPI visuals:", ", ".join(stems))


if __name__ == "__main__":
    main()
