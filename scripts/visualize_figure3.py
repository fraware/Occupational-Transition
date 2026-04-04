"""Figure 3: matplotlib panels (catalog stems) and PIL composite for manuscript."""

from __future__ import annotations

import textwrap
from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import font_manager
from matplotlib.patches import Patch
from PIL import Image, ImageDraw, ImageFont

from viz_style import (
    PNG_DIR,
    VECTOR_DIR,
    apply_matplotlib_style,
    ensure_visual_dirs,
    save_dual,
)
from viz_utils import read_figure_csv

COMPOSITE_STEM = "figure3_redesigned_composite"


def _pil_dejavu_fonts() -> tuple[ImageFont.ImageFont, ImageFont.ImageFont]:
    try:
        path = Path(font_manager.findfont("DejaVu Sans"))
        return ImageFont.truetype(str(path), 30), ImageFont.truetype(str(path), 18)
    except OSError:
        return ImageFont.load_default(), ImageFont.load_default()


def build_panel_a(dfa: pd.DataFrame) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(10.8, 4.8))

    ax.plot(
        dfa["dt"],
        dfa["ai_use_current_rate"] * 100,
        linewidth=2.3,
        label="Current AI use",
    )
    ax.plot(
        dfa["dt"],
        dfa["ai_use_expected_6m_rate"] * 100,
        linewidth=2.3,
        linestyle="--",
        label="Expected AI use (6m)",
    )

    wording_change = pd.Timestamp("2025-11-17")
    ax.axvline(wording_change, linewidth=1.2)
    ax.annotate(
        "Question wording change\nnew BTOS series",
        xy=(wording_change, 24.2),
        xytext=(pd.Timestamp("2025-07-01"), 35.5),
        arrowprops={"arrowstyle": "->", "lw": 1.0},
        fontsize=10.2,
        ha="left",
        va="center",
    )

    x_last = dfa["dt"].iloc[-1]
    y_current = float(dfa["ai_use_current_rate"].iloc[-1] * 100)
    y_expected = float(dfa["ai_use_expected_6m_rate"].iloc[-1] * 100)

    ax.annotate(
        f"Current AI use\n{y_current:.1f}%",
        xy=(x_last, y_current),
        xytext=(8, -2),
        textcoords="offset points",
        fontsize=10.2,
        ha="left",
        va="center",
    )
    ax.annotate(
        f"Expected AI use (6m)\n{y_expected:.1f}%",
        xy=(x_last, y_expected),
        xytext=(8, 2),
        textcoords="offset points",
        fontsize=10.2,
        ha="left",
        va="center",
    )

    ax.set_title("Figure 3 Panel A: BTOS AI use trends", fontsize=13.5, pad=10)
    ax.set_ylabel("Firm-weighted share (%)", fontsize=11)
    ax.set_xlabel("")
    ax.set_ylim(0, 42)
    ax.grid(True, axis="y", linewidth=0.5)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=4))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b\n%Y"))

    fig.tight_layout()
    return fig


def build_panel_b(direct: pd.DataFrame, proxy: pd.DataFrame) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(10.8, 5.8))

    direct_y = [5.8, 4.8, 3.8]
    proxy_y = [1.8, 0.8, -0.2]

    ax.barh(
        direct_y,
        (direct["weighted_share"] * 100).tolist(),
        height=0.72,
        label="Direct published",
    )
    bars_proxy = ax.barh(
        proxy_y,
        (proxy["weighted_share"] * 100).tolist(),
        height=0.72,
        label="Proxy-interpreted",
    )
    for bar in bars_proxy:
        bar.set_hatch("///")
        bar.set_linewidth(1.0)

    ax.set_yticks(direct_y + proxy_y)
    ax.set_yticklabels(
        direct["category_label"].tolist() + proxy["category_label"].tolist(),
        fontsize=10.4,
    )

    ax.axhline(2.75, linewidth=1.1)
    ax.text(
        0,
        6.45,
        "Direct published BTOS rows",
        fontsize=10.8,
        fontweight="bold",
        ha="left",
        va="center",
    )
    ax.text(
        0,
        2.25,
        "Proxy-interpreted indicators",
        fontsize=10.8,
        fontweight="bold",
        ha="left",
        va="center",
    )

    for y, v in zip(direct_y, (direct["weighted_share"] * 100).tolist(), strict=True):
        ax.text(v + 1.0, y, f"{v:.1f}%", fontsize=10.2, va="center")
    for y, v in zip(proxy_y, (proxy["weighted_share"] * 100).tolist(), strict=True):
        ax.text(v + 1.0, y, f"{v:.1f}%", fontsize=10.2, va="center")

    top_direct_pct = float(direct["weighted_share"].iloc[0] * 100)
    ax.annotate(
        "Modal direct public finding",
        xy=(top_direct_pct, 5.8),
        xytext=(62, 6.55),
        arrowprops={"arrowstyle": "->", "lw": 1.0},
        fontsize=10.2,
        ha="left",
        va="center",
    )

    ax.set_xlim(0, 102)
    ax.set_xlabel(
        "Share among AI-using firms in pooled supplement window (%)",
        fontsize=11,
    )
    ax.set_title(
        "Figure 3 Panel B: Workforce-effect evidence classes",
        fontsize=13.5,
        pad=10,
    )
    ax.grid(True, axis="x", linewidth=0.5)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    legend_handles = [
        Patch(label="Direct published"),
        Patch(label="Proxy-interpreted", hatch="///"),
    ]
    ax.legend(handles=legend_handles, frameon=False, loc="lower right", fontsize=10.4)

    fig.tight_layout()
    return fig


def build_composite(panel_a_png: Path, panel_b_png: Path) -> tuple[Path, Path]:
    im_a = Image.open(panel_a_png).convert("RGB")
    im_b = Image.open(panel_b_png).convert("RGB")

    margin = 56
    width = max(im_a.width, im_b.width) + 2 * margin

    font_title, font_body = _pil_dejavu_fonts()
    title = (
        "Figure 3. Business-reported AI adoption is visible, but evidentiary strength "
        "differs across BTOS measures"
    )
    subtitle = (
        "Panel A uses direct published national BTOS AI-use series and marks the "
        "November 2025 wording change explicitly. Panel B separates direct published "
        "employment-effect rows from proxy-interpreted task indicators."
    )
    sub_lines = textwrap.wrap(subtitle, width=72)

    y_cursor = 28
    header_height = y_cursor + 44 + len(sub_lines) * 22 + 24

    height = header_height + im_a.height + margin + im_b.height + margin
    canvas = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(canvas)

    draw.text((margin, y_cursor), title, font=font_title, fill="black")
    y_cursor += 44
    for line in sub_lines:
        draw.text((margin, y_cursor), line, font=font_body, fill="black")
        y_cursor += 22

    canvas.paste(im_a, (margin, header_height))
    canvas.paste(im_b, (margin, header_height + im_a.height + margin))

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

    # Top bar (y=5.8) must be the modal direct row ("Employment did not change").
    direct = direct.sort_values("category_label", ascending=True)
    proxy = proxy.sort_values("category_label", ascending=True)

    fig_a = build_panel_a(dfa)
    p1, _ = save_dual(fig_a, "btos_ai_trends")

    fig_b = build_panel_b(direct, proxy)
    p2, _ = save_dual(fig_b, "btos_workforce_effects_barh")

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
