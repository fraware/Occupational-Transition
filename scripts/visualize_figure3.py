from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd

from viz_style import STYLE, apply_matplotlib_style, save_dual
from viz_utils import read_figure_csv


def render_t006() -> list[str]:
    df = read_figure_csv("figure3_panelA_btos_ai_trends.csv").copy()
    df["dt"] = pd.to_datetime(df["period_start_date"], errors="coerce")
    df = df.sort_values("dt")
    fig, ax = plt.subplots(figsize=(9.5, 4.6))
    ax.plot(
        df["dt"],
        df["ai_use_current_rate"],
        color=STYLE.high_color,
        label="Current AI use",
    )
    ax.plot(
        df["dt"],
        df["ai_use_expected_6m_rate"],
        color=STYLE.middle_color,
        label="Expected AI use (6m)",
    )
    ax.set_title("T-006 Figure 3 Panel A: BTOS AI Use Trends")
    ax.set_xlabel("Period start date")
    ax.set_ylabel("Rate")
    ax.legend()
    p1, _ = save_dual(fig, "t006_btos_ai_trends")
    return [p1.stem]


def render_t007() -> list[str]:
    df = read_figure_csv("figure3_panelB_btos_workforce_effects.csv").copy()
    df = df.sort_values("weighted_share", ascending=True)
    fig, ax = plt.subplots(figsize=(9.2, 5.2))
    ax.barh(df["category_label"], df["weighted_share"], color="#5f9ea0")
    ax.set_title("T-007 Figure 3 Panel B: Workforce Effects")
    ax.set_xlabel("Weighted share")
    ax.set_ylabel("Category")
    p1, _ = save_dual(fig, "t007_btos_workforce_effects_barh")
    return [p1.stem]


def main() -> None:
    apply_matplotlib_style()
    stems: list[str] = []
    stems += render_t006()
    stems += render_t007()
    print("Wrote figure3 visuals:", ", ".join(stems))


if __name__ == "__main__":
    main()
