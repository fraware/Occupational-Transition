from __future__ import annotations

import matplotlib.pyplot as plt

from viz_style import STYLE, apply_matplotlib_style, save_dual
from viz_utils import parse_month_col, read_figure_csv


def render_t008() -> list[str]:
    df = read_figure_csv("figure4_panelA_jolts_sector_rates.csv").copy()
    df["month_dt"] = parse_month_col(df, "month")
    sub = df[df["rate_name"] == "job_openings_rate"].copy()
    fig, ax = plt.subplots(figsize=(10, 5))
    for i, (sector, g) in enumerate(sub.groupby("sector6_label")):
        ax.plot(
            g.sort_values("month_dt")["month_dt"],
            g.sort_values("month_dt")["rate_value"],
            label=sector,
            color=STYLE.palette_sector[i % len(STYLE.palette_sector)],
            linewidth=1.6,
        )
    ax.set_title("T-008 Figure 4 Panel A: JOLTS Job Openings Rate")
    ax.set_xlabel("Month")
    ax.set_ylabel("Rate")
    ax.legend(ncol=2, fontsize=8)
    p1, _ = save_dual(fig, "t008_jolts_openings_rate")
    return [p1.stem]


def render_t009() -> list[str]:
    df = read_figure_csv("figure4_panelB_ces_sector_index.csv").copy()
    df["month_dt"] = parse_month_col(df, "month")
    fig, ax = plt.subplots(figsize=(10, 5))
    for i, (sector, g) in enumerate(df.groupby("sector6_label")):
        g = g.sort_values("month_dt")
        ax.plot(
            g["month_dt"],
            g["index_aug2023_100"],
            label=sector,
            color=STYLE.palette_sector[i % len(STYLE.palette_sector)],
            linewidth=1.6,
        )
    ax.axhline(100.0, linestyle="--", linewidth=1.0, color=STYLE.neutral_color)
    ax.set_title("T-009 Figure 4 Panel B: CES Payroll Index (Aug-2023 = 100)")
    ax.set_xlabel("Month")
    ax.set_ylabel("Index")
    ax.legend(ncol=2, fontsize=8)
    p1, _ = save_dual(fig, "t009_ces_payroll_index")
    return [p1.stem]


def main() -> None:
    apply_matplotlib_style()
    stems: list[str] = []
    stems += render_t008()
    stems += render_t009()
    print("Wrote figure4 visuals:", ", ".join(stems))


if __name__ == "__main__":
    main()
