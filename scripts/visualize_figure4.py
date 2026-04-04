"""Figure 4: four JOLTS rate panels (stem jolts_openings_rate), CES, PIL composite."""

from __future__ import annotations

import tempfile
from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image

from viz_style import (
    PNG_DIR,
    STYLE,
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

# Shorter legend text so six series do not overlap when placed below the subplot.
SECTOR_LEGEND_LABELS = [
    "Manufacturing",
    "Information",
    "Financial activities",
    "Prof. & business services",
    "Health care & social assistance",
    "Retail trade",
]


def build_jolts_rate_chart(
    sub: pd.DataFrame,
    rate_name: str,
    panel_title: str,
    outfile: Path,
) -> None:
    fig, ax = plt.subplots(figsize=(7.35, 4.55))
    lines: list = []
    palette = STYLE.palette_sector
    for i, sector in enumerate(SECTOR_ORDER):
        g = sub[
            (sub["sector6_label"] == sector) & (sub["rate_name"] == rate_name)
        ].sort_values("month_dt")
        color = palette[i % len(palette)]
        (ln,) = ax.plot(
            g["month_dt"],
            g["rate_value"],
            linewidth=1.9,
            color=color,
            label=SECTOR_LEGEND_LABELS[i],
        )
        lines.append(ln)
    ax.set_title(panel_title, fontsize=10.8, pad=10)
    ax.set_xlabel("")
    ax.set_ylabel("Rate (%)", fontsize=9.8)
    ax.grid(True, axis="y", linewidth=0.45)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.legend(
        handles=lines,
        labels=SECTOR_LEGEND_LABELS,
        fontsize=6.9,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.22),
        ncol=3,
        frameon=False,
        columnspacing=0.95,
        labelspacing=0.35,
        handlelength=1.65,
        handletextpad=0.35,
        borderaxespad=0.25,
    )
    fig.subplots_adjust(bottom=0.42, top=0.90)
    fig.savefig(outfile, bbox_inches="tight")
    plt.close(fig)


def build_jolts_composite(jolts: pd.DataFrame) -> tuple[Path, Path]:
    ensure_visual_dirs()
    out_png = PNG_DIR / "jolts_openings_rate.png"
    out_pdf = VECTOR_DIR / "jolts_openings_rate.pdf"
    m = 12

    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        temp_paths: list[Path] = []
        for rate_name, panel_title in RATE_META:
            out = td_path / f"{rate_name}.png"
            build_jolts_rate_chart(jolts, rate_name, panel_title, out)
            temp_paths.append(out)

        imgs = []
        for pth in temp_paths:
            with Image.open(pth) as im:
                imgs.append(im.convert("RGB").copy())

        w = max(im.width for im in imgs)
        h = max(im.height for im in imgs)
        gap = 24
        canvas_w = 2 * w + gap + 2 * m
        canvas_h = m + 2 * h + gap + m
        canvas = Image.new("RGB", (canvas_w, canvas_h), "white")

        positions = [
            (m, m),
            (m + w + gap, m),
            (m, m + h + gap),
            (m + w + gap, m + h + gap),
        ]
        for im, pos in zip(imgs, positions, strict=True):
            canvas.paste(im, pos)

        canvas.save(out_png)
        canvas.save(out_pdf, format="PDF")

    return out_png, out_pdf


def build_ces_panel(ces: pd.DataFrame) -> tuple[Path, Path]:
    fig, ax = plt.subplots(figsize=(11.2, 5.15))
    palette = STYLE.palette_sector

    line_handles: list = []
    line_labels: list[str] = []
    for i, sector in enumerate(SECTOR_ORDER):
        g = ces[ces["sector6_label"] == sector].sort_values("month_dt")
        if g.empty:
            continue
        color = palette[i % len(palette)]
        (ln,) = ax.plot(
            g["month_dt"],
            g["index_aug2023_100"],
            linewidth=2.0,
            color=color,
        )
        line_handles.append(ln)
        line_labels.append(SECTOR_LEGEND_LABELS[i])

    ax.axhline(100.0, linestyle="--", linewidth=1.0, color="#666666")
    ax.set_title("CES payroll employment index", fontsize=12.4, pad=12)
    ax.set_ylabel("Index (Aug 2023 = 100)", fontsize=10.5)
    ax.set_xlabel("")
    ax.grid(True, axis="y", linewidth=0.45)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.margins(x=0.02)
    ax.legend(
        handles=line_handles,
        labels=line_labels,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.18),
        bbox_transform=ax.transAxes,
        ncol=3,
        frameon=False,
        fontsize=8.5,
        columnspacing=1.05,
        labelspacing=0.35,
        handlelength=1.85,
        handletextpad=0.35,
        borderaxespad=0,
    )
    fig.subplots_adjust(bottom=0.24, top=0.90, left=0.09, right=0.98)
    return save_dual(fig, "ces_payroll_index", tight_layout=False)


def build_composite(panel_a_png: Path, panel_b_png: Path) -> tuple[Path, Path]:
    im_a = Image.open(panel_a_png).convert("RGB")
    im_b = Image.open(panel_b_png).convert("RGB")

    margin = 48
    top_pad = 20
    canvas_w = max(im_a.width, im_b.width) + 2 * margin
    canvas_h = top_pad + im_a.height + margin + im_b.height + margin
    canvas = Image.new("RGB", (canvas_w, canvas_h), "white")

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
