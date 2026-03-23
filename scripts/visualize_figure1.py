from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np

from viz_style import apply_matplotlib_style, save_dual
from viz_utils import read_figure_csv


def render_t001() -> list[str]:
    df = read_figure_csv("figure1_panelA_occ_baseline.csv").copy()
    df = df.sort_values("employment_share", ascending=True)
    fig, ax = plt.subplots(figsize=(9, 7.5))
    bars = ax.barh(
        df["occupation_group"], df["employment_share"], color="#4c78a8"
    )
    ax.set_title("T-001 Figure 1 Panel A: Occupation Employment Share")
    ax.set_xlabel("Employment share")
    ax.set_ylabel("Occupation group")
    for b, wage in zip(bars, df["median_annual_wage"]):
        ax.text(
            b.get_width() + 0.0015,
            b.get_y() + b.get_height() / 2.0,
            f"${int(wage):,}",
            va="center",
            fontsize=8,
        )
    p1, _ = save_dual(fig, "t001_occupation_share_barh")
    return [p1.stem]


def render_t002() -> list[str]:
    df = read_figure_csv("figure1_panelB_task_heatmap.csv").copy()
    zcols = [c for c in df.columns if c.startswith("z_")]
    m = df.sort_values("occ22_id")[zcols].to_numpy()
    fig, ax = plt.subplots(figsize=(10, 6.5))
    im = ax.imshow(m, aspect="auto", cmap="coolwarm")
    ax.set_title("T-002 Figure 1 Panel B: Task Heatmap (z-scores)")
    ax.set_yticks(np.arange(len(df)))
    ax.set_yticklabels(
        df.sort_values("occ22_id")["occupation_group"], fontsize=7
    )
    ax.set_xticks(np.arange(len(zcols)))
    ax.set_xticklabels(
        [c.replace("z_", "") for c in zcols], rotation=30, ha="right"
    )
    fig.colorbar(im, ax=ax, fraction=0.03, pad=0.02)
    p1, _ = save_dual(fig, "t002_task_heatmap")
    return [p1.stem]


def main() -> None:
    apply_matplotlib_style()
    stems: list[str] = []
    stems += render_t001()
    stems += render_t002()
    print("Wrote figure1 visuals:", ", ".join(stems))


if __name__ == "__main__":
    main()
