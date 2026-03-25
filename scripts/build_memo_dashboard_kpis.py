"""
Build figures/memo_dashboard_kpis.csv for memo Visual 1.

Precision (full detail: docs/memo_visual_precision.md):
- CPS entry KPIs use origin_mass from figure2_panelB_transition_counts.csv merged onto
  summary rows in figure2_panelB_transition_probs.csv (probs-file origin_mass is not used).
- Reference month for entry KPIs is the latest month (descending) where both
  unemployment_entry_rate and nilf_entry_rate are computable for high tercile; this can
  differ from max(month) in figure2_panelA_hours_by_ai_tercile.csv (recorded in metadata).

Run from repo root:
  python scripts/build_memo_dashboard_kpis.py
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures"
INTER = ROOT / "intermediate"

OUT_CSV = FIG / "memo_dashboard_kpis.csv"
OUT_META = INTER / "memo_dashboard_kpis_run_metadata.json"


def _kpi_row(**kwargs: object) -> dict[str, object]:
    return {
        "kpi_id": kwargs["kpi_id"],
        "kpi_label": kwargs["kpi_label"],
        "value": kwargs["value"],
        "unit": kwargs["unit"],
        "reference_period": kwargs["reference_period"],
        "change_value": kwargs.get("change_value"),
        "change_unit": kwargs.get("change_unit"),
        "change_window": kwargs.get("change_window"),
        "source_primary": kwargs["source_primary"],
        "source_path_or_endpoint": kwargs["source_path_or_endpoint"],
        "notes_limits": kwargs["notes_limits"],
    }


def main() -> None:
    FIG.mkdir(parents=True, exist_ok=True)
    INTER.mkdir(parents=True, exist_ok=True)

    btos = pd.read_csv(FIG / "figure3_panelA_btos_ai_trends.csv").sort_values("period_start_date")
    hours = pd.read_csv(FIG / "figure2_panelA_hours_by_ai_tercile.csv").sort_values("month")
    trans = pd.read_csv(FIG / "figure2_panelB_transition_probs.csv").sort_values("month")
    counts = pd.read_csv(FIG / "figure2_panelB_transition_counts.csv")
    occ = pd.read_csv(FIG / "figure1_panelA_occ_baseline.csv")
    terc = pd.read_csv(INTER / "ai_relevance_terciles.csv")
    jolts = pd.read_csv(FIG / "figure4_panelA_jolts_sector_rates.csv")
    ces = pd.read_csv(FIG / "figure4_panelB_ces_sector_index.csv")

    rows: list[dict[str, object]] = []

    # KPI 1: BTOS current AI use level + change over 4 periods.
    btos_last = btos.iloc[-1]
    btos_prev = btos.iloc[-5] if len(btos) >= 5 else btos.iloc[0]
    rows.append(
        _kpi_row(
            kpi_id="btos_current_ai_use_rate",
            kpi_label="BTOS current AI use (national)",
            value=float(btos_last["ai_use_current_rate"]),
            unit="share",
            reference_period=str(btos_last["period_start_date"]),
            change_value=float(btos_last["ai_use_current_rate"] - btos_prev["ai_use_current_rate"]),
            change_unit="share",
            change_window="4 BTOS periods",
            source_primary="BTOS API national stratum",
            source_path_or_endpoint="figures/figure3_panelA_btos_ai_trends.csv",
            notes_limits="Business-reported adoption share; descriptive monitoring only.",
        )
    )

    # KPI 2: CPS hours high-low gap, latest month.
    h_last_month = str(hours["month"].max())
    h_last = hours[hours["month"] == h_last_month].set_index("ai_relevance_tercile")
    gap = float(h_last.loc["high", "mean_usual_weekly_hours"] - h_last.loc["low", "mean_usual_weekly_hours"])
    rows.append(
        _kpi_row(
            kpi_id="cps_hours_high_minus_low",
            kpi_label="CPS weekly-hours gap (high AI tercile minus low)",
            value=gap,
            unit="hours",
            reference_period=h_last_month,
            change_value=None,
            change_unit=None,
            change_window=None,
            source_primary="CPS Basic Monthly",
            source_path_or_endpoint="figures/figure2_panelA_hours_by_ai_tercile.csv",
            notes_limits="Survey-based weighted means by frozen AI terciles; descriptive only.",
        )
    )

    # KPI 3: CPS entry rates by AI tercile (high tercile headline).
    occ_to_terc = {f"occ22_{int(r.occ22_id):02d}": str(r.ai_relevance_tercile) for r in terc.itertuples(index=False)}

    origin_mass = (
        counts.groupby(["month", "origin_state"], as_index=False)["weighted_transition_count"]
        .sum()
        .rename(columns={"weighted_transition_count": "origin_mass"})
    )

    def _terc_metric_value(month: str, metric_name: str, tercile_name: str) -> float:
        t_month = trans[(trans["month"] == month) & (trans["record_type"] == "summary")].copy()
        t_month = t_month[t_month["origin_state"].astype(str).str.startswith("occ22_")].copy()
        t_month["ai_relevance_tercile"] = t_month["origin_state"].map(occ_to_terc)
        t_month = t_month[t_month["ai_relevance_tercile"].isin(["low", "middle", "high"])].copy()
        # figure2_panelB_transition_probs.csv may carry placeholder columns from the matrix rows;
        # origin mass for weighting must come from transition_counts aggregation.
        for col in ("origin_mass", "weighted_transition_count", "transition_probability", "destination_state"):
            if col in t_month.columns:
                t_month = t_month.drop(columns=[col])
        t_month = t_month.merge(origin_mass, on=["month", "origin_state"], how="left")
        sub = t_month[t_month["metric_name"] == metric_name].copy()
        sub["metric_value"] = pd.to_numeric(sub["metric_value"], errors="coerce")
        sub["origin_mass"] = pd.to_numeric(sub["origin_mass"], errors="coerce")
        sub = sub[sub["metric_value"].notna() & sub["origin_mass"].notna()]
        s = sub[sub["ai_relevance_tercile"] == tercile_name]
        if s.empty:
            raise RuntimeError(
                f"No rows for metric={metric_name} tercile={tercile_name} in month {month}"
            )
        return float((s["metric_value"] * s["origin_mass"]).sum() / s["origin_mass"].sum())

    months_desc = sorted(trans["month"].dropna().astype(str).unique(), reverse=True)
    chosen_month: str | None = None
    u_entry: float | None = None
    nilf_entry: float | None = None
    months_skipped: list[dict[str, str]] = []
    for m in months_desc:
        try:
            u = _terc_metric_value(m, "unemployment_entry_rate", "high")
            n = _terc_metric_value(m, "nilf_entry_rate", "high")
        except RuntimeError:
            months_skipped.append(
                {
                    "month": m,
                    "outcome": "incomplete_or_missing_for_high_tercile_after_counts_merge",
                }
            )
            continue
        chosen_month = m
        u_entry = u
        nilf_entry = n
        break
    if chosen_month is None or u_entry is None or nilf_entry is None:
        raise RuntimeError("Could not compute tercile-weighted entry KPIs for any month.")

    entry_notes_common = (
        "Origin-mass-weighted mean of summary metric_value across high-tercile occ22 "
        "origins; origin_mass = sum of weighted_transition_count from "
        "figure2_panelB_transition_counts by (month, origin_state). "
        "Month = latest (descending) where both unemployment_entry_rate and "
        "nilf_entry_rate are computable. Descriptive matched-month construct only."
    )
    if h_last_month != chosen_month:
        entry_notes_common += (
            f" Month alignment: CPS hours KPI uses latest month in figure2_panelA "
            f"({h_last_month}); these entry KPIs use {chosen_month}. "
            "See docs/memo_visual_precision.md."
        )

    rows.append(
        _kpi_row(
            kpi_id="cps_unemployment_entry_rate",
            kpi_label="CPS unemployment-entry rate (high AI tercile origins)",
            value=u_entry,
            unit="share",
            reference_period=chosen_month,
            change_value=None,
            change_unit=None,
            change_window=None,
            source_primary="CPS matched-month transition summary",
            source_path_or_endpoint=(
                "figures/figure2_panelB_transition_probs.csv; "
                "figures/figure2_panelB_transition_counts.csv (origin mass)"
            ),
            notes_limits=entry_notes_common,
        )
    )
    rows.append(
        _kpi_row(
            kpi_id="cps_nilf_entry_rate",
            kpi_label="CPS NILF-entry rate (high AI tercile origins)",
            value=nilf_entry,
            unit="share",
            reference_period=chosen_month,
            change_value=None,
            change_unit=None,
            change_window=None,
            source_primary="CPS matched-month transition summary",
            source_path_or_endpoint=(
                "figures/figure2_panelB_transition_probs.csv; "
                "figures/figure2_panelB_transition_counts.csv (origin mass)"
            ),
            notes_limits=entry_notes_common,
        )
    )

    # KPI 4: Top-5 high-tercile occupation employment share total.
    high_groups = set(terc[terc["ai_relevance_tercile"] == "high"]["occupation_group"])
    occ_high = occ[occ["occupation_group"].isin(high_groups)].sort_values("employment_share", ascending=False).head(5)
    rows.append(
        _kpi_row(
            kpi_id="top5_high_ai_occ_employment_share_sum",
            kpi_label="Top-5 high-AI occupation groups: combined employment share",
            value=float(occ_high["employment_share"].sum()),
            unit="share",
            reference_period="OEWS May 2024",
            change_value=None,
            change_unit=None,
            change_window=None,
            source_primary="OEWS + frozen AI terciles",
            source_path_or_endpoint="figures/figure1_panelA_occ_baseline.csv; intermediate/ai_relevance_terciles.csv",
            notes_limits="Structural occupation mix baseline; not evidence of realized AI impact.",
        )
    )

    # KPI 5: Sector demand context ranges (JOLTS openings, CES index).
    j_last_month = str(jolts["month"].max())
    j_last = jolts[(jolts["month"] == j_last_month) & (jolts["rate_name"] == "job_openings_rate")]
    c_last_month = str(ces["month"].max())
    c_last = ces[ces["month"] == c_last_month]
    rows.append(
        _kpi_row(
            kpi_id="jolts_openings_rate_sector_range",
            kpi_label="JOLTS job-openings-rate range across six sectors",
            value=float(j_last["rate_value"].max() - j_last["rate_value"].min()),
            unit="percentage_points",
            reference_period=j_last_month,
            change_value=float(j_last["rate_value"].max()),
            change_unit="max_level",
            change_window="cross-sector spread",
            source_primary="BLS JOLTS sector6 mapped series",
            source_path_or_endpoint="figures/figure4_panelA_jolts_sector_rates.csv",
            notes_limits="Sector context only; not occupation-level AI-attributed demand.",
        )
    )
    rows.append(
        _kpi_row(
            kpi_id="ces_payroll_index_sector_range",
            kpi_label="CES payroll index range across six sectors (Aug 2023=100)",
            value=float(c_last["index_aug2023_100"].max() - c_last["index_aug2023_100"].min()),
            unit="index_points",
            reference_period=c_last_month,
            change_value=float(c_last["index_aug2023_100"].max()),
            change_unit="max_level",
            change_window="cross-sector spread",
            source_primary="BLS CES sector6 mapped series",
            source_path_or_endpoint="figures/figure4_panelB_ces_sector_index.csv",
            notes_limits="Payroll context by sector; descriptive, not occupation-level attribution.",
        )
    )

    out = pd.DataFrame(rows)
    out.to_csv(OUT_CSV, index=False)

    meta = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "output_csv": str(OUT_CSV.relative_to(ROOT)).replace("\\", "/"),
        "row_count": int(len(out)),
        "kpi_schema": list(out.columns),
        "precision_reference": "docs/memo_visual_precision.md",
        "cps_hours_kpi_latest_month": h_last_month,
        "cps_entry_kpi_reference_month": chosen_month,
        "cps_dashboard_kpi_month_alignment": bool(h_last_month == chosen_month),
        "cps_entry_kpi_selection_rule": (
            "Walk months in descending string order from figure2_panelB_transition_probs; "
            "first month where both unemployment_entry_rate and nilf_entry_rate "
            "are computable for high tercile via counts-derived origin_mass merge."
        ),
        "cps_entry_kpi_months_skipped_before_selection": months_skipped,
        "notes": "Memo dashboard KPIs are descriptive monitoring constructs only.",
    }
    OUT_META.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(f"Wrote {OUT_CSV} ({len(out)} rows)")
    print(f"Wrote {OUT_META}")


if __name__ == "__main__":
    main()

