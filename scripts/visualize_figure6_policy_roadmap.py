"""Figure 6: Section 8 policy roadmap from frozen layout CSV."""

from __future__ import annotations

import textwrap

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle

from viz_style import apply_matplotlib_style, save_dual
from viz_utils import read_figure_csv

# Horizontal gap (data coords) so arrow endpoints sit outside box edges, not on text.
_ARROW_GAP = 0.045


def _box_size(kind: str) -> tuple[float, float]:
    if kind == "frontier":
        return 1.35, 1.06
    return 1.22, 0.88


def _box_center_y(row: pd.Series) -> float:
    _, h = _box_size(row["kind"])
    return float(row["y"] + h / 2)


def _point_right_of_box(row: pd.Series) -> tuple[float, float]:
    w, h = _box_size(row["kind"])
    return float(row["x"] + w + _ARROW_GAP), float(row["y"] + h / 2)


def _point_left_of_box(row: pd.Series) -> tuple[float, float]:
    return float(row["x"] - _ARROW_GAP), _box_center_y(row)


def _add_flow_arrows(ax: plt.Axes, df: pd.DataFrame) -> None:
    """Left-to-right flow; endpoints offset past box borders to avoid text overlap."""
    current = df[df["kind"] == "current"].sort_values("y", ascending=False)
    frontier = df[df["kind"] == "frontier"].iloc[0]
    proposal = df[df["kind"] == "proposal"].sort_values("y", ascending=False)
    horizon = df[df["kind"] == "horizon"].iloc[0]

    _, fh = _box_size(str(frontier["kind"]))
    f_cy = float(frontier["y"] + fh / 2)
    f_left = (float(frontier["x"]) - _ARROW_GAP, f_cy)

    arrow_kw: dict = {
        "arrowstyle": "->",
        "mutation_scale": 10,
        "linewidth": 1.15,
        "color": "#333333",
        "zorder": 1,
        "clip_on": False,
    }

    for _, row in current.iterrows():
        xy1 = _point_right_of_box(row)
        patch = FancyArrowPatch(xy1, f_left, **arrow_kw)
        ax.add_patch(patch)

    f_right = _point_right_of_box(frontier)
    for _, row in proposal.iterrows():
        xy2 = _point_left_of_box(row)
        patch = FancyArrowPatch(f_right, xy2, **arrow_kw)
        ax.add_patch(patch)

    mid_prop = proposal.iloc[len(proposal) // 2]
    p_right = _point_right_of_box(mid_prop)
    h_left = _point_left_of_box(horizon)
    ax.add_patch(FancyArrowPatch(p_right, h_left, **arrow_kw))


def main() -> None:
    apply_matplotlib_style()
    df = read_figure_csv("figure6_policy_roadmap.csv").copy()

    fig, ax = plt.subplots(figsize=(15.8, 9.0))
    ax.set_xlim(-0.2, 6.48)
    ax.set_ylim(0.0, 3.95)
    ax.axis("off")

    style = {
        "current": {"linestyle": "solid", "linewidth": 1.2},
        "frontier": {"linestyle": "solid", "linewidth": 2.4},
        "proposal": {"linestyle": "solid", "linewidth": 1.2},
        "horizon": {"linestyle": "dashed", "linewidth": 1.4},
    }

    _add_flow_arrows(ax, df)

    for _, r in df.iterrows():
        kind = str(r["kind"])
        width, height = _box_size(kind)
        box = FancyBboxPatch(
            (float(r["x"]), float(r["y"])),
            width,
            height,
            boxstyle="round,pad=0.02,rounding_size=0.03",
            fill=True,
            facecolor="white",
            edgecolor="black",
            linestyle=style[kind]["linestyle"],
            linewidth=style[kind]["linewidth"],
            zorder=2,
        )
        ax.add_patch(box)

    for _, r in df.iterrows():
        kind = str(r["kind"])
        width, height = _box_size(kind)
        title_y = float(r["y"]) + height - 0.095
        body_top = float(r["y"]) + height - 0.24
        ax.text(
            float(r["x"]) + width / 2,
            title_y,
            str(r["title"]),
            fontsize=11.0,
            fontweight="bold",
            ha="center",
            va="top",
            zorder=3,
        )
        wrap_w = 30 if kind != "frontier" else 34
        ax.text(
            float(r["x"]) + 0.065,
            body_top,
            textwrap.fill(str(r["body"]), width=wrap_w),
            fontsize=9.4,
            ha="left",
            va="top",
            zorder=3,
        )

    header_y = 3.44
    rule_y = 3.28
    headers = [
        ("Current public observables", 0.35),
        ("Identification frontier", 1.9),
        ("Near-term survey agenda", 3.55),
        ("Long-run horizon", 5.15),
    ]
    for title, xpos in headers:
        ax.text(
            xpos,
            header_y,
            title,
            fontsize=12.6,
            fontweight="bold",
            ha="center",
            va="center",
            zorder=4,
        )
        ax.plot(
            [xpos - 0.65, xpos + 0.65],
            [rule_y, rule_y],
            linewidth=1.2,
            color="black",
            zorder=4,
        )

    legend_specs = [
        (0.06, 0.13, "Observed directly or structurally supported", "current"),
        (2.05, 0.13, "Hard public-data frontier", "frontier"),
        (0.06, 0.045, "Defensible marginal intervention", "proposal"),
        (2.05, 0.045, "Long-run institutional horizon", "horizon"),
    ]
    for x0, legend_y, label, kind in legend_specs:
        ax.add_patch(
            Rectangle(
                (x0, legend_y),
                0.15,
                0.085,
                fill=False,
                linestyle=style[kind]["linestyle"],
                linewidth=min(style[kind]["linewidth"], 2.0),
                zorder=4,
            )
        )
        ax.text(
            x0 + 0.2,
            legend_y + 0.042,
            label,
            fontsize=9.1,
            va="center",
            ha="left",
            zorder=4,
        )

    fig.text(
        0.055,
        0.018,
        "Section 8 synthesis; layout from figures/figure6_policy_roadmap.csv.",
        fontsize=9.4,
        ha="left",
        va="bottom",
    )

    save_dual(fig, "policy_roadmap", tight_layout=False)
    print("Wrote figure6 roadmap visuals: policy_roadmap")


if __name__ == "__main__":
    main()
