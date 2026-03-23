from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd

from viz_style import STYLE, apply_matplotlib_style, save_dual
from viz_utils import TERCILE_ORDER, parse_month_col, read_figure_csv


def render_t003() -> list[str]:
    df = read_figure_csv("figure2_panelA_hours_by_ai_tercile.csv").copy()
    df["month_dt"] = parse_month_col(df, "month")
    fig, ax = plt.subplots(figsize=(10, 4.8))
    colors = {"low": STYLE.low_color, "middle": STYLE.middle_color, "high": STYLE.high_color}
    for t in TERCILE_ORDER:
        sub = df[df["ai_relevance_tercile"] == t].sort_values("month_dt")
        ax.plot(sub["month_dt"], sub["mean_usual_weekly_hours"], label=t, color=colors[t], linewidth=2)
    ax.set_title("T-003 Figure 2 Panel A: Mean Usual Weekly Hours")
    ax.set_xlabel("Month")
    ax.set_ylabel("Hours")
    ax.legend(title="AI tercile")
    p1, _ = save_dual(fig, "t003_hours_timeseries")
    return [p1.stem]


def render_t004() -> list[str]:
    df = read_figure_csv("figure2_panelB_transition_counts.csv").copy()
    latest = df["month"].max()
    sub = df[df["month"] == latest].copy()
    mat = sub.pivot_table(
        index="origin_state",
        columns="destination_state",
        values="weighted_transition_count",
        aggfunc="sum",
        fill_value=0.0,
    )
    fig, ax = plt.subplots(figsize=(8.5, 7))
    im = ax.imshow(mat.to_numpy(), cmap="viridis", aspect="auto")
    ax.set_title(f"T-004 Figure 2 Panel B Counts: {latest}")
    ax.set_xlabel("Destination state")
    ax.set_ylabel("Origin state")
    ax.set_xticks(range(len(mat.columns)))
    ax.set_xticklabels(mat.columns, rotation=90, fontsize=6)
    ax.set_yticks(range(len(mat.index)))
    ax.set_yticklabels(mat.index, fontsize=6)
    fig.colorbar(im, ax=ax, fraction=0.03, pad=0.02)
    p1, _ = save_dual(fig, "t004_transition_counts_heatmap_latest")
    return [p1.stem]


def render_t005() -> list[str]:
    df = read_figure_csv("figure2_panelB_transition_probs.csv").copy()
    sub = df[df["record_type"] == "summary"].copy()
    if sub.empty:
        return []
    sub["month_dt"] = parse_month_col(sub, "month")
    fig, ax = plt.subplots(figsize=(10, 4.8))
    for metric, g in sub.groupby("metric_name"):
        g = g.sort_values("month_dt")
        ax.plot(g["month_dt"], g["metric_value"], linewidth=1.8, label=metric)
    ax.set_title("T-005 Figure 2 Panel B: Summary Transition Metrics")
    ax.set_xlabel("Month")
    ax.set_ylabel("Rate")
    ax.legend(ncol=2, fontsize=8)
    p1, _ = save_dual(fig, "t005_transition_summary_metrics")
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
