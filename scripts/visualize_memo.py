from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from viz_style import STYLE, apply_matplotlib_style, save_dual
from viz_utils import read_figure_csv


def render_t102() -> list[str]:
    """
    Memo two-panel: BTOS national AI adoption trend + AI supplement workforce effects.

    Inputs:
      - figures/figure3_panelA_btos_ai_trends.csv
      - figures/figure3_panelB_btos_workforce_effects.csv
    """
    trends = read_figure_csv("figure3_panelA_btos_ai_trends.csv").copy()
    trends["dt"] = pd.to_datetime(trends["period_start_date"], errors="coerce")
    trends = trends.sort_values("dt")

    effects = read_figure_csv("figure3_panelB_btos_workforce_effects.csv").copy()
    effects = effects.sort_values("weighted_share", ascending=True)

    fig = plt.figure(figsize=(12.4, 4.8))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.25, 1.0])
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1])

    ax1.plot(
        trends["dt"],
        trends["ai_use_current_rate"],
        color=STYLE.high_color,
        label="Current AI use",
    )
    ax1.plot(
        trends["dt"],
        trends["ai_use_expected_6m_rate"],
        color=STYLE.middle_color,
        label="Expected AI use (6m)",
    )
    ax1.set_title("BTOS AI use (national)")
    ax1.set_xlabel("Period start date")
    ax1.set_ylabel("Firm-weighted share")
    ax1.legend(loc="upper left", frameon=True)

    ax2.barh(effects["category_label"], effects["weighted_share"], color="#5f9ea0")
    ax2.set_title("BTOS AI supplement: workforce effects (retained categories)")
    ax2.set_xlabel("Share (Scope 2 AI-using firms)")
    ax2.set_ylabel("")

    p1, _ = save_dual(fig, "memo_btos_two_panel")
    return [p1.stem]


def render_t107() -> list[str]:
    """
    Memo capability matrix: same underlying categorical matrix, more memo-friendly labels.

    Input:
      - figures/figure5_capability_matrix.csv
    """
    df = read_figure_csv("figure5_capability_matrix.csv").copy()
    cols = [
        "worker_outcomes",
        "worker_occupational_transitions",
        "firm_ai_adoption",
        "labor_demand_turnover",
        "occupational_structure_wages",
        "task_exposure_mechanism",
        "worker_firm_ai_linkage",
    ]
    code = {"direct": 2, "partial": 1, "none": 0}
    mat = np.array([[code.get(str(v).strip().lower(), 0) for v in row] for row in df[cols].to_numpy()])

    col_labels = [
        "Worker outcomes",
        "Worker transitions",
        "Firm AI adoption",
        "Labor demand/turnover",
        "Occ. structure & wages",
        "Task mechanism",
        "Worker–firm AI linkage",
    ]

    fig, ax = plt.subplots(figsize=(11.4, 4.8))
    im = ax.imshow(mat, cmap="YlGnBu", vmin=0, vmax=2, aspect="auto")
    ax.set_title("Memo: What public data can measure directly (capability matrix)")
    ax.set_yticks(range(len(df)))
    ax.set_yticklabels(df["dataset_label"])
    ax.set_xticks(range(len(cols)))
    ax.set_xticklabels(col_labels, rotation=25, ha="right")
    cbar = fig.colorbar(im, ax=ax, fraction=0.03, pad=0.02)
    cbar.set_ticks([0, 1, 2])
    cbar.set_ticklabels(["none", "partial", "direct"])

    p1, _ = save_dual(fig, "memo_capability_matrix")
    return [p1.stem]


def main() -> None:
    apply_matplotlib_style()
    stems: list[str] = []
    stems += render_t102()
    stems += render_t107()
    print("Wrote memo visuals:", ", ".join(stems))


if __name__ == "__main__":
    main()

