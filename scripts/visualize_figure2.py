from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from viz_style import STYLE, apply_matplotlib_style, save_dual
from viz_utils import TERCILE_ORDER, parse_month_col, read_figure_csv


def render_t003() -> list[str]:
    df = read_figure_csv("figure2_panelA_hours_by_ai_tercile.csv").copy()
    df["month_dt"] = parse_month_col(df, "month")
    fig, ax = plt.subplots(figsize=(10, 4.8))
    colors = {
        "low": STYLE.low_color,
        "middle": STYLE.middle_color,
        "high": STYLE.high_color,
    }
    for t in TERCILE_ORDER:
        sub = df[df["ai_relevance_tercile"] == t].sort_values("month_dt")
        ax.plot(
            sub["month_dt"],
            sub["mean_usual_weekly_hours"],
            label=t,
            color=colors[t],
            linewidth=2,
        )
    ax.set_title("Figure 2 Panel A: Mean Usual Weekly Hours")
    ax.set_xlabel("Month")
    ax.set_ylabel("Hours")
    ax.legend(title="AI tercile")
    p1, _ = save_dual(fig, "hours_timeseries")
    return [p1.stem]


def render_t004() -> list[str]:
    df = read_figure_csv("figure2_panelB_transition_counts.csv").copy()
    latest = df["month"].max()
    sub = df[df["month"] == latest].copy()
    state_order = [f"occ22_{i:02d}" for i in range(1, 23)] + [
        "unemployed",
        "nilf",
    ]
    mat = sub.pivot_table(
        index="origin_state",
        columns="destination_state",
        values="weighted_transition_count",
        aggfunc="sum",
        fill_value=0.0,
    )
    mat = mat.reindex(index=state_order, columns=state_order, fill_value=0.0)
    fig, ax = plt.subplots(figsize=(8.5, 7))
    mat_display = np.log1p(mat.to_numpy())
    im = ax.imshow(mat_display, cmap="viridis", aspect="auto")
    ax.set_title(f"Figure 2 Panel B Counts: {latest}")
    ax.set_xlabel("Destination state")
    ax.set_ylabel("Origin state")
    ax.set_xticks(range(len(mat.columns)))
    ax.set_xticklabels(mat.columns, rotation=90, fontsize=6)
    ax.set_yticks(range(len(mat.index)))
    ax.set_yticklabels(mat.index, fontsize=6)
    cbar = fig.colorbar(im, ax=ax, fraction=0.03, pad=0.02)
    cbar.set_label("log1p(weighted transition count)")
    p1, _ = save_dual(fig, "transition_counts_heatmap_latest")
    return [p1.stem]


def render_t005() -> list[str]:
    df = read_figure_csv("figure2_panelB_transition_probs.csv").copy()
    employed_origins = [f"occ22_{i:02d}" for i in range(1, 23)]
    summary = df[df["record_type"] == "summary"][
        ["month", "origin_state", "metric_name", "metric_value"]
    ].copy()
    if summary.empty:
        return []
    origin_mass = (
        df[df["record_type"] == "matrix"][
            ["month", "origin_state", "origin_mass"]
        ]
        .drop_duplicates(["month", "origin_state"])
        .copy()
    )
    sub = summary.merge(
        origin_mass,
        on=["month", "origin_state"],
        how="left",
        validate="many_to_one",
    )
    # Use employed-origin occupations only for transition interpretation.
    sub = sub[sub["origin_state"].isin(employed_origins)].copy()
    sub["metric_value"] = pd.to_numeric(sub["metric_value"], errors="coerce")
    sub["origin_mass"] = pd.to_numeric(sub["origin_mass"], errors="coerce")
    sub = sub[
        sub["metric_value"].notna() & sub["origin_mass"].gt(0)
    ].copy()
    if sub.empty:
        return []

    agg = (
        sub.groupby(["month", "metric_name"], as_index=False)
        .apply(
            lambda g: pd.Series(
                {
                    "metric_value": np.average(
                        g["metric_value"].astype(float),
                        weights=g["origin_mass"].astype(float),
                    )
                }
            )
        )
        .reset_index(drop=True)
    )
    agg["month_dt"] = parse_month_col(agg, "month")
    fig, axes = plt.subplots(2, 1, figsize=(10, 7.2), sharex=True)
    upper = agg[agg["metric_name"] == "retention_rate"].copy()
    lower = agg[agg["metric_name"] != "retention_rate"].copy()

    if not upper.empty:
        g = upper.sort_values("month_dt")
        axes[0].plot(
            g["month_dt"],
            g["metric_value"],
            linewidth=2.0,
            label="retention_rate",
        )
    axes[0].set_title(
        "Figure 2 Panel B: Employed-origin summary transition metrics"
    )
    axes[0].set_ylabel("Retention rate")
    axes[0].legend(loc="best", fontsize=8)

    for metric, g in lower.groupby("metric_name"):
        g = g.sort_values("month_dt")
        axes[1].plot(
            g["month_dt"], g["metric_value"], linewidth=1.8, label=metric
        )
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Entry/switch rates")
    axes[1].legend(ncol=3, fontsize=8)
    p1, _ = save_dual(fig, "transition_summary_metrics")
    return [p1.stem]


def main() -> None:
    apply_matplotlib_style()
    stems: list[str] = []
    stems += render_t003()
    stems += render_t004()
    stems += render_t005()
    print("Wrote figure2 visuals:", ", ".join(stems))


if __name__ == "__main__":
    main()
