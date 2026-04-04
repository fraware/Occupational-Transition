"""Figure 6: Section 8 policy roadmap from frozen layout CSV."""

from __future__ import annotations

import textwrap

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle

from viz_style import apply_matplotlib_style, save_dual
from viz_utils import read_figure_csv


def _box_size(kind: str) -> tuple[float, float]:
    if kind == "frontier":
        return 1.35, 1.02
    return 1.22, 0.82


def _box_right_mid(row: pd.Series) -> tuple[float, float]:
    w, h = _box_size(row["kind"])
    return float(row["x"] + w), float(row["y"] + h / 2)


def _box_left_mid(row: pd.Series) -> tuple[float, float]:
    _, h = _box_size(row["kind"])
    return float(row["x"]), float(row["y"] + h / 2)


def _add_flow_arrows(ax: plt.Axes, df: pd.DataFrame) -> None:
    current = df[df["kind"] == "current"].sort_values("y", ascending=False)
    frontier = df[df["kind"] == "frontier"].iloc[0]
    proposal = df[df["kind"] == "proposal"].sort_values("y", ascending=False)
    horizon = df[df["kind"] == "horizon"].iloc[0]

    fl = _box_left_mid(frontier)
    arrow_kw = {"arrowstyle": "->", "mutation_scale": 14, "linewidth": 1.2}

    for _, row in current.iterrows():
        xy1 = _box_right_mid(row)
        ax.add_patch(FancyArrowPatch(xy1, fl, **arrow_kw))

    fr = _box_right_mid(frontier)
    for _, row in proposal.iterrows():
        xy2 = _box_left_mid(row)
        ax.add_patch(FancyArrowPatch(fr, xy2, **arrow_kw))

    mid_prop = proposal.iloc[len(proposal) // 2]
    pr = _box_right_mid(mid_prop)
    hl = _box_left_mid(horizon)
    ax.add_patch(FancyArrowPatch(pr, hl, **arrow_kw))


def main() -> None:
    apply_matplotlib_style()
    df = read_figure_csv("figure6_policy_roadmap.csv").copy()

    fig, ax = plt.subplots(figsize=(15.8, 9.0))
    ax.set_xlim(-0.2, 6.45)
    ax.set_ylim(0.0, 3.68)
    ax.axis("off")

    headers = [
        ("Current public observables", 0.35),
        ("Identification frontier", 1.9),
        ("Near-term survey agenda", 3.55),
        ("Long-run horizon", 5.15),
    ]
    for title, xpos in headers:
        ax.text(
            xpos,
            3.22,
            title,
            fontsize=13.0,
            fontweight="bold",
            ha="center",
            va="center",
        )
        ax.plot([xpos - 0.65, xpos + 0.65], [3.05, 3.05], linewidth=1.2)

    style = {
        "current": {"linestyle": "solid", "linewidth": 1.2},
        "frontier": {"linestyle": "solid", "linewidth": 2.4},
        "proposal": {"linestyle": "solid", "linewidth": 1.2},
        "horizon": {"linestyle": "dashed", "linewidth": 1.4},
    }

    for _, r in df.iterrows():
        kind = str(r["kind"])
        width, height = _box_size(kind)
        box = FancyBboxPatch(
            (float(r["x"]), float(r["y"])),
            width,
            height,
            boxstyle="round,pad=0.02,rounding_size=0.03",
            fill=False,
            linestyle=style[kind]["linestyle"],
            linewidth=style[kind]["linewidth"],
        )
        ax.add_patch(box)
        ax.text(
            float(r["x"]) + width / 2,
            float(r["y"]) + height - 0.11,
            str(r["title"]),
            fontsize=11.2,
            fontweight="bold",
            ha="center",
            va="top",
        )
        wrap_w = 34 if kind != "frontier" else 36
        ax.text(
            float(r["x"]) + 0.07,
            float(r["y"]) + height - 0.27,
            textwrap.fill(str(r["body"]), width=wrap_w),
            fontsize=9.7,
            ha="left",
            va="top",
        )

    _add_flow_arrows(ax, df)

    legend_y = 0.10
    legend_items = [
        ("Observed directly or structurally supported", "current"),
        ("Hard public-data frontier", "frontier"),
        ("Defensible marginal intervention", "proposal"),
        ("Long-run institutional horizon", "horizon"),
    ]
    x0 = 0.05
    for label, kind in legend_items:
        ax.add_patch(
            Rectangle(
                (x0, legend_y),
                0.16,
                0.10,
                fill=False,
                linestyle=style[kind]["linestyle"],
                linewidth=min(style[kind]["linewidth"], 2.0),
            )
        )
        ax.text(
            x0 + 0.22,
            legend_y + 0.05,
            label,
            fontsize=9.4,
            va="center",
            ha="left",
        )
        x0 += 1.55

    fig.text(
        0.055,
        0.965,
        "Section 8 roadmap. Survey design should follow the observability frontier",
        fontsize=16.4,
        fontweight="bold",
        ha="left",
        va="top",
    )
    fig.text(
        0.055,
        0.928,
        (
            "The public system already observes several margins well. The agenda is to "
            "strengthen exactly the places where the current stack runs out, without "
            "pretending that marginal extensions solve the missing worker-firm AI "
            "linkage problem."
        ),
        fontsize=11.0,
        ha="left",
        va="top",
    )
    fig.text(
        0.055,
        0.015,
        "Section 8 synthesis; layout from figures/figure6_policy_roadmap.csv.",
        fontsize=9.6,
        ha="left",
    )

    save_dual(fig, "policy_roadmap", tight_layout=False)
    print("Wrote figure6 roadmap visuals: policy_roadmap")


if __name__ == "__main__":
    main()
