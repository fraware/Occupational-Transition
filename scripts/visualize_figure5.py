from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np

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
        "local_geographic_exposure",
    ]
    code = {"direct": 2, "partial": 1, "none": 0}
    mat = np.array(
        [
            [code.get(str(v).strip().lower(), 0) for v in row]
            for row in df[cols].to_numpy()
        ]
    )

    fig, ax = plt.subplots(figsize=(11, 4.8))
    im = ax.imshow(mat, cmap="YlGnBu", vmin=0, vmax=2, aspect="auto")
    ax.set_title("T-010 Figure 5: Capability Matrix")
    ax.set_yticks(range(len(df)))
    ax.set_yticklabels(df["dataset_label"])
    ax.set_xticks(range(len(cols)))
    ax.set_xticklabels(
        [c.replace("_", " ") for c in cols], rotation=25, ha="right"
    )
    cbar = fig.colorbar(im, ax=ax, fraction=0.03, pad=0.02)
    cbar.set_ticks([0, 1, 2])
    cbar.set_ticklabels(["none", "partial", "direct"])
    p1, _ = save_dual(fig, "t010_capability_matrix_heatmap")
    print("Wrote figure5 visuals:", p1.stem)


if __name__ == "__main__":
    main()
