"""Figure 4: four JOLTS rate panels (stem jolts_openings_rate), CES, PIL composite."""

from __future__ import annotations

import tempfile
import textwrap
from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import font_manager
from PIL import Image, ImageDraw, ImageFont

from viz_style import (
    PNG_DIR,
    VECTOR_DIR,
    apply_matplotlib_style,
    ensure_visual_dirs,
    save_dual,
)
from viz_utils import parse_month_col, read_figure_csv

COMPOSITE_STEM = "figure4_redesigned_composite"

SECTOR_ORDER = [
    "Manufacturing",
    "Information",
    "Financial activities",
    "Professional and business services",
    "Health care and social assistance",
    "Retail trade",
]

RATE_META = [
    ("job_openings_rate", "Openings rate"),
    ("hires_rate", "Hires rate"),
    ("quits_rate", "Quits rate"),
    ("layoffs_discharges_rate", "Layoffs & discharges"),
]


def _pil_dejavu_fonts() -> tuple[ImageFont.ImageFont, ImageFont.ImageFont]:
    try:
        path = Path(font_manager.findfont("DejaVu Sans"))
        return ImageFont.truetype(str(path), 30), ImageFont.truetype(str(path), 18)
    except OSError:
        return ImageFont.load_default(), ImageFont.load_default()


def _pil_panel_a_header_font() -> ImageFont.ImageFont:
    try:
        path = Path(font_manager.findfont("DejaVu Sans"))
        return ImageFont.truetype(str(path), 20)
    except OSError:
        return ImageFont.load_default()


def build_jolts_rate_chart(
    sub: pd.DataFrame,
    rate_name: str,
    title: str,
    outfile: Path,
) -> None:
    fig, ax = plt.subplots(figsize=(6.8, 3.9))
    for sector in SECTOR_ORDER:
        g = sub[
            (sub["sector6_label"] == sector) & (sub["rate_name"] == rate_name)
        ].sort_values("month_dt")
        ax.plot(g["month_dt"], g["rate_value"], linewidth=1.9)
        if not g.empty:
            x = g["month_dt"].iloc[-1]
            y = float(g["rate_value"].iloc[-1])
            ax.annotate(
                f"{sector}\n{y:.1f}",
                xy=(x, y),
                xytext=(6, 0),
                textcoords="offset points",
                fontsize=8.1,
                ha="left",
                va="center",
            )
    ax.set_title(title, fontsize=11.8, pad=8)
    ax.set_xlabel("")
    ax.set_ylabel("Rate (%)", fontsize=9.8)
    ax.grid(True, axis="y", linewidth=0.45)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    fig.tight_layout()
    fig.savefig(outfile, bbox_inches="tight")
    plt.close(fig)


def build_jolts_composite(jolts: pd.DataFrame) -> tuple[Path, Path]:
    ensure_visual_dirs()
    out_png = PNG_DIR / "jolts_openings_rate.png"
    out_pdf = VECTOR_DIR / "jolts_openings_rate.pdf"
    header_h = 52
    m = 12

    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        temp_paths: list[Path] = []
        for rate_name, title in RATE_META:
            out = td_path / f"{rate_name}.png"
            build_jolts_rate_chart(jolts, rate_name, title, out)
            temp_paths.append(out)

        imgs = []
        for pth in temp_paths:
            with Image.open(pth) as im:
                imgs.append(im.convert("RGB").copy())

        w = max(im.width for im in imgs)
        h = max(im.height for im in imgs)
        gap = 24
        canvas_w = 2 * w + gap + 2 * m
        canvas_h = header_h + 2 * h + gap + m
        canvas = Image.new("RGB", (canvas_w, canvas_h), "white")
        draw = ImageDraw.Draw(canvas)
        draw.text(
            (m, 8),
            "Panel A. JOLTS sector rates",
            font=_pil_panel_a_header_font(),
            fill="black",
        )

        positions = [
            (m, header_h),
            (m + w + gap, header_h),
            (m, header_h + h + gap),
            (m + w + gap, header_h + h + gap),
        ]
        for im, pos in zip(imgs, positions, strict=True):
            canvas.paste(im, pos)

        canvas.save(out_png)
        canvas.save(out_pdf, format="PDF")

    return out_png, out_pdf


def build_ces_panel(ces: pd.DataFrame) -> tuple[Path, Path]:
    fig, ax = plt.subplots(figsize=(11.2, 4.8))
    for sector in SECTOR_ORDER:
        g = ces[ces["sector6_label"] == sector].sort_values("month_dt")
        ax.plot(g["month_dt"], g["index_aug2023_100"], linewidth=2.0)
        if not g.empty:
            x = g["month_dt"].iloc[-1]
            y = float(g["index_aug2023_100"].iloc[-1])
            ax.annotate(
                f"{sector}\n{y:.1f}",
                xy=(x, y),
                xytext=(6, 0),
                textcoords="offset points",
                fontsize=8.6,
                ha="left",
                va="center",
            )

    ax.axhline(100.0, linestyle="--", linewidth=1.0)
    ax.set_title(
        "Panel B. CES payroll employment index (Aug 2023 = 100)",
        fontsize=13.2,
        pad=10,
    )
    ax.set_ylabel("Index", fontsize=10.5)
    ax.set_xlabel("")
    ax.grid(True, axis="y", linewidth=0.45)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    fig.tight_layout()
    return save_dual(fig, "ces_payroll_index")


def build_composite(panel_a_png: Path, panel_b_png: Path) -> tuple[Path, Path]:
    im_a = Image.open(panel_a_png).convert("RGB")
    im_b = Image.open(panel_b_png).convert("RGB")

    margin = 56
    font_title, font_body = _pil_dejavu_fonts()
    title = (
        "Figure 4. Sector labor-demand and payroll context, kept clearly "
        "subordinate to the paper's core claims"
    )
    subtitle = (
        "Panel A restores the full JOLTS flow-rate layer across the six-sector "
        "comparison set: openings, hires, quits, and layoffs/discharges. "
        "Panel B tracks CES payroll employment for the same sectors indexed to "
        "August 2023 = 100."
    )
    sub_lines = textwrap.wrap(subtitle, width=72)

    y_cursor = 28
    header_height = y_cursor + 44 + len(sub_lines) * 22 + 24

    canvas_w = max(im_a.width, im_b.width) + 2 * margin
    canvas_h = header_height + im_a.height + margin + im_b.height + margin + 40
    canvas = Image.new("RGB", (canvas_w, canvas_h), "white")
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

    jolts = read_figure_csv("figure4_panelA_jolts_sector_rates.csv").copy()
    ces = read_figure_csv("figure4_panelB_ces_sector_index.csv").copy()

    jolts["month_dt"] = parse_month_col(jolts, "month")
    ces["month_dt"] = parse_month_col(ces, "month")

    panel_a_png, _ = build_jolts_composite(jolts)
    panel_b_png, _ = build_ces_panel(ces)
    c_png, c_pdf = build_composite(panel_a_png, panel_b_png)

    print(
        "Wrote figure4 visuals:",
        panel_a_png.stem,
        Path(panel_b_png).stem,
        c_png.name,
        c_pdf.name,
    )


if __name__ == "__main__":
    main()
