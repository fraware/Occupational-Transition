"""Figure 3: matplotlib panels (catalog stems) and PIL composite for manuscript."""

from __future__ import annotations

from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import Patch
from PIL import Image

from viz_style import (
    PNG_DIR,
    VECTOR_DIR,
    apply_matplotlib_style,
    ensure_visual_dirs,
    save_dual,
)
from viz_utils import read_figure_csv

COMPOSITE_STEM = "figure3_redesigned_composite"


def build_panel_a(dfa: pd.DataFrame) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(11.2, 5.25))

    ax.plot(
        dfa["dt"],
        dfa["ai_use_current_rate"] * 100,
        linewidth=2.35,
        label="Current AI use",
    )
    ax.plot(
        dfa["dt"],
        dfa["ai_use_expected_6m_rate"] * 100,
        linewidth=2.35,
        linestyle="--",
        label="Expected AI use (6m)",
    )

    wording_change = pd.Timestamp("2025-11-17")
    ax.axvline(wording_change, linewidth=1.15, color="#333333", zorder=0)
    ax.annotate(
        "Question wording change\nnew BTOS series",
        xy=(wording_change, 24.2),
        xytext=(pd.Timestamp("2025-07-01"), 36.0),
        arrowprops={"arrowstyle": "->", "lw": 1.05, "color": "#333333"},
        fontsize=10.5,
        ha="left",
        va="center",
        color="#222222",
    )

    x_last = dfa["dt"].iloc[-1]
    y_current = float(dfa["ai_use_current_rate"].iloc[-1] * 100)
    y_expected = float(dfa["ai_use_expected_6m_rate"].iloc[-1] * 100)

    ax.annotate(
        f"Current AI use\n{y_current:.1f}%",
        xy=(x_last, y_current),
        xytext=(10, -3),
        textcoords="offset points",
        fontsize=10.5,
        ha="left",
        va="center",
    )
    ax.annotate(
        f"Expected AI use (6m)\n{y_expected:.1f}%",
        xy=(x_last, y_expected),
        xytext=(10, 4),
        textcoords="offset points",
        fontsize=10.5,
        ha="left",
        va="center",
    )

    ax.set_title("BTOS AI use trends", fontsize=12.8, pad=12)
    ax.set_ylabel("Firm-weighted share (%)", fontsize=11.2, labelpad=8)
    ax.set_xlabel("")
    ax.set_ylim(0, 42)
    ax.margins(x=0.03)
    ax.grid(True, axis="y", linewidth=0.48, alpha=0.9)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(axis="both", labelsize=10.0)
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=4))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b\n%Y"))

    ax.legend(
        frameon=False,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.16),
        bbox_transform=ax.transAxes,
        ncol=2,
        fontsize=10.0,
        columnspacing=1.15,
        handlelength=2.0,
        handletextpad=0.45,
        borderaxespad=0,
    )
    fig.subplots_adjust(bottom=0.22, left=0.08, right=0.98, top=0.92)
    return fig


def build_panel_b(direct: pd.DataFrame, proxy: pd.DataFrame) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(11.2, 6.45))

    bar_h = 0.66
    direct_y = [6.05, 4.78, 3.52]
    proxy_y = [2.08, 0.82, -0.44]
    group_divider_y = (direct_y[-1] + proxy_y[0]) / 2

    ax.barh(
        direct_y,
        (direct["weighted_share"] * 100).tolist(),
        height=bar_h,
        label="Direct published",
    )
    bars_proxy = ax.barh(
        proxy_y,
        (proxy["weighted_share"] * 100).tolist(),
        height=bar_h,
        label="Proxy-interpreted",
    )
    for bar in bars_proxy:
        bar.set_hatch("///")
        bar.set_linewidth(1.0)

    ax.set_yticks(direct_y + proxy_y)
    ax.set_yticklabels(
        direct["category_label"].tolist() + proxy["category_label"].tolist(),
        fontsize=10.6,
    )

    ax.axhline(group_divider_y, linewidth=1.05, color="#555555")
    ax.text(
        0,
        6.62,
        "Direct published BTOS rows",
        fontsize=11.0,
        fontweight="bold",
        ha="left",
        va="center",
    )
    ax.text(
        0,
        1.35,
        "Proxy-interpreted indicators",
        fontsize=11.0,
        fontweight="bold",
        ha="left",
        va="center",
    )

    pct_pad = 1.15
    for y, v in zip(direct_y, (direct["weighted_share"] * 100).tolist(), strict=True):
        ax.text(v + pct_pad, y, f"{v:.1f}%", fontsize=10.4, va="center")
    for y, v in zip(proxy_y, (proxy["weighted_share"] * 100).tolist(), strict=True):
        ax.text(v + pct_pad, y, f"{v:.1f}%", fontsize=10.4, va="center")

    top_direct_pct = float(direct["weighted_share"].iloc[0] * 100)
    ax.annotate(
        "Modal direct public finding",
        xy=(top_direct_pct, direct_y[0]),
        xytext=(62, 6.72),
        arrowprops={"arrowstyle": "->", "lw": 1.05, "color": "#333333"},
        fontsize=10.5,
        ha="left",
        va="center",
        color="#222222",
    )

    ax.set_title("Workforce-effect evidence classes", fontsize=12.8, pad=12)
    ax.set_xlim(0, 102)
    ax.set_xlabel(
        "Share among AI-using firms in pooled supplement window (%)",
        fontsize=11.2,
        labelpad=10,
    )
    ax.grid(True, axis="x", linewidth=0.48, alpha=0.9)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(axis="x", labelsize=10.0)
    ax.margins(y=0.12)

    legend_handles = [
        Patch(label="Direct published"),
        Patch(label="Proxy-interpreted", hatch="///"),
    ]
    ax.legend(
        handles=legend_handles,
        frameon=False,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.12),
        bbox_transform=ax.transAxes,
        ncol=2,
        fontsize=10.0,
        columnspacing=1.0,
        handlelength=1.5,
        handletextpad=0.4,
        borderaxespad=0,
    )
    fig.subplots_adjust(bottom=0.20, left=0.12, right=0.98, top=0.90)
    return fig


def build_composite(panel_a_png: Path, panel_b_png: Path) -> tuple[Path, Path]:
    im_a = Image.open(panel_a_png).convert("RGB")
    im_b = Image.open(panel_b_png).convert("RGB")

    margin = 48
    top_pad = 20
    width = max(im_a.width, im_b.width) + 2 * margin
    height = top_pad + im_a.height + margin + im_b.height + margin
    canvas = Image.new("RGB", (width, height), "white")

    canvas.paste(im_a, (margin, top_pad))
    canvas.paste(im_b, (margin, top_pad + im_a.height + margin))

    ensure_visual_dirs()
    out_png = PNG_DIR / f"{COMPOSITE_STEM}.png"
    out_pdf = VECTOR_DIR / f"{COMPOSITE_STEM}.pdf"
    canvas.save(out_png)
    canvas.save(out_pdf, format="PDF")
    return out_png, out_pdf


def main() -> None:
    apply_matplotlib_style()

    dfa = read_figure_csv("figure3_panelA_btos_ai_trends.csv").copy()
    dfb = read_figure_csv("figure3_panelB_btos_workforce_effects.csv").copy()

    dfa["dt"] = pd.to_datetime(dfa["period_start_date"], errors="coerce")
    dfa = dfa.sort_values("dt").copy()

    direct = dfb[dfb["evidence_directness"] == "direct_published"].copy()
    proxy = dfb[dfb["evidence_directness"] != "direct_published"].copy()

    direct_order = [
        "Employment did not change",
        "Employment increased",
        "Employment decreased",
    ]
    proxy_order = [
        "Perform a task previously done by an employee",
        "Supplement or enhance a task performed by an employee",
        "Introduce a new task not previously done by an employee",
    ]

    direct["category_label"] = pd.Categorical(
        direct["category_label"],
        categories=direct_order,
        ordered=True,
    )
    proxy["category_label"] = pd.Categorical(
        proxy["category_label"],
        categories=proxy_order,
        ordered=True,
    )

    # Top bar must be the modal direct row ("Employment did not change").
    direct = direct.sort_values("category_label", ascending=True)
    proxy = proxy.sort_values("category_label", ascending=True)

    fig_a = build_panel_a(dfa)
    p1, _ = save_dual(fig_a, "btos_ai_trends", tight_layout=False)

    fig_b = build_panel_b(direct, proxy)
    p2, _ = save_dual(fig_b, "btos_workforce_effects_barh", tight_layout=False)

    c_png, c_pdf = build_composite(Path(p1), Path(p2))
    print(
        "Wrote figure3 visuals:",
        p1.stem,
        p2.stem,
        c_png.name,
        c_pdf.name,
    )


if __name__ == "__main__":
    main()
