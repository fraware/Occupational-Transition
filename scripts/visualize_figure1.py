"""Figure 1: Panel A occupational baseline; Panel B task heatmap with AI bands."""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Rectangle

from viz_style import apply_matplotlib_style, save_dual
from viz_utils import read_figure_csv

OCC_SHORT_LABELS: dict[str, str] = {
    "Management Occupations": "Management",
    "Business and Financial Operations Occupations": "Business & finance",
    "Computer and Mathematical Occupations": "Computer & math",
    "Architecture and Engineering Occupations": "Architecture & engineering",
    "Life, Physical, and Social Science Occupations": (
        "Life / physical / social science"
    ),
    "Community and Social Service Occupations": "Community & social service",
    "Legal Occupations": "Legal",
    "Educational Instruction and Library Occupations": "Education & library",
    "Arts, Design, Entertainment, Sports, and Media Occupations": (
        "Arts / design / media"
    ),
    "Healthcare Practitioners and Technical Occupations": "Healthcare practitioners",
    "Healthcare Support Occupations": "Healthcare support",
    "Protective Service Occupations": "Protective service",
    "Food Preparation and Serving Related Occupations": "Food prep & serving",
    "Building and Grounds Cleaning and Maintenance Occupations": "Building & grounds",
    "Personal Care and Service Occupations": "Personal care",
    "Sales and Related Occupations": "Sales",
    "Office and Administrative Support Occupations": "Office & admin support",
    "Farming, Fishing, and Forestry Occupations": "Farming / fishing / forestry",
    "Construction and Extraction Occupations": "Construction & extraction",
    "Installation, Maintenance, and Repair Occupations": "Installation / repair",
    "Production Occupations": "Production",
    "Transportation and Material Moving Occupations": (
        "Transportation / material moving"
    ),
}


def build_panel_a(dfa: pd.DataFrame) -> plt.Figure:
    dfa = dfa.sort_values("employment_share", ascending=True).reset_index(drop=True)
    dfa["short_label"] = dfa["occupation_group"].map(OCC_SHORT_LABELS)

    fig, ax = plt.subplots(figsize=(11.2, 7.2))
    y = np.arange(len(dfa))
    ax.barh(y, dfa["employment_share"] * 100, height=0.72)
    ax.set_yticks(y)
    ax.set_yticklabels(dfa["short_label"], fontsize=9.6)
    ax.set_xlabel("Employment share (%)", fontsize=11)
    ax.grid(True, axis="x", linewidth=0.5)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax2 = ax.twiny()
    ax2.scatter(dfa["median_annual_wage"], y, s=30, marker="o")
    ax2.set_xlabel("Median annual wage (USD)", fontsize=11, labelpad=8)
    ax2.tick_params(axis="x", labelsize=9.4)

    top_three = dfa.sort_values("employment_share", ascending=False).head(3)
    occ_to_y = dict(zip(dfa["occupation_group"], y, strict=True))
    for _, row in top_three.iterrows():
        yy = occ_to_y[row["occupation_group"]]
        ax.text(
            row["employment_share"] * 100 + 0.6,
            float(yy),
            f"{row['employment_share'] * 100:.1f}%",
            fontsize=9.2,
            va="center",
        )

    wx0, wx1 = ax2.get_xlim()
    ax2.set_xlim(wx0, wx1 + (wx1 - wx0) * 0.075)

    fig.tight_layout()
    return fig


def build_panel_b(dfb: pd.DataFrame) -> plt.Figure:
    ai_cols = [
        "z_analyzing_data_or_information",
        "z_processing_information",
        "z_documenting_recording_information",
        "z_working_with_computers",
    ]
    heat_cols = ai_cols + [
        "z_assisting_and_caring_for_others",
        "z_handling_and_moving_objects",
    ]
    label_map = {
        "z_analyzing_data_or_information": "Analyzing\ninformation",
        "z_processing_information": "Processing\ninformation",
        "z_documenting_recording_information": "Documenting /\nrecording",
        "z_working_with_computers": "Working with\ncomputers",
        "z_assisting_and_caring_for_others": "Assisting /\ncaring",
        "z_handling_and_moving_objects": "Handling /\nmoving objects",
    }

    dfb = dfb.copy()
    dfb["ai_task_index"] = dfb[ai_cols].mean(axis=1)
    dfb = dfb.sort_values(
        ["ai_task_index", "occ22_id"],
        ascending=[True, True],
    ).reset_index(drop=True)
    dfb["short_label"] = dfb["occupation_group"].map(OCC_SHORT_LABELS)

    fig, ax = plt.subplots(figsize=(11.2, 8.2))
    heat_data = dfb[heat_cols].to_numpy()
    im = ax.imshow(heat_data, aspect="auto", cmap="coolwarm", vmin=-2.5, vmax=2.5)

    ax.set_yticks(np.arange(len(dfb)))
    ax.set_yticklabels(dfb["short_label"], fontsize=9.4)
    ax.set_xticks(np.arange(len(heat_cols)))
    ax.set_xticklabels([label_map[c] for c in heat_cols], fontsize=9.8)
    band_specs = [("Low", 0, 7), ("Middle", 7, 14), ("High", 14, 22)]
    for label, start, end in band_specs:
        rect = Rectangle(
            (-0.5, start - 0.5),
            len(heat_cols),
            end - start,
            fill=False,
            linewidth=2.0,
        )
        ax.add_patch(rect)
        ax.text(
            len(heat_cols) + 0.15,
            (start + end - 1) / 2,
            label,
            fontsize=11.0,
            fontweight="bold",
            va="center",
        )

    ax.set_xlim(-0.5, len(heat_cols) + 1.15)
    cbar = fig.colorbar(im, ax=ax, fraction=0.03, pad=0.02)
    cbar.set_label("Standardized task value (z-score)", fontsize=10.2)

    fig.tight_layout()
    return fig


def main() -> None:
    apply_matplotlib_style()

    dfa = read_figure_csv("figure1_panelA_occ_baseline.csv").copy()
    dfb = read_figure_csv("figure1_panelB_task_heatmap.csv").copy()

    fig_a = build_panel_a(dfa)
    save_dual(fig_a, "occupation_share_barh")

    fig_b = build_panel_b(dfb)
    save_dual(fig_b, "task_heatmap")

    print("Wrote figure1 visuals: occupation_share_barh, task_heatmap")


if __name__ == "__main__":
    main()
