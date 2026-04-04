from __future__ import annotations

import matplotlib.pyplot as plt
from matplotlib.patches import Patch, Rectangle

from viz_style import apply_matplotlib_style, save_dual
from viz_utils import read_figure_csv


def main() -> None:
    apply_matplotlib_style()
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

    col_labels = {
        "worker_outcomes": "Worker\noutcomes",
        "worker_occupational_transitions": "Occupational\ntransitions",
        "firm_ai_adoption": "Firm AI\nadoption",
        "labor_demand_turnover": "Demand &\nturnover",
        "occupational_structure_wages": "Structure &\nwages",
        "task_exposure_mechanism": "Task\nmechanism",
        "worker_firm_ai_linkage": "Worker-firm\nAI linkage",
    }

    group_spans = [
        ("Worker-side", 0, 1),
        ("Firm-side", 2, 2),
        ("Context", 3, 3),
        ("Structure & mechanism", 4, 5),
        ("Integrated linkage", 6, 6),
    ]

    style_map = {
        "direct": {"hatch": "////", "linewidth": 1.4},
        "partial": {"hatch": "..", "linewidth": 1.0},
        "none": {"hatch": "", "linewidth": 0.8},
    }

    rows = df["dataset_label"].tolist()
    n_rows = len(rows)
    n_cols = len(cols)

    fig = plt.figure(figsize=(13.8, 6.7))
    ax = fig.add_axes([0.10, 0.17, 0.72, 0.63])
    ax.grid(False)

    for i, _ in enumerate(rows):
        for j, col in enumerate(cols):
            val = str(df.loc[i, col]).strip().lower()
            st = style_map[val]
            y = n_rows - 1 - i
            rect = Rectangle(
                (j, y),
                1,
                1,
                fill=False,
                hatch=st["hatch"],
                linewidth=st["linewidth"],
            )
            ax.add_patch(rect)

    for x in range(n_cols + 1):
        ax.plot([x, x], [0, n_rows], linewidth=0.8)
    for y in range(n_rows + 1):
        ax.plot([0, n_cols], [y, y], linewidth=0.8)

    frontier_outline = Rectangle((6, 0), 1, n_rows, fill=False, linewidth=2.6)
    ax.add_patch(frontier_outline)

    ax.set_xlim(0, n_cols)
    ax.set_ylim(0, n_rows + 1.05)
    ax.set_xticks([i + 0.5 for i in range(n_cols)])
    ax.set_xticklabels([col_labels[c] for c in cols], fontsize=10)
    ax.tick_params(
        axis="x", bottom=False, top=False, labeltop=True, labelbottom=False, pad=8
    )
    ax.set_yticks([n_rows - 0.5 - i for i in range(n_rows)])
    ax.set_yticklabels(rows, fontsize=10.5)
    ax.tick_params(axis="y", left=False)
    for spine in ax.spines.values():
        spine.set_visible(False)

    header_y = n_rows + 0.55
    for title, start, end in group_spans:
        mid = (start + end + 1) / 2
        ax.text(
            mid,
            header_y,
            title,
            ha="center",
            va="bottom",
            fontsize=10.5,
            fontweight="bold",
        )
        ax.plot([start, end + 1], [n_rows + 0.38, n_rows + 0.38], linewidth=1.2)

    fig.text(
        0.10,
        0.93,
        "Figure 5. The public measurement stack is modular, not integrated",
        fontsize=16,
        fontweight="bold",
        ha="left",
    )
    fig.text(
        0.10,
        0.885,
        (
            "Direct observation is distributed across sources; "
            "worker-firm AI linkage is absent across the full public stack."
        ),
        fontsize=11.5,
        ha="left",
    )
    fig.text(
        0.84,
        0.60,
        "Hard public-data frontier",
        fontsize=11.5,
        fontweight="bold",
        ha="left",
    )
    fig.text(
        0.84,
        0.50,
        (
            "No core public source jointly observes worker occupation, "
            "employer AI adoption, and subsequent worker outcomes."
        ),
        fontsize=10.5,
        ha="left",
        wrap=True,
    )

    legend_handles = [
        Patch(fill=False, hatch="////", label="Direct"),
        Patch(fill=False, hatch="..", label="Partial"),
        Patch(fill=False, label="Not observed"),
    ]
    fig.legend(
        handles=legend_handles,
        loc="lower left",
        bbox_to_anchor=(0.10, 0.04),
        ncol=3,
        frameon=False,
        fontsize=10.5,
        title="Public support status",
    )

    fig.text(
        0.10,
        0.005,
        (
            "Rule-based synthesis figure from the frozen capability-matrix CSV. "
            "Grouped headers are editorial presentation only."
        ),
        fontsize=9.5,
        ha="left",
    )

    p1, _ = save_dual(fig, "capability_matrix_heatmap", tight_layout=False)
    print("Wrote figure5 visuals:", p1.stem)


if __name__ == "__main__":
    main()
